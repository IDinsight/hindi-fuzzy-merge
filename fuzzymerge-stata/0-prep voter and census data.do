
******************************
** Prepare Household Census **
******************************

* Import
	use "$raw_census", clear
	
* Rename father_or_spouse_name to relation_name, to be consistent with voter rolls
rename father_or_spouse_name relation_name
	
* Generate new name variables 
foreach name in name father_name spouse_name relation_name{
	global name `name'
	do "$do/0i-transliteration.do"
}	

* Generate other matching variables
	
	* Original name variable
	foreach name in name father_name spouse_name relation_name{
	rename `name' `name'1
	label var `name'1 "Original `name' variable"
	}
	
	
* Rename unique household id to be consistent with voter rolls data

	rename unique_hh_id census_hhid
	
* Married (if female)
	
	gen married_female = (marital_status == 2 | marital_status == 3 | marital_status == 4 | marital_status == 5) & (gender == 1)
	label var married_female "Ever married female" 

* Apparent duplicates (same name, father name, spouse name, very similar age)
// Manually inspected, suggests these are duplicates, arbitrarily dropping
	// Duplicates are of two types: 1. same individual type across different household IDs 
		//and different individual type within same household
	
bys psid name2 father_name2 spouse_name2 relation_name2 vot_id (census_uniqid): drop if _n > 1 


* Keep PSIDs where full census was conducted
keep if psid == 194 | psid == 219 | psid ==33 | psid ==225 | psid ==88 | psid ==147 | ///
psid == 117 | psid ==190 | psid ==66 | psid ==182  | ///
psid == 2 | psid ==188  | psid ==330 | psid ==352 //for now only keep the sample polling stations where
// full census was conducted and Muzaffarpur PS

* Order matching variables first
order census_uniqid psid vot_id *name1 *name2 *name3 *name4 *name5 *name6 age ///
 gender married_female individual_type  census_hhid 

* Save
compress
save "$clean_dta/census_nmerge0", replace

*************************
** Prepare Voter Rolls **
*************************

* Import
use "$raw_voter", clear

rename father_or_spouse_name relation_name

* Keep PSIDs where full census was conducted

keep if psid == 194 | psid == 219 | psid ==33 | psid ==225 | psid ==88 | psid ==147 | ///
psid == 117 | psid ==190 | psid ==66 | psid ==182  | ///
psid == 2 | psid ==188  | psid ==330 | psid ==352 //for now only keep the sample polling stations where
// full census was conducted and Muzaffarpur PS

* Generate new voter HH ID that is unique across PS
// HH ID starts over for each PS part, so need to include that in grouping variable
sort psid part_no house_no_dev, stable
egen voter_hhid = group(psid part_no house_no_dev)


* Generate new name variables 
foreach name in name relation_name{
	global name `name'
	do "$do/0i-transliteration.do"
}
* Generate other matching variables

	* Original name variable
	foreach name in name relation_name{
		rename `name' `name'1
		label var `name'1 "Original `name' variable"
	}
	
	* Married (if female)
	gen married_female = (relation_new == 1) & (gender == 1)
	label var married_female "Ever married female"


* Apparent duplicates (same name, father name, spouse name, very similar age)
// Manually inspected, suggests these are duplicates, arbitrarily dropping 
bys psid name2 relation_name2 age (voter_uniqid): drop if _n > 1
	
* Order matching variables first
order voter_uniqid psid vot_id *name1 *name2 *name3 *name4 *name5 *name6 age gender married_female 

* Save
compress
save "$clean_dta/voter_nmerge0", replace
