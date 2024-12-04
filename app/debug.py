from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb://mongodb:27017"
DATABASE_NAME = "imdb"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

def analyze_collection_schema(collection_name):
    collection = db[collection_name]
    sample_record = collection.find_one()
    if not sample_record:
        print(f"[ERROR] {collection_name}: Collection is empty!")
        return
    print(f"Fields and types in {collection_name}:")
    for field, value in sample_record.items():
        print(f"  - {field}: {type(value).__name__}")

def main():
    print("Analyzing collection schemas...")

    # Collections to analyze
    collections = ["name_basics", "akas", "titles"]

    for collection_name in collections:
        print(f"\nAnalyzing {collection_name} collection...")
        analyze_collection_schema(collection_name)

if __name__ == "__main__":
    main()