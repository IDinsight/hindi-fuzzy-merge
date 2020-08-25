# hin-fuzzy-merge

This repository contains customizable Fuzzy Matching scripts written in STATA and Python, expecially useful for datasets containing Hindi text transliterated to English.

## Overview

This algorithm is motivated by the fact that Hindi names written in Devanagari script are not transliterated in a consistent way to Latin script. Although fuzzy matching programs exist, most are optimized for text originally written in Latin script, and so they perform poorly when applied to Hindi transliterated names. 

We also found that match rates could be improved substantially by taking a stepwise approach, starting with the most certain matches and progressively loosening restrictions. False matches in fuzzy matching algorithms propagate: an early false match that incorrectly removes an individual from the match pool leads the algorithm to make false matches with other individuals in later steps. 

By completing more certain matches before moving onto less certain matches, we found that our stepwise algorithm reduced false match rates more than running a fuzzy match program a single time.


## Directory Structure
```bash
.
|-- hindi-fuzzy-merge
     |-- fuzzymerge-python # Directory with an example of the algorithm implemented in Python for matching household survey results with data collected from school registers
     |-- fuzzymerge-stata # Directory with an example of the algorithm implemented in STATA for matching household census data with voter rolls
     |-- transliteration # Directory with example code for trasliteration of Devanagiri script to English using Polyglot Python package

```