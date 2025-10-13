import pandas as pd
df=pd.read_csv("students.csv")
df.dropna(inplace=True)
df["Marks"]=df["Marks"].astype(int)
df["Result"]=df["Marks"].apply(lambda x: "Pass" if x>=50 else "Fail")
df.to_csv(path_or_buf="cleaned_students.csv",index=False)
print("DATA PIPELINE COMPLETED. CLEANED DATA SAVED TO cleaned_students.csv")