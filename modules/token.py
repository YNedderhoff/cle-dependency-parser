class Token(object):
    # A non-empty line in CoNLL06 format

    def __init__(self, line):

        entries = line.split('\t')
        if len(entries) != 10:
            print "Length not right."
        self.id = int(entries[0])
        self.form = entries[1]
        self.lemma = entries[2]
        self.pos = entries[3]
        if entries[6] == "_":  # happens for test data, in that case it can't be 'integered'
            self.head = None
        else:
            self.head = int(entries[6])


def sentences(file_stream):
    # Generator that returns sentences as lists of Token objects.
    # Reads CoNLL06 format.

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
