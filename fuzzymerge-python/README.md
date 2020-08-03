# fuzzymerge-python

## Overview

Python code for merging two datasets containing columns with Hindi tranlisterated text/names. This code was originally written for matching two datasets containing the variables: village code, cluster code, child name, father name, gender, age and social category. 

The underlying algorithm relies on using different combinations of available variables in a step-by-step manner starting with the most reliable criteria for identifying true matches (which is, exact matches on all variables), and progressively using less and less reliable criteria. The reliability was decided based on running the algorithm on a small sample of test data.

This code is meant to serve as an example of the algorithm. When working on a similar matching datasets problem, you can take this code and customize it to work with your own dataset by changing variables names, matching steps etc. based on the data you are working with.


## Directory Structure
```bash
.
|-- 0-matching_config.json  # Config file for specifying the input file paths, column name mapping etc.
|-- 1-helper_functions.py 	# All functions used in the matching steps like string manipulation functions, transliteration fixes etc. 
|-- 2-cleaning_functions.py 	# All data reading and cleaning functions
|-- 3-merge_functions.py 	# All functions used for merge operations 
|-- 4-merge_steps.py 	# Main Python file with the merge steps which calls functions from other files 
|-- Data 	# Optional: Directory to store the input and output files
	  |-- *.csv/*.excel 	# Optional: Input files for left and right datasets
	  |-- Results 	# Optional: Subfolder for storing output file containg the match results
	  		|-- *.csv 
```

## Files
1. 0-matching_config.json

Here is a description for each key in the configuration file:
  * `inputs.(left/right)_dataset.path`: Path to the left and right datasets. The aim of the matching problem for which this code was written was to find a match for each row in the left dataset, in the right dataset. In each matching step, as soon as a match is found for a row in left dataset, it was removed from the left dataset while the right dataset continues to be the same throughout.
  * `inputs.(left/right)_dataset.csv_or_excel`: File type (csv/excel) of the input file.
  * `inputs.(left/right)_dataset.dataset_unique_id`: Column name for the unique identifier for each row in the left/right dataset. The code throws an error in case this column is not unique.
  * `inputs.(left/right)_dataset.columns_mapping`: All columns which are going to be used in the matching steps except the unique id column can be specified here. The keys are the actual (expected) column names and the values are the corresponding columns in the file. This mapping is used to rename the columns to the expected column names for the code to work with files with different column headers, if needed. 
  * `outputs.path`: Path to the folder where the outputs file 'matches.csv' should be stored.
  * `outputs.(left/right)_columns_to_keep`: Columns from the left/right dataset you want to include in the output file. Here the 'keys' specified in columns_mapping which are the expected column names can be used to refer to the columns.


2. 1-helper_functions.py
Functions used for manipulation of strings to create new variables for matching like keeping first name/last name, applying transliteration fixes etc. are all provided here. The functions here which should be customized are:
  * `fix_transliterations_level_1`: Gentle letter subsitutions for commonly found differences in Hindi transliterated names. This should be based on the data you are working with. For example: replacing 'DEVI' with blank string was done because in the data we were working with, 'Devi' was a common surname which was removed.
  * `fix_transliterations_level_2`: More aggressive substitution of letters like removing all occurances of 'A'. This should also depend on the data you are working with.


3. 2-cleaning_functions.py
Contains the following funcitons:
  * `get_dataset`: Load data and rename columns using the configurstions provided in matching_config.json.
  * `process_(left/right)_dataset`: Cleaning left/right data like changing column variable types, creating new columns to be used in the matching steps etc. 


4. 3-merge_functions.py
Contains the following functions:
  * `merge_data`: Custom function to merge two datasets and return the merged dataframe
  * `fuzzywuzzy_match`: Function using the fuzzywuzzy Python package to merge two dataframes

5. 4-merge_steps.py
  * Main Python file to be called to merge two datasets. This calls function from the other files. The json `v_matching_steps_json` is used to specify all the combinations of variables to be used in each matching step followed by a for loop which performs the merges based on this json configuration. This is followed by two steps using fuzzywuzzy matching. These should be changed significantly based on the variables in your data and the order of reliability of the steps for your data.


