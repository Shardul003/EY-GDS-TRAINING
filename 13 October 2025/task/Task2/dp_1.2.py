import pandas as pd
from datetime import datetime

def run_pipeline():
    df=pd.read_csv("inventory.csv")
    df["TotalValue"] = df["Quantity"] * df["PricePerUnit"]

    df["RestockNeeded"]=df.apply(
        lambda row: "Yes" if row["Quantity"]<row["ReorderLevel"] else "No",
        axis=1
    )
    df.to_csv("restock.csv",index=False)
    print(f"Inventory Pipeline completed at {datetime.now()}")
    print("Output saved to restock.csv")


if __name__ == "__main__":
    run_pipeline()