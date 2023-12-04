import pandas as pd
import json

# Read Excel file
#excel_file_url = 'https://docs.google.com/spreadsheets/d/1mn-HDxtI3XXaSnkPoxdslzwB6sOwsm0g/export?format=xlsx'
df = pd.read_excel('toll.xlsx', sheet_name='Sheet1')

# Read JSON file
#json_file_url = 'https://drive.google.com/u/0/uc?id=15dz6yquesd2kN4kCS6O2DXpnSmKYTFxV&export=download'
json_data = pd.read_csv('toll.json', error_bad_lines=False)

# Write the JSON data to a file
json_data.to_json('tolll_data.json', orient='records')

with open('tolll_data.json') as f:
    data_json = json.load(f)

# Create a dictionary with toll station names as keys and toll data as values
name_to_data = {}
for d in data_json:
    if 'name' in d:
        name_to_data[d['name'].lower()] = d


# Loop through each toll station in the Excel sheet and get the toll data
toll_data = []
for toll_station_name in df[1:]:
    toll_station_name_lower = toll_station_name.lower()
    if toll_station_name_lower in name_to_data:
        toll_data_dict = name_to_data[toll_station_name_lower]
        toll_data.append([
            toll_data_dict.get('name', ''),
            toll_data_dict.get('tariffs', {}).get('1', {}).get('full_price', ''),
            toll_data_dict.get('tariffs', {}).get('1', {}).get('by_appointment', ''),
            toll_data_dict.get('tariffs', {}).get('1', {}).get('zero_emission_with_agreement', ''),
            toll_data_dict.get('tariffs', {}).get('2', {}).get('full_price', ''),
            toll_data_dict.get('tariffs', {}).get('2', {}).get('by_appointment', ''),
            toll_data_dict.get('tariffs', {}).get('2', {}).get('zero_emission_with_agreement', ''),
        ])
    else:
        toll_data.append([toll_station_name, '', '', '', '', '', ''])

# Create a new data frame with the toll data
columns = ['Toll Station Names', 'Tariff group 1 - Full price', 'Tariff group 1 - By appointment',
           'Tariff group 1 - Zero emission vehicle with agreement', 'Tariff group 2 - Full price',
           'Tariff group 2 - By appointment', 'Tariff group 2 - Zero emission vehicle with agreement']
df_toll = pd.DataFrame(toll_data, columns=columns)

# Export the new data frame to a new Excel file
with pd.ExcelWriter('toll_data_with_tariffs.xlsx', engine='openpyxl', mode='w') as writer:
    df_toll.to_excel(writer, sheet_name='Sheet1', index=False)
