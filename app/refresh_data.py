import os
import requests
import gzip
import shutil

# IMDb Dataset URLs
IMDB_URLS = {
    "title.basics": "https://datasets.imdbws.com/title.basics.tsv.gz",
    "title.akas": "https://datasets.imdbws.com/title.akas.tsv.gz",
    "title.crew": "https://datasets.imdbws.com/title.crew.tsv.gz",
    "title.ratings": "https://datasets.imdbws.com/title.ratings.tsv.gz",
    "title.principals": "https://datasets.imdbws.com/title.principals.tsv.gz",
    "name.basics": "https://datasets.imdbws.com/name.basics.tsv.gz"
}

# Data folder
DATA_FOLDER = "../data"

# Ensure the data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

def download_and_decompress(file_name, url):
    gz_file_path = os.path.join(DATA_FOLDER, file_name + ".tsv.gz")
    tsv_file_path = os.path.join(DATA_FOLDER, file_name + ".tsv")

    try:
        # Download the file
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise error for HTTP issues
        
        # Save the .gz file
        with open(gz_file_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {file_name}.gz")

        # Decompress the .gz file
        print(f"Decompressing {file_name}.gz...")
        with gzip.open(gz_file_path, "rb") as gz_file:
            with open(tsv_file_path, "wb") as tsv_file:
                shutil.copyfileobj(gz_file, tsv_file)
        print(f"Decompressed {file_name}.tsv")

        # Remove the .gz file after decompression
        os.remove(gz_file_path)
        print(f"Removed {file_name}.gz")
    except Exception as e:
        print(f"Error downloading or decompressing {file_name}: {e}")

def refresh_imdb_data():
    for file_name, url in IMDB_URLS.items():
        download_and_decompress(file_name, url)
    print("Data refresh complete.")

if __name__ == "__main__":
    refresh_imdb_data()
