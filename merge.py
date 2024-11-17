from pymongo import MongoClient
import pandas as pd

# Kết nối MongoDB
def connect_to_mongodb(uri, database_name):
    client = MongoClient("mongodb+srv://axellent2004:0964212618@bigdata.l07vk.mongodb.net/")
    return client["thpt"]

# Truy vấn và tải dữ liệu theo bộ lọc
def load_data_by_filter(db, year=None, subject=None):
    query = {}
    if year:
        query["Year"] = {"$in": year}
    if subject:
        query["Subject"] = {"$in": subject}

    # Chỉ lấy các cột cần thiết
    projection = {
        "sbd": 1,
        "year": 1,
        "toan": 1,
        "ngu_van": 1,
        "ngoai_ngu": 1,
        "vat_li": 1,
        "hoa_hoc": 1,
        "sinh_hoc": 1,
        "lich_su": 1,
        "dia_li": 1,
        "gdcd": 1,
    }

    # Truy vấn MongoDB
    records = db.scores.find(query, projection)
    return pd.DataFrame(records)