import spacy
nlp = spacy.load("en_core_web_md")
print([t.text for t in nlp("CI/CD")])
print([t.text for t in nlp("CI / CD")])
print([t.text for t in nlp("C++")])
print([t.text for t in nlp("C ++")])
print([t.text for t in nlp("React.js")])
print([t.text for t in nlp("React .js")])

