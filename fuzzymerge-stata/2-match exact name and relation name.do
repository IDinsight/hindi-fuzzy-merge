
	
* 2 - Match exact name and relation name 
// 6 versions of names and 2 possible relations

	* Specifying last non-merge datasets to start loop
	local census_nmerge "$clean_dta/census_nmerge1"
	local voter_nmerge "$clean_dta/voter_nmerge1"
	local z 1 // Version 
	
	
	* Loop over 6 name variables
	forval i = 1/6{
		
		* Loop over 2 relations
		foreach relation in father spouse{
		
			* Prep Census
			use "`census_nmerge'", clear
			replace `relation'_name`i' = relation_name`i' if (`relation'_name`i') == "." & relation_name`i' != "." // Relatives' names for individuals with unmatched voter IDs are in the variable "relation_name`i'"
			keep if (name`i') != "." & (`relation'_name`i') != "."
			keep census_uniqid psid name`i' `relation'_name`i' individual_type 
			
				* Drop duplicates
				duplicates tag psid name`i' `relation'_name`i', gen(dup)
				drop if dup > 0
				drop dup
				
			tempfile census_working
			save `census_working', replace
		
			* Prep Voter
			use "`voter_nmerge'", clear
			rename relation_name`i' `relation'_name`i'
			keep if (name`i') !="." & (`relation'_name`i') !="."
			keep voter_uniqid psid name`i' `relation'_name`i' 
			
				* Drop duplicates
				duplicates tag psid name`i' `relation'_name`i', gen(dup)
				drop if dup > 0
				drop dup

			* Merge
			merge 1:1 psid name`i' `relation'_name`i' using `census_working'

			* Temporary save
				
				* Keep merges
				keep if _merge == 3
				keep census_uniqid voter_uniqid 
				gen merge_type = "2-`z'(exact name and `relation' name),v`i' names"
				local ++z
				tempfile merge_`relation'`i'
				save `merge_`relation'`i'', replace
				
				* Remainder Census
				use "`census_nmerge'", clear
				merge 1:1 census_uniqid using `merge_`relation'`i''
				keep if _merge == 1
				drop _merge merge_type voter_uniqid
				tempfile census_nmerge
				save `census_nmerge', replace
				
				* Remainder Voter
				use "`voter_nmerge'", clear
				merge 1:1 voter_uniqid using `merge_`relation'`i''
				keep if _merge == 1
				drop _merge merge_type census_uniqid
				tempfile voter_nmerge
				save `voter_nmerge', replace
		}
	}
	
	* Append merge files and save
	clear
	forval i = 1/6{
		foreach relation in father spouse{
			append using `merge_`relation'`i''
		}
	}
	
	save "$clean_dta/merge2", replace

	* Remainder Census
	use `census_nmerge', clear
	save "$clean_dta/census_nmerge2", replace

	* Remainder Voter
	use `voter_nmerge', clear
	save "$clean_dta/voter_nmerge2", replace
