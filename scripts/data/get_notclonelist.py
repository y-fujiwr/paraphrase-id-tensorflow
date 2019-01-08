import pandas as pd
from pathlib import Path
import configargparse
from tqdm import tqdm

if __name__ == "__main__":
    df = pd.read_csv(Path("..", "..", "data", "external","bcb", "functionality_id_test.csv"), names=("id","func"))
    df_new = pd.DataFrame(columns=["id1","id2"])
    for x in tqdm(range(len(df.id))):
        for y in tqdm(range(x+1,len(df.id))):
            df_new = df_new.append(pd.DataFrame([[df.id[x],df.id[y]]],columns=["id1","id2"]))
    
    clones = pd.read_csv(Path("..","..","data","processed","bcb","clones.csv"),names=("id1","id2","sim1","sim2"))
    clones2 = pd.read_csv(Path("..","..","data","processed","bcb","clones.csv"),names=("id2","id1","sim1","sim2"))
    clones_id = clones.loc[:,["id1","id2"]]
    clones_id2 = clones2.loc[:,["id1","id2"]]
    result = df_new.append(clones_id).append(clones_id).append(clones_id2).append(clones_id2).drop_duplicates(keep=False)
    result.to_csv("notclonelist.csv",index=False)