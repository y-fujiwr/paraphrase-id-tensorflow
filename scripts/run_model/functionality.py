import pandas as pd
from pathlib import Path
import configargparse

def main():

    argparser = configargparse.ArgumentParser()
    argparser.add_argument("file", type=str, help="path of the file to be analized about false positive.") 
    config = argparser.parse_args()

    df = pd.read_csv(Path("..", "..", "data", "external","bcb", "functionality_id.csv"), names=("id","func"))
    df2 = pd.read_csv(config.file, names=("id1","id2","rabel","prediction"))

    result = pd.merge(df2, df, left_on="id1", right_on="id", how="left").drop(columns="id").merge(df, left_on="id2", right_on="id", how="left", suffixes=["_1","_2"]).drop(columns="id")

    fp = result[result["rabel"] != result["prediction"]]
    fp["pair"] = "(" + fp["func_1"].astype(str) + "," + fp["func_2"].astype(str) + ")"
    fp_data = fp["pair"].value_counts()
    result.to_csv(Path("..", "..", "data", "external","bcb", "result.csv"),index=False)
    print(fp_data)
    fp_data.to_csv(Path("..", "..", "data", "external","bcb", "fp_data.csv"))

if __name__ == "__main__":
    main()