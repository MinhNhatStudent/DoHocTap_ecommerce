# Tổng quan kiến trúc dự án "Hệ tư vấn thông tin"


## 1. Tổng quát
## 1.1 Mục tiêu hệ thống
Đây là một hệ thống tư vấn thông tin (information recommendation system) được thiết kế để đề xuất các sản phẩm tương tự hoặc phù hợp cho người dùng dựa trên các tương tác của họ và đặc điểm của sản phẩm. Hệ thống được xây dựng để trình bày những kiến thức về content-based filtering trong môn học hệ tư vấn thông tin. Hệ thống bao gồm cả backend xử lý logic đề xuất và frontend demo trực quan kết quả đề xuất. Hệ thống không nhắm đến việc trở thành một e-commerce website hoàn chỉnh.

## 1.2 Đối tượng sử dụng chính
- Học sinh, sinh viên với nhu cầu trình bày đồ án những kiến thức đã học
- Giảng viên và người đánh giá đồ án
- Không có người dùng bên ngoài

## 1.3 Mục tiêu chức năng chính
- Xây hệ thống tư vấn ở backend
- Xây dựng frontend để demo chức năng của recommend system 
    +   Website sẽ có giao diện và màu sắc giống như các website ecommerce 
    +   Trang chủ giúp hiển thị danh sách các sản phẩm (trong đó có mục hiển thị sản phẩm mới nhất)
    +   Trang chi tiết sản phẩm hiện thị sản phảm chi tiết (trong đó có mục hiển thị sản phẩm liên quan)
    +   Trang giỏ hàng (Trang này không nhất thiết phải implement toàn bộ chức năng, chỉ cần đảm bảo thêm sản phẩm vào giỏ hàng, hiển thị các sản phẩm liên quan tới người dùng và liên quan đến các sản phẩm liên quan trong giỏ hàng)
    +   Trang đăng nhập
    +   Trang đăng ký
- Giải quyết vấn đề cold-start:
    + Sử dụng phương pháp content-based filtering để đề xuất sản phẩm dựa trên đặc điểm của sản phẩm mà không cần dữ liệu tương tác từ người dùng
    + Sử dụng vector nhúng (embeddings) từ mô hình đa ngôn ngữ để biểu diễn sản phẩm dựa trên nội dung mô tả
    + Triển khai hệ thống đề xuất sản phẩm phổ biến (popular products) cho người dùng mới chưa có lịch sử tương tác
    + Tạo profile người dùng từ thông tin cơ bản và các tương tác ban đầu để nhanh chóng cung cấp đề xuất có liên quan


- Lưu ý khi xây dựng hệ thống
    + Không implement các giao diện hay chức năng liên quan tới bảng favorite (bảng này chỉ có tác dụng trình bày cho thầy cô)



## 2. Kiến trúc hệ thống

### 2.1. Backend (Flask)
Hệ thống sử dụng Flask làm framework backend chính, với cấu trúc được tổ chức theo mô hình MVC (Model-View-Controller):

#### Models (Mô hình dữ liệu):
- **Database**: MySQL được sử dụng làm cơ sở dữ liệu, với kết nối thông qua SQLAlchemy ORM
- **Các models chính**:
  - `SanPham`: Thông tin về sản phẩm (tên, nhãn hàng, mô tả, giá, số lượng, hình ảnh)
  - `NguoiDung`: Thông tin người dùng (tên, email, mật khẩu, vai trò, tuổi)
  - `TuongTac`: Lưu trữ tương tác giữa người dùng và sản phẩm (xem, thêm vào giỏ hàng, yêu thích)
  - `SanPhamEmbed`: Lưu trữ vector nhúng (embedding) của sản phẩm cho mô hình đề xuất
  - `DonHang` và `SanPhamTrongDonHang`: Quản lý thông tin đơn hàng
  - `Cart`: Quản lý giỏ hàng người dùng
  - `Favorite`: Quản lý danh sách yêu thích

#### API đã xây dựng:
- **API Người dùng (Users)**: 
  - `GET /users` - Lấy danh sách người dùng
  - `POST /users` - Tạo người dùng mới
  - `GET /users/{user_id}` - Lấy thông tin người dùng theo ID
  - `PUT /users/{user_id}` - Cập nhật thông tin người dùng
  - `DELETE /users/{user_id}` - Xóa người dùng

- **API Sản phẩm (Products)**:
  - `GET /products` - Lấy danh sách sản phẩm
  - `POST /products` - Tạo sản phẩm mới
  - `GET /products/{product_id}` - Lấy thông tin chi tiết sản phẩm
  - `PUT /products/{product_id}` - Cập nhật thông tin sản phẩm
  - `DELETE /products/{product_id}` - Xóa sản phẩm

- **API Tương tác (Interactions)**:
  - `POST /interactions` - Thêm tương tác mới
  - `GET /interactions/{user_id}` - Lấy danh sách tương tác của người dùng
  - `DELETE /interactions/delete/{interaction_id}` - Xóa một tương tác

- **API Sản phẩm yêu thích (Favorites)**:
  - `POST /favorites` - Thêm sản phẩm vào danh sách yêu thích
  - `GET /favorites/{user_id}` - Lấy danh sách sản phẩm yêu thích của người dùng
  - `DELETE /favorites/delete/{favorite_id}` - Xóa sản phẩm khỏi danh sách yêu thích

- **API Giỏ hàng (Cart)**:
  - `POST /cart` - Thêm sản phẩm vào giỏ hàng
  - `GET /cart/{user_id}` - Lấy danh sách sản phẩm trong giỏ hàng của người dùng
  - `PUT /cart/{cart_id}` - Cập nhật số lượng sản phẩm trong giỏ hàng
  - `DELETE /cart/{cart_id}` - Xóa sản phẩm khỏi giỏ hàng

- **API Đơn hàng (Orders)**:
  - `POST /orders` - Tạo đơn hàng mới
  - `GET /orders/{user_id}` - Lấy danh sách đơn hàng của người dùng
  - `PUT /orders/{order_id}` - Cập nhật trạng thái đơn hàng
  - `DELETE /orders/{order_id}` - Xóa đơn hàng

- **API Đề xuất (Recommendations)**:
  - `GET /recommend_bp/similar/{product_id}` - Lấy các sản phẩm tương tự với một sản phẩm
  - `GET /recommend_bp/user/{user_id}` - Lấy các đề xuất sản phẩm cho người dùng
  - `GET /recommend_bp/popular` - Lấy các sản phẩm phổ biến

- **API Vector hóa sản phẩm (Vectorize)**:
  - Các API liên quan đến xử lý dữ liệu sản phẩm ở dạng vector

- **API Swagger UI**:
  - `GET /swagger` - Giao diện tài liệu API tương tác

- **API Khác**:
  - `POST /reset-database` - Xóa và tạo lại toàn bộ cơ sở dữ liệu

#### Services (Dịch vụ):
- `embed_service.py`: Dịch vụ tạo vector nhúng cho sản phẩm sử dụng mô hình Sentence Transformers
- `preprocess.py`: Xử lý tiền xử lý văn bản tiếng Việt (loại bỏ stopwords, dấu câu, số...)
- `recommend.py`: Dịch vụ đề xuất sản phẩm dựa trên độ tương đồng cosine giữa các vector nhúng
- `evaluation.py`: Công cụ đánh giá hiệu suất của hệ thống đề xuất


## 3. Quy trình hoạt động của hệ thống

### 3.1. Tạo vector nhúng cho sản phẩm
1. Hệ thống sử dụng mô hình `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` để tạo vector nhúng cho sản phẩm
2. Văn bản mô tả sản phẩm được tiền xử lý (loại bỏ stopwords, dấu câu, số...)
3. Vector nhúng được lưu trữ trong bảng `SanPhamEmbed`

### 3.2. Đề xuất sản phẩm
Hệ thống cung cấp 3 phương pháp đề xuất sản phẩm:
1. **Similar Products**: Đề xuất sản phẩm tương tự dựa trên độ tương đồng cosine giữa các vector nhúng
2. **User Recommendations**: Đề xuất sản phẩm cho người dùng dựa trên lịch sử tương tác của họ
3. **Popular Products**: Đề xuất các sản phẩm phổ biến nhất

### 3.3. Đánh giá hiệu suất
- Hệ thống có tích hợp công cụ đánh giá hiệu suất của các thuật toán đề xuất (`evaluation.py`)

## 4. Công nghệ sử dụng
- **Backend**: Flask (Python)
- **Database**: MySQL + SQLAlchemy ORM
- **NLP**: NLTK, Sentence Transformers
- **Xử lý dữ liệu**: NumPy, Scikit-learn

## 5. Cấu trúc thư mục
- **Backend/**: Chứa code backend của hệ thống
  - **models/**: Các model định nghĩa cấu trúc dữ liệu
  - **routes/**: Các API endpoint
  - **services/**: Các dịch vụ xử lý logic nghiệp vụ
  - **app.py**: File khởi chạy Flask app
- **Data/**: Công cụ thu thập dữ liệu và dữ liệu thô
- **Faker/**: Công cụ tạo dữ liệu giả
- **Documents/**: Tài liệu dự án

