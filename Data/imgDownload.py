import os
import requests
import pandas as pd

def download_image(image_url, save_folder, file_name):
    try:
        # Gửi yêu cầu tải ảnh
        response = requests.get(image_url, stream=True)
        response.raise_for_status()

        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(save_folder, exist_ok=True)

        # Đường dẫn lưu ảnh
        file_path = os.path.join(save_folder, file_name)

        # Ghi dữ liệu ảnh vào file
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Image downloaded: {file_path}")
    except Exception as e:
        print(f"Error downloading image {image_url}: {e}")

# Đọc file Excel
excel_file = "d:/HeTuVanThongTin/Data/linkAnh.xlsx"  # Đường dẫn file Excel
save_folder = "d:/HeTuVanThongTin/Data/img"  # Thư mục lưu ảnh

try:
    # Đọc danh sách URL từ file Excel
    df = pd.read_excel(excel_file)

    # Kiểm tra cột chứa URL ảnh
    if 'Image URL' not in df.columns:
        print("Error: 'Image URL' column not found in the Excel file.")
    else:
        # Lặp qua từng URL và tải ảnh
        for index, row in df.iterrows():
            image_url = row['Image URL']
            if pd.notna(image_url):  # Kiểm tra URL không bị null
                file_name = os.path.basename(image_url)  # Lấy tên file từ URL
                download_image(image_url, save_folder, file_name)
except Exception as e:
    print(f"Error processing the Excel file: {e}")