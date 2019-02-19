from pathlib import Path
import sys
from tqdm import tqdm

method_name = ["println\n","write\n","close\n","append\n","add\n","getChannel\n","read\n","printStackTrace\n","File\n","getName\n",
"getInstance\n","put\n","URL\n","getMessage\n","openConnection\n","digest\n","assertEquals\n","debug\n","substring\n"]

def extract(path):
    target = open(str(path), "r").readlines()
    output = open(str(path.with_suffix("")), "w")
    for i in range(len(target)):
        string = target[i].split("\t")[2]
        if "&" in string:
            string = string.split("&")[0] + "\n"
        if "java.util" in string:
            string = "id|" + string.split(".")[-1]
        if "id" in string and "c_func" in target[i+1].split("\t")[2].split("|")[0] and string.split("|")[1] in method_name:
            output.write(string)
        elif "|" not in string:
            output.write(string)
        else:
            output.write(string.split("|")[0] + "\n")

if __name__ == '__main__':
    for target in tqdm(Path(sys.argv[1]).glob("**/*.orig")):
        extract(target)
