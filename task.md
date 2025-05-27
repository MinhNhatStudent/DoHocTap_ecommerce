As you complete tasks and references relevant files, update this file as our memory to help with future tasks.

# Danh sách nhiệm vụ phát triển Hệ thống tư vấn thông tin
# Lưu ý những gì đã được xây dựng từ trước (được đánh dấu đã hoàn thành) không cần tối ưu hay sửa lại, nếu cần sửa lại hãy hỏi chủ hệ thống

## 1. Thiết lập cơ sở hạ tầng

### 1.1. Cấu hình database
- [x] Thiết lập cơ sở dữ liệu MySQL (`Backend/models/database.py`)
- [x] Tạo các bảng theo mô hình dữ liệu (các file trong `Backend/models/`)
- [x] Thiết lập SQLAlchemy ORM (`Backend/models/database.py`)

### 1.2. Thiết lập Flask Framework
- [x] Cài đặt Flask và các dependencies cần thiết (`Backend/app.py`)
- [x] Cấu hình môi trường phát triển (`Backend/app.py`)
- [x] Thiết lập cấu trúc thư mục dự án

## 2. Phát triển backend

### 2.1. Models
- [x] Tạo model SanPham (`Backend/models/product.py`)
- [x] Tạo model NguoiDung (`Backend/models/user.py`)
- [x] Tạo model TuongTac (`Backend/models/interaction.py`)
- [x] Tạo model SanPhamEmbed (`Backend/models/product_embed.py`)
- [x] Tạo model DonHang và SanPhamTrongDonHang (`Backend/models/orders.py`, `Backend/models/order_item.py`)
- [x] Tạo model Cart (`Backend/models/cart.py`)
- [x] Tạo model Favorite (`Backend/models/favorite.py`)

### 2.2. API Routes
- [x] Phát triển API Users (CRUD) (`Backend/routes/user_routes.py`)
- [x] Phát triển API Products (CRUD) (`Backend/routes/product_routes.py`)
- [x] Phát triển API Interactions (`Backend/routes/interaction_routes.py`)
- [x] Phát triển API Favorites (`Backend/routes/favorite_routes.py`)
- [x] Phát triển API Cart (`Backend/routes/cart_routes.py`)
- [x] Phát triển API Orders (`Backend/routes/order_routes.py`)
- [x] Phát triển API Recommendations (`Backend/routes/recommend_routes.py`)
- [x] Phát triển API Vectorize (`Backend/routes/product_vectorize.py`)
- [x] Thiết lập Swagger UI (`Backend/routes/swagger_routes.py`)

### 2.3. Services
- [x] Phát triển dịch vụ embed_service.py (tạo vector nhúng) (`Backend/services/embed_service.py`)
- [x] Phát triển dịch vụ preprocess.py (xử lý tiền xử lý văn bản) (`Backend/services/preprocess.py`)
- [x] Phát triển dịch vụ recommend.py (đề xuất sản phẩm) (`Backend/services/recommend.py`)
- [x] Phát triển công cụ evaluation.py (đánh giá hiệu suất) (`Backend/services/evaluation.py`)

## 3. Phát triển Frontend
## Approach: Use Flask templates (Jinja2) with HTML/CSS/JavaScript
## Frontend templete HTML/CSS/JavaScript được cài đặt ở folder FrontEnd Template, hãy sử dụng nó để xây dựng frontend 


### 3.1. Thiết lập cấu trúc frontend
- [ ] Tạo cấu trúc thư mục frontend
- [ ] Cài đặt các dependencies cần thiết

### 3.2. Phát triển các trang 
- [ ] Tạo trang chủ (hiển thị danh sách sản phẩm và sản phẩm mới nhất) (sử dụng trang index.html trong FrontEnd template)
- [ ] Tạo trang chi tiết sản phẩm (hiển thị sản phẩm chi tiết và sản phẩm liên quan) (sử dụng trang product trong FrontEnd template)
- [ ] Tạo trang giỏ hàng (sử dụng trang blank.html trong FrontEnd template)
- [ ] Tạo trang đăng nhập (sử dụng trang blank.html trong FrontEnd template)
- [ ] Tạo trang đăng ký (sử dụng trang blank.html trong FrontEnd template)

### 3.3. Tích hợp API
- [ ] Kết nối API Users
- [ ] Kết nối API Products
- [ ] Kết nối API Recommendations
- [ ] Kết nối API Cart
- [ ] Kết nối API Interactions

## 4. Phát triển hệ thống đề xuất

### 4.1. Content-based Filtering
- [x] Cài đặt mô hình sentence-transformers (`Backend/services/embed_service.py`)
- [x] Tiền xử lý dữ liệu sản phẩm (`Backend/services/preprocess.py`)
- [x] Tạo vector nhúng cho sản phẩm (`Backend/services/embed_service.py`)
- [x] Phát triển thuật toán tìm sản phẩm tương tự dựa trên độ tương đồng cosine (`Backend/services/recommend.py`)

### 4.2. Giải quyết vấn đề cold-start
- [x] Triển khai đề xuất sản phẩm phổ biến cho người dùng mới (`Backend/services/recommend.py`)
- [x] Tạo profile người dùng từ thông tin cơ bản (`Backend/services/recommend.py`)
- [x] Phát triển thuật toán đề xuất dựa trên profile người dùng (`Backend/services/recommend.py`)

### 4.3. Đánh giá hiệu suất
- [x] Xây dựng metrics đánh giá (`Backend/services/evaluation.py`)
- [x] Đánh giá hiệu suất các thuật toán đề xuất (`Backend/services/evaluation.py`)


## 7. Ưu tiên nhiệm vụ tiếp theo

### Các nhiệm vụ ưu tiên cao:
1. Tạo cấu trúc thư mục frontend và thiết lập môi trường phát triển
2. Phát triển các trang frontend cơ bản (trang chủ, chi tiết sản phẩm, giỏ hàng)
3. Kết nối API Recommendations vào frontend để hiển thị sản phẩm liên quan
4. Tích hợp các tính năng đăng nhập/đăng ký
5. Kiểm thử tích hợp hệ thống đề xuất

### Các nhiệm vụ ưu tiên trung bình:
1. Hoàn thiện các tính năng frontend còn thiếu
2. Cải thiện giao diện người dùng
3. Hoàn thiện tài liệu kỹ thuật

