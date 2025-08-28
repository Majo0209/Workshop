import pandas as pd          # Main library for data manipulation and analysis
import mysql.connector       # To connect Python with MySQL and execute queries
import datetime              # For handling dates, creating timestamps, and default dates

# ===============================
# 1. MySQL Connection
# ===============================
def get_connection():
    """
    Returns a MySQL connection object to the 'hires_model' database.
    Used anywhere in the ETL where database interaction is needed.
    """
    return mysql.connector.connect(
        host="localhost",       # MySQL server address
        user="root",            # User with read/write permissions
        password="root",        # User password
        database="hires_model"  # Database containing our Data Warehouse
    )

# ===============================
# 2. DATA EXTRACTION
# ===============================
def extract_candidates(path: str) -> pd.DataFrame:
    """
    Extracts candidate data from a CSV file.
    Args:
        path (str): Path to the CSV file
    Returns:
        pd.DataFrame: DataFrame with the original CSV data
    """
    # Read CSV using pandas; separator is ';' because the original file uses this format
    df = pd.read_csv(path, sep=";")  
    print("✅ Data extracted from CSV")
    return df

# ===============================
# 3. DATA TRANSFORMATION
# ===============================
def transform_candidates(df: pd.DataFrame) -> dict:
    """
    Applies transformations to the original dataset and generates dimension tables
    and the fact table.
    Args:
        df (pd.DataFrame): Original DataFrame extracted from CSV
    Returns:
        dict: Dictionary containing tables dim_date, dim_country, dim_seniority,
              dim_technology, dim_candidate, and fact_data
    """

    # ----------------------------
    # Rename columns to standard snake_case format
    # Helps maintain consistency across the database and the pipeline
    # ----------------------------
    df = df.rename(columns={
        "First Name": "first_name",
        "Last Name": "last_name",
        "Email": "email",
        "Application Date": "application_date",
        "Country": "country",
        "YOE": "yoe",
        "Seniority": "seniority",
        "Technology": "technology",
        "Code Challenge Score": "code_score",
        "Technical Interview Score": "interview_score"
    })

    # ----------------------------
    # Type transformations
    # ----------------------------
    # Convert application_date to datetime type, ignoring errors
    df["application_date"] = pd.to_datetime(df["application_date"], errors="coerce")  

    # Normalize country names (capitalize)
    df["country"] = df["country"].astype(str).str.title()  

    # Normalize seniority levels (capitalize)
    df["seniority"] = df["seniority"].astype(str).str.capitalize()  

    # Create 'hired' column: 1 if both scores >= 7, else 0
    # Determines if a candidate was hired based on our rules
    df["hired"] = ((df["code_score"] >= 7) & (df["interview_score"] >= 7)).astype(int)

    # ----------------------------
    # CREATE DIMENSION TABLES
    # ----------------------------

    # dim_date → unique dates only, extract year, month, day
    dim_date = df[["application_date"]].drop_duplicates().reset_index(drop=True)
    dim_date["year"] = dim_date["application_date"].dt.year
    dim_date["month"] = dim_date["application_date"].dt.month
    dim_date["day"] = dim_date["application_date"].dt.day

    # dim_country → unique countries
    dim_country = df[["country"]].drop_duplicates().reset_index(drop=True)

    # dim_seniority → unique seniority levels
    dim_seniority = df[["seniority"]].drop_duplicates().reset_index(drop=True)

    # dim_technology → unique technologies
    dim_technology = df[["technology"]].drop_duplicates().reset_index(drop=True)

    # dim_candidate → unique candidate information
    dim_candidate = df[["first_name", "last_name", "email", "yoe"]].drop_duplicates().reset_index(drop=True)

    # ----------------------------
    # Return dictionary with all tables
    # ----------------------------
    return {
        "dim_date": dim_date,
        "dim_country": dim_country,
        "dim_seniority": dim_seniority,
        "dim_technology": dim_technology,
        "dim_candidate": dim_candidate,
        "fact_data": df  # Fact table
    }

# ===============================
# 4. DATA LOAD
# ===============================
def load_to_dw(tables: dict):
    """
    Inserts dimension and fact tables into the MySQL database.
    Args:
        tables (dict): Dictionary containing all tables generated in the transformation phase
    """
    # Connect to the database
    conn = get_connection()       
    cursor = conn.cursor()        

    # ----------------------------
    # INSERT DIMENSIONS
    # ----------------------------
    # INSERT IGNORE avoids errors due to duplicates
    for _, row in tables["dim_date"].iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_date (application_date, year, month, day)
            VALUES (%s, %s, %s, %s)
        """, (row.application_date.date(), row.year, row.month, row.day))

    for _, row in tables["dim_country"].iterrows():
        cursor.execute("INSERT IGNORE INTO dim_country (country_name) VALUES (%s)", (row.country,))

    for _, row in tables["dim_seniority"].iterrows():
        cursor.execute("INSERT IGNORE INTO dim_seniority (seniority_level) VALUES (%s)", (row.seniority,))

    for _, row in tables["dim_technology"].iterrows():
        cursor.execute("INSERT IGNORE INTO dim_technology (technology_name) VALUES (%s)", (row.technology,))

    for _, row in tables["dim_candidate"].iterrows():
        cursor.execute("""
            INSERT IGNORE INTO dim_candidate (first_name, last_name, email, years_of_experience)
            VALUES (%s, %s, %s, %s)
        """, (row.first_name, row.last_name, row.email, row.yoe))

    # Commit dimension inserts
    conn.commit()

    # ----------------------------
    # MAP DIMENSION IDS IN MEMORY
    # ----------------------------
    # Allows linking dimensions to fact table without SQL joins
    cursor.execute("SELECT date_id, application_date FROM dim_date")
    date_map = {d: i for i, d in cursor.fetchall()}

    cursor.execute("SELECT country_id, country_name FROM dim_country")
    country_map = {n: i for i, n in cursor.fetchall()}

    cursor.execute("SELECT seniority_id, seniority_level FROM dim_seniority")
    seniority_map = {n: i for i, n in cursor.fetchall()}

    cursor.execute("SELECT technology_id, technology_name FROM dim_technology")
    tech_map = {n: i for i, n in cursor.fetchall()}

    cursor.execute("SELECT candidate_id, email FROM dim_candidate")
    candidate_map = {e: i for i, e in cursor.fetchall()}

    # ----------------------------
    # INSERT FACT TABLE (fact_hires)
    # ----------------------------
    for _, row in tables["fact_data"].iterrows():
        candidate_id = candidate_map.get(row.email)
        date_id = date_map.get(row.application_date.date())
        country_id = country_map.get(row.country)
        seniority_id = seniority_map.get(row.seniority)
        technology_id = tech_map.get(row.technology)

        cursor.execute("""
            INSERT INTO fact_hires (
                candidate_id, date_id, country_id, technology_id, seniority_id,
                hired, code_challenge_score, technical_interview_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            candidate_id, date_id, country_id, technology_id, seniority_id,
            row.hired, row.code_score, row.interview_score
        ))

    # Final commit and close connection
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data successfully loaded into MySQL.")

# ===============================
# 5. FULL ETL PIPELINE
# ===============================
def run_etl(path: str = "data/candidates.csv"):
    """
    Runs the full ETL flow: Extract → Transform → Load
    Args:
        path (str): Path to the candidates CSV file.
    """
    print("▶️ Extracting data...")
    df = extract_candidates(path)           # Data extraction

    print("▶️ Transforming data...")
    tables = transform_candidates(df)      # Data transformation

    print("▶️ Loading data into MySQL DW...")
    load_to_dw(tables)                      # Data loading

    print("✅ ETL process completed successfully.")

# Allows running ETL directly from this script
if __name__ == "__main__":
    run_etl()
