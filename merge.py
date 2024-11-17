from pymongo import MongoClient
import pandas as pd

# MongoDB connection details
MONGO_URI = "mongodb+srv://axellent2004:0964212618@bigdata.l07vk.mongodb.net/"  # Replace with your MongoDB URI
DATABASE_NAME = "thpt"

# Function to fetch data and label it with year
def fetch_and_label_data(collection, year):
    data = list(collection.find({}))
    df = pd.DataFrame(data)
    df["Year"] = year  # Add Year column
    

# Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]

# Fetch data from three collections
    diem_2022 = fetch_and_label_data(db["2022"], 2022)
    diem_2023 = fetch_and_label_data(db["2023"], 2023)
    diem_2024 = fetch_and_label_data(db["2024"], 2024)


# Combine the tables using pd.concat
    combined_data = pd.concat([diem_2022, diem_2023, diem_2024], ignore_index=True)

# Output the combined table
    return combined_data

