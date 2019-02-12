from pathlib import Path
import sys
from tqdm import tqdm

def extract(path):
    target = open(path, "r").readlines()
    output = open(path.with_suffix(""), "w")
    for i in range(len(target)):
        string = target[i].split("\t")[2]
        if "&" in string:
            string = string.split("&")[0] + "\n"
        if "java.util" in string:
            string = "id|" + string.split(".")[-1]
        if "id" in string and "c_func" in target[i+1].split("\t")[2].split("|")[0]:
            output.write(string)
        elif "|" not in string:
            output.write(string)
        else:
            output.write(string.split("|")[0] + "\n")

if __name__ == '__main__':
    for target in tqdm(Path(sys.argv[1]).glob("**/*.orig")):
        extract(target)