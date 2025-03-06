import pandas as pd
import numpy as np

class QuanQual:
    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for ColunmName in dataset.columns:
            if dataset[ColunmName].dtypes=="object":
                Qual.append(ColunmName)
            else:
                Quan.append(ColunmName)
        print("Quan=", Quan)
        print("Qual=", Qual)
        return Quan, Qual

    def Univariate_Table(Quan,dataset):
        Table=pd.DataFrame(index=['Mean', 'Median', 'Mode', 'Q1:25%','Q2:50%', 'Q3:75%', "99%", 'Q4:100%', "Min", "Max", 'IQR', '1.5rule', 'Lesser', 'Greater' ],columns=Quan)
        for columnname in Quan:
            Table[columnname]['Mean']=dataset[columnname].mean()
            Table[columnname]['Median']=dataset[columnname].median()
            Table[columnname]['Mode']=dataset[columnname].mode()[0]
            Table[columnname]['Q1:25%']=dataset.describe()[columnname]['25%']
            Table[columnname]['Q2:50%']=dataset.describe()[columnname]['50%']
            Table[columnname]['Q3:75%']=dataset.describe()[columnname]['75%']
            Table[columnname]['99%']=np.percentile(dataset[columnname],99)    
            Table[columnname]['Q4:100%']=dataset.describe()[columnname]['max']
            Table[columnname]['Min']=dataset[columnname].min()
            Table[columnname]['Max']=dataset[columnname].max()
            Table[columnname]['IQR']=Table[columnname]['Q3:75%']-Table[columnname]['Q1:25%']
            Table[columnname]['1.5rule']=1.5* Table[columnname]['IQR']
            Table[columnname]['Lesser']= Table[columnname]['Q1:25%']-Table[columnname]['1.5rule']
            Table[columnname]['Greater']= Table[columnname]['Q3:75%']+Table[columnname]['1.5rule']
            Table[columnname]['Skew']=dataset[columnname].skew()
            Table[columnname]['Kurtosis']=dataset[columnname].kurtosis()
        return Table

    def outlier(Table, Quan):
        lesser=[]
        greater=[]
        for columnname in Quan:
            if Table[columnname]["Lesser"]>Table[columnname]["Min"]:
                lesser.append(columnname)
            if Table[columnname]["Greater"]<Table[columnname]["Max"]:
                greater.append(columnname)
        print("lesser=", lesser)
        print("greater=", greater)
        return lesser, greater

    def outlier_replace(lesser, greater, Table, dataset):
        for columnname in lesser:
            dataset[columnname][dataset[columnname]<Table[columnname]["Lesser"]]=Table[columnname]["Lesser"]
        for columnname in greater:
            dataset[columnname][dataset[columnname]>Table[columnname]["Greater"]]=Table[columnname]["Greater"]
        return lesser , greater

    def freqTable(dataset, columnname):
        freqTable=pd.DataFrame(columns=["Unique_Values", "Frequency", "Relative Freqn", "Cumsum"])
        freqTable["Unique_Values"]=dataset[columnname].value_counts().index
        freqTable["Frequency"]=dataset[columnname].value_counts().values
        freqTable["Relative Freqn"]=(freqTable["Frequency"]/103)
        freqTable["Cumsum"]= freqTable["Relative Freqn"].cumsum()
        return freqTable
            