from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:The%40lphs987@localhost/COURSES_MANAGEMENT"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        for row in result:
            print("Test query result:", row)
except Exception as e:
    print("❌ Database connection failed!")
    print("Error:", e)