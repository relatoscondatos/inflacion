import pandas as pd
import io
import sys

# Load the first parquet file
ipc_file_path = "src/data/ipc.parquet"
df = pd.read_parquet(ipc_file_path)

# Create an in-memory buffer
buffer = io.BytesIO()

# Convert the merged DataFrame to a Parquet file in memory
df.to_parquet(buffer, engine='pyarrow')

# Write the buffer content to sys.stdout
sys.stdout.buffer.write(buffer.getvalue())
