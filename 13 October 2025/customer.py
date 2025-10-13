import pandas as pd
df=pd.read_csv('customer.csv')
df['Age']=df['Age'].astype(int)
def categorize_age(age):
    if age<30:
        return "Young"
    elif 30<=age<50:
        return "Adult"
    else:
        return "Senior"
df['AgeGroup']=df['Age'].apply(categorize_age)
df_filtered=df[df['Age']>=20]
df_filtered.to_csv("filtered_customers.csv",index=False)
print("Pipeline executed")