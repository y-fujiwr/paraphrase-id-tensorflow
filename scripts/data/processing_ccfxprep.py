from pathlib import Path
import sys,os
from tqdm import tqdm
import pandas as pd

method_name = ["println\n","write\n","close\n","append\n","add\n","getChannel\n","read\n","printStackTrace\n","File\n","getName\n",
"getInstance\n","put\n","URL\n","getMessage\n","openConnection\n","digest\n","assertEquals\n","debug\n","substring\n"]
c2v_data = open("all-tokens-in-clones.txt", "w")

def preprocessing(path):
    output = open(str(path.with_suffix("")), "w")
    output_tokenlist(path,output)

def extract(path):
    output_tokenlist(path,c2v_data)

def output_tokenlist(path,openedfile_obj):
    target = open(str(path), "r").readlines()
    for i in range(len(target)):
        string = target[i].split("\t")[2]
        if "&" in string:
            string = string.split("&")[0] + "\n"
        if "java.util" in string:
            string = "id|" + string.split(".")[-1]
        """
        if "id" in string and "c_func" in target[i+1].split("\t")[2].split("|")[0] and string.split("|")[1] in method_name:
            openedfile_obj.write(string)
        
        el
        """
        if "|" not in string:
            openedfile_obj.write(string)
        else:
            openedfile_obj.write(string.split("|")[0] + "\n")


if __name__ == '__main__':
    df = pd.read_csv(os.path.join("..","..","data","processed","bcb","clones.csv"), names=("id1","id2","line_sim","token_sim"))
    u = df["id1"].append(df["id2"]).unique()
    for x in u:
        extract(Path(sys.argv[1] + str(x) + ".java.java.2_0_0_0.default.ccfxprep.orig"))
    for target in tqdm(Path(sys.argv[1]).glob("**/*.orig")):
        preprocessing(target)
