# fuzzymerge-python
Python code for merging two datasets containing columns with Hindi tranlisterated text/names.

## Table of Contents

* [Overview](#overview)
* [Directory Structure](#directory)
* [Usage](#usage)
* [Files](#files)
  * [0-matching_config.json](#matching_config)
  * [1-helper_functions.json](#helper_functions)
  * [2-cleaning_functions.json](#cleaning_functions)
  * [3-merge_functions.json](#merge_functions)
  * [4-merge_steps.json](#merge_steps)
<br>

<a name="overview"></a>
## Overview

This code was originally written for matching two datasets containing the variables: village code, cluster code, child name, father name, gender, age and social category. Here child name and father name were Indian names transliterated in English.

The underlying algorithm used here relies on using different combinations of variables in a step-by-step manner starting with the most reliable criteria for identifying true matches (which is, exact matches on all variables), and progressively using less and less reliable criteria. In the combination of variables used is each step, matching on exact names was followed by matching on variations of the names based on expected transliteration differences. The reliability of the steps was decided based on running the algorithm on a small sample of test data.

This code is meant to serve as an example of the algorithm. When working on a similar matching datasets problem, you can take this code and customize it to work with your own dataset by changing variables names, matching steps, order of the steps etc. based on the data you are working with.
<br>

<a name="directory"></a>
## Directory Structure
```bash
.
|-- 0-matching_config.json  # Config file for specifying the input file paths, column name mapping etc.
|-- 1-helper_functions.py # All functions used in the matching steps like string manipulation functions, transliteration fixes etc. 
|-- 2-cleaning_functions.py # All data reading and cleaning functions
|-- 3-merge_functions.py # All functions used for merge operations 
|-- 4-merge_steps.py 	  # Main Python file with the merge steps which calls functions from other files 
|-- Data 	    # Optional: Directory to store the input and output files
	  |-- *.csv/*.excel # Optional: Input files for left and right datasets
	  |-- Results 	  # Optional: Subfolder for storing output file containg the match results
	  		|-- *.csv 
```
<br>

<a name="usage"></a>
## Usage
Command to run the code is: `python3 4-merge_steps.py`
<br>

<a name="files"></a>
## Files
<b>1. <a name="matching_config"></a>0-matching_config.json</b><br>
    Json file for specifying configurations relating to input and output files. Here is a description for each key in the configuration file:
    * `inputs.(left/right)_dataset.path`: Path to the input left and right datasets. The aim of this code was to find a match for each row in the left dataset, in the right dataset. Hence, after each matching step, rows were removed from the left dataset if a match was found in the right  dataset. The right dataset on the other hand remained the same throughout.
    * `inputs.(left/right)_dataset.csv_or_excel`: File extension type of the input file. The allowed values are csv or excel. 
    * `inputs.(left/right)_dataset.dataset_unique_id`: Column name for the unique identifier for each row in the left/right dataset. The code throws an error in case this column is not unique in the input data. In absence of a column which uniquely identifies each row, users can add a dummy column with row number to the file. 
    * `inputs.(left/right)_dataset.columns_mapping`: All columns which are going to be used in the matching steps except the unique id column can be specified here. The keys are the actual (expected) column names used in subsequent steps in the code and the values are the corresponding column headers in the file. This mapping is used to rename the columns to the expected column names for the code to work with files with different column headers, if needed. 
    * `outputs.path`: Path to the folder where the outputs file 'matches.csv' should be stored.
    * `outputs.(left/right)_columns_to_keep`: Columns from the left/right dataset you want to include in the output file. Here the 'keys' specified in columns_mapping configuration which are the expected column names can be used to refer to the columns.


<b>2. <a name="helper_functions"></a>1-helper_functions.py</b><br>
    Functions used for various purposes in the code, example for manipulation of strings to create new variables for matching like keeping first name/last name, applying transliteration fixes etc. are provided here. Among these functions, the ones which should be customized are:
    * `fix_transliterations_level_1`: Gentle letter subsitutions for commonly found differences in Hindi to English transliterated names. More rules can be added or existing rules removed based on the data you are working with. For example: replacing 'DEVI' with blank string was done because in the data we were working with, 'Devi' was a common surname which was often added/removed in names.
    * `fix_transliterations_level_2`: More aggressive substitution of letters like removing all occurances of 'A' or replacing 'C' with 'S'. More rules can be added or existing rules removed based on the data you are working with.


<b>3. <a name="cleaning_functions"></a>2-cleaning_functions.py</b><br>
    Fetching and processing data functions are provided here. The funcitons are:
    * `get_dataset`: Load data and rename columns using the configurations provided in matching_config.json file. All columns in the dataframe are renamed to the names specified in the 'keys' in matching_config and columns in the left dataset are given the prefix 'left' and columns in right dataset are given the prefix 'right' here.
    * `process_(left/right)_dataset`: Cleaning left/right datasets like changing column variable types, creating new columns to be used in the matching steps etc. These cleaning actions are very specific to the dataset you are working with. For example, one of the features of the data for which this code was written was that child name and father name in the left dataset could have strings seperated by a '/' which mean there are two names. So we seperate these into columns 'childname' and 'childname_alt' and 'fathername' and 'fathername_alt' and then make sure that every merge with a variation of childname/fathername is also applied to the corresponding variation of childname_alt/fathername_alt.


<b>4. <a name="merge_functions"></a>3-merge_functions.py</b><br>
    Functions with merging operations are provided here. The functions are:
    * `merge_data`: Custom function to merge two datasets using pandas merge function. This function returns the merged results dataframe. Since one of the variables in the dataset was age and we wanted to be able to use a range for the age, you will see a age limit parameter is passed into this function and is used to further subset the merged dataset to have only rows where age difference is within the specified limits.
    * `fuzzywuzzy_match`: Function using the fuzzywuzzy Python package to merge two dataframes.


<b>5. <a name="merge_steps"></a>4-merge_steps.py</b><br>
    Main Python code which calls functions defined in the above files. 

    The json `matching_steps_json` is used to specify all the combinations of variables to be used in each matching step followed by a for loop which performs the merges. The combintation of variables to be used in the steps was specified in json format only for convienience of keeping these together in one place. The same combination of variables is used first at a village region level and then at a cluster region level. This is followed by two steps using fuzzywuzzy python package. The code also contains commented out step using a combination of soundex and masala-merge to find more matches.

    The combination of variables in each step and order of steps should be changed significantly based on the variables in your data and the order of reliability of the steps for your data. More steps using other available fuzzy matching python packages can also be added.

