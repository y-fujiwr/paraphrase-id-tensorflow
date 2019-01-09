import pandas as pd
from pathlib import Path
import configargparse
from tqdm import tqdm
import re
from random import randrange

func = pd.read_csv(Path("..", "..", "data", "external","bcb", "functionality_id.csv"),names=("id","func"))

def get_functionality(id):
    return func.query('id=={}'.format(id)).func.reset_index(drop=True)[0]

if __name__ == "__main__":
    argparser = configargparse.ArgumentParser()
    argparser.add_argument("file", type=str, help="path of the file to be used for training.") 
    config = argparser.parse_args()
    df = pd.read_csv(config.file,header=None)
    num_posi = len(df[df[2] == 1])
    used_func = df[1].append(df[0]).drop_duplicates().reset_index(drop=True)

    ncd = pd.DataFrame(columns=["id1","id2","label"]) #NotCloneData

    while len(ncd) < num_posi:
        x = randrange(len(used_func))
        y = randrange(len(used_func))
        funcx = get_functionality(used_func[x])
        funcy = get_functionality(used_func[y])
        if funcx != funcy and "_" not in funcx and "_" not in funcy:
            ncd = ncd.append(pd.DataFrame([[used_func[x],used_func[y],0]],columns=["id1","id2","label"]))

    ncd.to_csv(Path(Path(config.file).parent, str(Path(config.file).name) + "_nd.csv"),header=False,index=False)

    """
    for x in tqdm(range(len(used_func))):
        for y in tqdm(range(x+1,len(used_func))):
            funcx = get_functionality(used_func[x])
            funcy = get_functionality(used_func[y])
            if funcx != funcy and "_" not in funcx and "_" not in funcy:
                ncd = ncd.append(pd.DataFrame([[used_func[x],used_func[y],0]],columns=["id1","id2","label"]))

    ncd.to_csv(Path(Path(config.file).parent, str(Path(config.file).name) + "_nd.csv"),header=False,index=False)
    """