from faker import Faker
import random
import datetime
import csv

# Khởi tạo Faker
fake = Faker('en_US')

# Giả định số lượng người dùng và sản phẩm đã có
user_ids = list(range(1, 101))  # UserID từ 1-100
product_ids = list(range(1, 538))  # ProductID từ 1-537

# Giả định giá sản phẩm (trong thực tế nên lấy từ database)
product_prices = {}
for product_id in product_ids:
    # Giá từ 100,000 đến 10,000,000 VND
    product_prices[product_id] = round(random.uniform(100000, 10000000), 2)

# Tạo đơn hàng và chi tiết đơn hàng
orders = []
order_items = []
order_item_id = 1

# Tạo 200 đơn hàng
for order_id in range(1, 100):
    # Chọn người dùng ngẫu nhiên
    user_id = random.choice(user_ids)
    
    # Ngày đặt hàng trong 1 năm gần đây
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    
    # Trạng thái đơn hàng (phần lớn là completed)
    status_weights = [15, 75, 10]  # 15% pending, 75% completed, 10% cancelled
    status = random.choices(['pending', 'completed', 'cancelled'], weights=status_weights)[0]
    
    # Tạo các mặt hàng trong đơn hàng (1-5 sản phẩm mỗi đơn hàng)
    num_items = random.randint(1, 5)
    selected_products = random.sample(product_ids, num_items)
    
    # Tính tổng tiền đơn hàng
    total_amount = 0
    
    # Tạo chi tiết đơn hàng
    for product_id in selected_products:
        quantity = random.randint(1, 3)
        price = product_prices[product_id]
        item_amount = quantity * price
        total_amount += item_amount
        
        order_items.append({
            'OrderItemID': order_item_id,
            'OrderID': order_id,
            'ProductID': product_id,
            'SoLuong': quantity,
            'GiaThanh': price
        })
        order_item_id += 1
    
    # Thêm đơn hàng
    orders.append({
        'OrdersID': order_id,
        'UserID': user_id,
        'TongTien': round(total_amount, 2),
        'NgayDat': order_date.strftime('%Y-%m-%d %H:%M:%S'),
        'TrangThai': status
    })

# Xuất đơn hàng ra file SQL
with open('donhang_generated.sql', 'w', encoding='utf-8') as f:
    f.write("-- Generated with Faker\n")
    f.write("-- Dữ liệu mock cho bảng DonHang\n\n")
    f.write("INSERT INTO `DonHang` (`UserID`, `TongTien`, `NgayDat`, `TrangThai`) VALUES\n")
    
    for idx, order in enumerate(orders):
        f.write(f"({order['UserID']}, {order['TongTien']}, '{order['NgayDat']}', '{order['TrangThai']}')")
        
        if idx < len(orders) - 1:
            f.write(",\n")
        else:
            f.write(";\n\n")
    
    f.write("-- Dữ liệu mock cho bảng SanPhamTrongDonHang\n\n")
    f.write("INSERT INTO `SanPhamTrongDonHang` (`OrderID`, `ProductID`, `SoLuong`, `GiaThanh`) VALUES\n")
    
    for idx, item in enumerate(order_items):
        f.write(f"({item['OrderID']}, {item['ProductID']}, {item['SoLuong']}, {item['GiaThanh']})")
        
        if idx < len(order_items) - 1:
            f.write(",\n")
        else:
            f.write(";\n")

# Xuất đơn hàng ra file CSV
with open('donhang_generated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['OrdersID', 'UserID', 'TongTien', 'NgayDat', 'TrangThai']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for order in orders:
        writer.writerow(order)

# Xuất chi tiết đơn hàng ra file CSV
with open('chitietdonhang_generated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['OrderItemID', 'OrderID', 'ProductID', 'SoLuong', 'GiaThanh']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for item in order_items:
        writer.writerow(item)

print(f"Đã tạo thành công 200 đơn hàng với {len(order_items)} mặt hàng!")
print(f"- File SQL: donhang_generated.sql")
print(f"- File CSV đơn hàng: donhang_generated.csv")
print(f"- File CSV chi tiết đơn hàng: chitietdonhang_generated.csv")