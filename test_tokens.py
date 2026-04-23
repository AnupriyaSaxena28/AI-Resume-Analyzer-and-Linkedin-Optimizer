import sys
import spacy
from spacy.matcher import PhraseMatcher
import re

def test_extract():
    nlp = spacy.load("en_core_web_md")
    
    text = "Java,Kotlin,C,C++,Python"
    doc = nlp(text)
    
    print("Tokens for text:")
    for token in doc:
        print(f"  [{token.text}]")
        
    print("\nTokens for C++ pattern:")
    for token in nlp("C++"):
        print(f"  [{token.text}]")

if __name__ == "__main__":
    test_extract()
