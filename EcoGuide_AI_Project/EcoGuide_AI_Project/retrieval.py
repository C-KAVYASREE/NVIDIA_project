import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class WasteRetriever:
    def __init__(self, path):
        self.records = json.loads(Path(path).read_text(encoding="utf-8"))
        self.texts = [f"{r['item']} {r['category']} {r['guidance']} {r['keywords']}" for r in self.records]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
        self.matrix = self.vectorizer.fit_transform(self.texts)

    def search(self, query, top_k=3):
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix).flatten()
        indices = scores.argsort()[::-1][:top_k]
        found = []
        for i in indices:
            if scores[i] > 0:
                row = dict(self.records[i])
                row["score"] = float(scores[i])
                found.append(row)
        return found
