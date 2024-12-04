import os
import pandas as pd
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
DATABASE_NAME = "imdb"
COLLECTION_NAME_BASICS = "name_basics"
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
    "name_basics": os.path.join(DATA_FOLDER, "name.basics.tsv"),
}

def load_data(file_path, **kwargs):
    """Load a TSV file into a Pandas DataFrame with low_memory set to False."""
    return pd.read_csv(file_path, sep="\t", na_values="\\N", low_memory=False, **kwargs)

def process_name_basics():
    """Processes the name.basics data and handles data types."""
    name_df = load_data(FILES["name_basics"], dtype={"nconst": str, "primaryName": str})
    
    # Handle year fields as integers, replacing NaN with 0
    name_df["birthYear"] = pd.to_numeric(name_df["birthYear"], errors="coerce").fillna(0).astype(int)
    name_df["deathYear"] = pd.to_numeric(name_df["deathYear"], errors="coerce").fillna(0).astype(int)
    
    # Split primaryProfession and knownForTitles into lists
    name_df["primaryProfession"] = name_df["primaryProfession"].fillna("").apply(lambda x: x.split(",") if x else [])
    name_df["knownForTitles"] = name_df["knownForTitles"].fillna("").apply(lambda x: x.split(",") if x else [])
    
    return name_df

def import_name_basics_data():
    """Import IMDb name.basics data into MongoDB."""
    print("Processing name.basics.tsv...")
    name_basics_df = process_name_basics()

    print("Clearing old data from MongoDB (name_basics)...")
    db[COLLECTION_NAME_BASICS].delete_many({})

    print("Inserting name.basics data into MongoDB...")
    name_basics_records = name_basics_df.to_dict("records")

    # Insert records in chunks to manage large data
    for i in range(0, len(name_basics_records), 10000):
        chunk = name_basics_records[i:i + 10000]
        db[COLLECTION_NAME_BASICS].insert_many(chunk)
        # print(f"Inserted {i + len(chunk)} records into '{COLLECTION_NAME_BASICS}'.")
    
    db[COLLECTION_NAME_BASICS].create_index([("nconst", 1)])
    print(f"Inserted {len(name_basics_records)} records into '{COLLECTION_NAME_BASICS}'.")
    print("Data import for name.basics completed.")

if __name__ == "__main__":
    try:
        import_name_basics_data()
    except Exception as e:
        print(f"Error during import: {e}")
