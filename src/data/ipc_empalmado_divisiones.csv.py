import pandas as pd

# Path to the local CSV file
file_path = 'src/data/serie-histórica-empalmada-divisiones-ipc-diciembre-2009-a-la-fecha-csv.csv'

# Read the CSV file using the semicolon as the delimiter and the comma as the decimal separator
df = pd.read_csv(file_path, delimiter=';', decimal=',', encoding='latin1')

# Convert specific columns to numeric
numeric_columns = ['Índice', 'Variación Mensual (%)']
df[numeric_columns] = df[numeric_columns].replace('', float('nan')).apply(pd.to_numeric)

# Print the DataFrame to standard CSV format
print(df.to_csv(index=False))
