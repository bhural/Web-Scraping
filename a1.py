import pandas as pd
import json

# Read the JSON file
with open('toll.json') as f:
    data = json.load(f)

# Convert the JSON data to a list of dictionaries
data_list = []
for d in data:
    new_d = {}
    for key, value in d.items():
        if isinstance(value, dict):
            for k, v in value.items():
                new_d[f"{key} - {k}"] = v
        else:
            new_d[key] = value
    data_list.append(new_d)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data_list)

# Write the DataFrame to an Excel file without any JSON notation
with pd.ExcelWriter('output.xlsx', engine='openpyxl', mode='w') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=True, float_format="%.2f", freeze_panes=(1,0))
    worksheet = writer.sheets['Sheet1']
    for idx, col in enumerate(df):
        series = df[col]
        max_len = max((
            series.astype(str).map(len).max(),
            len(str(series.name))
        )) + 1
        worksheet.column_dimensions[chr(65+idx)].width = max_len
        for cell in worksheet[f"{chr(65+idx)}1:{chr(65+idx)}{len(series)+1}"]:
            cell.number_format = 'General'
