import re

# STEP 1: split text into tokens
def split_text(text):
    text = text.lower()
    return re.findall(r"\w+|[^\w\s]", text)

print("STEP 1")
print(split_text("Hello world! I love AI."))

# STEP 2: build a vocabulary
def build_vocab(texts):
    vocab = {"<UNK>": 0}
    for text in texts:
        for token in split_text(text):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab

training_texts = [
    "I love AI.",
    "AI loves data!",
    "I love learning about AI and data.",
]
vocab = build_vocab(training_texts)
print("\nSTEP 2")
print(vocab)



# STEP 3: encode and decode
def encode(text, vocab):
    return [vocab.get(token, vocab["<UNK>"]) for token in split_text(text)]

def decode(ids, vocab):
    id_to_token = {i: t for t, i in vocab.items()}
    return " ".join(id_to_token[i] for i in ids)

print("\nSTEP 3")
ids = encode("I love data.", vocab)
print(ids)
print(decode(ids, vocab))

# STEP 4: unknown words
print("\nSTEP 4")
ids = encode("I love pizza!", vocab)
print(ids)
print(decode(ids, vocab))


# STEP 5: put it all in a class
class SimpleTokenizer:
    def __init__(self):
        self.vocab = {"<UNK>": 0}
        self.id_to_token = {0: "<UNK>"}

    def train(self, texts):
        for text in texts:
            for token in split_text(text):
                if token not in self.vocab:
                    new_id = len(self.vocab)
                    self.vocab[token] = new_id
                    self.id_to_token[new_id] = token

    def encode(self, text):
        return [self.vocab.get(t, 0) for t in split_text(text)]

    def decode(self, ids):
        return " ".join(self.id_to_token.get(i, "<UNK>") for i in ids)

print("\nSTEP 5")
tok = SimpleTokenizer()
tok.train(training_texts)
print("Vocab size:", len(tok.vocab))
ids = tok.encode("AI loves learning!")
print(ids)
print(tok.decode(ids))


tok2 = SimpleTokenizer()
tok2.train(["the cat sat on the mat"])
print(tok2.vocab)
print(tok2.encode("the dog sat"))

# BONUS: subwords with BPE (tiny version)
def most_common_pair(words):
    counts = {}
    for w in words:
        for a, b in zip(w, w[1:]):
            counts[(a, b)] = counts.get((a, b), 0) + 1
    return max(counts, key=counts.get)

def merge(w, pair):
    out, i = [], 0
    while i < len(w):
        if i < len(w) - 1 and (w[i], w[i + 1]) == pair:
            out.append(w[i] + w[i + 1]); i += 2
        else:
            out.append(w[i]); i += 1
    return out

print("\nBONUS")
words = [list(w) for w in ["low", "lower", "lowest", "slow", "slowly"]]
for step in range(3):
    pair = most_common_pair(words)
    words = [merge(w, pair) for w in words]
    print(f"Merge {step+1}: {pair} ->", words)

