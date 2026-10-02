import spacy
from spacy.tokens import DocBin
from modules import PDFReader, AutomaticAnnotations
from modules import is_known, write_known_names, is_unknown, write_unknown_names, negative_positive

# Tokenizer and sentencizer
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")
#print(nlp.pipe_names)

# Get weevil names
with open("data/weevil_names.txt", "r", encoding="utf-8") as f:
    weevil_names = f.read().splitlines()

# Read text1 for training data
text1 = PDFReader()
text1.open_pdf("data/observation_weevils.pdf")
dirty_pdf = text1.read_all_pages() # OBSERVATION_VEEVILS.PDF = first text used for training
clean_first_text = text1.remove_n(dirty_pdf) # cleaned and processed version


# Create doc1
doc_1 = nlp(str(clean_first_text))
# = doc de tokens, et non doc de listes de tokens ! (c'est parfait)


# Automatic label on training data
annotations_train = AutomaticAnnotations(nlp)
annotations_train.phrase_matcher(weevil_names)
weevil_ents = annotations_train.matching_weevils(doc_1)
annotations_train.delete_overlap(doc_1, weevil_ents)
train_docs = annotations_train.create_doc(doc_1) # DONNÉES ENTRAINEMENT
# train_docs = LISTE DE DOCS


# Training data
"""FAIT"""
#train_docbin = DocBin(docs=train_docs)
#train_docbin.to_disk("./train.spacy")

# Docbin attend un LISTE DE DOCS ! (bon pour train doc)