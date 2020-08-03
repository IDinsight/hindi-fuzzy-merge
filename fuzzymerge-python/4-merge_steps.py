#######################################################################################################

# DESCRIPTION: Python file with customizable python code to match two datasets containing transliterated Hindi texts,
# 			   age limits etc.

# AUTHOR: Jeenu Thomas (IDinsight Inc.)
# LAST UPDATED ON: 31-07-2020   

# CODE TO RUN: python3 fuzzymerge.py

# GENERAL NOTES: 
# 		1. Prerequisites are: A Python environment
# 		2. Update the matching_config.json for file paths and variable names
# 		3. Update the code to use the variables names and steps based on your dataset

# Install: python-Levenshtein, fuzzywuzzy, pandas, json, 
########################################################################################################

exec(open('2-cleaning_functions.py').read())
exec(open('3-merge_functions.py').read())

def run():

    # Initialize dataframes to store all the matched datasets
    results_final_df = pd.DataFrame()
    left_data_df = pd.DataFrame()
    right_data_df = pd.DataFrame()

    # If manual files are provided, read in config and then the files
    matching_config = read_matching_config()
    inputs_config = matching_config["inputs"]
    outputs_config = matching_config["outputs"]

    # Get left and right datasets
    left_data_df = get_dataset(inputs_config, 'left')
    right_data_df = get_dataset(inputs_config, 'right')

    print(left_data_df.shape)
    print(right_data_df.shape)

    ################################################### Merges ###########################################################

    left_columns_to_keep = outputs_config["left_columns_to_keep"]
    right_columns_to_keep = outputs_config["right_columns_to_keep"]

    columns_to_keep = ['left_' + str(col) for col in left_columns_to_keep] + ['right_' + str(col) for col in right_columns_to_keep]

    if 'left_dataset_unique_id' not in columns_to_keep:
        # Add to beginning of the list
        columns_to_keep = ['left_dataset_unique_id'] + columns_to_keep

    columns_to_keep.append('merge_level')
    columns_to_keep.append('merge_desc')


    matching_steps_json =[
    {
    # 1 - Exact match on all variables at village level
    "level_desc":"Village, All 5 variables",
    "left_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    {
    "level_desc":"Village, All 5 variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt1', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    # 2 - Exact match on full names, all variables except age, allow age ± 15  (Child name, father name, gender and caste, age ± 15)
    {                             
    "level_desc":"Village, Age ± 15, Other variables",
    "left_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category'],
    "age_limit": "15",
    },  
    {
    "level_desc":"Village, Age ± 15, Other variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender', 'social_category'],
    "age_limit": "15",
    },
    # 3 - Match without social category (Child name, father name, gender, age ± 3)
    {
    "level_desc":"Match by fuzzy name, gender, mobile and age",
    "left_columns": ['village_code', 'childname1', 'fathername1', 'gender'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender'],
    "age_limit": "3",
    },
    {
    "level_desc":"Match by fuzzy name, gender, mobile and age",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt1', 'gender'],
    "right_columns": ['village_code', 'childname1', 'fathername1', 'gender'],
    "age_limit": "3",
    },
    # 4.1 - Exact match on first father names and all other variables
    {
    "level_desc": "Village, First Father Names, Other variables",
    "left_columns": ['village_code', 'childname1', 'fathername2', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname1', 'fathername2', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    {
    "level_desc": "Village, First Father Names, Other variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt2', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname1', 'fathername2', 'gender', 'social_category', 'age' ],
    "age_limit": "0",
    },
    # 4.2 - Exact match on first child names and all other variables
    {
    "level_desc": "Village, First Child Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    {
    "level_desc": "Village, First Child Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt1', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    # 4.3 - Exact match on first names and all other variables
    {
    "level_desc": "Village, First Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    {
    "level_desc":"Village, First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt2', 'gender', 'social_category', 'age'],
    "right_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category', 'age'],
    "age_limit": "0",
    },
    # 5.1 - Exact match on first father names, all other variables except age, allow age ± 2
    {
    "level_desc":"Village, Age ± 2, First Father Names, Other variables",
    "left_columns": ['village_code', 'childname1', 'fathername2', 'gender', 'social_category'],
    "right_columns":['village_code', 'childname1', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, First Father Names, Other variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
    # 5.2 - Exact match on first child names, all other variables except age, allow age ± 2 
    {
    "level_desc":"Village, Age ± 2, First Child Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, First Child Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },
    # 5.3 - Exact match on first names, all other variables except age, allow age ± 2
    {
    "level_desc":"Village, Age ± 2, First Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
	# 6.1 - Exact match on full father name with level 1 transliteration fixes, all other variables except age, allow age ± 2 (Child name, father name level 1, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 Father names, Other variables",
    "left_columns": ['village_code', 'childname1', 'fathername3', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername3', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 Father names, Other variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt3', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername3', 'gender', 'social_category'],
    "age_limit": "2",
    },   
	# 6.2 - Exact match on full child names with level 1 transliteration fixes, all other variables except age, allow age ± 2 (Child name level 1, father name, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 Child Names, Other variables",
    "left_columns": ['village_code', 'childname3', 'fathername1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname3', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 Child Names, Other variables",
    "left_columns": ['village_code', 'childname_alt3', 'fathername_alt1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname3', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },  
	# 6.3 - Exact match on full names with level 1 transliteration fixes, all other variables except age, allow age ± 2 (Child name level 1, father name level 1, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 Names, Other variables",
    "left_columns": ['village_code', 'childname3', 'fathername3', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname3', 'fathername3', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 Names, Other variables",
    "left_columns": ['village_code', 'childname_alt3', 'fathername_alt3', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname3', 'fathername3', 'gender', 'social_category'],
    "age_limit": "2",
    },    
	# 7.1 - Exact match on first names with level 1 transliteration fixes, all other variables except age, allow age ± 2 (Child first name, father first name level 1, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 Father First Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername4', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname4', 'fathername4', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 Father First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt4', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername4', 'gender', 'social_category'],
    "age_limit": "2",
    }, 
	# 7.2 - Exact match on first names with level 1 transliteration fixes, all other variables except age, allow age ± 2 (Child first name level 1, father first name, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 Child First Names, Other variables",
    "left_columns": ['village_code', 'childname4', 'fathername2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname4', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 Child First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt4', 'fathername_alt2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname4', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    }, 
	# 7.3 - Exact match on first names with level 2 transliteration fixes, all other variables except age, allow age ± 2 (Child first name level 1, father first name level 1, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 First Names, Other variables",
    "left_columns": ['village_code', 'childname4', 'fathername4', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname4', 'fathername4', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt4', 'fathername_alt4', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname4', 'fathername4', 'gender', 'social_category'],
    "age_limit": "2",
    },  
	# 8.1 - Exact match on full names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child name, father name level 2, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Father Names, Other variables",
    "left_columns": ['village_code', 'childname1', 'fathername5', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername5', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Father Names, Other variables",
    "left_columns": ['village_code', 'childname_alt1', 'fathername_alt5', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname1', 'fathername5', 'gender', 'social_category'],
    "age_limit": "2",
    }, 
    # 8.2 - Exact match on full names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child name level 2, father name, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Child Names, Other variables",
    "left_columns": ['village_code', 'childname5', 'fathername1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname5', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Child Names, Other variables",
    "left_columns": ['village_code', 'childname_alt5', 'fathername_alt1', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname5', 'fathername1', 'gender', 'social_category'],
    "age_limit": "2",
    },   
    # 8.3 - Exact match on full names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child name level 2, father name level 2, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Names, Other variables",
    "left_columns": ['village_code', 'childname5', 'fathername5', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname5', 'fathername5', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Names, Other variables",
    "left_columns": ['village_code', 'childname_alt5', 'fathername_alt5', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname5', 'fathername5', 'gender', 'social_category'],
    "age_limit": "2",
    },     
    # 9.1 - Exact match on first names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child first name, father first name level 2, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Father First Names, Other variables",
    "left_columns": ['village_code', 'childname2', 'fathername6', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername6', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Father First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt2', 'fathername_alt6', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname2', 'fathername6', 'gender', 'social_category'],
    "age_limit": "2",
    },
    # 9.2 - Exact match on first names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child first name level 2, father first name, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Child First Names, Other variables",
    "left_columns": ['village_code', 'childname6', 'fathername2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname6', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 Child First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt6', 'fathername_alt2', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname6', 'fathername2', 'gender', 'social_category'],
    "age_limit": "2",
    }, 
	# 9.3 - Exact match on first names with level 1 + 2 transliteration fixes, all other variables except age, allow age ± 2 (Child first name level 2, father first name level 2, gender and caste, age ± 2)
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 First Names, Other variables",
    "left_columns": ['village_code', 'childname6', 'fathername6', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname6', 'fathername6', 'gender', 'social_category'],
    "age_limit": "2",
    },
    {
    "level_desc":"Village, Age ± 2, Level 1 & 2 First Names, Other variables",
    "left_columns": ['village_code', 'childname_alt6', 'fathername_alt6', 'gender', 'social_category'],
    "right_columns": ['village_code', 'childname6', 'fathername6', 'gender', 'social_category'],
    "age_limit": "2",
    }
    ]

    # Loop through matching config jsom and perform merge
    step_counter = 1
    for match_step in matching_steps_json:

        match_step_results_df = merge_data(left_data_df,
                                           right_data_df,
                                           ['left_' + x for x in match_step["left_columns"]],
                                           ['right_' + x for x in match_step["right_columns"]],
                                           step_counter,
                                           match_step["level_desc"],
                                           match_step["age_limit"]
                                           )

		# remove matched rows from left dataset
        left_data_df = left_data_df[~left_data_df['left_dataset_unique_id'].isin(match_step_results_df['left_dataset_unique_id'])]
        
        match_step_results_df = match_step_results_df[columns_to_keep]
        results_final_df = pd.concat([results_final_df, match_step_results_df], ignore_index=True, sort=True)
        
        print("Matched dataset is :" + str(results_final_df.shape))
        print("Remaining left dataset is :" + str(left_data_df.shape))

        step_counter = step_counter + 1


    # ############################################# Fuzzy Wuzzy Ratio Merge ################################################

    print("*******************************************************************")
    merge_level = step_counter
    merge_desc = "Exact fathername6, child names merged using fuzzy wuzzy ratio, Age+5"
    print(str(merge_level) + " - " + merge_desc)

    left_data_df['left_merge_column_concat'] = left_data_df['left_village_code'] + left_data_df['left_fathername6'] + left_data_df['left_gender']
    right_data_df['right_merge_column_concat'] = right_data_df['right_village_code'] + right_data_df['right_fathername6'] +  right_data_df['right_gender']


    left_data_df['childname1_match'] = left_data_df.apply(fuzzywuzzy_match, 
                                                    args=('left_childname1', 'right_childname1', 
                                                          'left_merge_column_concat', 'right_merge_column_concat',
                                                          right_data_df, fuzz.ratio, 90), 
                                                    axis=1)
                                         

    fuzzywuzzy_results_df = pd.merge(left_data_df, right_data_df, 
                                     left_on=['childname1_match', 'left_village_code', 'left_fathername6', 'left_gender'],
                                     right_on=['right_childname1', 'right_village_code', 'right_fathername6', 'right_gender'],
                                     how='inner', indicator=True, suffixes=['', '_y'])

    fuzzywuzzy_results_df['right_age_low'] = fuzzywuzzy_results_df['right_age'] - 5
    fuzzywuzzy_results_df['right_age_high'] = fuzzywuzzy_results_df['right_age'] + 5
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[fuzzywuzzy_results_df.left_age.between(fuzzywuzzy_results_df.right_age_low, fuzzywuzzy_results_df.right_age_high)]

    # Keep rows for each unique id for which the age is closest in the 2 datasets
    fuzzywuzzy_results_df['age_diff'] = abs(fuzzywuzzy_results_df['right_age'] - fuzzywuzzy_results_df['left_age'])
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[fuzzywuzzy_results_df['age_diff'] == fuzzywuzzy_results_df.groupby('left_dataset_unique_id')['age_diff'].transform('min')]

    fuzzywuzzy_results_df['merge_level'] = merge_level
    fuzzywuzzy_results_df['merge_desc'] = merge_desc

    # remove matched rows from left dataset
    left_data_df = left_data_df[~left_data_df['left_dataset_unique_id'].isin(fuzzywuzzy_results_df['left_dataset_unique_id'])]
    
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[columns_to_keep]
    results_final_df = pd.concat([results_final_df, fuzzywuzzy_results_df], ignore_index=True, sort=True)
    
    print("Matched dataset is :" + str(results_final_df.shape))
    print("Remaining left dataset is :" + str(left_data_df.shape))

    step_counter = step_counter + 1

    
    # ############################################### Lev + Soundex ##################################################
    # # Combining lev (masala merge code) with soundex because the masala merge code is too slow and first merging by 
    # # soundex allows bringing down the number of rows to calculated edit distance for

    # print("*******************************************************************")
    # merge_level = step_counter
    # merge_desc = "Exact gender, names merged using lev and soundex, Age+5"
    # print(str(merge_level) + " - " + merge_desc)

    # # 26 - Levenshtein merges
    # lev_results_df = pd.merge(left_data_df, right_data_df, 
    #                   left_on=['left_village_code', 'left_gender', 'left_social_category', 'left_fathername1_soundex'],
    #                   right_on=['right_village_code', 'right_gender', 'right_social_category', 'right_fathername1_soundex'],
    #                   how='inner', indicator=True, suffixes=['', '_y'])

    # if (len(lev_results_df) > 0):
    #     lev_results_df.loc[:,'childname1_lev'] = lev_results_df.apply(lambda row: levenshtein(row['left_childname1'], row['right_childname1']), axis=1)
    #     lev_results_df.loc[:,'fathername1_lev'] = lev_results_df.apply(lambda row: levenshtein(row['left_fathername1'], row['right_fathername1']), axis=1)
    #     lev_results_df.loc[:,'total_lev_scores'] = lev_results_df['childname1_lev'] + lev_results_df['fathername1_lev']
    #     lev_results_df = lev_results_df[lev_results_df['total_lev_scores'] == lev_results_df.groupby('left_dataset_unique_id')['total_lev_scores'].transform('min')]
    #     v_result_threshhold_lev_1 = lev_results_df[lev_results_df['total_lev_scores'] <= 1]

    #     v_result_threshhold_lev_1.loc[:,'right_age_low'] = v_result_threshhold_lev_1['right_age'] - 5
    #     v_result_threshhold_lev_1.loc[:,'right_age_high'] = v_result_threshhold_lev_1['right_age'] + 5
    #     v_result_threshhold_lev = v_result_threshhold_lev_1[v_result_threshhold_lev_1.left_age.between(v_result_threshhold_lev_1.right_age_low, v_result_threshhold_lev_1.right_age_high)]

    #     # Keep rows for each unique id for which the age is closest in the 2 datasets
    #     v_result_threshhold_lev['age_diff'] = abs(v_result_threshhold_lev['right_age'] - v_result_threshhold_lev['left_age'])
    #     v_result_threshhold_lev = v_result_threshhold_lev[v_result_threshhold_lev['age_diff'] == v_result_threshhold_lev.groupby('left_dataset_unique_id')['age_diff'].transform('min')]

    #     v_result_threshhold_lev = v_result_threshhold_lev[columns_to_keep]    
    #     v_result_threshhold_lev['merge_level'] = merge_level
    #     v_result_threshhold_lev['merge_desc'] = merge_desc

    #     # remove matched rows from left dataset
    #     left_data_df = left_data_df[~left_data_df['left_dataset_unique_id'].isin(v_result_threshhold_lev['left_dataset_unique_id'])]
        
    #     fuzzywuzzy_results_df = fuzzywuzzy_results_df[columns_to_keep]
    #     results_final_df = pd.concat([results_final_df, fuzzywuzzy_results_df], ignore_index=True, sort=True)

    # print("Matched dataset is :" + str(results_final_df.shape))
    # print("Remaining left dataset is :" + str(left_data_df.shape))

    # step_counter = step_counter + 1


    # ############################################# Fuzzy Wuzzy Partial Ratio ################################################
  
    print("*******************************************************************")
    merge_level = step_counter
    merge_desc = "Exact fathername6, child names merged using fuzzy wuzzy partial ratio, Age+5"
    print(str(merge_level) + " - " + merge_desc)

    left_data_df['left_merge_column_concat'] = left_data_df['left_village_code'] + left_data_df['left_fathername6'] + left_data_df['left_gender']
    right_data_df['right_merge_column_concat'] = right_data_df['right_village_code'] + right_data_df['right_fathername6'] +  right_data_df['right_gender']



    left_data_df['childname1_match'] = left_data_df.apply(fuzzywuzzy_match, 
                                                    args=('left_childname1', 'right_childname1', 
                                                          'left_merge_column_concat', 'right_merge_column_concat',
                                                          right_data_df, fuzz.partial_ratio, 90), 
                                                    axis=1)
                                         

    fuzzywuzzy_results_df = pd.merge(left_data_df, right_data_df, 
                                     left_on=['childname1_match', 'left_village_code', 'left_fathername6', 'left_gender'],
                                     right_on=['right_childname1', 'right_village_code', 'right_fathername6', 'right_gender'],
                                     how='inner', indicator=True, suffixes=['', '_y'])

    fuzzywuzzy_results_df['right_age_low'] = fuzzywuzzy_results_df['right_age'] - 5
    fuzzywuzzy_results_df['right_age_high'] = fuzzywuzzy_results_df['right_age'] + 5
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[fuzzywuzzy_results_df.left_age.between(fuzzywuzzy_results_df.right_age_low, fuzzywuzzy_results_df.right_age_high)]

    # Keep rows for each unique id for which the age is closest in the 2 datasets
    fuzzywuzzy_results_df['age_diff'] = abs(fuzzywuzzy_results_df['right_age'] - fuzzywuzzy_results_df['left_age'])
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[fuzzywuzzy_results_df['age_diff'] == fuzzywuzzy_results_df.groupby('left_dataset_unique_id')['age_diff'].transform('min')]

    fuzzywuzzy_results_df['merge_level'] = merge_level
    fuzzywuzzy_results_df['merge_desc'] = merge_desc

    # remove matched rows from left dataset
    left_data_df = left_data_df[~left_data_df['left_dataset_unique_id'].isin(fuzzywuzzy_results_df['left_dataset_unique_id'])]
    
    fuzzywuzzy_results_df = fuzzywuzzy_results_df[columns_to_keep]
    results_final_df = pd.concat([results_final_df, fuzzywuzzy_results_df], ignore_index=True, sort=True)
    
    print("Matched dataset is :" + str(results_final_df.shape))
    print("Remaining left dataset is :" + str(left_data_df.shape))

    step_counter = step_counter + 1


    #########################################################################################################
    ############################################### Output ##################################################
    #########################################################################################################

    # Write the outputs to the outputs path provided in config
    outputs_path = outputs_config["path"]

    # columns = []
    # results_final_df_file = results_final_df[columns]

    results_final_df_file = results_final_df.copy()
    results_final_df_file = results_final_df_file[columns_to_keep]
    results_final_df_file.sort_values(by=['left_dataset_unique_id'])
    results_final_df_file.to_csv(outputs_path + "/matches.csv", index=False)


if __name__ == '__main__':

    run()
    

