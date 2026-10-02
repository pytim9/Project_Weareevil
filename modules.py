import pypdf
import spacy
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span

class PDFReader:
    def __init__(self):
        pass

    def open_pdf(self, pdf):
        self.reader = pypdf.PdfReader(pdf) # Reads the pdf

    def read_all_pages(self): # extract every page's content and append it to pages[]
        self.pages = []
        for page in self.reader.pages:
            page = page.extract_text() # works page by page
            self.pages.append(page)
        return self.pages

    def remove_n(self, pages): # erases "\n"
        clean_pdf = [sent.replace("\n","") for sent in pages]
        return clean_pdf

    def __getitem__(self, page):
        return self.pages[page]

class AutomaticAnnotations:
    def __init__(self, nlp):
        self.nlp = nlp

        """
        Works on ONE DOC AT A TIME !
        If multiple Docs are passed, it triggers [E195]
        """

    def phrase_matcher(self, names): # names = weevil_names pour training, unknown_names pour évaluation
        """Initialize PhraseMatcher and define patterns"""
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        patterns = [self.nlp.make_doc(name) for name in names] # transform every weevil name in pattern
        self.phrase_matcher.add("WEEVIL", patterns) # add patterns as "WEEVILS"
        return self.phrase_matcher

    def matching_weevils(self, doc): # matches weevils and creates corresponding labels
        """Matches weevils"""
        weevil_ents = []
        for _, start, end in self.phrase_matcher(doc):
            span = doc[start:end]
            weevil_ents.append(Span(doc, start, end, label="WEEVIL"))
        return weevil_ents

    def delete_overlap(self, doc, spans): # correct overlap problems
        """Filter overlapping spans to obtain non-conflicting entities"""
        weevil_ents = spacy.util.filter_spans(spans)
        doc.ents = weevil_ents

    def create_doc(self, doc): 
        """Each sentence is turned into a doc"""
        docs = [] # list of Docs (with Weevil annotation) for DocBin
        for sent in doc.sents:
            sent_doc = sent.as_doc()
            docs.append(sent_doc) # Doc already contains our annotations
        return docs

    # add dunder ? for what purpose ?

# Separation between training and evaluating data
def is_known(train_docs):
    """Finds names that will be present in the training data"""
    names_model_has_seen = [] # list de str
    for ent in train_docs.ents:
        names_model_has_seen.append(str(ent))
    names_model_has_seen = set(names_model_has_seen)
    return len(names_model_has_seen)

def write_known_names(known_names):
    """Write names it has seen on "names_model_has_seen.txt"""
    with open("data/names_model_has_seen.txt", "w", encoding="utf-8") as f:
        for name in known_names:
            f.write(name.title())
            f.write("\n")

def is_unknown(known_names, full_names):
    """Find names the model hasn't seen un training"""
    unknown_names = []
    for name in full_names:
        if name not in known_names:
            unknown_names.append(name)
    return unknown_names

def write_unknown_names(known_names, full_names):
    """Write names model has not seen in "unknown_names.txt"""
    with open("data/unknown_names.txt", "w", encoding="utf-8") as f:
        for name in is_unknown(known_names, full_names):
            f.write(name)
            f.write("\n")

def negative_positive(train_docs):
    """How many sentences with weevils, and with no weevils ?"""
    no_weevils = 0
    with_weevils = 0
    for doc in train_docs:
        if not doc.ents:
            no_weevils += 1
        else:
            with_weevils += 1
    return no_weevils, with_weevils
#print(negative_positive(train_docs))