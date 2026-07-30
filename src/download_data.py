import urllib.request
from pathlib import Path

BASE_URL = "https://engineering.case.edu/sites/default/files/{}.mat"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

FILES = {
    "Normal_1hp": 98,
    "IR007_1hp": 106,
    "IR014_1hp": 170,
    "IR021_1hp": 210,
    "OR007_1hp": 131,
    "OR014_1hp": 198,
    "OR021_1hp": 235,
    "B007_1hp": 119,
    "B014_1hp": 186,
    "B021_1hp": 223,
}

def download_all():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, file_id in FILES.items():
        url = BASE_URL.format(file_id)
        out_path = OUTPUT_DIR / f"{name}.mat"
        if out_path.exists():
            print(f"Skipping {name}, already exists.")
            continue
        print(f"Downloading {name} from {url} ...")
        urllib.request.urlretrieve(url, out_path)
    print("Done.")

if __name__ == "__main__":
    download_all()