# open readme.txt for instructions

import os

# adds colors to output
class bcolors:
    PURPLE = '\033[95m'
    VIOLET = '\033[35m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    YELLOW = '\033[33m'
    ORANGE = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDCOLOR = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

os.system('')

try:
    import requests
except ModuleNotFoundError:
    import sys
    print(f'{bcolors.RED}"Requests" Module Not Found{bcolors.ENDCOLOR}\n{bcolors.GREEN}Installing...{bcolors.ENDCOLOR}\n')
    os.system(f"{sys.executable} -m pip install requests")
    import requests
    print("\n\n")


try:
    f = open("Workshop Download List.txt", "r")
except FileNotFoundError:
    with open("Workshop Download List.txt", "a") as workshop_list:
        workshop_list.write("# Enter workshop links here shown below, seperate each link with a new line. # Comments out a line and will be ignored.")
        workshop_list.write("\n")
        workshop_list.write("# Copy all the links inside \"Workshop Link List.txt\" for a list of workshop maps. (Top 150, Most Popular, All Time)")

    print(f"{bcolors.RED}\"Workshop Download List.txt\" Doesn't Exist{bcolors.ENDCOLOR}")
    print(f"{bcolors.GREEN}Created One for You. Copy Paste Steam Workshop Link, Separate Each Link With a New Line.{bcolors.ENDCOLOR}")
    input("\n\nPress Enter to Continue...")
    exit()

import shutil
import concurrent.futures


def get_workshop_download(id): # converted from curl to python requests. https://curlconverter.com/#python
    headers = {
        'Connection': 'keep-alive',
        'Origin': 'http://steamworkshop.download',
        'Referer': f'http://steamworkshop.download/download/view/{id}',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'item': f'{id}',
        'app': '824270',
    }

    response = requests.post('http://steamworkshop.download/online/steamonline.php', headers=headers, data=data, verify=False)
    try:
        download_list.append(response.text.split("'")[1]) # there will be error in some cases
        print(f"{bcolors.GREEN}Getting Download Link For Workshop ID \"{id}\" → Successful{bcolors.ENDCOLOR}")
    except IndexError:
        print(f"{bcolors.RED}Something Went Wrong With Workshop ID \"{id}\" → SKIPPING{bcolors.ENDCOLOR}")


def download_workshop(url):
    response = requests.get(url, verify=False)
    open(url.split("/")[-1], "wb").write(response.content)
    zip_file = f"{os.path.join(script_dir, url.split('/')[-1])}"
    print(f"{bcolors.BLUE}{url.split('/')[-1].split('.')[0]}{bcolors.ORANGE} → {bcolors.PURPLE}{zip_file}{bcolors.ENDCOLOR}")


# gets the folder the script is in
script_dir = os.path.dirname(os.path.realpath(__file__))

id_list = []
download_list = []

print(f"\n\n{bcolors.BOLD}{bcolors.YELLOW}Extracting Workshop ID{bcolors.ENDCOLOR}\n")
with open("Workshop Download List.txt") as f: # read text file for workshop links
    url_list = f.read().splitlines()
    for lines in url_list: # read file line by line
        if lines == "":
            continue
        if lines[0] == "#":
            continue
        workshop_id = lines.split("=")[1].split("&")[0]
        id_list.append(workshop_id) # get workshop id from lines
        print(f"{lines}{bcolors.ORANGE} → {bcolors.BLUE}{workshop_id}{bcolors.ENDCOLOR}")


print(f"\n\n{bcolors.BOLD}{bcolors.YELLOW}Getting Workshop Download Link{bcolors.ENDCOLOR}\n")
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(get_workshop_download, id_list)


print(f"\n\n{bcolors.BOLD}{bcolors.YELLOW}Downloading Workshop Maps{bcolors.ENDCOLOR}\n")
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(download_workshop, download_list)


print(f"\n\n{bcolors.BOLD}{bcolors.YELLOW}Unzipping Zip Files{bcolors.ENDCOLOR}\n")
for file in os.scandir(script_dir):
    if os.path.splitext(file)[-1].lower() == ".zip":
        zip_file = os.path.join(script_dir, file) # gets absolute zip file path
        target_file_path = os.path.splitext(file)[0] # gets the output directory path
        shutil.unpack_archive(file, script_dir, "zip")
        map_file_path = os.path.join(target_file_path, os.listdir(target_file_path)[0]) # gets unzipped map file path
        print(f"{bcolors.PURPLE}{zip_file}{bcolors.ORANGE} → {bcolors.BLUE}{map_file_path}{bcolors.ENDCOLOR}")

print(f"\n\n{bcolors.BOLD}{bcolors.YELLOW}Copying Map Files{bcolors.ENDCOLOR}\n")
for file in os.scandir(script_dir):
    if file.is_dir():
        map_file = os.path.join(file, os.listdir(file)[0]) # get absolute file path for files in those folders
        target_file_path = os.path.join(os.path.dirname(script_dir), os.listdir(file)[0]) # gets the parent directory of the script file
        shutil.copyfile(map_file, target_file_path)
        print(f"{bcolors.BLUE}{map_file}{bcolors.ORANGE} → {bcolors.GREEN}{target_file_path}{bcolors.ENDCOLOR}")

input("\n\nPress Enter to Continue...")