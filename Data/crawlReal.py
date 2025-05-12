import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import time

import sys
import os

# Thêm thư mục gốc của dự án vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Backend.models.database import db
from Backend.models.product import SanPham
from flask import Flask

# Khởi tạo Flask app để sử dụng SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/hetuvan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def fetch_product_urls(sitemap_url, limit=10):
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        root = ET.fromstring(response.content)

        namespace = {
            'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
            'image': 'http://www.google.com/schemas/sitemap-image/1.1'
        }

        product_data = []
        for url in root.findall("ns:url", namespace):
            loc = url.find("ns:loc", namespace)
            image_loc = url.find("image:image/image:loc", namespace)

            if loc is not None:
                product_info = {
                    'url': loc.text,
                    'image': image_loc.text if image_loc is not None else "N/A"
                }
                product_data.append(product_info)

            if len(product_data) >= limit:
                break

        return product_data
    except Exception as e:
        print(f"Error fetching product URLs: {e}")
        return []

def fetch_product_details(product_url, image_from_sitemap="N/A"):
    try:
        response = requests.get(product_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Tên sản phẩm
        name = soup.find('h1', class_='title-product')
        name = name.text.strip() if name else "N/A"

        # Giá sản phẩm
        price = soup.find('span', class_='old-price')
        price = price.text.strip() if price else "N/A"

        # Ảnh sản phẩm (ưu tiên dùng từ sitemap)
        image = image_from_sitemap
        if image == "N/A":
            img_tag = soup.find('a', class_='d-block  pos-relative embed-responsive embed-responsive-1by1')
            if img_tag:
                img = img_tag.find('img')
                image = img['src'] if img else "N/A"

        # Nhà cung cấp hoặc trạng thái
        supplier = soup.find('span', class_='status_name')
        supplier = supplier.text.strip() if supplier else "N/A"

        # Nội dung mô tả sản phẩm
        content_div = soup.find('div', id='content', class_='m0')
        content = content_div.get_text(separator=" ", strip=True) if content_div else "N/A"

        return {
            'name': name,
            'price': price,
            'image': image,
            'supplier': supplier,
            'content': content,
            'url': product_url
        }
    except Exception as e:
        print(f"Error fetching product details from {product_url}: {e}")
        return None

def save_product_to_db(product):
    """Lưu sản phẩm vào cơ sở dữ liệu"""
    try:
        with app.app_context():
            # Kiểm tra sản phẩm đã tồn tại chưa (dựa trên URL)
            existing_product = SanPham.query.filter_by(Ten=product['name']).first()
            if existing_product:
                print(f"Product already exists: {product['name']}")
                return

            # Tạo sản phẩm mới
            new_product = SanPham(
                Ten=product['name'],
                NhanHang=product['supplier'],
                MoTa=product['content'],
                Gia=float(product['price'].replace(',', '').replace('₫', '')) if product['price'] != "N/A" else 0,
                SoLuong=100,  # Giá trị mặc định
                HinhAnh=product['image']
            )
            db.session.add(new_product)
            db.session.commit()
            print(f"Product saved: {product['name']}")
    except Exception as e:
        print(f"Error saving product to database: {e}")
        db.session.rollback()

# URL sitemap sản phẩm
sitemap_url = "https://thienlong.vn/sitemap_products_1.xml"

# Lấy danh sách sản phẩm (giới hạn n sản phẩm)
product_entries = fetch_product_urls(sitemap_url, limit=2)

# Lấy thông tin chi tiết từng sản phẩm và lưu vào cơ sở dữ liệu
with app.app_context():  # Đảm bảo toàn bộ vòng lặp chạy trong ngữ cảnh ứng dụng Flask
    for entry in product_entries:
        url = entry['url']
        image = entry['image']
        product_details = fetch_product_details(url, image_from_sitemap=image)
        if product_details:
            save_product_to_db(product_details)
        time.sleep(12)