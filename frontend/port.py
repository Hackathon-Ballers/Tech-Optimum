import shutil
from pathlib import Path

def main():
    TEMPLATE_DIR = 'templates/'
    CSS_DIR = 'static/styles/'
    JS_DIR = 'static/js/'

    IGNORE = ['lib/']

    print("The CSS dir is:", CSS_DIR)
    print("The JS dir is:", JS_DIR)
    print("The HTML dir is:", TEMPLATE_DIR)
    print("you are ignoring:", IGNORE)
    if "y" not in input("Is this correct? ").lower(): exit()

    css_files = getFiles(".css", IGNORE)
    js_files = getFiles(".js", IGNORE)
    html_files = getFiles('.html', IGNORE)

    moveFiles(css_files, CSS_DIR)
    moveFiles(js_files, JS_DIR)
    moveFiles(html_files, TEMPLATE_DIR)


def contains(target, lst):
    for item in lst:
        if item not in target: continue
        return True
    return False

fileName = lambda x: str(x).split("/")[-1]

def getFiles(fileType, IGNORE):
    full_list = list(Path(".").rglob(f"*{fileType}"))
    lst = []
    for file_dir in full_list:
        if contains(str(file_dir), IGNORE): continue
        lst.append(str(file_dir))
    return lst

def moveFiles(files, dir_prefix):
    for file in files:
        if file == dir_prefix + fileName(file): continue
        print(f'[*] moving {file} -> {dir_prefix + fileName(file)}')
        try:
            shutil.copy(str(file), dir_prefix + fileName(file))
        except IsADirectoryError:
            print("Ignoring this since it's a directory")

if __name__ == "__main__":
    main()