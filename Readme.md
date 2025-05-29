# 🏪 Hệ Thống Tư Vấn Thông Tin - E-commerce Recommendation System

## 📋 Giới thiệu tổng quan

Hệ thống tư vấn thông tin là một ứng dụng e-commerce hiện đại chuyên về **văn phòng phẩm, sách và đồ dùng học tập**, được xây dựng với mục tiêu cung cấp trải nghiệm mua sắm thông minh thông qua **hệ thống đề xuất sản phẩm tự động**.

### 🎯 Mục tiêu chính
- **Hệ thống đề xuất thông minh**: Sử dụng Content-Based Filtering và Machine Learning để đề xuất sản phẩm phù hợp
- **Giao diện người dùng thân thiện**: Website responsive với thiết kế hiện đại, màu sắc chủ đạo xanh dương (#BFECFF) và tím nhạt (#CDC1FF)  
- **Giải pháp Cold-start**: Xử lý vấn đề người dùng mới thông qua đề xuất sản phẩm phổ biến và tương tự
- **Demo trực quan**: Trình bày các khái niệm recommendation system một cách dễ hiểu

## 🏗️ Kiến trúc hệ thống

### Backend (Flask + Python)
- **Framework**: Flask với cấu trúc MVC
- **Database**: MySQL với SQLAlchemy ORM  
- **Machine Learning**: 
  - Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2)
  - Scikit-learn cho tính toán độ tương đồng cosine
  - NLTK cho xử lý văn bản tiếng Việt
- **API**: RESTful API với Swagger documentation

### Frontend (HTML/CSS/JavaScript) (Bỏ vue.js vì làm màu quá không tốt cho sức khỏe)
- **Template Engine**: Jinja2 
- **UI Framework**: Bootstrap + Custom CSS
- **JavaScript**: jQuery, Slick Carousel
- **Design**: Responsive design với màu sắc hiện đại

## ✨ Tính năng chính

### 🛍️ Chức năng E-commerce cơ bản
- **Trang chủ**: Hiển thị sản phẩm mới nhất, phổ biến nhất, bán chạy nhất
- **Chi tiết sản phẩm**: Thông tin đầy đủ với sản phẩm liên quan
- **Giỏ hàng**: Quản lý sản phẩm, cập nhật số lượng
- **Cửa hàng**: Tìm kiếm, lọc theo nhãn hàng, giá, phân trang
- **Đăng ký/Đăng nhập**: Quản lý tài khoản người dùng

### 🤖 Hệ thống đề xuất thông minh  
1. **Similar Products**: Đề xuất sản phẩm tương tự dựa trên vector embedding
2. **User-based Recommendations**: Đề xuất theo lịch sử tương tác người dùng
3. **Popular Products**: Sản phẩm phổ biến cho người dùng mới
4. **Hybrid Scoring**: Kết hợp nhiều yếu tố (nhãn hàng, danh mục, tương tác)

### 📊 Thu thập & Phân tích dữ liệu
- **Interaction Tracking**: Thu thập tương tác view, cart, wishlist
- **Performance Evaluation**: Metrics NDCG, Precision cho đánh giá hiệu quả
- **User Profiling**: Xây dựng profile người dùng từ behavior data

## 🛠️ Công nghệ sử dụng

| Lĩnh vực | Công nghệ |
|----------|-----------|
| **Backend** | Flask, SQLAlchemy, MySQL |
| **Machine Learning** | Sentence Transformers, Scikit-learn, NLTK |
| **Frontend** | HTML5, CSS3, JavaScript, jQuery, Bootstrap |
| **API** | Flask-RESTX, Swagger UI |
| **Database** | MySQL, Vector Embeddings |

## 📦 Cấu trúc thư mục

```
HeTuVanThongTin/
├── Backend/                 # Flask application
│   ├── models/             # Database models  
│   ├── routes/             # API routes
│   ├── services/           # Business logic & ML services
│   ├── templates/          # HTML templates
│   └── static/             # CSS, JS, images
├── Data/                   # Raw data & crawling scripts
├── Faker/                  # Mock data generation
└── Documents/              # Project documentation
```

💡 **Lưu ý**: Đây là hệ thống demo nhằm trình bày các khái niệm recommendation system, không phải e-commerce website thương mại hoàn chỉnh.







 

### 📋 Tổng quan
Hệ thống User Profiling được thiết kế để theo dõi, phân tích và học từ hành vi người dùng nhằm tạo ra các đề xuất sản phẩm cá nhân hóa chính xác.

### 📊 Thu thập dữ liệu người dùng

#### 2. **Loại tương tác được theo dõi**
- **View (xem)**: Thời gian xem, số lần xem sản phẩm
- **Cart (giỏ hàng)**: Thêm/xóa sản phẩm khỏi giỏ hàng
- **Wishlist (yêu thích)**: Đánh dấu sản phẩm yêu thích
- **Rating (đánh giá)**: Điểm đánh giá từ 1-5 sao


## Các file cần lưu ý hiểu
**view_routes.py**: Nơi gọi API và xử lý dữ liệu, tải dữ liệu cho từng trang, bảo đảm các chức năng recommend
**product_vectorize.py**: API, Đây là đầu ra của backend để gộp các quy trình xử lý đề xuất thành 1

**recommend.py**: Nơi xử lý logic việc tính độ tương đồng và đề xuất thành danh sách sản phẩm
**preprocess.py**: Nơi xử lý dữ liệu trước khi nhúng
**embed_service.py**: Nơi nhúng dữ liệu
**evaluation.py**: Nơi đánh giá dữ liệu 

## Cách dữ liệu di chuyển

Dữ liệu thô trên db -> Preprocess -> Embed_service -> Recommend -> Product_vectorzie -> view_routes -> Frontend
-> Evaluation (nếu cần thiết)


## -----------------------------------------------------------------------------------------------------------------


### 🎯 Xây dựng User Profile

#### 1. **Mô hình dữ liệu tương tác** (Bảng interaction và model interact trong folder models)

#### 2. **Phân tích hành vi và tạo profile**
- **Weighted Scoring**: Gán trọng số khác nhau cho từng loại tương tác
  - Cart interactions: 0.8 (quan tâm mua hàng cao)
  - Wishlist interactions: 0.5 (quan tâm trung bình)
  - View interactions: 0.2 (quan tâm thấp)
  - Rating: Chuẩn hóa theo thang 0-1




### 🤖 Hệ thống đề xuất cá nhân hóa

#### 1. **Thuật toán Hybrid Recommendation**
```python
def recommend_for_user(self, user_id, top_n=5):
    # Lấy tương tác gần đây nhất
    user_interactions = TuongTac.query.filter_by(UserID=user_id).all()
    
    # Ưu tiên: Cart > Wishlist > View
    source_items = cart_items or wishlist_items or viewed_items
    recent_product_id = source_items[0].ProductID
    
    # Đề xuất sản phẩm tương tự với hybrid scoring
    return self.recommend_similar_products(recent_product_id, use_hybrid=True)
```

#### 2. **Content-based 
- **Similarity calculation**: Cosine similarity trên product embeddings
- **Hybrid scoring**: Kết hợp thông tin sản phẩm (brand, category) với behavior data
- **Temporal weighting**: Ưu tiên tương tác gần đây





### 📈 Đánh giá chất lượng đề xuất

#### 1. **Relevance Scoring**
```python
def get_relevance_scores(user_id, recommended_product_ids):
    for product_id in recommended_product_ids:
        interactions = TuongTac.query.filter_by(UserID=user_id, ProductID=product_id)
        
        # Tính điểm dựa trên loại tương tác
        if cart_interactions: score = 0.8
        elif wishlist_interactions: score = 0.5  
        elif view_interactions: score = 0.2
        elif ratings: score = avg_rating / 5.0
```

#### 2. **Evaluation Metrics**
- **NDCG (Normalized Discounted Cumulative Gain)**: Đánh giá ranking quality
- **Precision**: Tỷ lệ sản phẩm relevant trong danh sách đề xuất


### 🔄 Quy trình hoạt động chung của chức năng đánh giá và vai trò của nó trong hệ thống

1. **Thu thập**: JavaScript tracking ghi nhận mọi tương tác người dùng
2. **Lưu trữ**: API `/api/interactions` lưu vào database MySQL
3. **Phân tích**: RecommendationService phân tích pattern từ interaction history
4. **Tính toán**: Vector similarity + hybrid scoring cho personalized recommendations  
5. **Đánh giá**: Continuous evaluation với NDCG/Precision metrics
6. **Cải thiện**: Feedback loop để optimize algorithm




