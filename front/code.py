print("Hello from python!")

import pandas as pd
import matplotlib.pyplot as plt

from pyodide.http import open_url

# read data from CSV file using Pandas
url_filename = "https://pystravans.s3.us-east-2.amazonaws.com/front/data.csv"
data = pd.read_csv(open_url(url_filename), skiprows=2)

data['Total'] = data['Total'].str.replace(',','.').astype(float)

print(data[['Name', 'Total']])