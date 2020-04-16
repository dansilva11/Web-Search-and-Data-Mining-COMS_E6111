import pandas as pd
from itertools import combinations
import sys
from operator import itemgetter

def run_association(data_path, min_sup,min_conf):
    df = pd.read_csv(data_path)
    L ,L_1 = run_apriori(df)

    text = open("example_run.txt",'w')
    print("==Frequent itemsets (min_sup="+str(min_sup*100)+")\n")
    text.write("==Frequent itemsets (min_sup=" + str(min_sup * 100) + ")\n")

    L= {k: v for k, v in sorted(L.items(), key=lambda item: item[1], reverse=True)}
    for k,v in L.items():
        print(str(list(k)).replace("'","")+", Supp: "+str(round(v*100,4))+"%")
        text.write(str(list(k)).replace("'", "") + ", Supp: " + str(round(v * 100, 4)) + "%\n")
    sup_lookup = {**L , **L_1}

    ass_list = []
    for itemset in L.keys():
        for RHS in itemset:
            LHS = itemset-{RHS}

            conf = sup_lookup[itemset]/sup_lookup[LHS]


            if conf > min_conf:
                ass_list.append([LHS,RHS,itemset,conf])

    ass_list = sorted(ass_list, key=itemgetter(3), reverse=True)
    print("\n")
    text.write("\n")
    print("==High-confidence association rules (min_conf=" + str(min_conf * 100) + ")")
    text.write("==High-confidence association rules (min_conf=" + str(min_conf * 100) + ")\n")
    for ass in ass_list:
        LHS = ass[0]
        RHS = ass[1]
        itemset = ass[2]
        conf = ass[3]
        print(str(list(LHS)).replace("'","")+"=>["+str(RHS)+"] (Conf: "+
                          str(round(conf*100,4))+"%, Supp: "+ str(round(sup_lookup[itemset]*100,4)))
        text.write(str(list(LHS)).replace("'","")+"=>["+str(RHS)+"] (Conf: "+
                          str(round(conf*100,4))+"%, Supp: "+ str(round(sup_lookup[itemset]*100,4))+ "\n")
    text.close()


def run_apriori(df):
    L_k = {'initialize'}
    L = {}
    basket_count = len(df)
    k=0
    while len(L_k)>0:
        k+=1
        if k==1:
            L_k = {}
            L_1 = {}
            for col in df.columns:
                if col in ['month_year','zip']:
                    continue
                sup = df[col].count()/basket_count
                if sup > min_sup:
                    L_k[frozenset({col})]=sup
                    L_1[frozenset({col})]=sup
                    # L[frozenset({col})] = sup
        else:
            C_k = apriori_gen(L_k)
            L_k = {}
            for c in C_k:
                sup = (df[list(c)].sum(axis=1)==len(c)).astype(int).sum(axis=0)/basket_count
                if sup > min_sup:
                    L_k[c] = sup
                    L[c] = sup

    return L, L_1

def apriori_gen(L_k):
    C_k=set()
    for itemset1,itemset2 in combinations(L_k.keys(),2):
        if len(itemset1-itemset2)==1:
            c = itemset1.union(itemset2)
            prune=False
            for subset in combinations(c, len(itemset1)):
                if frozenset(subset) not in L_k.keys():
                    prune=True
                    break
            if prune==False:
                C_k.add(c)
    return C_k


if __name__ == "__main__":
    # data_path = sys.argv[1]
    # min_sup = sys.argv[2]
    # min_conf = sys.argv[3]

    data_path = "City_Events_by_Month_and_Zip.csv"
    min_sup = 0.05
    min_conf = 0.75

    run_association(data_path, min_sup, min_conf)
