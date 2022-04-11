
#讀出產品名稱以方便爬取成分網址
import csv
import re

name = []
with open('namelist0-1000.csv',newline='',encoding="utf-8") as csvfile:
    for line in csvfile.readlines():
        name.append(line.strip())

print('Done read listname.')
name.remove('url')
unique = []
for i in range(len(name)):         # 1st loop
    if name[i] not in unique:   # 2nd loop
        unique.append(name[i])

#把listname裡面的產品匯入陣列中
import time
import requests
from bs4 import BeautifulSoup

url = 'https://www.cosdna.com/cht/product.php?q='
sort = '&sort=date'
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
cnt = 0
#k1 = '108.61.187.83:8080'
#proxy = {'http':'http://'+ k1,
# 'https':'https://'+ k1}

#於Skin Salvation找出成分致粉刺程度
#ssIngre = 成分名稱; snIngre = 成分致粉刺程度



url = 'https://skinsalvationsf.com/comedogenic/'
r = requests.get(url,headers=header)
header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}
objSoup = BeautifulSoup(r.text,'lxml')
page = objSoup.find_all('tr')
ssIngre = []
snIngre = []
for i in range(len(page)):
    if(page[i].text.find('							 ') != -1):
        d = page[i].text.strip()
        d = d.replace('							 ',',')
        temp = d.split(',')
        for j in range(len(temp)):
            if j > 1:
                break
            elif j == 1:
                try:
                    snIngre.append(int(temp[j]))
                except:
                    snIngre.append(0)
            else:
                ssIngre.append(temp[j])

print("Done with Skinsalvation")
#找出產品成分
#pName = 產品名稱; pIngre = 所有產品對應成分;
#IngreChara = 所有成分特性; IngreAcne = 所有成分致粉刺; IngreSti = 所有成分刺激性; IngreSafe = 所有成分安全性
#IngreDalton = PubChem的分子量
#IngreScore = EWG成分總評分
import pubchempy as pcp

pIngre = []
pName = []
IngreChara = []
IngreAcne = []
IngreSti = []
IngreSafe = []
IngreDalton = []
IngreScore = []

for i in range(len(unique)):
    #if i == 30: break #試驗用只爬30個網址,若需全部資料即把這行刪掉
    r = requests.get(unique[i],headers=header)
    objSoup = BeautifulSoup(r.text,'lxml')
    p = objSoup.find('span',{'class':'prod-name'})
    n = objSoup.find_all('span',{'class':'colors'})
    chara = objSoup.find_all('td','small-85 text-vampire align-middle')
    acne_sti_safe = objSoup.find_all('td','text-nowrap text-center align-middle')
    print(i,":",p.text.strip())
    #拆成分
    iTemp = []
    for j in n:
        iTemp.append(j.text.strip())
        
    #拆特性
    cTemp = []
    for j in chara:
        if j.text.strip() == "":
            cTemp.append("None")
        elif len(j.text.strip().split(",")) >= 2:
            temp = j.text.strip().split(",")
            s = ''
            for k in range(len(temp)):
                if k == len(temp)-1:
                    s = s + temp[k].strip()
                else:
                    s = s + temp[k].strip() + ","
            cTemp.append(s)
        else:
            cTemp.append(j.text.strip())
            
    #拆粉刺&刺激&安心度
    aTemp = []
    stiTemp = []
    sTemp = []
    cnt = 0
    for j in range(len(acne_sti_safe)):
        data = acne_sti_safe[j].text.strip()
        if cnt == 0:
            if data == "":
                #若cosDNA沒有即到Skin Salvation找出
                query = iTemp[int(j/3)]
                tempLen = len(aTemp)
                for k in range(len(ssIngre)):
                    if ssIngre[k] == query:
                        aTemp.append(snIngre[k])
                        break
                if len(aTemp) == tempLen:
                    aTemp.append('0')
            else:
                aTemp.append(data)
            cnt = cnt + 1
        elif cnt == 1:
            if data == "":
                stiTemp.append('0')
            else:
                stiTemp.append(data)
            cnt = cnt + 1
        elif cnt == 2:
            if data == "":
                sTemp.append('None')
            else:
                sTemp.append(data)
            cnt = 0
    
    #找出成分阻塞
    dTemp = []
    for j in iTemp:
        if j.find('/') != -1:
            j = j[:j.find('/')]
        results = pcp.get_compounds(j, 'name')
        try:
            dTemp.append(results[0].molecular_weight)
        except:
            dTemp.append('None')
    
    #找出成分總分
    scoreTemp = []
    for j in range(len(iTemp)):
        time.sleep(1)
        if iTemp[j].find(' ') != -1:
            t = iTemp[j].replace(' ','+')
            sLink = 'https://www.ewg.org/skindeep/search/?utf8=%E2%9C%93&search='+t
        else:
            sLink = 'https://www.ewg.org/skindeep/search/?utf8=%E2%9C%93&search='+iTemp[j]
        try:
            r = requests.get(sLink,headers=header)
            objSoup = BeautifulSoup(r.text,'lxml')
            allContent = objSoup.find_all('div','product-tile')
            allScore = objSoup.find_all('div','product-score')
            for k in range(len(allContent)):
                t = iTemp[j].replace(' ','_').lower()
                title = allContent[k].find('a').get('href')
                title = title[title.index('-')+1:len(title)-1].lower()
                if title == t:
                    s = allScore[k].find('img').get('src')
                    s = s[s.find('score=')+len('score='):s.find('&')]
                    #according to the guiding of EWG
                    if int(s) >= 7:
                        s = s + '分 (高危)'
                    elif int(s) >= 3:
                        s = s + '分 (普通)'
                    elif int(s) >= 1:
                        s = s + '分 (安全)'
            scoreTemp.append(s)
        except:
            print('Cannot find:',iTemp[j])
            scoreTemp.append('None')
                
    pName.append(p.text.strip())
    pIngre.append(iTemp)
    IngreChara.append(cTemp)
    IngreDalton.append(dTemp)
    IngreSafe.append(sTemp)
    IngreAcne.append(aTemp)
    IngreSti.append(stiTemp)
    IngreScore.append(scoreTemp)

#所有product(轉成csv)*測試用
with open('AllProducts.csv','w',encoding='utf_8',newline='') as csvfile:
    fieldnames = ['Name','Ingredients','Character','Acne','Dalton','Stimulation','Safeness','EWG_Score']
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for i in range(len(pName)):
        temp = ''
        for j in pIngre[i]:
            temp = temp + j + ','
        writer.writerow({'Name':pName[i],'Ingredients':temp,'Character':IngreChara[i],'Acne':IngreAcne[i],'Dalton':IngreDalton[i],'Stimulation':IngreSti[i],'Safeness':IngreSafe[i],'EWG_Score':IngreScore[i]})
