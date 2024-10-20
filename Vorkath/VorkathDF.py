import pandas as pd
import json

# Set pandas display options to show all rows and columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.expand_frame_repr', False)  # Prevents DataFrame from being split across multiple lines


# Path to the txt file
file_path = 'VorkathObjects.txt'

# Read the text file, assuming each line is a separate JSON object
with open(file_path, 'r') as file:
    lines = file.readlines()

# Parse each line as a JSON object
data = [json.loads(line) for line in lines]

# Create a list to hold the flattened data
flattened_data = []

# Flatten the 'drops' into individual rows
for entry in data:
    for drop in entry['drops']:
        flattened_data.append({
            'name': entry['name'],
            'level': entry['level'],
            'killCount': entry['killCount'],
            'type': entry['type'],
            'drop_name': drop['name'],
            'drop_id': drop['id'],
            'drop_quantity': drop['quantity'],
            'drop_price': drop['price'],
            'date': entry['date']
        })

# Create a DataFrame from the flattened data
df = pd.DataFrame(flattened_data)

# Display the DataFrame
print(df)

# Example: Total price of drops per kill count
df_grouped = df.groupby('killCount').agg({'drop_price': 'sum'}).reset_index()


# Aggregate data by killCount
agg_df = df.groupby('killCount').agg(
    items_dropped=('drop_name', lambda x: ', '.join(sorted(set(x)))),
    total_qty=('drop_quantity', 'sum'),
    total_price=('drop_price', lambda x: (x * df.loc[x.index, 'drop_quantity']).sum()),
    total_gp_per_kill=('drop_price', lambda x: (x * df.loc[x.index, 'drop_quantity']).sum())
).reset_index()

# Display the aggregated DataFrame
print(agg_df)

output_df_grouped_csv_file = 'VorkathDropsRaw.csv'
output_csv_file = 'VorkathDropsAggregated.csv'
agg_df.to_csv(output_csv_file, index=False)
df.to_csv(output_df_grouped_csv_file, index=False)

print(f"Aggregated data saved to {output_csv_file}.")
print(f'nonaggreated data saved to {output_df_grouped_csv_file}.')