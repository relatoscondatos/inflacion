import sys, os
import pandas as pd

print("Python executable:", sys.executable)
print("sys.path:", sys.path)
print("PYTHONPATH:", os.environ.get("PYTHONPATH"))

# Read the CSV
df = pd.read_csv("src/data/penguins.csv")

print(df)