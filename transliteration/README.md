# transliteration

In one of our applications of fuzzy matching, the data was available to us only in Devnagari script and we had to first transliterate it to English using Polyglot– a Python library that supports transliteration. 

Before transliterating through Polyglot, we modified the algorithm to ensure greater consistency in tranlisterations and hence, better matching rates. 

1. Tranlisteration by letters:
	Instead of using the algorithm’s default process of transliterating from Devnagari to Latin by word, we modified it to transliterate names by letters and half-letters. For different combinations of letters in a word, we discovered that Polyglot was using some implicit transliteration rules by word which would lead to inconsistencies in the transliteration output. For example, while ‘कोमल’ was transliterated to ‘koml’ (no ‘a’ appears between ‘m’ and ‘l’), ‘अजय’ was transliterated to ‘ajay’ (‘a’ appears between ‘j’ and ‘y’). We also know that the name ‘अजय’ can also be recorded in Devnagari as ‘अजे’ which is  transliterated to ‘aje’. 

	It is possible that there are other such inconsistencies when transliterating by word, that exacerbate differences between similar names during the fuzzy matching stage, which in turn could yield artificially low match rates. Since we don’t have a list of these implicit rules of transliteration for different combinations of letters in a word, we decided to err on the side of caution and transliterate by individual letters, which are easier to match across the two scripts.

	However, transliterating by letter also resulted in a new outcome – all half letters then got transliterated with an extra ‘e’. But this trade-off was acceptable for our matching purposes because in addition to the benefit of eliminating inconsistencies such as the one noted above, it also helped eliminate inconsistencies in how Polyglot was originally transliterating half letters. For example, when transliterating by word, ‘अक्रम’ was getting transliterated to ‘acrm’. But when transliterating by letter, it was transliterated to ‘akerm’. On the other hand, despite getting transliterated by word the name ‘दुर्गा’ was getting transliterated to ‘duerga’ i.e. with an extra ‘e’ for half letter (when transliterating by letter it showed up as durega). Thus, transliterating by letter allowed us to standardise both types names with half-letters to be similarly outputted with an appended ‘e’, thus minimising artificial differences in names for the fuzzy matching stage.

2. Include missing characters:
	We also had to expand the Polyglot dictionary to include missing Devnagari characters. The available version of Polyglot was not outputting any transliteration for some letters, perhaps because they were not available in its dictionary. For instance, the name  ‘उमा’ was transliterated to uma but its variation ‘ ऊमा’ was outputting an empty string. So we appended the following dictionary to make the package comprehensive for transliterating all kinds of names:     'छ': 'ch',    'ड़': 'd',    'झ': 'jh',    'ढ': 'dh',    'ज़': 'z',    'ढ़': 'rh',    'ण': 'n',    'ऐ': 'e',  'फ़': 'f',   'औ': 'au',    'ऊ': 'u'. 

Once these changes were made, we transliterated both datasets in the same manner to set up the stage for fuzzy matching.

It should be noted that as a result of these modifications, the names outputted in Latin were slightly difficult to discern. However, since the transliteration rules were the same across both datasets, these non-standard spellings do not interfere with our matching process.

