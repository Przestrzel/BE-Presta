from random import randint
from bs4 import BeautifulSoup
import requests
import re

headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

URLs = [
    "https://szkolenia.com/szkolenia/online-uslugi",
    "https://szkolenia.com/szkolenia/online-finanse-i-bankowosc",
    "https://szkolenia.com/szkolenia/online-informatyka-i-telekomunikacja",
    "https://szkolenia.com/szkolenia/online-rozwoj-osobisty",
]
descriptionUrl = "https://szkolenia.com/"

categoryList = ["Usługi", "Finanse i bankowość", "Informatyka i telekomunikacja", "Rozwój osobisty"]
index = 0
categoryCounter = 0
for page in URLs:
    print("Strona :", page)
    res = requests.get(page, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    # we want to scrap courses with every page (pagination on site)

    pageCount = soup.find("div", {"class": "pagination js-has-clickables"})
    print("Page Count", pageCount.text)
    pagesOnSite = int(pageCount.text[-2])
    pageCounter = 1
    for i in range(1, pagesOnSite + 1):
        Descriptions = []
        links = []
        print(page + '?page=' + str(pageCounter))
        pageCounter += 1
        params = {"page": pageCounter}
        res = requests.get(page, headers=headers, params=params)
        soup = BeautifulSoup(res.text, "html.parser")
        Titles = soup.find_all("a", {"class": "publication-row-name"})
        Categories = [categoryList[categoryCounter] for x in range(len(Titles))]
        Authors = soup.find_all("div", {"class": "publication-row-subname"})
        DescriptionLinks = soup.find_all("div", {"class": "js-link-wrapper"})
        # print("Liczba opisow", len(DescriptionLinks))
        Prices = soup.find_all("div", {"class": "publication-row-item-fixed-size is-180px"})

        # print("Liczba tytulow", len(Titles))
        for j in range(len(DescriptionLinks)):
            newURL = descriptionUrl + DescriptionLinks[j]['data-href']
            descriptionResponse = requests.get(newURL, headers=headers, params=params)
            soup2 = BeautifulSoup(descriptionResponse.text, "html.parser")
            Descriptions.append(soup2.find("div", {"class": "icube-ce-section-content"}).text)
            helpDiv = soup2.find("div", {"class": "company-card js-has-clickables"})
            links.append(helpDiv.find('img').attrs['src'])
            # print(len(links))
            # print("URL",newURL)
            # print("Wyciagniety DIV", helpDiv.text)
            # print("Adres obrazka",helpDiv.find('img').attrs['src'])
        # print("Opisy",len(DescriptionLinks))
        # print("Zdjecia",len(links))

        with open('courses2.csv', mode='a+', newline='', encoding='utf-8') as coursesFile:
            for k in range(len(Titles)):
                if "cena do ustalenia" in Prices[k].text:
                    continue
                if ".svg" in links[k] or ".gif" in links[k]:
                    continue
                if not Descriptions[k][1:].replace('\n', ''):
                    continue
                priceBrutto = Prices[k].text.split('zł')[0].replace(",", ".")
                tmp = Prices[k].text.split('zł')[1].replace(",", ".")
                tmp1 = tmp.replace("(", "")
                tmp2 = tmp1.replace(")", "")
                priceNetto = tmp2.replace("netto", "").replace(" ", "")
                active = 1
                descriptionFixed = re.sub(r'\n', ' <br>', Descriptions[k][1:])
                descriptionFixed = re.sub(r'\r', ' <br>', descriptionFixed)
                descriptionFixed = descriptionFixed.replace(";", " ")
                descriptionFixed = descriptionFixed.replace("❓", "")
                tmp = randint(0, 1000)
                onSale = 0
                percentageDiscount = 0
                date = '2021-10-01'
                if tmp < 100:
                    onSale = 1
                    percentageDiscount = 20
                elif tmp < 200:
                    onSale = 1
                    percentageDiscount = 15
                elif tmp > 900:
                    date = '2021-11-21'
                coursesFile.write(str(index)+";"+Titles[k].text.replace(';', ' ') + ";" + Categories[k] + ";" + priceBrutto.replace(' ', '') + ";" +
                                  priceNetto + ";" + links[k] + ";" + str(active) + ";" + descriptionFixed + ';' + str(999999) + ";" +
                                  str(onSale) + ";" + date + ";" + str(percentageDiscount) + ";" + '\n')
                index += 1
    categoryCounter += 1
