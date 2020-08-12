

* 4 - Match exact name and fuzzy relation name with flipped relations (in case relation is misidentified)
// 6 versions of names (exact match name: stricter about this since fuzzy matching relation name)
// Run twice, first with stricter threshold on each of 6 names (matchscore > 0.9), then on looser threshold (matchscore > 0.8) 

	* Specifying last non-merge datasets to start loop
	local census_nmerge "$clean_dta/census_nmerge3"
	local voter_nmerge "$clean_dta/voter_nmerge3"
	local z 1 // Version 
	
	
	
	* Loop over two matchscore thresholds (stricter first, then looser)
	foreach m in 9 8{
		
		* Loop over 6 name variables
		forval i = 1/6{
			
			* Loop over 2 relations
			foreach relation in father spouse{
		
				* Prep Census
				use "`census_nmerge'", clear
				replace `relation'_name`i' = relation_name`i' if (`relation'_name`i') == "." & relation_name`i' != "." // Relatives' names for individuals with unmatched voter IDs are in the variable "relation_name`i'"
				keep if name`i'!="." & `relation'_name`i'!="."
				
					*Keep most likely relation
					
					if "`relation'" == "father"{
						keep if married_female == 0
						keep census_uniqid psid name`i' father_name`i' 
					}
					if "`relation'" == "spouse"{
						keep if married_female == 1
						keep census_uniqid psid name`i' spouse_name`i' 
					}	
					
					* Drop duplicates
					duplicates tag psid name`i' `relation'_name`i', gen(dup)
					drop if dup > 0
					drop dup
					
				tempfile census_working
				save `census_working', replace
			
				* Prep Voter
				use "`voter_nmerge'", clear
				rename relation_name`i' `relation'_name`i'
				keep if name`i'!="." & `relation'_name`i'!="."

					* Keep most likely relation and FLIP
				
					if "`relation'" == "father"{
						keep if relation_new != 0
						keep voter_uniqid psid name`i' father_name`i'
					}
					if "`relation'" == "spouse"{
						keep if relation_new == 0
						keep voter_uniqid psid name`i' spouse_name`i' 
					}
											
					* Drop duplicates
					duplicates tag psid name`i' `relation'_name`i', gen(dup)
					drop if dup > 0
					drop dup

				* Merge
				reclink psid `relation'_name`i' name`i' using `census_working', idmaster(voter_uniqid) idusing(census_uniqid) gen(matchscore) required(psid `relation'_name`i') wmatch(1 1 10)

				* Keep good merges 
				
					* Keep with sufficiently high match score
					keep if matchscore > 0.`m' & !missing(matchscore)

					* Drop matches with big differences in lengths - reclink doesn't weight length similarity enough
					gen L`relation'_name`i' = strlen(subinstr(`relation'_name`i'," ","",.))
					gen LU`relation'_name`i' = strlen(subinstr(`relation'_name`i'," ","",.))
					gen length_diff = abs(L`relation'_name`i'-LU`relation'_name`i')
					drop if length_diff > 3
					drop length_diff L*
					
					* Go to next loop if no matches
					if _N == 0{
						continue
					}

					* If there are multiple using matches to a master code, keep the one with the highest match score
					bys voter_uniqid (matchscore): drop if _n < _N

					* If there are multiple master matches to a using code, keep the one with the highest match score
					bys census_uniqid (matchscore): drop if _n < _N
			
					* Drop all remaining duplicates on master code
					duplicates tag voter_uniqid, gen(dup)
					drop if dup > 0
					drop dup
					
					* Drop all remaining duplicates on using code
					duplicates tag census_uniqid, gen(dup)
					drop if dup > 0
					drop dup
				
				* Temporary save
					
					* Keep merges
					keep if _merge == 3
					count
					local num_`relation'`i'`m' `r(N)'
					
					keep census_uniqid voter_uniqid matchscore
					gen merge_type = "4-`z'(exact name,fuzzy `relation' name FLIPPED),v`i' names,matchscore > 0.`m'"
					local ++z
					tempfile merge_`relation'`i'`m'
					save `merge_`relation'`i'`m'', replace
					
					* Remainder Census
					use "`census_nmerge'", clear
					merge 1:1 census_uniqid using `merge_`relation'`i'`m''
					keep if _merge == 1
					drop _merge merge_type matchscore voter_uniqid
					tempfile census_nmerge
					save `census_nmerge', replace
					
					* Remainder Voter
					use "`voter_nmerge'", clear
					merge 1:1 voter_uniqid using `merge_`relation'`i'`m''
					keep if _merge == 1
					drop _merge merge_type matchscore census_uniqid
					tempfile voter_nmerge
					save `voter_nmerge', replace
			}
		}
	}
	
	* Append merge files and save
	clear
	foreach m in 9 8{
		forval i = 1/6{
			foreach relation in father spouse{
				cap append using `merge_`relation'`i'`m''
			}
		}
	}
	
	save "$clean_dta/merge4", replace

	* Remainder Census
	use `census_nmerge', clear
	save "$clean_dta/census_nmerge4", replace

	* Remainder Voter
	use `voter_nmerge', clear
	save "$clean_dta/voter_nmerge4", replace 
	
	
