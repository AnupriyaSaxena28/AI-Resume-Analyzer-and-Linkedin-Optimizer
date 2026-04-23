import spacy
from spacy.matcher import PhraseMatcher

def test_canonical():
    nlp = spacy.load("en_core_web_md")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    canonical_skill = "Mobile Development"
    variations = ["Mobile Development", "Mobile Application Development"]
    
    patterns = [nlp.make_doc(v) for v in variations]
    
    # Add with the canonical string as the match ID
    matcher.add(canonical_skill, patterns)
    
    text = "I have 5 years of Mobile Application Development experience."
    doc = nlp(text)
    matches = matcher(doc)
    
    found_canonicals = set()
    for match_id, start, end in matches:
        canonical = nlp.vocab.strings[match_id]
        print(f"Matched text: '{doc[start:end].text}' -> Canonical: '{canonical}'")
        found_canonicals.add(canonical)
        
    print(f"Returned Canonical Skills: {found_canonicals}")

if __name__ == "__main__":
    test_canonical()
