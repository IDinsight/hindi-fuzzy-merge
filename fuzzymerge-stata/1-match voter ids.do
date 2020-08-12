*********************** 1. Match on voter IDs for households able to share voter IDs***************************

* 1. Match on voter IDs for households able to share voter IDs

	* Prep Census
	use "$clean_dta/census_nmerge0", clear
	keep if vot_id != "." //Drop missing values
	
		* Fix misentered voter IDs
		
			* PS-2
			replace vot_id = "CHF9782194" if vot_id == "CHE9782194"
			replace vot_id = "CHF1892801" if vot_id == "CHJ1892801"
			replace vot_id = "CHF1853522" if vot_id == "HF1853522"
			replace vot_id = "RJ19124000791" if vot_id == "RJ1912400791"
			replace vot_id = "RJ19124000124" if vot_id == "RJ19124000121"
	
			* PS-33
			replace vot_id = subinstr(vot_id,"BR4425","BR4025",.) if psid == 33 // only applies to PS-33. There are valid voter IDs with BR4425 in PS-225
			replace vot_id = "BR40251114082" if vot_id == "BR4025114082"
			replace vot_id = subinstr(vot_id,"JJBO","JJB0",.)
			replace vot_id = "YBZ1782788" if vot_id == "YB1782788"
			replace vot_id = "YBZ1173566" if vot_id == "YBZ11735660"
			replace vot_id = "YBZ1782275" if vot_id == "YBZ182275"
			replace vot_id = "YBZ0753236" if vot_id == "YBZ20753236"
			replace vot_id = "YBZ2350742" if vot_id == "YBZ235742"
			replace vot_id = subinstr(vot_id,"YBZO","YBZ0",.)
			replace vot_id = "YBZ1173236" if vot_id == "YBZ01173236"
			replace vot_id = "YBZ2627693" if vot_id == "YBZ262793"
			replace vot_id = subinstr(vot_id,"BZO","YBZ0",.)
			replace vot_id = "JJB0720383" if vot_id == "JJB0720382"
			replace vot_id = "JJB0720920" if vot_id == "JJB0720972"
			replace vot_id = "YBZ0111906" if vot_id == "YBZ0111"
			replace vot_id = "YBZ0188680" if vot_id == "YBZ018860"
			
			* PS-66 -- come back to later
			
			* PS-88
			replace vot_id = "ISQ1169812" if vot_id == "ISQ01169812"
			replace vot_id = "ISQ0608901" if vot_id == "ISQ06608901"
			replace vot_id = "ISQ1418466" if vot_id == "ISQ141866"
			replace vot_id = subinstr(vot_id,"MP035","MP35",.)
			replace vot_id = "GYX0669866" if vot_id == "GYX0669861"
			replace vot_id = "GYX0671298" if vot_id == "GYX0671248"
			
			* PS-117			
			replace vot_id = "JKD5535901" if vot_id == "JKD553590"
			replace vot_id = subinstr(vot_id,"ULK","UIK",.)
			
			* PS-147
			replace vot_id = "GYX0826172" if vot_id == "GYX082617"
			replace vot_id = "ISQ1128362" if vot_id == "ISQ112836"
			* replace vot_id = subinstr(vot_id,"MP035","MP35",.) // already included in PS-88 above
			replace vot_id = "MP35288210033" if vot_id == "MP288210033"
			replace vot_id = "GYX0826677" if vot_id == "GYX0826667"
			replace vot_id = "GYX1347988" if vot_id == "GYX1347998"
			
			* PS-182
			replace vot_id = "ULQ0847673" if vot_id == "ULQ847673"
			
			* PS-188
			replace vot_id = "CHF1682772" if vot_id == "CHF16882772"
			replace vot_id = "CHF9793621" if vot_id == "CHF979362"
			replace vot_id = "ISU1285287" if vot_id == "ISU285287"
			replace vot_id = "RJ19124147707" if vot_id == "RJ19124147707A"
			replace vot_id = "RJ19124147710" if vot_id == "RJ19124147710A"
			replace vot_id = "RJ19124147776" if vot_id == "RJ1912414776"
			replace vot_id = "CHF1683424" if vot_id == "CHF1683429"
			replace vot_id = "RJ19124147488" if vot_id == "RJ19124147486"

			* PS-190
			replace vot_id = subinstr(vot_id,"JVD","JKD",.)
			replace vot_id = "UIK1065317" if vot_id == "UIK10065317"
			* replace vot_id = subinstr(vot_id,"ULK","UIK",.) // already included in PS-117 above
			replace vot_id = "UIK1138171" if vot_id == "UIKI138171"
			replace vot_id = "UIK1262906" if vot_id == "UIKI262906"
			replace vot_id = "UIK1262930" if vot_id == "UKD1262930"
			replace vot_id = "UIK1065283" if vot_id == "UIK1043546"
			replace vot_id = "UIK1754647" if vot_id == "UIK1764647"
			
			* PS-194
			replace vot_id = subinstr(vot_id,"GSBO","GSB0",.)
			replace vot_id = subinstr(vot_id,"RAM","REM",.)
			replace vot_id = "REM0979047" if vot_id == "REM097047"
			replace vot_id = "REM1072180" if vot_id == "REM107280"
			replace vot_id = "REM2279073" if vot_id == "REM229073"
			replace vot_id = "REM0230540" if vot_id == "REMO230540"
			replace vot_id = "RME0230565" if vot_id == "REMO230565"
			replace vot_id = "REM0230698" if vot_id == "REMO230698" // REMO is not consistently census only - also in some valid voter roll IDs
			replace vot_id = "REM0230706" if vot_id == "REMO230706"
				// honestly the error is probably in the voter roll entry for these but to be consistent I'm converting all to the IDs as recorded from the voter rolls
				replace vot_id = "RME0230557" if vot_id == "REM0230557" 
				replace vot_id = "RME2273670" if vot_id == "REM2273670"
			replace vot_id = "REM0177782" if vot_id == "177782"
			replace vot_id = "REM0230599" if vot_id == "230599"
			replace vot_id = "REM1072230" if vot_id == "1072230"
			replace vot_id = "REM0230607" if vot_id == "230607"
			replace vot_id = "REM0230623" if vot_id == "230623"
			replace vot_id = "REM2394542" if vot_id == "2394542"
			replace vot_id = "REM2514313" if vot_id == "2514313"
			replace vot_id = "REM3046661" if vot_id == "3046661"
			replace vot_id = "REM0379594" if vot_id == "379594"
			replace vot_id = "REM0408195" if vot_id == "408195"
			replace vot_id = "REM0537878" if vot_id == "537878"
			replace vot_id = "REM0719203" if vot_id == "719203"
			replace vot_id = "REM0230466" if vot_id == "REM0230468"

			* PS-219
			replace vot_id = "BR10059756399" if vot_id == "BR10059756299"
			
			* PS-225
			replace vot_id = "JJB0928606" if vot_id == "JJB928606"
			replace vot_id = "JJB0928788" if vot_id == "JJBO928788"
			replace vot_id = "JJB0928440" if vot_id == "JJB0928448"
			replace vot_id = "YBZ1906981" if vot_id == "YBZ1906881"

			* PS-330
			replace vot_id = "BDV2873214" if vot_id == "BDA2873214"
			replace vot_id = "TKA2357929" if vot_id == "TAK2357929"
			replace vot_id = "TKA0517532" if vot_id == "TKA01517532"
			replace vot_id = "TKA0971499" if vot_id == "TKA097149"
			replace vot_id = subinstr(vot_id,"UP793911","UP7939101",.)
			replace vot_id = "BDV2873217" if vot_id == "BDV2873271"
			replace vot_id = "BDV6858625" if vot_id == "BDV6858623"
			replace vot_id = "TKA2549129" if vot_id == "TKA2549180"
			replace vot_id = "TKA1904432" if vot_id == "TKL1904432"
			
			* PS-352
			replace vot_id = subinstr(vot_id,"UP793917","UP7939107",.)

	duplicates tag vot_id, gen(dup)
	drop if dup>0  // 2 observations where voter IDs are the same 
	keep census_uniqid census_hhid vot_id psid *name2 name1 individual_type // Keeping more vars than necessary to compare names
	rename *name* C*name*
	rename psid Cpsid

	tempfile census_working
	save `census_working', replace

	
	* Prep Voter
		
	use "$clean_dta/voter_nmerge0", clear
	duplicates tag vot_id, gen(dup)
	drop if dup > 0 // 0 duplicates
	keep  voter_uniqid psid vot_id *name2 name1 // Keeping more vars than necessary to compare names
	rename *name* V*name*
	rename psid Vpsid	
	tempfile voter_working
	save `voter_working', replace
	

* Merge
	merge 1:1 vot_id using `census_working'

	order *psid ?name2 ?name1 *father_name2 *spouse_name2 *relation_name2

*Designate as non-matches obs that dont match on psid although they match on voter ID

/*Either they're due to typos in our entry of the voter IDs or the person is actually 
	listed in the wrong PS. If the former we may pick them up in the name matches. If the latter then we would not be able 
	to sample them from the roll, so they should be listed as exclusion errors.*/

replace _merge=2 if Vpsid != Cpsid & _merge==3 // 8 changes



* Save
	
	* Keep merges
	keep if _merge == 3
	keep census_uniqid voter_uniqid
	gen merge_type = "1(voter IDs)"
	save "$clean_dta/merge1", replace
	
	* Remainder Census
	use "$clean_dta/census_nmerge0", clear
	merge 1:1 census_uniqid using "$clean_dta/merge1"
	keep if _merge == 1
	drop _merge merge_type 
	save "$clean_dta/census_nmerge1", replace
	count
	local census_nmerge1 `r(N)'
	
	* Remainder Voter
	use "$clean_dta/voter_nmerge0", clear
	
	merge 1:1 voter_uniqid using "$clean_dta/merge1"
	keep if _merge == 1
	drop _merge merge_type 
	save "$clean_dta/voter_nmerge1", replace
	count
	local voter_nmerge1 `r(N)'
	
	disp `census_nmerge1'
	disp `voter_nmerge1'
	

