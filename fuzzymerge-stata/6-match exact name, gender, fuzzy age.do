
* 6 - Match exact name, exact gender, and fuzzy age
// 6 versions of names
// +/- 5 years, which is the average difference in the census and voter roll ages in the previous merges

	* Specifying last non-merge datasets to start loop
	local census_nmerge "$clean_dta/census_nmerge5"
	local voter_nmerge "$clean_dta/voter_nmerge5"
	local z 1 // Version 
	
	* Loop over 6 name variables
	forval i = 1/6{

		* Prep Census
		use "`census_nmerge'", clear
		keep if name`i'  != "."  & !missing(gender) & !missing(age)
		keep census_uniqid psid name`i' gender age
		rename age Cage
		
			* Drop duplicates
			duplicates tag psid name`i' gender, gen(dup) // Using age range so must be unique on other variables
			drop if dup > 0
			drop dup
			
		tempfile census_working
		save `census_working', replace
		
		* Prep Voter
		use "`voter_nmerge'", clear
		keep if name`i' !="." & !missing(gender) & !missing(age)
		keep voter_uniqid psid name`i' gender age
		rename age Vage
		
			* Drop duplicates
			duplicates tag psid name`i' gender, gen(dup) // Using age range so must be unique on other variables
			drop if dup > 0
			drop dup

			* Merge
			merge 1:1 psid name`i' gender using `census_working'
			
			* Drop if reported ages are not within 5 years of each other
			gen age_diff = abs(Cage-Vage)
			drop if age_diff > 5

			* Temporary save
				
				* Keep merges
				keep if _merge == 3
				keep census_uniqid voter_uniqid age_diff
				gen merge_type = "6-`z'(exact name, gender, fuzzy age),v`i' names"
				local ++z
				tempfile merge`i'
				save `merge`i'', replace
				
				* Remainder Census
				use "`census_nmerge'", clear
				merge 1:1 census_uniqid using `merge`i''
				keep if _merge == 1
				drop _merge merge_type age_diff voter_uniqid
				tempfile census_nmerge
				save `census_nmerge', replace
				
				* Remainder Voter
				use "`voter_nmerge'", clear
				merge 1:1 voter_uniqid using `merge`i''
				keep if _merge == 1
				drop _merge merge_type age_diff census_uniqid
				tempfile voter_nmerge
				save `voter_nmerge', replace
	}
		
	* Append merge files and save
	clear
	forval i = 1/6{
		cap append using `merge`i''
	}
	save "$clean_dta/merge6", replace

	* Remainder Census
	use `census_nmerge', clear
	save "$clean_dta/census_nmerge6", replace

	* Remainder Voter
	use `voter_nmerge', clear
	save "$clean_dta/voter_nmerge6", replace
	 	 
