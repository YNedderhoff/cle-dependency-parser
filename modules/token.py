class Token(object):
    """
    Represents one token 
    (a non-empty line in CoNLL09 format).
    """
    def __init__(self, line):
        entries = line.split('\t')
        self.id = entries[0]
        self.form = entries[1]
        self.lemma = entries[2]
        self.pos = entries[3]
        self.head = entries[6]
        self.rel = entries[7].rstrip()

def sentences(file_stream):
    """
    Generator that returns sentences as lists of Token objects.
    Reads CoNLL09 format.
    """
    sentence = []
    for line in file_stream:
        line = line.rstrip()
        if line:
            sentence.append(Token(line))
        elif sentence:
            yield sentence
            sentence = []
    if sentence:
        yield sentence
