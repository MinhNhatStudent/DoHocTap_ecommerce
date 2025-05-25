from faker import Faker
import random
import datetime
import csv

# Khởi tạo Faker
fake = Faker('en_US')

# Giả định số lượng người dùng và sản phẩm đã có trong hệ thống
user_ids = list(range(1, 101))  # UserID từ 1-100
product_ids = list(range(1, 538))  # ProductID từ 1-537

# Các loại tương tác
interaction_types = ['view', 'cart', 'wishlist']
# Tỷ lệ phân bố: view nhiều hơn cart, cart nhiều hơn wishlist
weights = [70, 20, 10]

# Tạo 2000 tương tác ngẫu nhiên
interactions = []
for i in range(1, 300):
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    interaction_type = random.choices(interaction_types, weights=weights)[0]
    
    # Rating chỉ cho một số tương tác, không phải tất cả
    rating = random.randint(1, 5) if random.random() < 0.3 else None
    
    # Tạo thời gian tương tác trong 6 tháng gần đây
    interaction_time = fake.date_time_between(start_date='-6m', end_date='now')
    
    # Ghi chú chỉ có ở một số tương tác
    note = fake.sentence() if random.random() < 0.2 else None
    
    # Số lần xem và thời gian xem chỉ có ý nghĩa cho loại 'view'
    view_count = random.randint(1, 10) if interaction_type == 'view' else 1
    view_time = random.randint(10, 300) if interaction_type == 'view' else 0
    
    interactions.append({
        'InteractionID': i,
        'GhiChu': note,
        'UserID': user_id,
        'ProductID': product_id,
        'InteractionType': interaction_type,
        'Rating': rating,
        'InteractionTime': interaction_time.strftime('%Y-%m-%d %H:%M:%S'),
        'SoLanXem': view_count,
        'ThoiGianXem': view_time
    })

# Xuất ra file SQL
with open('tuongtac_generated.sql', 'w', encoding='utf-8') as f:
    f.write("-- Generated with Faker\n")
    f.write("-- Dữ liệu mock cho bảng TuongTac\n\n")
    f.write("INSERT INTO `TuongTac` (`GhiChu`, `UserID`, `ProductID`, `InteractionType`, `Rating`, `InteractionTime`, `SoLanXem`, `ThoiGianXem`) VALUES\n")
    
    for idx, interaction in enumerate(interactions):
        # Xử lý NULL cho các trường có thể NULL
        note = f"'{interaction['GhiChu']}'" if interaction['GhiChu'] else "NULL"
        rating = interaction['Rating'] if interaction['Rating'] else "NULL"
        
        f.write(f"({note}, {interaction['UserID']}, {interaction['ProductID']}, '{interaction['InteractionType']}', {rating}, '{interaction['InteractionTime']}', {interaction['SoLanXem']}, {interaction['ThoiGianXem']})")
        
        if idx < len(interactions) - 1:
            f.write(",\n")
        else:
            f.write(";\n")

# Xuất ra file CSV để dễ xem
with open('tuongtac_generated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['InteractionID', 'GhiChu', 'UserID', 'ProductID', 'InteractionType', 
                 'Rating', 'InteractionTime', 'SoLanXem', 'ThoiGianXem']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for interaction in interactions:
        writer.writerow(interaction)

print(f"Đã tạo thành công 2000 tương tác ngẫu nhiên!")
print(f"- File SQL: tuongtac_generated.sql")
print(f"- File CSV: tuongtac_generated.csv")