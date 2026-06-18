import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import json

class DynamicRAG:
    def __init__(self, golden_set_path):
        with open(golden_set_path, 'r', encoding='utf-8') as f:
            self.golden_data = json.load(f)
        
        self.df_kb = pd.DataFrame(self.golden_data)
        self.vectorizer = TfidfVectorizer(analyzer='char_wb', ngram_range=(3, 5))
        self.X_kb = self.vectorizer.fit_transform(self.df_kb['text'])
        
        self.knn = NearestNeighbors(n_neighbors=3, metric='cosine')
        self.knn.fit(self.X_kb)

    def get_dynamic_context(self, input_text):
        input_vec = self.vectorizer.transform([input_text])
        distances, indices = self.knn.kneighbors(input_vec)
        
        context = "CRITICAL CALIBRATION EXAMPLES (DYNAMICALLY RETRIEVED):\n"
        for idx in indices[0]:
            ex_text = self.df_kb.iloc[idx]['text']
            ex_label = self.df_kb.iloc[idx]['label']
            context += f"- Text: \"{ex_text}\" -> Intent: {ex_label}\n"
        return context