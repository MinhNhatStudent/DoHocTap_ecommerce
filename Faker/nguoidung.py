from faker import Faker
import random
import datetime
import csv

# Khởi tạo Faker với locale tiếng Việt
fake = Faker('en_US')

# Đảm bảo email là duy nhất
used_emails = set()

# Tạo dữ liệu cho 100 người dùng
users = []
for i in range(1, 101):
    # Tạo email độc nhất
    while True:
        email = fake.email()
        if email not in used_emails:
            used_emails.add(email)
            break
    
    # Tạo ngày đăng ký trong 2 năm gần đây
    created_at = fake.date_time_between(start_date='-2y', end_date='now')
    
    # Tất cả đều là user theo yêu cầu
    role = 'user'
    
    # Password đơn giản không hash
    password = fake.password(length=8)
    
    users.append({
        'UserID': i,
        'Ten': fake.name(),
        'Email': email,
        'Pass': password,
        'Role': role,
        'Age': random.randint(18, 35),
        'CreatedAt': created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

# Xuất ra file SQL
with open('nguoidung_generated.sql', 'w', encoding='utf-8') as f:
    f.write("-- Generated with Faker\n")
    f.write("-- Dữ liệu mock cho bảng nguoidung\n\n")
    f.write("INSERT INTO `nguoidung` (`Ten`, `Email`, `Pass`, `Role`, `Age`, `CreatedAt`) VALUES\n")
    
    for idx, user in enumerate(users):
        f.write(f"('{user['Ten']}', '{user['Email']}', '{user['Pass']}', '{user['Role']}', {user['Age']}, '{user['CreatedAt']}')")
        
        if idx < len(users) - 1:
            f.write(",\n")
        else:
            f.write(";\n")

# Xuất ra file CSV để dễ xem
with open('nguoidung_generated.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['UserID', 'Ten', 'Email', 'Pass', 'Role', 'Age', 'CreatedAt']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for user in users:
        writer.writerow(user)

print(f"Đã tạo thành công 100 người dùng!")
print(f"- File SQL: nguoidung_generated.sql")
print(f"- File CSV: nguoidung_generated.csv")