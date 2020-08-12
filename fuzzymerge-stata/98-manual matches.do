* Merge all files together

	* Append merged files
	clear
	forval i = 1/8{
		append using "$clean_dta/merge`i'"
	}
/*	Deleted those three steps, so no longer a problem
	* Drop merge rejections based on manual inspection
	merge 1:1 census_uniqid using "$clean_dta/rejections from manual inspection"
	assert _merge != 2
	drop if _merge == 3
	drop _merge
*/	
	* Merge with Census data
	merge 1:1 census_uniqid using "$clean_dta/census_nmerge0"
	assert _merge != 1
	drop _merge
	foreach var of varlist vot_id-occupation{
		rename `var' C`var'
	}
	
	* Merge with Voter rolls
	replace voter_uniqid = 100000+_n if missing(voter_uniqid)
	merge 1:1 voter_uniqid using "$clean_dta/voter_nmerge0"
	replace voter_uniqid =. if voter_uniqid > 100000
	foreach var of varlist vot_id-voter_hhid{
		rename `var' V`var'
	}

* Save data for manual matching
preserve

	* Put all Census relative names into two variables for ease of inspection
	replace Cfather_name1 = Crelation_name1 if Cfather_name1 == "." & Crelation_name1 != "."

	* Save Census non-matches
	compress
	sort psid Cname1 Cfather_name1 Cspouse_name1
	export excel psid Cname1 Cfather_name1 Cspouse_name1 census_uniqid using "$clean_dta/manual matching_pre census.xlsx" if _merge == 1, replace firstrow(variable)
	
	* Save Voter Roll non-matches
	sort psid Vname1 Vrelation_name1
	export excel psid Vname1 Vrelation_name1 voter_uniqid using "$clean_dta/manual matching_pre voter.xlsx" if _merge == 2, replace firstrow(variable)

restore

* Import results from manual matching
// Add voter_uniqid next to census_uniqid for manual matches
import excel using "$clean_dta/manual matching_post.xlsx", clear firstrow
keep if !missing(voter_uniqid)
keep census_uniqid voter_uniqid
gen merge_type = "98-manual matching names"
save "$clean_dta/merge98", replace 
