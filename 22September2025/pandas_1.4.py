import numpy as np
import pandas as pd
data=data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram","soham"],
    "Age": [21, 22, 20, 23, 21,25],
    "Course": ["AI", "ML", "Data Science", "AI", "ML","DSBS"],
    "Marks": [85, 90, 78, 88, 95,np.nan]
}
df=pd.DataFrame(data)
print(df.iloc[3])
print(df['Name'])

print(df.loc[3,"Age"])
print (df['Marks']>80)
print ("CHECKING MARKS OF NEHA if greater",df['Marks'][2]>79)

high_score=df[df["Marks"]>90]
print(high_score)


#UPDATING COLUMNS
df.loc[df["Name"]=="Neha","Marks"]=92
print(df)

