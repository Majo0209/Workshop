# main.py
import subprocess
import sys

def run_script(script_name):
    """Runs a Python script and displays its output in the console."""
    try:
        print(f"\n▶ Running  {script_name} ...")
        subprocess.run([sys.executable, script_name], check=True)
        print(f"✅ {script_name} executed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error executing {script_name}: {e}\n")

def main():
    print("Starting Hires Data Warehouse project\n")

    # 1. Create dimensional model
    run_script("dimensional_model.py")

     # 2. Run ETL
    run_script("etl.py")

     # 3. Calculate KPIs
    run_script("KPI's.py")

    print("Process completed.")

if __name__ == "__main__":
    main()
