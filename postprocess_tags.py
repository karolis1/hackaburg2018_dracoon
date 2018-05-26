import spacy

nlp = spacy.load('de')


def postprocess_tags(tags):
    lemmatized_tags = set()
    for tag in tags:
        if len(tag.split()) > 1:
            lemmatized_tags.add(tag)
        tag = nlp(tag)
        for t in tag:
            lemmatized_tags.add(t.lemma_)
    return list(lemmatized_tags)
