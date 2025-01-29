from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class ContentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        
    def classify_text_block(self, text):
        """Classify text blocks as headers, paragraphs, etc."""
        features = {
            'length': len(text),
            'has_number': any(char.isdigit() for char in text),
            'capital_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }
        
        if features['length'] < 100 and features['capital_ratio'] > 0.5:
            return 'heading'
        elif features['has_number'] and features['length'] < 50:
            return 'list_item'
        else:
            return 'paragraph' 