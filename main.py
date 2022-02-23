import os
import sys
import shutil
import requests
# import webbrowser

import warnings
warnings.filterwarnings("ignore")


READ_PATH = "Files"
SAVE_PATH = "Processed"
REQUEST_URL = "https://api.deepai.org/api/colorizer"


def main():
    
    args: tuple = ("--file", "-f")
    
    filename: str = None

    if args[0] in sys.argv: filename = sys.argv[sys.argv.index(args[0]) + 1]
    if args[1] in sys.argv: filename = sys.argv[sys.argv.index(args[1]) + 1]


    assert filename is not None, "No Image Specified"
    assert filename in os.listdir(READ_PATH), "Image Not Found"
    
    response = requests.post(
        url=REQUEST_URL,
        files={
            "image" : open(os.path.join(READ_PATH, filename), "rb"),
        },
        headers={
            "api-key" : os.environ["DEEPAI_KEY"],
        }
    )

    # webbrowser.open(response.json()["output_url"])

    download = requests.get(response.json()["output_url"], stream=True)
    if download.status_code == 200:
        with open(os.path.join(SAVE_PATH, filename[:-4] + " - Colorized" + filename[-4:]), "wb") as f:
            shutil.copyfileobj(download.raw, f)
    else:
        print("Image couldn't be retrieved")


if __name__ == "__main__":
    sys.exit(main() or 0)
