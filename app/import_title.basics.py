import os
import pandas as pd
from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
DATABASE_NAME = "imdb"
COLLECTION_TITLES = "titles"
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
    "basics": os.path.join(DATA_FOLDER, "title.basics.tsv"),
    "crew": os.path.join(DATA_FOLDER, "title.crew.tsv"),
    "ratings": os.path.join(DATA_FOLDER, "title.ratings.tsv"),
}

def load_data(file_path, **kwargs):
    """Load a TSV file into a Pandas DataFrame with low_memory set to False."""
    return pd.read_csv(file_path, sep="\t", na_values="\\N", low_memory=False, **kwargs)

def process_basics():
    """Processes the title.basics file."""
    basics_df = load_data(FILES["basics"], dtype={"tconst": str})
    
    # Ensure numeric fields are properly converted
    basics_df["startYear"] = pd.to_numeric(basics_df["startYear"], errors="coerce").fillna(0).astype(int)
    basics_df["endYear"] = pd.to_numeric(basics_df["endYear"], errors="coerce").fillna(0).astype(int)
    basics_df["runtimeMinutes"] = pd.to_numeric(basics_df["runtimeMinutes"], errors="coerce").fillna(0).astype(int)

    # Convert `isAdult` to boolean
    basics_df["isAdult"] = basics_df["isAdult"].astype(bool)

    # Split genres into lists
    basics_df["genres"] = basics_df["genres"].apply(
        lambda x: x.split(",") if isinstance(x, str) else []
    )
    return basics_df

def process_crew():
    """Processes the title.crew and maps nconst to primary names."""
    crew_df = load_data(FILES["crew"], dtype={"tconst": str})
    crew_df["directors"] = crew_df["directors"].apply(
        lambda x: x.split(",") if isinstance(x, str) else []
    )
    crew_df["writers"] = crew_df["writers"].apply(
        lambda x: x.split(",") if isinstance(x, str) else []
    )
    return crew_df

def process_ratings():
    """Processes the title.ratings file."""
    ratings_df = load_data(FILES["ratings"], dtype={"tconst": str})
    
    # Ensure numeric fields are properly converted
    ratings_df["averageRating"] = pd.to_numeric(ratings_df["averageRating"], errors="coerce").fillna(0).astype(float)
    ratings_df["numVotes"] = pd.to_numeric(ratings_df["numVotes"], errors="coerce").fillna(0).astype(int)
    
    return ratings_df

def import_basics_data():
    """Import IMDb basics, crew, and ratings data into MongoDB."""
    print("Processing title.basics.tsv...")
    basics_df = process_basics()

    print("Processing title.crew.tsv...")
    crew_df = process_crew()

    print("Processing title.ratings.tsv...")
    ratings_df = process_ratings()

    print("Merging DataFrames...")
    merged_df = basics_df.merge(
        crew_df, on="tconst", how="left"
    ).merge(
        ratings_df, on="tconst", how="left"
    )

    print("Clearing old data from MongoDB (titles)...")
    db[COLLECTION_TITLES].delete_many({})

    print("Inserting titles data into MongoDB...")
    titles_records = merged_df.to_dict("records")
    db[COLLECTION_TITLES].insert_many(titles_records)
    db[COLLECTION_TITLES].create_index("tconst", unique=True)
    print(f"Inserted {len(titles_records)} records into '{COLLECTION_TITLES}'.")

    print("Data import for basics completed.")

if __name__ == "__main__":
    try:
        import_basics_data()
    except Exception as e:
        print(f"Error during import: {e}")
