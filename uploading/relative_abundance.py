import pandas as pd
from .agoraLists import agora2Species, agora2Genera

def gettingCols(overalldic):
    dfdic = {}
    for key, value in sorted(overalldic.items()):
        col = []
        for k, v in sorted(value.items()):
            col.append(v)
        dfdic[key] = col
    return dfdic

def overall(df, rows):
    overalldic = {}
    for s, c in df.iterrows():
        tax = c[1]
        reads = c[2]
        sampledic = {}
        for i in range(len(tax)):
            sampledic[tax[i]] = reads[i]
        keys = list(sampledic.keys())
        for entry in rows:
            if entry not in keys:
                sampledic[entry] = 0
            else:
                pass
        overalldic[c[0]] = sampledic
    return overalldic

def relative_abundance(df, SorG):
    
    rows = list(df["Tax Name"].unique())  
    rows.sort()

    df = df[["Sample Name", "Tax Name", "Reads"]].groupby('Sample Name').agg(lambda x: list(x))
    df = pd.DataFrame(df)
    df = df.reset_index()
    
    columns = list(df["Sample Name"])
    
    overalldic = overall(df, rows)
    dfdic = gettingCols(overalldic)
    
    dataframe = pd.DataFrame.from_dict(dfdic)
    dataframe[SorG] = rows
    dataframe = dataframe.set_index(SorG)
    dataframe = dataframe.loc[:].div(dataframe.sum(axis = 0))

    if SorG == "Species":
        dataframe = dataframe[dataframe.index.isin(agora2Species)]
    else:
        dataframe = dataframe[dataframe.index.isin(agora2Genera)]

    dataframe.set_index(dataframe.index.str.replace(" ", "_", regex = True), inplace = True)
    dataframe.set_index('pan' + dataframe.index.astype(str), inplace = True)
    
    return dataframe 
