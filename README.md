# Workshop

##  Project Description

This project simulates a **Data Engineer selection challenge**, where a **Data Warehouse** (DW) is built from a CSV file of candidates (`candidates.csv`).

The full workflow includes:

1. Creation of a **Dimensional Model** (Star Schema) with fact and dimension tables.
2. **ETL Pipeline** in Python to extract, transform, and load the data into MySQL.
3. Calculation of relevant **KPIs** on hirings and scores.
4. Optional visualization of the KPIs in **Power BI** (screenshots or online dashboard).

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
├─ docs/                 # Images of dashboard or visual results
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

[Power BI Dashboard](https://uao-my.sharepoint.com/:u:/g/personal/maria_jos_suarez_uao_edu_co/EWjBXGS1MlFImz6IoJJIfPsBObXkHjX9Cn6tl8s9AYCGbA?e=35WfRd)

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
