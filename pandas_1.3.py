import numpy as np
import pandas as pd
data=data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram","soham"],
    "Age": [21, 22, 20, 23, 21,25],
    "Course": ["AI", "ML", "Data Science", "AI", "ML","DSBS"],
    "Marks": [85, 90, 78, 88, 95,np.nan]
}
df=pd.DataFrame(data)
print(df)
df.info()
df.describe()
print(df.iloc[3])
print(df["Marks"])