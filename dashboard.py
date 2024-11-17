import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px


MONGO_URI = "mongodb+srv://axellent2004:096212618@bigdata.l07vk.mongodb.net/"  # Replace with your actual URI
DATABASE_NAME = "thpt"


@st.cache
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
    diem_2022 = fetch_and_label_data(db["2022"], 2022)
    diem_2023 = fetch_and_label_data(db["2023"], 2023)
    diem_2024 = fetch_and_label_data(db["2024"], 2024)

    for df in [diem_2022, diem_2023, diem_2024]:
        if "_id" in df.columns:
            df.drop(columns=["_id"], inplace=True)  # Drop "_id" column in-place

    # Combine the tables using pd.concat
    combined_data = pd.concat([diem_2022, diem_2023, diem_2024], ignore_index=True)

    return combined_data


def main():
    st.title("Phân Tích Điểm THPT 2022-2024")

    # Get data from the prepare function
    combined_data = prepare()

    # Display the first 10 rows
    st.subheader("First 10 records")
    st.dataframe(combined_data.head(10))

    # Rest of your code for data analysis and visualization
    # ... (replace with your specific visualizations)

if __name__ == "__main__":
    main()