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
- [x] Tạo cấu trúc thư mục frontend
- [x] Cài đặt các dependencies cần thiết

### 3.2. Phát triển các trang 

#### 3.2.1. Trang chủ
- [x] Xây dựng base.html
- [x] Chỉnh sửa template index.html để kế thừa từ base.html
- [x] Tạo route hiển thị danh sách tất cả sản phẩm 
- [x] Thêm phân mục sản phẩm mới nhất (sắp xếp theo ngày tạo)
- [x] Tạo các liên kết điều hướng giữa các trang

#### 3.2.2. Trang chi tiết sản phẩm
- [x] Chỉnh sửa product.html để kế thừa từ base.html
- [x] Tạo route hiển thị thông tin chi tiết của một sản phẩm theo ID
- [x] Hiển thị sản phẩm liên quan (sử dụng API Recommendations)
- [x] Tạo chức năng thêm sản phẩm vào giỏ hàng

#### 3.2.3. Trang giỏ hàng
- [ ] Chỉnh sửa cart.html để kế thừa từ base.html
- [ ] Tạo route hiển thị giỏ hàng của người dùng
- [ ] Tạo chức năng cập nhật số lượng sản phẩm trong giỏ hàng
- [ ] Tạo chức năng xóa sản phẩm khỏi giỏ hàng
- [ ] Hiển thị sản phẩm đề xuất dựa trên giỏ hàng

#### 3.2.4. Trang đăng nhập
- [ ] Tạo form đăng nhập trong dangnhap.html
- [ ] Tạo route xử lý đăng nhập
- [ ] Thiết lập xác thực người dùng và session
- [ ] Xử lý lỗi đăng nhập và hiển thị thông báo

#### 3.2.5. Trang đăng ký
- [ ] Tạo form đăng ký trong dangky.html khác
- [ ] Tạo route xử lý đăng ký
- [ ] Kiểm tra và xác thực dữ liệu đăng ký
- [ ] Xử lý lỗi đăng ký và hiển thị thông báo

#### 3.2.6. Trang danh sách sản phẩm 
- [ ] Tạo trang danh sách sản phẩm trong store.html để kế thừa từ base.html
- [ ] Tạo chức năng lọc và tìm kiếm theo nhãn hàng, thời gian, giá thành

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

