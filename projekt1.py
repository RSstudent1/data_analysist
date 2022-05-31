#import library
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyPDF2 import PdfMerger
import seaborn as sns
#help merge pdf https://pypi.org/project/PyPDF2/  https://stackoverflow.com/questions/3444645/merge-pdf-files


#add csv file to dataframe
df = pd.read_excel('C:\Python\Scripts\egzamin.xlsx',sheet_name='dane')



#create boxplot
#CREATE PDF
with PdfPages('big1.pdf') as pdf:
    boxplot = df.boxplot(column='wartosc', by='przedmiot', figsize = (10,10), rot = 1000, fontsize= '8', grid = True)
#    pdf.savefig()

with PdfPages('big2.pdf') as pdf:
    boxplot = df.boxplot(column='wartosc', by='plec', figsize = (10,10), rot = 1000, fontsize= '8', grid = True)
#    pdf.savefig()

#MERGE PDF
pdfs = ['big1.pdf', 'big2.pdf']

merger = PdfMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("result.pdf")
merger.close()

