import os
import kaggle

def download_data():
    print("Downloading dataset from Kaggle...")
    kaggle.api.dataset_download_files(
        'souparnadas/hacker-benign-communications-en-ru', 
        path='./data', 
        unzip=True
    )
    print("Download complete.")

if __name__ == "__main__":
    download_data()