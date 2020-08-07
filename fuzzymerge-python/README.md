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

<a name="overview"></a>
## Overview

The underlying algorithm used in this code was first implemented in Stata and then adapted to Python. It relies on using different combinations of variables in a step-by-step manner, starting with the most reliable criteria for identifying true matches (which is, exact matches on all variables), and progressively using less and less reliable criteria like matching on all expected variations of the names (POOJA - PUJA, SUMEET - SUMIT etc.). The reliability of the steps is decided based on running the algorithm on a small sample of test data. 

This code is meant to serve only as an example of the algorithm. It was written for matching two datasets containing the variables: cluster code, village code, child name, father name, gender, age and social category. Child name and father name are Indian names transliterated into English. When working on a similar matching datasets problem, you can take this code and customize it to work with your dataset by changing variables names, matching steps, order of the steps etc. based on the data you are working with.
<br>

<a name="directory"></a>
## Directory Structure
```bash
.
|-- fuzzymerge-python
|     |-- 0-matching_config.json  # Configuration file for specifying the input file paths, column name mapping etc.
|     |-- 1-helper_functions.py   # All functions used in the matching and cleaning steps like string manipulation functions, transliteration fixes etc. 
|     |-- 2-cleaning_functions.py # All data reading and cleaning functions
|     |-- 3-merge_functions.py    # All functions used for performing merge operations 
|     |-- 4-merge_steps.py 	  # Main Python script with the merge steps which calls functions from other files 
|-- data 	              # Optional: Directory to store the input and output files
     |-- *.csv/*.excel        # Optional: Input files for left and right datasets
     |-- results 	      # Optional: Subfolder for storing output file containg the match results
	    |-- *.csv 
```

<a name="usage"></a>
## Usage
Command to run the code is: `python3 4-merge_steps.py`
<br>

<a name="files"></a>
## Files
1. <a name="matching_config"></a><b>0-matching_config.json</b><br>
    Json file for specifying input and output file configurations. File level configurations are kept here so that the same code can work with data in different input files as long as the variables to be used for matching are the same. Here is a description for each key in the configuration file:
    * <i>`inputs.(left/right)_dataset.path`</i>: Path to the input left and right datasets. The difference between the two is that in the current implemntation after each matching step, rows were removed from the left dataset if a match is found in the right dataset. The right dataset on the other hand remains the same throughout.
    * <i>`inputs.(left/right)_dataset.csv_or_excel`</i>: File extension type of the input file. The allowed values are csv or excel. 
    * <i>`inputs.(left/right)_dataset.dataset_unique_id`</i>: Column name for the unique identifier for each row in the left/right dataset. The code throws an error in case this column is not unique in the input data. In absence of a column which uniquely identifies each row, users can simply add a dummy column with row numbers to the file. Please note that this column is renamed to `(left/right)_dataset_unique_id` in the code.
    * <i>`inputs.(left/right)_dataset.columns_mapping`</i>: All columns which are going to be used in the matching steps except the unique id column are specified here. The keys are the actual (expected) column names used in subsequent steps in the code and the values are the corresponding column headers in the file. This mapping is used to rename the columns to their expected column names. 
    * <i>`outputs.path`</i>: Path to the folder where the outputs file 'matches.csv' should be stored.
    * <i>`outputs.(left/right)_columns_to_keep`</i>: Array of columns from the left/right dataset you want to include in the output file. Here the columns are refered using the 'keys' under columns_mapping configuration.


2. <a name="helper_functions"></a><b>1-helper_functions.py</b><br>
    Functions used for various data fetching and cleaning operations are provided here. Most of these function are used for manipulation of strings columns to create new variables for matching like keeping first name, keeping full name without spaces, applying transliteration fixes etc. The two most important functions in this script are:
    * <i>`fix_transliterations_level_1`</i>: Gentle letter subsitutions for commonly found differences in Hindi to English transliterated names. More rules can be added or existing rules removed based on the data you are working with. For example: replacing 'DEVI' with blank string was done because in the data we were working with, 'Devi' was a common surname which was often added/removed.
    * <i>`fix_transliterations_level_2`</i>: More aggressive substitution of letters like removing all occurances of 'A' or replacing 'C' with 'S'. More rules can be added or existing rules removed based on the data you are working with.


3. <a name="cleaning_functions"></a><b>2-cleaning_functions.py</b><br>
    The following data fetching and processing functions are provided here:
    * <i>`get_dataset`</i>: Load data, perform simple data consitency checks and rename columns using the configurations provided in matching_config.json file. All columns in the dataframe are renamed to the names specified in the 'keys' in matching_config. In addition, columns in the left dataset are given the prefix 'left' and columns in right dataset are given the prefix 'right'.
    * <i>`process_(left/right)_dataset`</i>: Cleaning left/right datasets like changing column variable types, creating new columns to be used in the matching steps etc. These cleaning actions are very specific to the dataset you are working with. For example, one of the features of the data for which this code was written was that child name and father name in the left dataset could have names seperated by a '/'. So we seperate these into columns 'childname' and 'childname_alt' and 'fathername' and 'fathername_alt' and during merge, every merge with a variation of childname/fathername is also applied to the corresponding variation of childname_alt/fathername_alt.


4. <a name="merge_functions"></a><b>3-merge_functions.py</b><br>
    Functions used for different merging operations are provided here. The functions are:
    * <i>`merge_data`</i>: Custom function to merge two datasets using pandas merge function. This function returns the merged results dataframe. Since one of the variables in the dataset was age and we wanted to be able to use a upper/lower bounds for the age, you will see a age limit parameter is passed into this function and is used to further subset the merged dataset to have only rows where age difference is within the specified limits.
    * <i>`fuzzywuzzy_match`</i>: Function using the fuzzywuzzy Python package to merge two dataframes.


5. <a name="merge_steps"></a><b>4-merge_steps.py</b><br>
    Main Python code which calls functions defined in the above files. 

    The first few lines of code retrieves the data from the input files using the fetching and cleaning functions in other files. This is followed by the step by step matching process. The json `matching_steps_json` is used to specify the combination of variables to be used in each matching step. This json format is used for the convienience of keeping these stepwise configurations together in one place and using a for loop to run each step. The same combination of variables is used first at a village region level and then at a cluster region level. This is followed by two steps using the fuzzywuzzy python package. The code also contains commented out step using a combination of soundex and masala-merge to find more matches.

    The combination of variables in each step and order of steps should be changed significantly based on the variables in your data and the order of reliability of the steps which gives the most accurate result for your data. More steps using other available fuzzy matching python packages can also be added.

