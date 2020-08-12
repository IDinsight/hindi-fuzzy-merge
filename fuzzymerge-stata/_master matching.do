/**************************************************************************************** 

TITLE:			Household Census-Voter Roll Comparison
AUTHOR: 		Ruchika Joshi (ruchika.joshi@idinsight.org)
				Jeff McManus (jeffery.mcmanus@idinsight.org)
DATE: 			August 2020

DESCRIPTION: 	These .do files match individuals in the household census with individuals in 
				contemporaneous voter rolls.

USER-WRITTEN COMMANDS:  reclink

****************************************************************************************/
			  
clear

** SETTING PATHS
 
    global root ""
	global raw_census "${root}/"
	global raw_voter "${root}/"
	global clean_dta "${root}/" 
	global output_dta "${root}/" 
	global do "${root}/"
	*sysdir set PLUS "/Applications/Stata/ado/plus/"
	*sysdir set PERSONAL "/Applications/Stata/ado/personal/"
	
	set more off
***************************************************************************************************************

set rmsg on
local starttime = c(current_time)

* 0a - Prep Household and Voter Roll Census transliterated data
quietly do "$do/0-prep voter and census data.do"

* 1 - Match Voter IDs
quietly do "$do/1-match voter ids.do"

* 2 - Match exact name and exact relation name
// 6 versions of names and 2 possible relations (allow for mis-identified relation in voter roll)
quietly do "$do/2-match exact name and relation name.do"
		
* 3 - Match exact name and fuzzy relation name
// 6 versions of names (exact match relation name: stricter about this since fuzzy matching relation name)
// Run twice, first with stricter threshold on each of 6 names (matchscore > 0.9), then on looser threshold (matchscore > 0.8) 
quietly do "$do/3-match exact name and fuzzy relation name.do"

* 4 - Match exact name and fuzzy relation name with flipped relations (in case relation is misidentified)
// 6 versions of names (exact match name: stricter about this since fuzzy matching relation name)
// Run twice, first with stricter threshold on each of 6 names (matchscore > 0.9), then on looser threshold (matchscore > 0.8) 
quietly do "$do/4-match exact name and flipped fuzzy relation name.do"

* 5 - Match fuzzy name and exact relation name
// 6 versions of names (exact match relation name: stricter about this since fuzzy matching relation name)
// Run twice, first with stricter threshold on each of 6 names (matchscore > 0.95), then on looser threshold (matchscore > 0.9) 
// Using stricter thresholds than (3) since more important that name matches than relative's name matches
quietly do "$do/5-match fuzzy name and exact relation name.do"

* 6 - Match exact name, exact gender, and fuzzy age
// 6 versions of names
// +/- 5 years, which is the average difference in the census and voter roll ages in the previous merges
quietly do "$do/6-match exact name, gender, fuzzy age.do"


* 7 - Match fuzzy name and fuzzy relation name
// 6 versions of names
// Run twice, first with stricter threshold on each of 6 names (matchscore > 0.9), then on looser threshold (matchscore > 0.8) 
quietly do "$do/7-match fuzzy name and fuzzy relation name.do"

* 8 - Match within household fuzzy name and fuzzy age
quietly do "$do/8-match within hh fuzzy name and fuzzy age.do"

* 98 - Manual matching of unmatched names
// Based on manual review of remaining unmatched census & voter rolls
quietly do "$do/98-manual matches.do"

* 99 - Append and clean
quietly do "$do/99_append and clean.do"

local endtime = c(current_time)
disp "`starttime'"
disp "`endtime'"
set rmsg off
