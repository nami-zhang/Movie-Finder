import os
import pandas as pd
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
DATABASE_NAME = "imdb"
COLLECTION_AKAS = "akas"
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=600000,  # 600 seconds
    connectTimeoutMS=600000,          # 600 seconds
    socketTimeoutMS=600000            # 600 seconds
)
db = client[DATABASE_NAME]

# Data file paths
DATA_FOLDER = "../data"
FILES = {
    "akas": os.path.join(DATA_FOLDER, "title.akas.tsv"),
}

def load_data(file_path, **kwargs):
    """Load a TSV file into a Pandas DataFrame with low_memory set to False."""
    return pd.read_csv(file_path, sep="\t", na_values="\\N", low_memory=False, **kwargs)

def process_akas():
    """Processes the title.akas data and drops unnecessary columns."""
    akas_df = load_data(FILES["akas"], dtype={"titleId": str})
    # Drop unnecessary columns
    akas_df = akas_df.drop(columns=["ordering", "types", "attributes"], errors="ignore")
    return akas_df

def import_akas_data():
    """Import IMDb akas data into MongoDB."""
    print("Processing title.akas.tsv...")
    akas_df = process_akas()

    print("Clearing old data from MongoDB (akas)...")
    db[COLLECTION_AKAS].delete_many({})

    print("Inserting akas data into MongoDB...")
    akas_records = akas_df.to_dict("records")

    # Insert records in chunks to manage large data
    for i in range(0, len(akas_records), 10000):
        chunk = akas_records[i:i + 10000]
        db[COLLECTION_AKAS].insert_many(chunk)
        # print(f"Inserted {i + len(chunk)} records into '{COLLECTION_AKAS}'.")
    
    db[COLLECTION_AKAS].create_index([("titleId", 1), ("region", 1)])
    db[COLLECTION_AKAS].create_index([("titleId", 1), ("language", 1)])
    print(f"Inserted {len(akas_records)} records into '{COLLECTION_AKAS}'.")
    print("Data import for akas completed.")

if __name__ == "__main__":
    try:
        import_akas_data()
    except Exception as e:
        print(f"Error during import: {e}")
