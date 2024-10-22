# This is not clean at all, but here we need the vocabulary used by the pre-trained Wave2Vec, it needs to be in the same order
DEFAULT_LABELS_W2V = ('-', '|', 'E', 'T', 'A', 'O', 'N', 'I', 'H', 'S', 'R', 'D', 'L', 'U', 'M', 'W', 'C', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', "'", 'X', 'J', 'Q', 'Z')
BLANK_TOKEN_W2V = '-'


class LabelsVocab:

    def __init__(self, labels=DEFAULT_LABELS_W2V):
        self.labels = labels
        self.stoi = {label: idx for idx, label in enumerate(labels)}
        self.itos = {idx: label for idx, label in enumerate(labels)}

    def __len__(self):
        return len(self.labels)

    def lookup_token(self, token):
        return self.stoi.get(token)

    def lookup_index(self, index):
        return self.itos.get(index)