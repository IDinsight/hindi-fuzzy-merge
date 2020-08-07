#####################################################################################################

# DESCRIPTION: Function used in 4-merge_steps.py for loading dataset and cleaning
# AUTHOR: IDinsight Inc.

######################################################################################################

exec(open('1-helper_functions.py').read())
import pandas as pd

def get_dataset(inputs_config, 
                left_or_right):

    """
        Function to fetch the left/right dataset based on the defined inputs, perform a few
        consistency checks and rename columns

    """

    if (left_or_right not in ['left', 'right']):
        print("Unexpected argument '" + left_or_right + "' passed in get_dataset function.")
        return

    # Dataset Configurations
    dataset_config = inputs_config[left_or_right + "_dataset"]
    dataset_file_type = dataset_config["csv_or_excel"]
    dataset_file_path = dataset_config["path"]
    dataset_unique_id = dataset_config["dataset_unique_id"]
    dataset_column_mapping = dataset_config["columns_mapping"]

    # Read data from provided filepath
    if (dataset_file_type == "csv"):
        data_df = pd.read_csv(dataset_file_path, dtype=str)
    elif (dataset_file_type == "excel"):
        data_df = pd.read_excel(dataset_file_path, dtype=str)
    else:
        print("Incorrect " + left_or_right + " dataset type. Allowed values are 'csv' and 'excel'.")
        return

    # Check columns
    column_names = []
    file_column_names = []
    rename_dict = {}
    for key, value in dataset_column_mapping.items():
        column_names.append(key)
        file_column_names.append(value)
        rename_dict[value] = key

    rename_dict[dataset_config["dataset_unique_id"]] = 'dataset_unique_id'

    for column in file_column_names:
        if column not in data_df.columns:
            print("Incorrect column name provided for " + left_or_right + " dataset in matching config: " + column + ". Check file and provide the correct column name.")
            return

    # Rename columns on the dataset
    data_df.rename(columns=rename_dict, inplace=True)

    # Check if dataset unique id column is indeed unique
    v_dup_unique_id_df = data_df.groupby('dataset_unique_id').filter(lambda x: len(x) > 1)
    if (len(v_dup_unique_id_df) > 0):
        print("The unique id column for the " + left_or_right + " dataset should be unique for each row.")
        return

    # Get number of rows and apply data cleaning
    num_of_data_rows = data_df.shape[0] 
    if (num_of_data_rows > 0):
        if (left_or_right == 'left'):
            data_df = process_left_dataset(data_df, left_or_right)
        else:
            data_df = process_right_dataset(data_df, left_or_right)
    else:
        print("No data to match. Empty " + left_or_right + " dataset.")
        return

    return data_df



def process_left_dataset(left_dataset, 
                         prefix):

    """
        Function to standardize columns in the left dataset, create new columns for the merge etc.
    """

    # Split the names with a slash -  may not be needed for the new incoming data
    child_names = left_dataset["childname"].str.split("/", n =-1, expand = True) 
    # Making first name and altername first name columns
    left_dataset['childname']= child_names[0]
    if (child_names.shape[1] > 1):
        left_dataset['childname_alt']= child_names[1].combine_first(child_names[0])
    else: 
        left_dataset['childname_alt'] = child_names[0]

    # Create transliteration fixed alterations for child name in form6 data
    left_dataset['childname'] = left_dataset['childname'].apply(lambda x: x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    left_dataset['childname1'] = left_dataset['childname'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    left_dataset['childname2'] = left_dataset['childname'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    left_dataset['childname3'] = left_dataset['childname1'].apply(lambda x: fix_transliterations_level_1(x))
    left_dataset['childname4'] = left_dataset['childname2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    left_dataset['childname5'] = left_dataset['childname3'].apply(lambda x: fix_transliterations_level_2(x))
    left_dataset['childname6'] = left_dataset['childname4'].apply(lambda x: fix_transliterations_level_2(x))

    left_dataset['childname_alt'] = left_dataset['childname_alt'].apply(lambda x: x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    left_dataset['childname_alt1'] = left_dataset['childname_alt'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    left_dataset['childname_alt2'] = left_dataset['childname_alt'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    left_dataset['childname_alt3'] = left_dataset['childname_alt1'].apply(lambda x: fix_transliterations_level_1(x))
    left_dataset['childname_alt4'] = left_dataset['childname_alt2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    left_dataset['childname_alt5'] = left_dataset['childname_alt3'].apply(lambda x: fix_transliterations_level_2(x))
    left_dataset['childname_alt6'] = left_dataset['childname_alt4'].apply(lambda x: fix_transliterations_level_2(x))

    # Split the names with a slash -  may not be needed for the new incoming data
    father_names = left_dataset["fathername"].str.split("/", n = 1, expand = True) 
    # Making first name and altername first name columns
    left_dataset['fathername']= father_names[0]
    if (father_names.shape[1] > 1):
        left_dataset['fathername_alt']= father_names[1].combine_first(father_names[0])
    else: 
        left_dataset['fathername_alt'] = father_names[0]

    # Create transliteration fixed alterations for father name in d2d data
    left_dataset['fathername'] = left_dataset['fathername'].apply(lambda x: x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    left_dataset['fathername1'] = left_dataset['fathername'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    left_dataset['fathername2'] = left_dataset['fathername'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    left_dataset['fathername3'] = left_dataset['fathername1'].apply(lambda x: fix_transliterations_level_1(x))
    left_dataset['fathername4'] = left_dataset['fathername2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    left_dataset['fathername5'] = left_dataset['fathername3'].apply(lambda x: fix_transliterations_level_2(x))
    left_dataset['fathername6'] = left_dataset['fathername4'].apply(lambda x: fix_transliterations_level_2(x))

    # Create transliteration fixed alterations for father name in d2d data
    left_dataset['fathername_alt'] = left_dataset['fathername_alt'].apply(lambda x: x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    left_dataset['fathername_alt1'] = left_dataset['fathername_alt'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    left_dataset['fathername_alt2'] = left_dataset['fathername_alt'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    left_dataset['fathername_alt3'] = left_dataset['fathername_alt1'].apply(lambda x: fix_transliterations_level_1(x))
    left_dataset['fathername_alt4'] = left_dataset['fathername_alt2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    left_dataset['fathername_alt5'] = left_dataset['fathername_alt3'].apply(lambda x: fix_transliterations_level_2(x))
    left_dataset['fathername_alt6'] = left_dataset['fathername_alt4'].apply(lambda x: fix_transliterations_level_2(x))

    # Update and format columns in form 6 df 
    left_dataset['gender'] = left_dataset['gender'].str.upper().str.strip()
    left_dataset['village'] = left_dataset['village_code'].str.upper().str.strip()
    left_dataset['cluster'] = left_dataset['cluster_code'].str.upper().str.strip()
    # left_dataset['block'] = left_dataset['block_code'].str.upper().str.strip()
    # left_dataset['district'] = left_dataset['district_code'].str.upper().str.strip()
    left_dataset["age"]= pd.to_numeric(left_dataset["age"])

    # First extract only number from the column - because the column could be in value - label format
    left_dataset['social_category'] = left_dataset['social_category'].apply(lambda x: "".join([str(i) for i in str(x) if is_float(i)]))
    left_dataset["social_category"]= pd.to_numeric(left_dataset["social_category"])

    # Soundex on child and father full names
    left_dataset['childname1_soundex'] = left_dataset['childname1'].apply(lambda x: soundex(x))
    left_dataset['fathername1_soundex'] = left_dataset['fathername1'].apply(lambda x: soundex(x))

    # Soundex on child and father first names
    # left_dataset['childname2_soundex'] = left_dataset['childname2'].apply(lambda x: soundex(x))
    # left_dataset['fathername2_soundex'] = left_dataset['fathername2'].apply(lambda x: soundex(x))

    left_dataset['cn_soundex_1'] = left_dataset['childname1_soundex'].apply(lambda x: get_first_letter_key(x))
    left_dataset['fn_soundex_1'] = left_dataset['fathername1_soundex'].apply(lambda x: get_first_letter_key(x))
    
    # Add prefix to all columns - 'l_' if left_dataset and 'r_' if right
    left_dataset.columns = [prefix + '_' + str(col) for col in left_dataset.columns]

    return left_dataset



def process_right_dataset(right_dataset,
                          prefix):
    """
        Function to standardize columns in the right dataset, create new columns for the merge etc.
    """

    # Create transliteration fixed alterations for child name in d2d data
    right_dataset['childname'] = right_dataset['childname'].apply(lambda x: x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    right_dataset['childname1'] = right_dataset['childname'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    right_dataset['childname2'] = right_dataset['childname'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    right_dataset['childname3'] = right_dataset['childname1'].apply(lambda x: fix_transliterations_level_1(x))
    right_dataset['childname4'] = right_dataset['childname2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    right_dataset['childname5'] = right_dataset['childname3'].apply(lambda x: fix_transliterations_level_2(x))
    right_dataset['childname6'] = right_dataset['childname4'].apply(lambda x: fix_transliterations_level_2(x))

    # Create transliteration fixed alterations for father name in d2d data
    right_dataset['fathername'] = right_dataset['fathername'].apply(lambda x:x.upper().strip() if x != None and not is_float(str(x)) else str(x))
    # First name and Full name
    right_dataset['fathername1'] = right_dataset['fathername'].apply(lambda x: keep_full_name(remove_non_alph_characters(x)))
    right_dataset['fathername2'] = right_dataset['fathername'].apply(lambda x: keep_first_name(remove_non_alph_characters(x)))
    # Level 1 on first name and full name
    right_dataset['fathername3'] = right_dataset['fathername1'].apply(lambda x: fix_transliterations_level_1(x))
    right_dataset['fathername4'] = right_dataset['fathername2'].apply(lambda x: fix_transliterations_level_1(x))
    # Level 1 and 3 on first name and full name
    right_dataset['fathername5'] = right_dataset['fathername3'].apply(lambda x: fix_transliterations_level_2(x))
    right_dataset['fathername6'] = right_dataset['fathername4'].apply(lambda x: fix_transliterations_level_2(x))

    # Update and format columns in d2d df 
    right_dataset['gender'] = right_dataset['gender'].str.upper().str.strip()
    right_dataset['village'] = right_dataset['village_code'].str.upper().str.strip()
    right_dataset['cluster'] = right_dataset['cluster_code'].str.upper().str.strip()
    # right_dataset['block'] = right_dataset['block_code'].str.upper().str.strip()
    # right_dataset['district'] = right_dataset['district_code'].str.upper().str.strip()
    right_dataset["age"]= pd.to_numeric(right_dataset["age"])

    # First extract only number from the column - because the column could be in value - label format
    right_dataset['social_category'] = right_dataset['social_category'].apply(lambda x: "".join([str(i) for i in str(x) if is_float(i)]))
    right_dataset["social_category"]= pd.to_numeric(right_dataset["social_category"])

    # Soundex on child and father full names
    right_dataset['childname1_soundex'] = right_dataset['childname1'].apply(lambda x: soundex(x))
    right_dataset['fathername1_soundex'] = right_dataset['fathername1'].apply(lambda x: soundex(x))

    # Soundex on child and father first names
    # right_dataset['childname2_soundex'] = right_dataset['childname2'].apply(lambda x: soundex(x))
    # right_dataset['fathername2_soundex'] = right_dataset['fathername2'].apply(lambda x: soundex(x))

    right_dataset['cn_soundex_1'] = right_dataset['childname1_soundex'].apply(lambda x: get_first_letter_key(x))
    right_dataset['fn_soundex_1'] = right_dataset['fathername1_soundex'] .apply(lambda x: get_first_letter_key(x))

    # Add prefix to all columns - 'r_' since right_dataset
    right_dataset.columns = [prefix + '_' + str(col) for col in right_dataset.columns]

    return right_dataset
