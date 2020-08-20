########################################################################################################

# DESCRIPTION: Functions used in 4-merge_steps.py for pandas column merge and Fuzzy wuzzy package

#########################################################################################################

from fuzzywuzzy import process
from fuzzywuzzy import fuzz

def merge_data(left_data_df,
               right_data_df,
               left_columns,
               right_columns,
               merge_level,
               merge_desc,
               age_limits):
    
    
    """
    Function to merge a left dataset and a right dataset based on some specified columns and an 
    age upper/lower bound
    
    """   
    
    print("*******************************************************************")
    print(str(merge_level) + ' - ' + merge_desc)
    
    # Initialize local variables
    results_df = pd.DataFrame()

    # Pandas merge
    results_df = pd.merge(left_data_df, 
                          right_data_df,
                          left_on=left_columns,
                          right_on=right_columns,
                          how='inner', 
                          indicator=True,
                          suffixes=['', '_y'])
        
    if (age_limits != "None"):
      results_df['right_age_low'] = results_df['right_age'] - int(age_limits)
      results_df['right_age_high'] = results_df['right_age'] + int(age_limits)
      results_df = results_df[results_df.left_age.between(results_df.right_age_low, results_df.right_age_high)]

      # Keep rows for each unique id for which the age is closest in the 2 datasets
      results_df['right_age_diff'] = abs(results_df['right_age'] - results_df['left_age'])
      results_df = results_df[results_df['right_age_diff'] == results_df.groupby('left_dataset_unique_id')['right_age_diff'].transform('min')]

    results_df['merge_level'] = merge_level
    results_df['merge_desc'] = merge_desc
    
    # print("Number of unique ids in the matched dataset is :" + str(len(results_df['Unique ID'].unique())))
    # print("Matched dataset is :" + str(results_df.shape))
    return results_df



def fuzzywuzzy_match(left_dataset, 
          					 left_dataset_match_column,
          					 right_dataset_match_column,
          					 additional_left_dataset_columns,
          					 additional_right_dataset_columns,
          					 right_dataset, 
          					 scorer, 
          					 cutoff):

    """
      Function to find matches in the specified right dataset column for a left dataset column 
      within the specified cutoff threshhold. The additional column specified looks for matches 
      within subset of rows where the additional column exactly matches.
  
    """

    match = process.extractOne(left_dataset[left_dataset_match_column], 
                             choices=right_dataset.loc[right_dataset[additional_right_dataset_columns] == left_dataset[additional_left_dataset_columns], 
                                     right_dataset_match_column], 
                             scorer=scorer, 
                             score_cutoff=cutoff)
    if match:
        return match[0]


