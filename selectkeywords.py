# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from rake_nltk import Rake
    
def selectkeywords(germantext):
    # Uses stopwords for english from NLTK, and all puntuation characters.
    r = Rake(language='german')
    r.extract_keywords_from_text(germantext)
    keywords= r.get_ranked_phrases() # To get keyword phrases ranked highest to lowest.

    return keywords