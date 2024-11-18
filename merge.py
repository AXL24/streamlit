import pandas as pd
from pymongo import MongoClient

# MongoDB connection
def connect_to_mongodb(uri, db_name):
    """Connect to MongoDB and return the database instance."""
    return MongoClient(uri)[db_name]

# Fetch data from a collection
def fetch_data(db, collection_name):
    """Fetch data from the specified collection and return a DataFrame."""
    projection = {
        "sbd": {"$toString": "$sbd"}, "toan": 1, "ngu_van": 1, "ngoai_ngu": 1,
        "vat_li": 1, "hoa_hoc": 1, "sinh_hoc": 1, "lich_su": 1,
        "dia_li": 1, "gdcd": 1, "_id": 0
    }
    data = pd.DataFrame(db[collection_name].find({}, projection))
    if not data.empty:
        data.columns = data.columns.str.lower()
        columns = ["sbd"] + [col for col in data.columns if col != "sbd"]
        data = data[columns]
    return data

# Load and combine data
@st.cache_data
def load_combined_data(uri, db_name):
    """Load data from multiple years and combine into a single DataFrame."""
    db = connect_to_mongodb(uri, db_name)
    combined_data = pd.concat(
        [fetch_data(db, str(year)).assign(nam=year) for year in [2022, 2023, 2024]],
        ignore_index=True
    )
    return combined_data
