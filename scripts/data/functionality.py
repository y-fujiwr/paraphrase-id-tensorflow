import pandas as pd
from pathlib import Path
import configargparse

def check(file_path):
    df = pd.read_csv(Path("..", "..", "data", "external","bcb", "functionality_id.csv"), names=("id","func"))
    df2 = pd.read_csv(file_path, names=("id1","id2","rabel","prediction"))

    result = pd.merge(df2, df, left_on="id1", right_on="id", how="left").drop(columns="id").merge(df, left_on="id2", right_on="id", how="left", suffixes=["_1","_2"]).drop(columns="id")
    result.to_csv(Path(Path(file_path).parent, "result.csv"),index=False)

    fp = result[((result["rabel"] - 0.5 ) * (result["prediction"] - 0.5) < 0) & (result["rabel"] == 0)]
    fn = result[((result["rabel"] - 0.5 ) * (result["prediction"] - 0.5) < 0) & (result["rabel"] == 1)]
    fp.to_csv(Path(Path(file_path).parent, "fp_data.csv"),index=False)
    fp["id1"].append(fp["id2"]).value_counts().to_csv(Path(Path(file_path).parent, "fp_count.csv"))
    fn.to_csv(Path(Path(file_path).parent, "fn_data.csv"),index=False)
    fn["id1"].append(fn["id2"]).value_counts().to_csv(Path(Path(file_path).parent, "fn_count.csv"))
    fp["pair"] = "(" + fp["func_1"].astype(str) + "," + fp["func_2"].astype(str) + ")"
    fn["pair"] = "(" + fn["func_1"].astype(str) + "," + fn["func_2"].astype(str) + ")"
    fp_metrics = fp["pair"].value_counts()
    fn_metrics = fn["pair"].value_counts()
    fp_metrics.to_csv(Path(Path(file_path).parent, "fp_metrics.csv"))
    fn_metrics.to_csv(Path(Path(file_path).parent, "fn_metrics.csv"))

    metrics = pd.Series(index=['Precision','Recall','F-value'])
    metrics['Precision'] = len(result[((result["rabel"] - 0.5 ) * (result["prediction"] - 0.5) >= 0) & (result["rabel"] == 1)]) / len(result[(result["rabel"] - 0.5 ) * (result["prediction"] - 0.5) >= 0])
    metrics['Recall'] = len(result[((result["rabel"] - 0.5 ) * (result["prediction"] - 0.5) >= 0) & (result["rabel"] == 1)]) / len(result[result["rabel"] == 1])
    metrics['F-value'] = 2 * metrics['Precision'] * metrics['Recall'] / (metrics['Precision'] + metrics['Recall'])
    metrics.to_csv(Path(Path(file_path).parent, "metrics.csv"))

if __name__ == "__main__":
    argparser = configargparse.ArgumentParser()
    argparser.add_argument("file", type=str, help="path of the file to be analized about false positive.") 
    config = argparser.parse_args()
    check(config.file)