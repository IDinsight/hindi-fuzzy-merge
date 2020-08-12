* Merge all files together

	* Append merged files
	clear
	forval i = 1/8{
		append using "$clean_dta/merge`i'"
	}
	
	* Add in manual matches
	append using "$clean_dta/merge98"

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

* Generate match variable
gen matched = _merge
label def matched 	1 "1-Household census only" ///
					2 "2-Voter rolls only" /// 
					3 "3-Matched"
label val matched matched
label var matched "Matched with Voter Roll"
drop _merge age_diff

* Generate merge type numeric variable

	* Merge variables
	split merge_type, parse("(") gen(m)
	split m1, parse("-") gen(merge_type_short)
	destring merge_type_short?, replace
	drop m? merge_type_short2
	rename merge_type_short merge_variables
	label def merge_vars 	1 "1-Voter IDs" ///
							2 "2-Exact Name/Exact Relation" ///
							3 "3-Exact Name/Fuzzy Relation" ///
							4 "4-Flip Father/Husband" ///
							5 "5-Fuzzy Name/Exact Relation" ///
							6 "6-Exact Name/Gender/Age" ///
							7 "7-Fuzzy Name/Fuzzy Relation" ///
							8 "8-Within HH Fuzzy Names" ///
							98 "98-Manual Matches"
	label val merge_variables merge_vars
	label var merge_variables "Variable list used for merging"

	* Name version
	gen merge_name_version = .
	forval i = 1/6{
		replace merge_name_version = `i' if regexm(merge_type,"v`i'")
	}
	label def name_version	1 "1-Exact Name" ///
							2 "2-Transliterations" ///
							3 "3-Only First Name" ///
							4 "4-More Transliterations" ///
							5 "5-More Transliterations, Only First Name" ///
							6 "6-Common Surnames Appended to First Name Removed" 
	label val merge_name_version name_version
	label var merge_name_version "Name version used in merging"
	
	* Relation	
	gen merge_relation = .
	replace merge_relation = 1 if regexm(merge_type,"father")
	replace merge_relation = 2 if regexm(merge_type,"spouse")
	label def rel 1 "Father" 2 "Spouse"
	label val merge_relation rel
	label var merge_relation "Relation used in merging"
	
	* Threshold
	split merge_type, parse(">") gen(temp)
	rename temp2 merge_fuzzy_threshold
	destring merge_fuzzy_threshold, replace
	label var merge_fuzzy_threshold "For fuzzy merges, reclink threshold of acceptable merge"
	label var matchscore "For fuzzy merges, matchscore from reclink"
	drop temp1
	
	* Self-reported registered to vote
	rename registration Cregistration
	label var Cregistration "Self-reported registered to vote"
	order Cregistration, after(Coccupation)

* Urban/rural PS
gen ps_type = 0 
label var ps_type "Urban/Rural PS"
replace ps_type = 1 if ( psid == 194 | psid == 219 |psid==117 | psid == 66 | psid == 182) // urban based on internal assessment
label define ps_type 0 "Rural" 1 "Urban"
label val ps_type ps_type

*Assigning corresponding acnames, state names, caste categories to PS (missing for when individual appears only on voter rolls)

	*AC Name
	recode psid (2 188 = 7) (33 225 = 2) (194 219 = 1) (88 147 = 3) (117 190 =4) (66 182 = 5) (330 352 = 9), generate (acname)
	label var acname "Assembly Constituency"
	label val acname acname //label previously defined
	drop Cacname
	
	* AC ID
	gen acid = .
	replace acid = 59 if acname == 9
	replace acid = 94 if acname == 1
	replace acid = 227 if acname == 2
	replace acid = 65 if acname == 4
	replace acid = 169 if acname == 7
	replace acid = 181 if acname == 3
	replace acid = 216 if acname == 5

	*State
	recode acname (1 2 = 1) (3 4 5 =2) (7=3) (9=4), generate(state)
	label var state "State"
	label define state 1 "Bihar" 2 "Madhya Pradesh" 3 "Rajasthan" 4 "Uttar Pradesh"
	label val state state
	
	*AC Caste category
	recode acname (1 4 5 7= 1) (2 9 =2) (3=3) , generate(acname_caste)
	label var acname_caste "Assembly Constituency Caste Reservation"
	label define acname_caste 1 "GEN" 2 "SC" 3 "ST" 
	label val acname_caste acname_caste
	
* Order
order matched merge_variables merge_name_version merge_relation merge_fuzzy_threshold matchscore *name1 state acname acname_caste acid ps_type psid census_uniqid C* voter_uniqid V* merge_type

* Save
gsort -matched merge_variables merge_name_version merge_relation merge_fuzzy_threshold Cname1 Cfather_name1
compress
local date: display %td_CCYY_NN_DD date(c(current_date), "DMY")
local date_string = subinstr(trim("`date'"), " " , "-", .)
save "$output_dta/`date_string'_Matched Household Census and Voter Rolls", replace
save "$output_dta/`date_string'_VoterRolls_Analysis", replace
