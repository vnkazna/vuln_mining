from pandas import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
import datetime
import time

df = read_excel('vullist.xlsx', sheet_name = 'Sheet', engine="openpyxl", skiprows=1, header=[1])
vulWF=df[df["Описание уязвимости"].str.contains("межсете")] 
vulIPS=df[df["Описание уязвимости"].str.contains("WAF")]
vul = vulWF.append(vulIPS)
vulWF=vulWF[['Описание уязвимости','Дата выявления']]
vulIPS=vulIPS[['Описание уязвимости','Дата выявления']]
vul=vul[['Описание уязвимости','Дата выявления']]
#print(vulIPS)
def cases_in_year(year, vul): #função de pesquisa de vulnerabilidades identificadas para o ano especificado
    year=int(year)
    if year > 2020:
        return print('Especifique o ano entre 2015-2020')

    if (year % 4 == 0) and (year % 100 != 0) or (year % 400 == 0): #Verificando se há um ano bissexto
        days=366
    else:
        days=365
    f_date=datetime.datetime(year,1,1)
    interval = datetime.timedelta(days=days)
    sec_date=f_date+interval
    vul['Дата выявления'] = to_datetime(vul['Дата выявления'], format='%d.%m.%Y')
    i=0
    for date in vul['Дата выявления']:
        if date is not None:
            if f_date <= date <= sec_date:
                i=i+1
    return i

year=2015
x = []
y = []
y2 = []
for case in range(2021-year):
    y.append(cases_in_year(year, vulWF))
    y2.append(cases_in_year(year, vulIPS))
    year=year+1
    x.append(year)

plt.title("Número de vulnerabilidades identificadas de FW e sistema de IDS") 
plt.xlabel("Anos")
plt.ylabel("Vulnerabilidades")
plt.grid()
plt.plot(x, y)           
plt.plot(x, y2) 
plt.legend(['FW', 'IDS'])
plt.show()
