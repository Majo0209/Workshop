import mysql.connector  # Import the MySQL connector to execute queries from Python

# ===============================
# 1. Connect to MySQL
# ===============================
# Create a connection to the local MySQL server using username and password
conn = mysql.connector.connect(
    host="localhost",   # MySQL server address (localhost for local server)
    user="root",        # MySQL username
    password="root"     # User password
)

# Create a cursor to execute SQL commands on the connection
cursor = conn.cursor()

# ===============================
# 2. Create the database
# ===============================
# Create the 'hires_model' database if it doesn't exist yet.
# This ensures the script can run multiple times without errors.
cursor.execute("CREATE DATABASE IF NOT EXISTS hires_model;")

# Select the database we just created to use it
cursor.execute("USE hires_model;")

# ===============================
# 3. Create dimension tables
# ===============================

# Candidate table
# Stores basic information about candidates
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_candidate (
    candidate_id INT PRIMARY KEY AUTO_INCREMENT,  # Unique ID for each candidate, auto-incremented
    first_name VARCHAR(100) NOT NULL,            # Candidate's first name, required
    last_name VARCHAR(100) NOT NULL,             # Candidate's last name, required
    email VARCHAR(150) UNIQUE NOT NULL,          # Candidate's unique email, required
    years_of_experience INT                       # Years of experience, can be null
);
""")

# Date table
# Allows analyzing hires over time
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INT PRIMARY KEY AUTO_INCREMENT,     # Unique ID for the date dimension
    application_date DATE NOT NULL,             # Full application date
    year INT NOT NULL,                           # Year extracted from the date
    month INT NOT NULL,                          # Month extracted from the date
    day INT NOT NULL                             # Day extracted from the date
);
""")

# Country table
# Stores the different countries from which candidates apply
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_country (
    country_id INT PRIMARY KEY AUTO_INCREMENT,  # Unique country ID
    country_name VARCHAR(100) NOT NULL          # Country name, required
);
""")

# Technology table
# Stores the technologies in which candidates apply
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_technology (
    technology_id INT PRIMARY KEY AUTO_INCREMENT,  # Unique technology ID
    technology_name VARCHAR(100) NOT NULL          # Technology name, required
);
""")

# Seniority table
# Defines the experience/seniority levels of candidates
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_seniority (
    seniority_id INT PRIMARY KEY AUTO_INCREMENT,  # Unique ID for seniority level
    seniority_level VARCHAR(50) NOT NULL          # Seniority level (junior, senior, etc.)
);
""")

# ===============================
# 4. Create fact table
# ===============================
# Fact table that connects all dimensions and stores hires
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_hires (
    hire_id INT PRIMARY KEY AUTO_INCREMENT,       # Unique row ID in the fact table
    candidate_id INT NOT NULL,                    # FK to dim_candidate
    date_id INT NOT NULL,                         # FK to dim_date
    country_id INT NOT NULL,                      # FK to dim_country
    technology_id INT NOT NULL,                   # FK to dim_technology
    seniority_id INT NOT NULL,                    # FK to dim_seniority
    hired TINYINT(1) NOT NULL,                    # 1 if hired, 0 if not
    code_challenge_score DECIMAL(5,2),            # Score in code challenge
    technical_interview_score DECIMAL(5,2),       # Score in technical interview
    FOREIGN KEY (candidate_id) REFERENCES dim_candidate(candidate_id),  # Relation with dim_candidate
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),                 # Relation with dim_date
    FOREIGN KEY (country_id) REFERENCES dim_country(country_id),        # Relation with dim_country
    FOREIGN KEY (technology_id) REFERENCES dim_technology(technology_id), # Relation with dim_technology
    FOREIGN KEY (seniority_id) REFERENCES dim_seniority(seniority_id)  # Relation with dim_seniority
);
""")

print("✅ Database and tables created successfully.")  # Confirmation message

# ===============================
# 5. Close connection
# ===============================
cursor.close()  # Close the cursor to free resources
conn.close()    # Close the connection to the MySQL server
