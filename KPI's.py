import mysql.connector  # To connect to MySQL from Python
import pandas as pd      # For data manipulation and KPI calculations

# ===============================
# 1. Connect to MySQL
# ===============================
# Create a connection to the MySQL Data Warehouse
conn = mysql.connector.connect(
    host="localhost",        # Local MySQL server
    user="root",             # Username
    password="root",         # Password
    database="hires_model"   # Database where our tables are stored
)

# ===============================
# 2. Fetch data from the DW
# ===============================
# SQL query joining the fact table with all necessary dimensions
query = """
SELECT 
    f.hired,                        -- 1 if hired, 0 if not
    f.code_challenge_score,         -- Code challenge score
    f.technical_interview_score,    -- Technical interview score
    c.years_of_experience,          -- Candidate experience
    co.country_name,                -- Candidate country
    t.technology_name,              -- Applied technology
    s.seniority_level,              -- Seniority level
    d.year                          -- Application year
FROM fact_hires f
JOIN dim_candidate c ON f.candidate_id = c.candidate_id
JOIN dim_country co ON f.country_id = co.country_id
JOIN dim_technology t ON f.technology_id = t.technology_id
JOIN dim_seniority s ON f.seniority_id = s.seniority_id
JOIN dim_date d ON f.date_id = d.date_id;
"""

# Execute the query and load the data into a Pandas DataFrame
df = pd.read_sql(query, conn)

# ===============================
# 3. KPI CALCULATIONS
# ===============================

## KPI 1 → Hires by technology
# Group by technology and sum hires
kpi1 = df.groupby("technology_name")["hired"].sum()

## KPI 2 → Hires by year
# Group by year and sum hires
kpi2 = df.groupby("year")["hired"].sum()

## KPI 3 → Hires by seniority level
# Group by seniority level and sum hires
kpi3 = df.groupby("seniority_level")["hired"].sum()

## KPI 4 → Hires by country over the years
# Focus on key countries
countries_focus = ["United States", "Brazil", "Colombia", "Ecuador"]

# Filter only the selected countries and group by country and year
kpi4 = df[df["country_name"].isin(countries_focus)] \
          .groupby(["country_name", "year"])["hired"].sum()

## KPI 5 → Hires by years of experience
# Only consider hired candidates
df_hired = df[df["hired"] == 1]

# Define experience ranges
bins = [0, 2, 5, 10, 15, 20, float('inf')]
labels = ["0-2", "3-5", "6-10", "11-15", "16-20", "21+"]

# Create a categorical column for experience ranges
df_hired["experience_range"] = pd.cut(
    df_hired["years_of_experience"],
    bins=bins,
    labels=labels,
    right=True
)

# Group by experience range and sum hires
kpi5_hired = (
    df_hired.groupby("experience_range")["hired"]
    .sum()
    .reset_index(name="total_hires")  # Rename resulting column
)

## KPI 6 → Average scores by seniority (only hired)
# Group by seniority and calculate mean scores
kpi6_hired = (
    df_hired.groupby("seniority_level")[["technical_interview_score", "code_challenge_score"]]
    .mean()
    .reset_index()
)

# ===============================
# 4. Display results in console
# ===============================
print("\n📊 KPI 1: Hires by Technology")
print(kpi1)

print("\n📊 KPI 2: Hires by Year")
print(kpi2)

print("\n📊 KPI 3: Hires by Seniority Level")
print(kpi3)

print("\n📊 KPI 4: Hires by Country over the Years (US, Brazil, Colombia, Ecuador)")
print(kpi4)

print("\n📊 KPI 5 (Hired candidates by experience range):")
print(kpi5_hired)

print("\n📊 KPI 6 (Average scores by seniority - only hired):")
print(kpi6_hired)

# ===============================
# 5. Close connection
# ===============================
conn.close()  # Always close the database connection to free resources
