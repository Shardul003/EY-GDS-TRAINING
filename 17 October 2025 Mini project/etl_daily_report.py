from datetime import datetime
import pandas as pd

def run_etl():
    # Load your enrollment data
    df = pd.read_csv("enrollments.csv")

    # Add calculated fields
    df['CompletionStatus'] = df['Progress'].apply(lambda x: 'Completed' if x >= 80 else 'Incomplete')
    df['EnrollMonth'] = pd.to_datetime(df['EnrollDate']).dt.to_period('M').astype(str)

    # Save with today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"daily_enrollment_report_{today}.csv"
    df.to_csv(filename, index=False)
    print(f"Report generated: {filename}")

if __name__ == "__main__":
    run_etl()