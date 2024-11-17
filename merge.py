import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Replace with your actual MongoDB connection details
MONGO_URI = "mongodb+srv://axellent2004:0964212618@bigdata.l07vk.mongodb.net/"
DATABASE_NAME = "thpt"


def fetch_and_label_data(collection, year):
    data = list(collection.find({}))
    df = pd.DataFrame(data)
    df["Year"] = year  # Add Year column
    return df


def prepare():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

    # Fetch data from three collections with caching
    
    diem_2024 = fetch_and_label_data(db["2024"], 2024)

    for df in [diem_2024]:
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)

    # Combine the tables using pd.concat
    combined_data = pd.concat([diem_2024], ignore_index=True)

    return combined_data


def main():
    st.title("Phân Tích Điểm THPT 2022-2024")

    # ... rest of your code using the combined_data

    if __name__ == "__main__":
        combined_data = prepare()
        main()
