*********************** Transliteration Fixes ***************************


/* 
	The following fixes were identified from manual inspection, comparing
	names in the Census and Voter Rolls that match on voter IDs.
*/

*********************************
** Create alternative name (1) **
*********************************

	* Generate variable
	local name $name
	gen `name'2 = `name'
	label var `name'2 "Alternative (1) to `name' -- Transliteration standardization"
	
	
	* Replace all variations of mohamad with abbreviation MO
	// Often abbreviated this way. Also de-weights Mohammad, which is a common name
	
	
	replace `name'2 = subinstr(`name'2,"mohmemd","mo",.)
	replace `name'2 = subinstr(`name'2,"mohmd","mo",.)
	replace `name'2 = subinstr(`name'2,"mauhmemd","mo",.)
	

	
	* Transliteration standardization
	replace `name'2 = subinstr(`name'2,"meb","nb",.)
	
	/*in hindi शंभु and शम्भु are often spelt interchangeably but polyglot transliterates the dot to NB
	because the same dot is used when the name has an N sound. Although the substitution should only 
	be M to N in such cases,that would be too aggressive and has been done later. The usual culprits were followed by B*/


	* Replace SING and SINGH with SINH
	// Often spelt interchangeably
	
	replace `name'2 = subinstr(`name'2,"sing","sinh",.) if  regexm(`name'2,"sing$") == 1
	replace `name'2 = subinstr(`name'2,"singh","sinh",.) if regexm(`name'2,"singh$") == 1
	
	
	* Replace CHNEDER,CHNDER and CHNED with CHND
	// Often spelt interchangeably
	
	replace `name'2 = subinstr(`name'2,"chneder","chnd",.) if regexm(`name'2,"chneder$") == 1
	replace `name'2 = subinstr(`name'2,"chneder","chnd",.) if regexm(`name'2,"chnder$") == 1
	replace `name'2 = subinstr(`name'2,"chned","chnd",.) if regexm(`name'2,"chned$") == 1
	
	* Replace BHUIYAN and BHUINYA with BHUIYA
	// Often spelt interchangeably
	
	replace `name'2 = subinstr(`name'2,"bhuiyan","bhuiya",.) if regexm(`name'2,"bhuiyan$") == 1
	replace `name'2 = subinstr(`name'2,"bhuinya","bhuiya",.) if regexm(`name'2,"bhuinya$") == 1
	
	* Delete sheri, let and sev from the start of names because they have been transliterated from श्री , लेट, स्व prefixes 
	
	replace `name'2 = subinstr(`name'2,"sheri","",1)
	replace `name'2 = subinstr(`name'2,"let","",1)
	replace `name'2 = subinstr(`name'2,"sev","",1)


	//RJ: KARAN the following have been picked up from Jeff's analysis, I think it checks out
	
	*Delete DEVI since it is a common suffix that is inconsistently used
	// But don't delete DEVI if that is the person's full name or the start of their name
	replace `name'2 = subinstr(`name'2,"devi","",.) if `name'2 != "devi" & regexm(`name'2,"devi$") == 1

	* Delete BANO/BANU since it is a common suffix that is inconsistently used
	// But don't delete BANO/BANU if that is the person's full name
	replace `name'2 = subinstr(`name'2,"bano","",.) if `name'2 != "bano" & regexm(`name'2,"bano$") == 1
	replace `name'2 = subinstr(`name'2,"banu","",.) if `name'2 != "banu" & regexm(`name'2,"banu$") == 1

	
*********************************
** Create alternative name (2) **
*********************************

// Only first name if multiple names (since latter names are often caste names, which are sometimes included/excluded)

	* Generate variable
	gen `name'3 = word(`name'2,1) //gets the first name
	label var `name'3 "Alternative (2) to `name' -- Transliteration standardization and only keeping first name if multiple"

	* Eliminate spaces in first alternative
	replace `name'2 = subinstr(`name'2," ","",.)

	
*********************************
** Create alternative name (3) **
*********************************


// Same as Alternative 1 (name2) with more aggressive substitution of letters

	* Generate variable
	gen `name'4 = `name'2
	label var `name'4 "Alternative (3) to `name' -- More aggressive transliteration standardization than Alternative (1)"
	
	
	* Replace SIG, SNH and SIN with SINH
	// Commonly misspelt
	
	replace `name'4 = subinstr(`name'4,"sig","sinh",.) if regexm(`name'4,"sig$") == 1
	replace `name'4 = subinstr(`name'4,"snh","sinh",.) if regexm(`name'4,"snh$") == 1
	replace `name'4 = subinstr(`name'4,"sih","sing",.) if regexm(`name'4,"sih$") == 1
	
	
	*Replace common errors when writing short forms for mohammad with mo 
	replace `name'4 = subinstr(`name'4,"moo","mo",1) 
	replace `name'4 = subinstr(`name'4,"mau","mo",1)
	replace `name'4 = subinstr(`name'4,"mau","mo",.)  if regexm(`name'4,"mau$") == 1
	replace `name'4 = subinstr(`name'4,"moo","mo",.) if regexm(`name'4,"moo$") == 1
	
	*Delete "e" from "ned", "meb", etc. because half letters are transliterated differently even if the sound is same 
		/* e.g. गोविन्द is transliterated as govined and गोविंद as govind, even though the sound is the same.
		while this substitution doesn't cover all possibilities of inconsistently spelt half letters,
		it does cover the most common cases based on manual inspections*/
		
	replace `name'4 = subinstr(`name'4,"ned","nd",.)
	replace `name'4 = subinstr(`name'4,"meb","mb",.)
	replace `name'4 = subinstr(`name'4,"net","nt",.)
	replace `name'4 = subinstr(`name'4,"tet","tt",.)
	replace `name'4 = subinstr(`name'4,"hen","hn",.)
	replace `name'4 = subinstr(`name'4,"hem","hm",.)
	replace `name'4 = subinstr(`name'4,"hev","hv",.)
	replace `name'4 = subinstr(`name'4,"yey","yy",.)
	replace `name'4 = subinstr(`name'4,"yey","yy",.)
	replace `name'4 = subinstr(`name'4,"lek","lk",.)
	replace `name'4 = subinstr(`name'4,"nes","ns",.)
	
	
	* Transliteration standardization	
	replace `name'4 = subinstr(`name'4,"a","",.)	
	replace `name'4 = subinstr(`name'4,"b","v",.)
	replace `name'4 = subinstr(`name'4,"z","j",.)
	replace `name'4 = subinstr(`name'4,"sh","s",.)
	replace `name'4 = subinstr(`name'4,"m","n",.) //this may be too aggressive, KARAN plz advise
	


*********************************
** Create alternative name (4) **
*********************************

// Same as Alternative 2 (name3) with more aggressive substitution of letters

	* Generate variable
	gen `name'5 = `name'3
	label var `name'5 "Alternative (4) to `name' -- More aggressive transliteration standardization than Alternative (2)"
	

	*Replace common errors when writing short forms for mohammad with mo 
	replace `name'5 = subinstr(`name'5,"moo","mo",1) 
	replace `name'5 = subinstr(`name'5,"mau","mo",1)
	replace `name'5 = subinstr(`name'5,"mau","mo",.)  if regexm(`name'5,"mau$") == 1
	replace `name'5 = subinstr(`name'5,"moo","mo",.) if regexm(`name'5,"moo$") == 1
	
	
		*Delete "e" from "ned", "meb", etc. because half letters are transliterated differently even if the sound is same 
		/* e.g. गोविन्द is transliterated as govined and गोविंद as govind, even though the sound is the same.
		while this substitution doesn't cover all possibilities of inconsistently spelt half letters,
		it does cover the most common cases based on manual inspections*/
		
	replace `name'5 = subinstr(`name'5,"ned","nd",.)
	replace `name'5 = subinstr(`name'5,"meb","mb",.)
	replace `name'5 = subinstr(`name'5,"net","nt",.)
	replace `name'5 = subinstr(`name'5,"tet","tt",.)
	replace `name'5 = subinstr(`name'5,"hen","hn",.)
	replace `name'5 = subinstr(`name'5,"hem","hm",.)
	replace `name'5 = subinstr(`name'5,"hev","hv",.)
	replace `name'5 = subinstr(`name'5,"yey","yy",.)
	replace `name'5 = subinstr(`name'5,"lek","lk",.)
	replace `name'5 = subinstr(`name'5,"nes","ns",.)	
	
	* Transliteration standardization
	replace `name'5 = subinstr(`name'5,"a","",.)	
	replace `name'5 = subinstr(`name'5,"b","v",.)
	replace `name'5 = subinstr(`name'5,"z","j",.)
	replace `name'5 = subinstr(`name'5,"sh","s",.)
	replace `name'5 = subinstr(`name'5,"m","n",.) //this may be too aggressive, KARAN plz advise

*********************************
** Create alternative name (5) **
*********************************

// Same as Alternative 4 (name5) with removal of common last names that were inconsistently appended to first names (rather than being a separate word)

	* Generate variable
	gen `name'6 = `name'5
	label var `name'6 "Alternative (5) to `name' -- Same as Alternative (4) with removal of common last names that were inconsistently appended to first names"
	
	* Remove last names appended to first names (but not if that's the whole name)
	replace `name'6 = subinstr(`name'6,"chnderji","",.) if regexm(`name'6,"chnderji$") == 1 & `name'6 != "chnderji"
	replace `name'6 = subinstr(`name'6,"chnder","",.) if regexm(`name'6,"chnder$") == 1 & `name'6 != "chnder"
	replace `name'6 = subinstr(`name'6,"chnd","",.) if regexm(`name'6,"chnd$") == 1 & `name'6 != "chnd"
	replace `name'6 = subinstr(`name'6,"sinh","",.) if regexm(`name'6,"sinh$") == 1 & `name'6 != "sinh"
	replace `name'6 = subinstr(`name'6,"nryn","",.) if regexm(`name'6,"nyrn$") == 1 & `name'6 != "nyrn"
	replace `name'6 = subinstr(`name'6,"sekhr","",.) if regexm(`name'6,"sekhr$") == 1 & `name'6 != "sekhr"
	replace `name'6 = subinstr(`name'6,"persd","",.) if regexm(`name'6,"persd$") == 1 & `name'6 != "persd"
	replace `name'6 = subinstr(`name'6,"kunr","",.) if regexm(`name'6,"kunr$") == 1 & `name'6 != "kunr"
	replace `name'6 = subinstr(`name'6,"vihri","",.) if regexm(`name'6,"vihri$") == 1 & `name'6 != "vihri"
