#####################################################################################################

# DESCRIPTION: Custom Polyglot implementation
# AUTHOR: IDinsight Inc.

######################################################################################################

import pandas as pd
import numpy as np
from polyglot.transliteration import Transliterator
from polyglot.detect import Detector
import re

'''
Load data.
'''

# Change directory to where the relevant file is stored
df = pd.read_excel("../data/supprolls_data_entry.xlsx")
df.head()


'''
Set up all custom transliteration function.
'''

translation_dict = {
    
    'छ': 'ch',
    'ड़': 'd',
    'झ': 'jh',
    'ढ': 'dh',
    'ज़': 'z',
    'ढ़': 'rh',
    'ण': 'n',
    'ऐ': 'e',
    'फ़': 'f',
    'औ': 'au',
    'ऊ': 'u'
    
}

'''
First, split the name by spaces, if applicable, creating a list
of first/last names (re.split()). Then, for each string in that list, do the 
following:

Iterate through each character in the string and identify, if any,
the indices for the 'bad' ones (which we conveniently have in a list 
format as translation_dict.keys()). Once we have the indices, we have to
do the following: 

* Split the name at those indices
* Iterate over the list of name parts, transliterating each piece
* At the part where there was a 'bad char' index, use the translation_dict
  to grab what the translit should be (e.g., translation_dict['छ'])
* Sew together all the separate transliterated parts of the word
  using .join(), effectively combining the different words (the 
  first and last names) with a space between them
'''

def translit_part(string, idxs, verbose=False):
    
    '''
    This function takes a string and
    list of haunted indices and uses the
    polygot transliterator to transliterate
    each "good" char, and uses the handmade
    dictionary to translate each of the "haunted"
    ones. It transliterates by CHARACTER,
    not giving the most high-integrity transliterations
    of each name (e.g., it outputs ajy instead of ajay,
    the latter of which polyglot knows to output if
    you pass the whole word instead of a letter at a time).
    '''
    
    trans = Transliterator(source_lang='hi', target_lang='en')
    
    if verbose == True:
        print("\n RUNNING CLEAN TRANSLIT FUNCTION ON: ", string)
        print("INITIALIZED EMPTY STRING TO BECOME FINAL CLEAN TRANSLITERATION")
    clean_translit = ''
    for i, char in enumerate(string):
        if verbose == True:
            print("EXAMINING CHAR ", char, "AT INDEX ", i)
        if i not in idxs:
            if verbose == True:
                print("INDEX IS CLEAR")
            clean_translit += trans.transliterate(char)
            if verbose == True:
                print("ADDING", trans.transliterate(char), "TO CLEAN TRANSLIT")
        if i in idxs:
            if verbose == True:
                print("INDEX IS HAUNTED")
            clean_translit += translation_dict[char]
            if verbose == True:
                print("ADDING", translation_dict[char], "TO CLEAN TRANSLIT")
    
    if verbose == True:        
        print()
        print("FINAL CLEAN TRANSLIT: ", clean_translit)
        print()
        
    return clean_translit
        

def transliterate(string, verbose=False):
    
    '''
    This function takes a full Devanagari entry,
    with spaces and bad chars, and returns the cleaned
    and fully ready Latin transliteration. During this
    process, it parses each part of the name (first and last,
    for example--anything separated with a space) for the
    haunted indices, at which point it uses translit_part()
    to get the part of the name transliterated.
    '''

    if verbose == True:
        print("STRING ENTERED: ", string)
    split_on_spaces = re.split(' ', string)
    
    if verbose == True:
        print("SPLIT STRING: ", split_on_spaces)
        print()

    # Here we'll put the transliterated parts of the name in a list
    # (e.g., ['kan', 'singh']) in order to eventually join them
    transliterated_parts = []
    if verbose == True:
        print("INITIALIZED EMPTY LIST OF TRANSLITERATED PARTS")

    for name_part in split_on_spaces:
        if verbose == True:
            print("EXECUTING ON PART OF NAME: ", name_part)

        # Here we'll store haunted indices
        if verbose == True:
            print("EMPTY LIST OF HAUNTED INDICES INITIALIZED")
        haunted_idxs = []

        # Check each char in name part
        if verbose == True:
            print("ITERATING THROUGH CHARS")
        for i, char in enumerate(name_part):
            if verbose == True:
                print("CHAR IDX IS: ", i, "| CHAR NAME IS: ", char)
                # Check if char is in the haunted dictionary of forbidden chars
                print("CHECKING HAUNTED DICTIONARY FOR CHAR")
            if char in translation_dict.keys():
                if verbose == True:
                    print("CHAR", char, " IN HAUNTED DICTIONARY!!!")
                haunted_idxs.append(i)
                if verbose == True:
                    print("UPDATED LIST OF HAUNTED INDICES: ", haunted_idxs)
            else:
                if verbose == True:
                    print("CHAR IS SAFE")
        
        if verbose == True:
            print("FINISHED ITERATING THROUGH CHARS")
            print("RUNNING translit_part ON ", name_part, " WITH HAUNTED IDXS", haunted_idxs)

        transliterated_parts.append(translit_part(name_part, haunted_idxs))
        if verbose == True:
            print()
            print("UPDATED LIST OF TRANSLITERATED PARTS: ", transliterated_parts)
            print()

    # Join together the transliterated parts into a whole
    final_transliteration = ' '.join(transliterated_parts)
    if verbose == True:
        print("JOINED ITEMS IN LIST OF TRANSLITERATED PARTS TO CREATE: ", final_transliteration)
    
    return final_transliteration

#transliterate('कोड़मलज़ कड़ोमल')


'''
Make the new columns and use the above function to transliterate.
'''

# Grab list of Devanagari columns
dev_cols = df[['Voter name', 'Father/ husband name', 'House no.']]

for col in dev_cols:

    
    print("COLUMN IS: ", col)
    
    # Find column index to help us place the Latin one
    col_idx = df.columns.get_loc(col)
    
    # Name the Latin column with "_l" for latin
    roman_col_name = str(col + "_l")
    
    # Create empty list to populate w/ transliterations
    transliterations = []
    
    # Transliterate entries
    for entry in df[col]:
        
        # Try running transliterate function (it won't)
        # work if the entry is np.nan, or just not a string
        try:
            transliteration = transliterate(entry)
            
            # Only use the transliteration output if it's a string
            # (this is important b/c an entry of '32' will actually
            # transliterate to ''; we don't want to add '' to the column)
            if len(transliteration) > 0:
                transliterations.append(transliteration)
                
            # If transliteration output was '' (i.e., if length = 0),
            # then just grab exactly what the initial entry was (e.g., '32')
            else:
                transliterations.append(entry)
            
        # If entry wasn't string, copy over whatever value was there
        except:
            transliterations.append(entry)
    
    df.insert(col_idx + 1, roman_col_name, transliterations)
    

'''
save dataframe to excel
'''
df.to_excel("../data/140120_data_entry_latin_supp.xlsx")
