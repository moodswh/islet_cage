
#!/usr/bin/env python
import argparse
import pandas
import math
import glob
import os
import seaborn as sns
import numpy as np
import sys

def log_with_nan(x, y):
    if np.isinf(x):
        return float('nan')
    try:
        return math.log(x, y)
    except ValueError:         ## Places with log(0)
        return float('nan')

def makeResultDf(all_files, string, split, infosplit):
    dlist = []
    for f in all_files:
        d = pandas.read_csv(f, comment="#", sep="\t", usecols=['observed','expected', 'fold', 'l2fold', 'stddev', 'qvalue', 'pvalue'])
        d.loc[:,'feature'] = os.path.basename(f).replace(string, "")
        dlist.append(d)
        
    df  = pandas.concat(dlist, ignore_index=True)
    print(df.head())
    if split is not None:
        df[infosplit] = pandas.DataFrame([x for x in df.loc[:,'feature'].str.split(split)])
        df.drop('feature', axis=1, inplace=True)
   
    return df

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make dataframe from GAT results.', usage='python ~arushiv/toolScripts/analyze_GATResults.py -s *.out -d outputDir/ ')
    parser.add_argument('-s','--inputString', type=str, default='*.txt', help="""Files which should be parsed. (default: *.txt)""")
    parser.add_argument('-d','--resultDir', type=str, default='.', help="""Directory where result files reside. (default: current Directory)""")
    parser.add_argument('outputfile', type=str, help="""Output file name.""")
    parser.add_argument('--split', help="""Split the feature name by this delimiter. If not provided, feature column is as is.""")
    parser.add_argument('-is', '--infosplit', nargs='+', help="""Supply header names into which the feature column should be split into (space separated). Default = ['motif','cell1','cell2']""")
    args = parser.parse_args()
    inputString = args.inputString
    resultDir = args.resultDir

    if args.split is not None and args.infosplit is None:
        print("Provide column names after splitting")
        sys.exit(1)
    elif args.split is None and args.infosplit is not None:
        print("Provide the delimiter to split on")
        sys.exit(1)
    
    all_files = glob.glob(os.path.join(resultDir, inputString))     

    df = makeResultDf(all_files, inputString.replace("*",""), args.split, args.infosplit)
    
    df.to_csv(args.outputfile, sep="\t", index=False, na_rep="NA")

