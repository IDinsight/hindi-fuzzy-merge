* 10 - Match within household fuzzy name, gender, and fuzzy age
// Run twice, first with stricter threshold on each of 5 names (matchscore > 0.9), then on looser threshold (matchscore > 0.7) 
// 5 versions of names - skipping original version since appears to give better matches within HH

/* Process: for each fuzzy match threshold and name version
a. Go person-by-person in matched dataset
b. Go in order of match priority, then ID within those
c. Identify all people in person's CENSUS HH that have NOT been matched
d. Identify all people in person's VOTER ROLL HH that have NOT been matched
e. Fuzzy match name, keep if above threshold
f. Append matches across all households
g. Drop if age_diff > 15 years (loose threshold since matching within households)
h. Drop exact duplicates
i. Drop duplicate IDs with same matchscores, keeping match with lowest age difference
j. Drop duplicate IDs with different matchscores, keeping match with highest matchscore
*/

	* Specifying last non-merge datasets to start loop
	local census_nmerge "$clean_dta/census_nmerge7" 
	local voter_nmerge "$clean_dta/voter_nmerge7" 
	local z 1 // Version 

	* Prep merged dataset with household IDs
	use "$clean_dta/census_nmerge0", clear
	keep census_uniqid psid census_hhid
	forval i = 1/7{
		merge 1:1 census_uniqid using "$clean_dta/merge`i'", update
		drop _merge
	}
		
	drop if missing(voter_uniqid)
	merge 1:1 voter_uniqid using "$clean_dta/voter_nmerge0"
	keep if _merge == 3
		
		* Generate merge type numeric variable
		split merge_type, parse("(") gen(m)
		split m1, parse("-") gen(merge_type_short)
		destring merge_type_short?, replace
		drop m?
		
	keep merge_type_short1 merge_type_short2 census_uniqid psid census_hhid voter_hhid merge_type
	order merge_type_short1 merge_type_short2 census_uniqid psid census_hhid voter_hhid merge_type
	sort merge_type_short1 merge_type_short2 census_uniqid 
	save "$clean_dta/for_hh_merge", replace
	count
	local hh_count `r(N)'
	
	* Loop over two matchscore thresholds (stricter first, then looser)
	foreach m in 9 7{
		
		*Loop over 5 name variables
		forval i = 2/6{
		
			* Loop over each HH
			forval num = 1/`hh_count'{
		
				* Get Census and Voter HH numbers
				use "$clean_dta/for_hh_merge", clear
				local census_hhnum = census_hhid[`num']
				local voter_hhnum = voter_hhid[`num']
							
				* Prep Census
				use "`census_nmerge'", clear
				keep if census_hhid == "`census_hhnum'"
				keep if name`i'!="." & !missing(gender) & !missing(age)
				keep census_uniqid census_hhid psid name`i' gender age
				rename age Cage
				count
								
					* Go to next loop if no matches
					if _N == 0{
						continue
					}
					
					* Drop duplicates
					duplicates tag name`i' gender, gen(dup) // Using age range so must be unique on other variables
					drop if dup > 0
					drop dup
								
					* Go to next loop if no matches
					if _N == 0{
						continue
					}
					
				tempfile census_working
				save `census_working', replace
										
				* Prep Voter
				use "`voter_nmerge'", clear
				keep if voter_hhid == `voter_hhnum'
				keep if name`i'!="." & !missing(gender) & !missing(age)
				keep voter_uniqid voter_hhid psid name`i' gender age
				rename age Vage
				count
				
					* Go to next loop if no matches
					if _N == 0{
						continue
					}
					
					* Drop duplicates
					duplicates tag name`i' gender, gen(dup) // Using age range so must be unique on other variables
					drop if dup > 0
					drop dup

					* Go to next loop if no matches
					if _N == 0{
						continue
					}

				* Merge
				reclink gender name`i' using `census_working', idmaster(voter_uniqid) idusing(census_uniqid) gen(matchscore) required(gender) wmatch(1 10)

					* Keep good merges 
					
						* Keep with sufficiently high match score
						keep if matchscore > 0.`m' & !missing(matchscore)
						
						* Drop matches with big differences in lengths - reclink doesn't weight length similarity enough
						// Don't apply since within HH
						
						* Drop if reported ages are not within 15 years of each other
						gen age_diff = abs(Cage-Vage)
						drop if age_diff > 15
											
						* Go to next loop if no matches
						if _N == 0{
							continue
						}
						
				* Temporary save
				tempfile file_`i'`m'num`num'
				save `file_`i'`m'num`num'', replace
			}
			
			* Append household merges and drop duplicates
			clear
			forval num = 1/`hh_count'{
				cap append using `file_`i'`m'num`num''
			}
				
				* Go to next loop if no matches
				if _N == 0{
					continue
				}
				
				* Drop exact duplicates
				duplicates drop
				
				* If same matchscore, drop duplicate with larger age difference (and arbitrary if same age difference)

					* Dropping duplicates on census ID
					sort census_uniqid matchscore age_diff, stable
					bys census_uniqid matchscore (age_diff): drop if _n != 1
					
					* Dropping duplicates on voter ID
					sort voter_uniqid matchscore age_diff, stable
					bys voter_uniqid matchscore (age_diff): drop if _n != 1

				* If different matchscore, keep higher matchscore

					* Dropping duplicates on census ID
					sort census_uniqid matchscore, stable
					bys census_uniqid (matchscore): drop if _n < _N

					* Dropping duplicates on voter ID
					sort voter_uniqid matchscore, stable
					bys voter_uniqid (matchscore): drop if _n < _N

			* Keep merges
			keep census_uniqid voter_uniqid matchscore age_diff
			gen merge_type = "8-`z'(within HH,fuzzy name, gender, fuzzy age),v`i' names"
			local ++z
			tempfile merge_`i'`m'
			save `merge_`i'`m'', replace
			save "$clean_dta/merge_`i'`m'", replace
			
			* Remainder Census
			use "`census_nmerge'", clear
			merge 1:1 census_uniqid using `merge_`i'`m''
			keep if _merge == 1
			drop _merge merge_type matchscore age_diff voter_uniqid
			tempfile census_nmerge
			save `census_nmerge', replace
			
			* Remainder Voter
			use "`voter_nmerge'", clear
			merge 1:1 voter_uniqid using `merge_`i'`m''
			keep if _merge == 1
			drop _merge merge_type matchscore age_diff census_uniqid
			tempfile voter_nmerge
			save `voter_nmerge', replace
			
		}
	}

	* Append merge files and save
	clear
	foreach m in 9 7{
		forval i = 2/6{
			cap append using `merge_`i'`m''
			*cap append using "$clean_dta/merge_`i'`m'"
		}
	}
	save "$clean_dta/merge8", replace 

	* Remainder Census
	use `census_nmerge', clear
	save "$clean_dta/census_nmerge8", replace

	* Remainder Voter
	use `voter_nmerge', clear
	save "$clean_dta/voter_nmerge8", replace
