import requests
from bs4 import BeautifulSoup
import json
import re

data = []

urls = ['https://ferde.no/bomanlegg-og-priser/ryfast',
'https://ferde.no/bomanlegg-og-priser/kvammapakken',
'https://ferde.no/bomanlegg-og-priser/gjesdal',
'https://ferde.no/bomanlegg-og-priser/askoypakken',
'https://ostfold.vegfinans.no/priser-og-betaling/takster-4',
'https://rv36telemark.vegfinans.no/priser-og-betaling/takster-20',
'https://rv4oppland.vegfinans.no/priser-og-betaling/takster-16',
'https://rv3ogrv25.vegfinans.no/priser-og-betaling/takster-22',
'http://www.oslofjordtunnelen.no/priser-og-betaling/takster-10',
'https://hallingporten.vegfinans.no/priser-og-betaling/takster-14',
'https://gausdalsvegen.vegfinans.no/priser-og-betaling/takster-9',
'https://fv311.vegfinans.no/priser-og-betaling/takster-23',
'https://fv34oppland.vegfinans.no/priser-og-betaling/takster-3',
'https://fv33oppland.vegfinans.no/priser-og-betaling/takster-13',
'https://e134buskerud.vegfinans.no/priser-og-betaling/takster-15',
'https://e18vestfold.vegfinans.no/priser-og-betaling/takster-7',
'https://e18telemark.vegfinans.no/priser-og-betaling/takster-21',
'https://e16oppland.vegfinans.no/priser-og-betaling/takster-1',
'https://kongsvingervegen.vegfinans.no/priser-og-betaling/takster-11',
'https://e16eggemoen-olum.vegfinans.no/priser-og-betaling/takster-5',
'https://e6ringebu-otta.vegfinans.no/priser-og-betaling/takster-8',
'https://e6oppland.vegfinans.no/priser-og-betaling/takster-2',
'https://e6bompenger.vegfinans.no/priser-og-betaling/takster-12',
'https://grenland.vegfinans.no/priser-og-betaling/takster',
'https://nedreglomma.vegfinans.no/priser-og-betaling/takster-6',
'https://www.fjellinjen.no/bompenger/historiske-takster',
'https://www.fjellinjen.no/bompenger/takster',
'https://www.fordepakken.no/bomring/alt-du-treng-a-vite-om-bomringen/',
'https://bpsnord.no/prosjekter/bypakke-harstad/',
'https://bpsnord.no/prosjekter/bypakke-bodo/',
'https://bpsnord.no/bypakke-tenk-tromso/',
'https://bpsnord.no/prosjekter/fv-78-toven,/',
'https://bpsnord.no/prosjekter/e6-helgeland/',
'https://bpsnord.no/prosjekter/e6-helgeland-sor/',
'https://bpsnord.no/prosjekter/ryaforbindelsen/',
'https://bpsnord.no/prosjekter/halogalandsbrua/',
'https://www.vegamot.no/takster-og-rabatter-9',
'https://www.vegamot.no/takster-og-rabatter/takstgruppe-1',
'https://www.vegamot.no/takster-og-rabatter-2',
'https://www.vegamot.no/takster-og-rabatter-3',
'https://www.vegamot.no/takster-og-rabatter-6',
'https://www.vegamot.no/takster-og-rabatter-4',
'https://www.vegamot.no/takster-og-rabatter-5',
'https://www.vegamot.no/takster-og-rabatter-7',
'https://www.vegamot.no/takster-og-rabatter-8',
'https://ferde.no/bomanlegg-og-priser/bergen',
'https://ferde.no/bomanlegg-og-priser/kristiansand',
'https://ferde.no/bomanlegg-og-priser/nord-jaeren',
'https://ferde.no/bomanlegg-og-priser/e39-kristiansand-vest-lyngdal-vest',
'https://ferde.no/bomanlegg-og-priser/e39-svegatjorn-raadal',
'https://ferde.no/bomanlegg-og-priser/haugalandspakken',
'https://ferde.no/bomanlegg-og-priser/rogfast',
'https://ferde.no/bomanlegg-og-priser/nordhordlandspakken',
'https://ferde.no/bomanlegg-og-priser/hardangerbrua',
'https://ferde.no/bomanlegg-og-priser/e18-tvedestrand-arendal',
'https://ferde.no/bomanlegg-og-priser/boemlopakken',
'https://ferde.no/bomanlegg-og-priser/fordepakken',
'https://ferde.no/bomanlegg-og-priser/kvinnheradpakken']

# Initialize an empty list to hold the toll data
toll_data = []

# Define the URLs to scrape


# Define the keywords to extract
keywords = [
    'Takstgruppe',
    'Autopass',
    'Autopass Discount',
    'Fuel type',
    'Payment rule',
    'Rush Hour',
    'Rules',
    'Zero emissons rule'
]

# Loop through the URLs and extract the toll data
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the table data
    table = soup.find('table')
    if table:
        headers = [header.text.strip() for header in table.find_all('th')]
        rows = []
        for row in table.find_all('tr')[1:]:
            cells = [cell.text.strip() for cell in row.find_all('td')]
            rows.append(dict(zip(headers, cells)))
    else:
        print(f"Table not found for {url}")
        rows = []

    # Extract the keywords
    data = {'url': url}
    for keyword in keywords:
        element = soup.find('div', text=re.compile(keyword))
        if element:
            data[keyword] = element.find_next('div').text.strip()

    # Add the table data and keywords to the toll data list
    data['toll_data'] = rows
    toll_data.append(data)

# Write the toll data to a JSON file
with open('toll_datttta.json', 'w', encoding='utf-8') as f:
    json.dump(toll_data, f, ensure_ascii=False, indent=4)
