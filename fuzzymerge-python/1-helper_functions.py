#####################################################################################################

# DESCRIPTION: Matching helper functions
# AUTHOR: Jeenu Thomas (IDinsight Inc.)
# LAST UPDATED ON: 31-07-2020   

######################################################################################################

import re
import copy
import json
import numpy as np
import pandas as pd


def read_matching_config():

    """
        Function to read the matching config from json file

    """
    with open("./0-matching_config.json") as json_file:
        v_config_json = json.load(json_file)

    return v_config_json


def is_float(s):
    
    """
        Function to convert string to float if number
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


    
def remove_double_letters(p_word):
    
    """
        Function to replace double letters with one
    """

    v_letters = [v_char for v_ind, v_char in enumerate(p_word)
                 if (v_ind == len(p_word) - 1 or (v_ind + 1 < len(p_word) and v_char != p_word[v_ind+1]))]
    
    v_string = "".join([str(v_l) for v_l in v_letters])
    
    return v_string



def remove_h_after_consonant(p_word):
    
    """
        Function to remove h after a consonent
    """

    v_letters = [v_char for v_ind, v_char in enumerate(p_word)
                 if (v_char.upper() != "H" or v_ind == 0 or ((p_word[v_ind-1]).upper() in ('A', 'E', 'I', 'O', 'U')))]
    
    v_string = "".join([str(v_l) for v_l in v_letters])
    
    return v_string



def replace_m_before_consonant(p_word):
    
    """
        Function to replace any m before consonent with n
    """

    v_letters = [v_char 
                if (v_char.upper() != 'M' or v_ind == len(p_word) - 1 or ((p_word[v_ind+1]).upper() in ('A', 'E', 'I', 'O', 'U'))) else 'N'
                for v_ind, v_char in enumerate(p_word)]
    
    v_string = "".join([str(v_l) for v_l in v_letters])
    
    return v_string



def remove_n_before_consonant(p_word):
    
    """
        Function to remove n before a consonent
    """

    v_letters = [v_char for v_ind, v_char in enumerate(p_word)
                 if (v_char.upper() != 'N' or v_ind == len(p_word) - 1 or ((p_word[v_ind+1]).upper() in ('A', 'E', 'I', 'O', 'U')))]
    
    v_string = "".join([str(v_l) for v_l in v_letters])
    
    return v_string



def fix_transliterations_level_1(p_word):

    """
        Function for gentle substitutions for transliteration standardization
    """

    # Replace MOHAMMAD with abbreviation MO, Often abbreviated this way
    v_word_upd = p_word.replace('MOHAMMADA', 'MO')
    v_word_upd = v_word_upd.replace('MOHAMMAD', 'MO')

    # Replace SIMHA with SINGH, and also SING with SINGH
    v_word_upd = v_word_upd.replace("SIMHA", "SINGH")
    if v_word_upd.count("SINGH") == 0:
        v_word_upd = v_word_upd.replace("SING", "SINGH") #

    # Delete DEVI since it is a common suffix that is inconsistently used
    # But don't delete DEVI if that is the person's full name or the start of their name
    if len((v_word_upd.replace("DEVI", "")).strip()) != 0:
        v_word_upd = v_word_upd.replace("DEVI", "")

    # Delete BANO/BANU since it is a common suffix that is inconsistently used
    # But don't delete BANO/BANU if that is the person's full name
    if len((v_word_upd.replace("BANO", "").replace("BANU", "")).strip()) != 0:
        v_word_upd = v_word_upd.replace("BANO", "").replace("BANU", "")

    # Transliteration standardization
    v_word_upd = v_word_upd.replace("JJ", "GY")
    v_word_upd = v_word_upd.replace("CHH", "CH") #
    v_word_upd = v_word_upd.replace("EE", "I") #
    v_word_upd = v_word_upd.replace("OO", "U") #
    v_word_upd = v_word_upd.replace("AI", "E") #
    v_word_upd = v_word_upd.replace("AU", "O")
    v_word_upd = v_word_upd.replace("OU", "O")
    v_word_upd = v_word_upd.replace("EO", "EV")
    v_word_upd = v_word_upd.replace("PH", "F")
    v_word_upd = v_word_upd.replace("W", "V") #
    v_word_upd = v_word_upd.replace("J", "Z") #
    v_word_upd = v_word_upd.replace("SH", "S") # Added to level 1 as this is very common
    v_word_upd = v_word_upd.replace("CA", "CHA")
    # Replace LAKSMAN/LAKSMI/LAKSHMAN/LAKSHMI with LAXMI
    v_word_upd = v_word_upd.replace("KSH", "X")
    v_word_upd = v_word_upd.replace("KS", "X")
    
    # Remove all adjacent double letters
    v_word_upd = remove_double_letters(v_word_upd)
    v_word_upd = replace_m_before_consonant(v_word_upd)

    # Commenting because this lead to increased number of false matches
    # if len((v_word_upd.replace("RAM", "")).strip()) != 0:
    #     v_word_upd = v_word_upd.replace("RAM", "")
        
    # if len((v_word_upd.replace("KUMARI", "")).strip()) != 0:
    #     v_word_upd = v_word_upd.replace("KUMARI", "")
        
    # if len((v_word_upd.replace("KUMAR", "")).strip()) != 0:
    #     v_word_upd = v_word_upd.replace("KUMAR", "")
    
    return v_word_upd



def fix_transliterations_level_2(p_word):

    """
        Function for more aggressive substitution of letters
    """

    #v_word_upd = p_word.replace("SH", "Z") # This can be problematic because all J, S and SH are being mapped to Z
    #v_word_upd = v_word_upd.replace("S", "Z") # SH <> S is done in level 1, BASU<>WAJU seems problematic
    v_word_upd = p_word
    
    v_word_upd = remove_h_after_consonant(v_word_upd)
    v_word_upd = remove_n_before_consonant(v_word_upd)
    
    v_word_upd = v_word_upd.replace("C", "S")
    v_word_upd = v_word_upd.replace("B", "V")
    v_word_upd = v_word_upd.replace("A", "") # most important 

    return v_word_upd



def keep_first_name(p_name):

    """
        Function to keep only first name if multiple names (since surnames are sometimes included/excluded)
    """
    
    if p_name.strip() != "":
        v_name_arr = p_name.split()
        return v_name_arr[0]
    else:
        return ""
    

    
def keep_last_name(p_name):

    """
        Function to keep only last name if multiple names 
    """

    v_name_arr = p_name.split()
    if len(v_name_arr) > 1:
        return v_name_arr[1]
    else:
        return v_name_arr[0]
    

    
def keep_full_name(p_name):

    """
        Function to keep full name without spaces
    """

    v_name_arr = "".join(p_name.split())
    return v_name_arr



def remove_non_alph_characters(p_word):

    """
        Function to remove all non-alphabet characters from the word
    """

    # Delete anything that is not [A-Z]
    regex = re.compile('[^a-zA-Z ]')
    v_word_upd = regex.sub('', p_word)

    return v_word_upd



def soundex(p_word):
    
    """
        Function to get the Soundex Key for a word (https://en.wikipedia.org/wiki/Soundex)

    """
    
    # Step 0: Clean up the word string
    p_word = p_word.lower()
    v_letters = [char for char in p_word if char.isalpha()]

    # Step 1: Save the first letter. Remove all occurrences of a, e, i, o, u, y, h, w.

    # If word contains only 1 letter, return word+"000" (Refer step 5)
    if len(p_word) == 1:
        return p_word + "000"

    v_to_remove = ('a', 'e', 'i', 'o', 'u', 'y', 'h', 'w')

    if len(v_letters) > 0:
        v_first_letter = v_letters[0]
        v_letters = v_letters[1:]
        v_letters = [v_char for v_char in v_letters if v_char not in v_to_remove]

        if len(v_letters) == 0:
            return v_first_letter + "000"
    else:
        return None

    # Step 2: Replace all consonants (include the first letter) with digits according to rules

    v_to_replace = {('b', 'f', 'p', 'v'): 1, ('c', 'g', 'j', 'k', 'q', 's', 'x', 'z'): 2,
                  ('d', 't'): 3, ('l',): 4, ('m', 'n'): 5, ('r',): 6}

    v_first_letter = [v_value if v_first_letter else v_first_letter for v_group, v_value in v_to_replace.items()
                     if v_first_letter in v_group]
    v_letters = [v_value if v_char else v_char
                 for v_char in v_letters
                 for v_group, v_value in v_to_replace.items()
                 if v_char in v_group]

    # Step 3: Replace all adjacent same digits with one digit.
    v_letters = [v_char for v_ind, v_char in enumerate(v_letters)
               if (v_ind == len(v_letters) - 1 or (v_ind+1 < len(v_letters) and v_char != v_letters[v_ind+1]))]

    # Step 4: If the saved letter’s digit is the same the resulting first digit, remove the digit (keep the letter)
    if len(v_letters) > 0:
        if v_first_letter == v_letters[0]:
            v_letters[0] = p_word[0]
        else:
            v_letters.insert(0, p_word[0])

        # Step 5: Append 3 zeros if result contains less than 3 digits.
        # Remove all except first letter and 3 digits after it.

        v_first_letter = v_letters[0]
        v_letters = v_letters[1:]

        v_letters = [v_char for v_char in v_letters if isinstance(v_char, int)][0:3]

        while len(v_letters) < 3:
            v_letters.append(0)

        v_letters.insert(0, v_first_letter)

        v_string = "".join([str(v_l) for v_l in v_letters])
    else:
        v_string = None
        
    return v_string



def get_first_letter_key(p_soundex_key):
    
    v_groups = {('a', 'e', 'i', 'o', 'u', 'y', 'h'): 0,
                ('b', 'v', 'w', 'f', 'p'): 1, 
                ('c', 'k', 'q', 's', 'x', 'g', 'j', 'z'): 2,
                ('d', 't'): 3, 
                ('l',): 4, 
                ('m', 'n'): 5, 
                ('r',): 6}
    
    if p_soundex_key is not None:
        v_soundex_key_letter = p_soundex_key[0]
    else:
        return None
    
    v_first_letter_key = [v_value for v_group, v_value in v_groups.items() if v_soundex_key_letter in v_group]
    
    if len(v_first_letter_key) > 0:
        return v_first_letter_key[0]
    else:
        return None



