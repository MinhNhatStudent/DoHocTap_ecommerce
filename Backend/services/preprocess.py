import re
import string
import os
import nltk
from nltk.tokenize import word_tokenize

class TextPreprocessor:
    def __init__(self):
        stopwords_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'vietnamese-stopwords.txt')
        self.stopwords = self._load_stopwords(stopwords_path)
        
        # DOWN TOKENIZER 
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def _load_stopwords(self, path):
        """Đọc file stopwords tiếng Việt"""
        stopwords = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                stopwords = [line.strip() for line in f if line.strip() and not line.startswith('//')]
        except Exception as e:
            print(f"Lỗi khi đọc file stopwords: {e}")
        return set(stopwords)
    
    def preprocess(self, text):
        """Tiền xử lý văn bản tiếng Việt"""
        if not text or text == "N/A":
            return ""
        
        # chu thuong
        text = text.lower()
        
        # so va dau cau
        text = re.sub(r'\d+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # tokenize, dung dung
        tokens = word_tokenize(text)
        
        # stopwords
        tokens = [word for word in tokens if word not in self.stopwords]
        
        #tra lai chuoi ky tu
        return " ".join(tokens)