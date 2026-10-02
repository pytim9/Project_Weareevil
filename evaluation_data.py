import spacy
from spacy.tokens import DocBin
from modules import PDFReader, AutomaticAnnotations
from modules import is_known, write_known_names, is_unknown, write_unknown_names, negative_positive

# Tokenizer and sentencizer
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")
#print(nlp.pipe_names)

# Get unknonwn weevil names
with open("data/unknown_names.txt", "r", encoding="utf-8") as f:
    unknown_names = f.read().splitlines()

# Read text1 for training data
text1 = PDFReader()
text1.open_pdf("data/weevils_everywhere.pdf")
dirty_pdf = text1.read_all_pages() # OBSERVATION_VEEVILS.PDF = first text used for training
clean_first_text = text1.remove_n(dirty_pdf) # cleaned and processed version

# Create doc1
doc_1 = nlp(str(clean_first_text))
# = doc de tokens, et non doc de listes de tokens ! (c'est parfait)


# Automatic label on training data
annotations_train = AutomaticAnnotations(nlp)
annotations_train.phrase_matcher(unknown_names)
weevil_ents = annotations_train.matching_weevils(doc_1)
annotations_train.delete_overlap(doc_1, weevil_ents)
dev_docs = annotations_train.create_doc(doc_1) # DONNÉES ÉVALUATION
# dev_docs = LISTE DE DOCS

# Evaluation data
"""FAIT"""
#dev_docbin = DocBin(docs=dev_docs)
#dev_docbin.to_disk("./dev.spacy")

