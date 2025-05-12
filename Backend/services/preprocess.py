import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


import nltk
# Tải dữ liệu stop words
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

def load_vietnamese_stopwords(filepath):
    """
    Đọc danh sách stop words tiếng Việt từ file.
    
    Args:
        filepath (str): Đường dẫn tới file chứa stop words.
    
    Returns:
        set: Tập hợp các stop words tiếng Việt.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File stop words không tồn tại: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        stopwords = set(line.strip() for line in f if line.strip())
    return stopwords


# Đường dẫn tới file stop words tiếng Việt
VIETNAMESE_STOPWORDS_PATH = r'D:\HeTuVanThongTin\vietnamese-stopwords.txt'
# Tải stop words tiếng Việt khi khởi động
VIETNAMESE_STOPWORDS = load_vietnamese_stopwords(VIETNAMESE_STOPWORDS_PATH)




def preprocess_text(text, remove_stopwords=True, min_word_length=2):
    """
    Tiền xử lý văn bản: loại bỏ ký tự đặc biệt, chuyển về chữ thường, loại bỏ stop words.
    
    Args:
        text (str): Văn bản cần tiền xử lý.
        remove_stopwords (bool): Có loại bỏ stop words hay không.
        min_word_length (int): Độ dài tối thiểu của từ để giữ lại.
    
    Returns:
        str: Văn bản đã được tiền xử lý.
    """

    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()  # Chuyển về chữ thường
    

    tokens = word_tokenize(text)
    

    if remove_stopwords:
        # Stop words tiếng Anh
        english_stopwords = set(stopwords.words('english'))
        
        # stop words tiếng Anh và tiếng Việt
        stop_words = english_stopwords.union(VIETNAMESE_STOPWORDS)
        
        tokens = [word for word in tokens if word not in stop_words]
    
 
    tokens = [word for word in tokens if len(word) >= min_word_length]
    
    # Lemmatization 
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)



def extract_keywords_tfidf(products, max_features=10, min_word_length=2):
    """
    Trích xuất từ khóa từ danh sách sản phẩm bằng TF-IDF.
    
    Args:
        products (list): Danh sách sản phẩm, mỗi sản phẩm là một dict với 'ProductID' và 'MoTa'.
        max_features (int): Số lượng từ khóa tối đa cần trích xuất.
        min_word_length (int): Độ dài tối thiểu của từ khóa để giữ lại.
    
    Returns:
        list: Danh sách từ khóa cho từng sản phẩm.
    """
    # Tiền xử lý mô tả 
    descriptions = [preprocess_text(product['MoTa'], min_word_length=min_word_length) for product in products]
    
    # Tạo TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=max_features)
    tfidf_matrix = vectorizer.fit_transform(descriptions)
    keywords = vectorizer.get_feature_names_out()
    
    # Tạo từ khóa cho từng sản phẩm
    product_keywords = []
    for idx, product in enumerate(products):
        feature_index = tfidf_matrix[idx, :].nonzero()[1]
        tfidf_scores = [(keywords[i], tfidf_matrix[idx, i]) for i in feature_index]
        sorted_keywords = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
        
        # Lọc từ khóa theo độ dài tối thiểu
        filtered_keywords = [kw[0] for kw in sorted_keywords if len(kw[0]) >= min_word_length]
        
        product_keywords.append({
            'ProductID': product['ProductID'],
            'Keywords': filtered_keywords
        })
    return product_keywords


