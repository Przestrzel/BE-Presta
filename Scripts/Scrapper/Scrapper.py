from bs4 import BeautifulSoup
import requests

headers = {"User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}


URLs = [
    "https://szkolenia.com/szkolenia/online-uslugi",
    "https://szkolenia.com/szkolenia/online-finanse-i-bankowosc",
    "https://szkolenia.com/szkolenia/online-informatyka-i-telekomunikacja",
    "https://szkolenia.com/szkolenia/online-rozwoj-osobisty",
]
descriptionUrl = "https://szkolenia.com/"

categoryList = ["Usługi","Finanse i bankowość","Informatyka i telekomunikacja", "Rozwój osobisty"]
Descriptions = []

categoryCounter = 0
for page in URLs:
            print("Strona :", page)
            res= requests.get(page, headers=headers)
            soup = BeautifulSoup(res.text,"html.parser")
            # we want to scrap courses with every page (pagination on site)

            pageCount = soup.find("div",{"class": "pagination js-has-clickables"})
            print("Page Count",pageCount.text)
            pagesOnSite = int(pageCount.text[-2])
            pageCounter = 1
            for i in range(1,pagesOnSite+1):
                print(page+'?page='+str(pageCounter))
                pageCounter +=1
                params = {"page": pageCounter}
                res= requests.get(page, headers=headers, params=params)
                soup = BeautifulSoup(res.text,"html.parser")
                Titles = soup.find_all("a",{"class": "publication-row-name"})
                Categories = [categoryList[categoryCounter] for x in range(len(Titles))]
                Authors =  soup.find_all("div",{"class": "publication-row-subname"})
                DescriptionLinks = soup.find_all("div",{"class": "js-link-wrapper"})
                Prices =  soup.find_all("div",{"class": "publication-row-item-fixed-size is-180px"})

                for i in range(len(DescriptionLinks)):
                    newURL = descriptionUrl + DescriptionLinks[i]['data-href']
                    descriptionResponse = requests.get(newURL, headers=headers, params=params)
                    soup2 = BeautifulSoup(descriptionResponse.text,"html.parser")
                    Descriptions.append(soup2.find("div",{"class": "icube-ce-section-content"}).text)
                links = soup.find_all('img')

                with open('courses.csv', mode='a+', newline='',encoding='utf-8') as coursesFile:
                    for i in range(len(Titles)):
                        if "cena do ustalenia" in Prices[i].text:
                            continue
                        if ".svg" in links[i]['src'] or ".gif" in links[i]['src']:
                            continue
                        priceBrutto = Prices[i].text.split('zł')[0].replace(",",".")
                        tmp = Prices[i].text.split('zł')[1].replace(",",".")
                        tmp1 = tmp.replace("(","")
                        tmp2 = tmp1.replace(")","")
                        priceNetto = tmp2.replace("netto","").replace(" ","")
                        active = 1
                        inSale = 1
                        descriptionFixed = Descriptions[i][1:500].replace("\n", " ")
                        coursesFile.write(Titles[i].text + ";" + Categories[i] + ";" + priceBrutto.replace(' ','') + ";" + 
                                            priceNetto + ";" + links[i]['src'] + ";" + str(active) + ";" + str(inSale) + ";" + descriptionFixed + ';' + str(999999) + '\n'
                                        )
            categoryCounter +=1
    