#import library
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfMerger
import seaborn as sns
from fpdf import FPDF
import os
import subprocess
import stat
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
sns.set(style="white")

pdf=FPDF()
pdf.add_page()
pdf.set_font('Courier','B',16)
pdf.cell(40,10,'PRZETWARZANIE I ANALIZA DANYCH')
pdf.output('tytul2.pdf','F')

# absolute path till parent folder
abs_path = os.getcwd()
path_array = abs_path.split("/")
path_array = path_array[:len(path_array)-1]
homefolder_path = ""
for i in path_array[1:]:
    homefolder_path = homefolder_path + "/" + i   

# path to clean data
clean_data_path = homefolder_path + "/Python/Scripts/Podatek_od_gier_1.csv"

# reading csv into raw dataframe
df = pd.read_csv(clean_data_path,encoding="latin-1")

#Usuniecie wartosci sprzed 2022 roku
df = df[df["Rok"]<2022]
print(df)

#Tabela z danymi z pliku csv fo pdfa
fig, ax =plt.subplots(figsize=(12,4))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')
pp = PdfPages("tabela2.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()

# barplot średniej wysokosci podatku od gier według lat
fig, ax = plt.subplots(figsize=(25,10))
colors = ["#00e600", "#ff8c1a","#a180cc"]
sns.barplot(x="Rodzaj", y="Podatek",hue="Rok", palette="husl",data=df)
ax.set_title("Uśredniniona wysokość podatku od gier w danym roku",fontdict= {'size':12})
ax.xaxis.set_label_text("Rodzaj gry",fontdict= {'size':14})
ax.yaxis.set_label_text("Średnia wysokość",fontdict= {'size':14})
plt.show()

fig.savefig("wykres_liga11.pdf", format="pdf", bbox_inches="tight")

# Uśredniniona wysokość podatku od gier w danym kwartale
colors = ["windows blue", "amber", "greyish", "faded green", "dusty purple"]
fig, ax = plt.subplots(figsize=(25,10))
sns.set_palette(sns.xkcd_palette(colors))
sns.barplot(x="Rodzaj", y="Podatek",hue="Kwartal",data=df)
ax.set_title("Uśredniniona wysokość podatku od gier w danym kwartale",fontdict= {'size':12})
ax.xaxis.set_label_text("Kwartały",fontdict= {'size':14})
ax.yaxis.set_label_text("Wysokość podatku",fontdict= {'size':14})
plt.show()
fig.savefig("wykres_liga12.pdf", format="pdf", bbox_inches="tight")

#heatmap
trial = pd.DataFrame()
for b in list(df["Rodzaj"].unique()):
    for v in list(df["Rok"].unique()):
        z = df[(df["Rodzaj"] == b) & (df["Rok"] == v)]["Podatek"].mean()
        trial = trial.append(pd.DataFrame({'Rodzaj':b , 'Rok':v , 'Podatek':z}, index=[0]))
trial = trial.reset_index()
del trial["index"]
trial["Podatek"].fillna(0,inplace=True)
trial["Podatek"].isnull().value_counts()
trial["Podatek"] = trial["Podatek"].astype(int)
# HeatMap tp show average prices of vehicles by brand and type together
tri = trial.pivot("Rodzaj","Rok", "Podatek")
fig, ax = plt.subplots(figsize=(15,20))
sns.heatmap(tri,linewidths=1,cmap="YlGnBu",annot=True, ax=ax, fmt="d")
ax.set_title("Średnia wartość podatku z uwzględnieniem rodzaju i roku",fontdict={'size':20})
ax.xaxis.set_label_text("Rok",fontdict= {'size':20})
ax.yaxis.set_label_text("Rodzaj podatku",fontdict= {'size':20})
plt.show()
fig.savefig("wykres_liga13.pdf", format="pdf", bbox_inches="tight")

#MERGE PDF
pdfs = ['tytul2.pdf', 'tabela2.pdf', 'wykres_liga11.pdf', 'wykres_liga12.pdf', 'wykres_liga13.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result1.pdf")
merger.close()

os.remove("tytul2.pdf")
os.remove("tabela2.pdf")
os.remove("wykres_liga11.pdf")