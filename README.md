# Workshop

##  Project Description

This project simulates a **Data Engineer selection challenge**, where a **Data Warehouse** (DW) is built from a CSV file of candidates (`candidates.csv`).

The full workflow includes:

1. Creation of a **Dimensional Model** (Star Schema) with fact and dimension tables.
2. **ETL Pipeline** in Python to extract, transform, and load the data into MySQL.
3. Calculation of relevant **KPIs** on hirings and scores.
4. Optional visualization of the KPIs in **Power BI** (screenshots or online dashboard).

---

## Schema

<img width="858" height="394" alt="image" src="https://github.com/user-attachments/assets/05cedc57-14a1-4b96-b54f-0bb94f194b9e" />
---

The diagram shows the workflow from the **data source** to the **final visualization**:

1. **Data Source (.CSV)**

   * I started with CSV files containing candidate information.
   * Before integrating them, I performed an **EDA (Exploratory Data Analysis)** to understand the structure and quality of the dataset.

2. **Extract (E)**

   * I used **Python (pandas)** to **extract** the data from the CSV files.
   * At this stage, I identified issues such as missing values and incorrect data types.

3. **Transform (T)**

   * Using Python, I applied the required **transformations**: data cleaning, column normalization, and format adjustments.
   * The goal was to prepare the data so it could be properly loaded into the database.

4. **Load (L)**

   * The transformed data was **loaded into MySQL**, where I designed and implemented a **Data Warehouse** following a star schema.
   * This structure allowed optimized queries and easier reporting.

5. **Visualization & GitHub**

   * Once the data was in the warehouse, I created **KPIs and visualizations** to answer key business questions.
   * Finally, I documented everything and uploaded the project to **GitHub**, ensuring version control and accessibility.

---

## Dimensional Model of Hires: Star Schema
---
<img width="917" height="738" alt="image" src="https://github.com/user-attachments/assets/0456c067-c457-4a37-8daa-071887cb3074" />

This project uses a **Star Schema** to structure the Data Warehouse, separating metrics (fact table) from descriptive attributes (dimensions). This design enables **efficient queries, KPI generation, and scalability**.

### 🔹 Fact Table: `fact_hires`

* **PK:** `hire_id`
* **FKs:** candidate\_id, date\_id, country\_id, technology\_id, seniority\_id
* **Metrics:**

  * `hired` (1 if scores ≥ 7 in both tests)
  * `code_challenge_score`, `technical_interview_score`

### 🔹 Dimensions

* **dim\_candidate:** candidate details (name, email, years\_of\_experience)
* **dim\_date:** time attributes (year, month, day)
* **dim\_technology:** technology area (Python, DevOps, etc.)
* **dim\_seniority:** level (Intern → Architect)
* **dim\_country:** country of candidate

### 📊 KPIs Generated

* Hires by **technology, country, seniority, year, and experience**
* Average scores by seniority level
* Hiring trends over time

This schema ensures **data consistency, analytical flexibility, and performance**, supporting dashboards and decision-making.

---

##  Project Structure

```
workshop/
│
├─ main.py               # Orchestrator that runs the entire workflow
├─ dimensional_model.py  # Creates the DW database and tables
├─ etl.py                # Full ETL pipeline (extract, transform, load)
├─ KPI's.py              # KPI calculations from the database
├─ data/                 # Folder with candidates CSV (provided by professor)
├─ EDA/                  # EDA notebooks and exploratory analysis
├─ KPI's interpretation/ # Images of dashboard or visual results and interpretation
├─ Start schema/         # Interpretation start schema
└─ README.md             # This file

```

---

##  Technologies and Libraries

* **Python 3.13.3**
* **Pandas** → data manipulation
* **MySQL** → Data Warehouse storage
* **mysql-connector-python** → Python ↔ MySQL connection
* **Power BI** → interactive KPI dashboard

> Note: To run the project, Power BI is not required — only the ETL and KPI code.

---

##  Installation and Setup

1. Clone the repository:

```bash
git clone <https://github.com/Majo0209/Workshop.git>
cd project
```

2. Create a virtual environment (recommended):

```bash
python -m venv env
env\Scripts\activate      # Windows
# or
source env/bin/activate   # Linux/Mac
```

3. Install dependencies:

```bash
pip install pandas mysql-connector-python
```

4. Place the candidates CSV file inside the `data/` folder.

---

##  Project Execution

The full workflow is executed with **`main.py`**:

```bash
python main.py
```

This will:

1. Create the database and tables (`dimensional_model.py`).
2. Run the ETL pipeline (`etl.py`).
3. Calculate all KPIs (`KPI's.py`).

> All KPIs are obtained directly from the MySQL database.

---

##  KPIs Calculated

1. **Hires by technology**

2. **Hires by year**

3. **Hires by seniority level**

4. **Hires by country over the years** (U.S., Brazil, Colombia, Ecuador)

5. **Hires by range of years of experience** (only hired):

   * Ranges: `0-2`, `3-5`, `6-10`, `11-15`, `16-20`, `21+`

6. **Average scores by seniority** (only hired):

   * **Code Challenge** score
   * **Technical Interview** score

> These KPI visualizations can be checked in Power BI or exported from Python.

---

##  Exploratory Data Analysis (EDA)

Before the ETL load, an EDA was performed with Pandas:

* Review of first rows and CSV structure
* Descriptive statistics of numeric columns
* Check for duplicates and null values
* Data types and available columns

---

##  Power BI

[Power BI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiMDExZjU5MDktNTUyYy00YzdiLWE5MWYtZWExMmQ2ZjYxMjk2IiwidCI6IjY5M2NiZWEwLTRlZjktNDI1NC04OTc3LTc2ZTA1Y2I1ZjU1NiIsImMiOjR9)

- [Here you can see the interpretation of each KPI.](https://github.com/Majo0209/Workshop/blob/8b67cc1908d8093a1d5996e77ecd531a305407fd/KPI's%20interpretation.pdf)
---

##  Additional Notes

* Make sure MySQL is running and accessible on `localhost` with user `root` and password `root`.

---

##  Final Result

After running the full workflow:

* The DW with all tables is created.
* Transformed data is loaded.
* KPIs are calculated and ready for visualization.
* An interactive dashboard can be built in Power BI or reports generated directly from Python.

---


## 

##  References

* [Pandas Documentation](https://pandas.pydata.org/docs/)
* [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
* [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
