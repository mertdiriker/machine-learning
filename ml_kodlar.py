                                               ***VERİ ÇEKME İŞLEMİ***
#importlar
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests


#listeler
linkler=[]
fiyatlar=[]
titles=[]
values=[]
for i in range(1,30):                                                       #30 sayfalık veri için 30 kullandım
    url1 = "https://www.trendyol.com/tablet?pi="+str(i)                    #her sayfa sonunda i kadar sayfa indexi var 
    r = requests.get(url1)                                                  #request atıp veriyi r değişkenine atıyorum
    source = bs(r.content,"lxml")                                           #xml dosyasını alıyorum
    urls = source.find_all("div",attrs={"class":"p-card-wrppr"})            #classı p-card-wrppr olan div leri urls değişkenine alıyorum
    for url in urls:
        sweat_link = "https://www.trendyol.com"+url.a.get("href")           #aldığım hrefleri link haline getiriyorum
        linkler.append(sweat_link)                                          #linkler listeme ekliyorum
        print(sweat_link) 
        sw = requests.get(sweat_link)                                       #tablet satış sayfasını sw değişkenine alıyorum
        sourcesw= bs(sw.content,"lxml")                                     #xml dosyasını sourcessw değişkenine alıyorum
        ozellikler = sourcesw.find_all("div",attrs={"class":"prop-item"})   #sourcessw içinde classı prop-item olan divleri alıyorum
        for ozellik in ozellikler:
            title = ozellik.find("div").text                                #özellik title ını alıyorum
            value = ozellik.find("div","item-value").text                   #özellik içeriğini alıyorum
            titles.append(title)                                            #titleları listeye alıyorum
            values.append(value)                                            #içeriği listeye alıyorum
            
    fiyat = source.find_all("div",attrs={"class":"prc-box-sllng"})          #fiyatların divini alıyorum
    for price in fiyat:
        fiyatlar.append(price.text)                                         #fiyatları listeye alıyorum
     #incelemek için liste uzunluklarını yazdırdım       
print(str(len(fiyatlar)))
print(str(len(linkler)))
print(str(len(titles)))
print(str(len(values)))    
    
df_link = pd.DataFrame()         #data frame oluşturuyorum
df_link["linkler"] = linkler     #linkler diye başlık atıp altına linkleri atıyorum
df_link["fiyatlar"] = fiyatlar   #fiyatlar diye başlık atıp altına fiyatları atıyorum
df_link.head()                   #yazdırıyorum kontrol için
sweats = len(linkler)            # kaç link olduğunu tutuyorum
columns = np.array(titles)       #kaç özellik varsa o kadar başlık oluşturuyorum
columns = np.unique(columns)     # kolonları ayarlıyorum

df = pd.DataFrame(columns=columns)  # belirlediğim standartlara uygun bir DataFrame oluşturuyorum
df["link"]=linkler                  #link diye bir başlık atıp altına linkleri atıyorum
df["fiyatlar"] =fiyatlar            #fiyatlar diye başlık atıp altına fiyatları atıyorum
df.head()                           #kontrol için yazdırıyorum
print(str(sweats))                  #kontrol için kaç tane link olduğunu yazdırıyorum
for j in range(0,sweats):           #kaç link varsa o kadar dönecek bir döngü kurup içerisine özellikleri atıyorum
    print(str(j+1))                 #hangi işlemde olduğunu kontrol etmek için yazdığım satır.
    url = df['link'].loc[j]
    sw = requests.get(url)
    sourcesw= bs(sw.content,"lxml")
    ozellikler = sourcesw.find_all("div",attrs={"class":"prop-item"})
    for ozellik in ozellikler:
        title = ozellik.find("div").text
        value = ozellik.find("div","item-value").text
        titles.append(title)
        values.append(value)
        df[title].loc[j]=value
#df.to_csv("D:\tablet.csv",index=False)
df.to_excel("D:\tablet.xlsx",index=False)  #dosyayı kaydediyorum
        
    



                                                ***VERİ ÖN İŞLEME***
# Data Preprocessing Tools

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('tablet.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values
print(X)
print(y)

# Taking care of missing data
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
imputer.fit(X[:, :])
X[:, :] = imputer.transform(X[:, :])
print(X)

# Encoding categorical data
# Encoding the Independent Variable
#from sklearn.compose import ColumnTransformer           kod olarak bu şekilde kullandığımda x arrayinde size hatası
                                                                #verdiği için binary koda parça parça dönüştürdüm.
#from sklearn.preprocessing import OneHotEncoder
#ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[0,1,2,3,4,5,6,7,8,9])], remainder='passthrough')
#X = np.array(ct.fit_transform(X))
#print(X)
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[0,1,2])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[25,26,27])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[36])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)

ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[38,39,40])], remainder='passthrough')
X = np.array(ct.fit_transform(X))
print(X)
yeni = pd.DataFrame(X)
yeni.to_excel("D:\\ozellikler.xlsx",index=False)

yeni = pd.DataFrame(y)
yeni.to_excel("D:\\fiyat.xlsx",index=False)
