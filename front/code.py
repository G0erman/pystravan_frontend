import pandas as pd
import matplotlib.pyplot as plt

from pyodide.http import open_url

import js
from js import document
from pyodide.ffi.wrappers import add_event_listener
import seaborn as sns

def string_has_digits(string):
	return any(char.isdigit() for char in str(string))

class Stravan():
    def __init__(self, info_dict, week_lbl_dict):
        self.name = info_dict['name']
        self.strava_id = info_dict['strava_id']
        self.week_1 = info_dict['1']
        self.week_2 = info_dict['2']
        self.week_3 = info_dict['3']
        self.week_4 = info_dict['4']
        self.week_1_lbl = week_lbl_dict['week_1_lbl']
        self.week_2_lbl = week_lbl_dict['week_2_lbl']
        self.week_3_lbl = week_lbl_dict['week_3_lbl']
        self.week_4_lbl = week_lbl_dict['week_4_lbl']
        self.total = info_dict['total']

    def __str__(self):
        return "Name: %s %s Total: %s" % (self.name, self.total)

    def on_click(self,e):
    	stravan_name_elem = document.getElementById("stravan_name")
    	stravan_name_elem.innerHTML = self.name
    	stravan_id_elem = document.getElementById("stravan_id")
    	stravan_id_elem.innerHTML = self.strava_id
    	total_km = document.getElementById("total_km")
    	total_km.innerHTML = self.total
    	df = pd.DataFrame({'Week': [self.week_1_lbl, self.week_2_lbl,self.week_3_lbl,self.week_4_lbl],
                   'Km': [self.week_1, self.week_2, self.week_3, self.week_4]})
    	fig, ax = plt.subplots()
    	sns.lineplot(x="Week", y="Km", data=df, ax=ax)
    	ax.tick_params(axis='y', rotation=90)
    	pyscript.write("chart1",fig)

    def create_row(self):
        row = document.createElement('tr')
        name_col = document.createElement('td')
        total_col = document.createElement('td')

        name_col.innerText = self.name
        total_col.innerText = self.total
         
        row.append(name_col)
        row.append(total_col)
        row.style.cursor = "pointer"
        row.setAttribute('data-bs-target', '#myModal')
        row.setAttribute('data-bs-toggle', 'modal')
        add_event_listener( row, 'click', self.on_click)
        
        return row

# read data from CSV file using Pandas
url_filename = "https://pystravan-gold.s3.amazonaws.com/data.csv"
data = pd.read_csv(open_url(url_filename))

data = data.sort_values("Total", ascending=False)
columns = data.columns

contents_element = document.getElementById("content")
for i in range(len(data)):
	week_labels_dict = {
		'week_1_lbl' : columns[3],
		'week_2_lbl' : columns[5],
		'week_3_lbl' : columns[7],
		'week_4_lbl' : columns[9]
	}
	week_1 = data.iloc[i,3] if string_has_digits(data.iloc[i,3]) else "0"
	week_2 = data.iloc[i,5] if string_has_digits(data.iloc[i,5]) else "0"
	week_3 = data.iloc[i,7] if string_has_digits(data.iloc[i,7]) else "0"
	week_4 = data.iloc[i,9] if string_has_digits(data.iloc[i,9]) else "0"
	
	stravan_info_dict = { 
		"strava_id": data.iloc[i,1],
		"name": data.iloc[i,0],
		"1": week_1,
		"2": week_2,
		"3": week_3,
		"4": week_4,
		"total": data.iloc[i,10]
	}
	stravan = Stravan( stravan_info_dict, week_labels_dict)
	contents_element.append(stravan.create_row())
