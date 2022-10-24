# have to install these on your computer
from bs4 import BeautifulSoup
import requests as rq
import csv 
import os
import re

mainpage = rq.get("https://collections.si.edu/search/gallery.htm?og=national-museum-of-the-american-indian")
mainpagesoup = BeautifulSoup(mainpage.text, "html.parser")

categories = []
for link in mainpagesoup.find_all('a'):
    if link.has_attr('href'):
        categories.append(link.attrs['href'])
categories = [lin for lin in categories if 'results.htm?' in lin]

#gets link by category
for link in categories:
    link = link[:0] + "https://collections.si.edu/search/" + link[0:]


    paintings = rq.get(link)
    paintingsoup = BeautifulSoup(paintings.text, "html.parser")
    individuals = []
    for link in paintingsoup.find_all('a'):
        if link.has_attr('href'):
            individuals.append(link.attrs['href'])
            
    individuals = [lin for lin in individuals if '=data_source' in lin]
    individuals = [lin for lin in individuals if '/detail' in lin]


    contentlinks = [] #links of all individual pages

    for lin in individuals:
        lin = lin[:0] + "https://collections.si.edu" + lin[0:]
        contentlinks.append(lin)

    # count = 0

    with open('art scraper/content.csv', mode='a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["title", "culture/people", "media/materials", "object type", "place", "collection history","image"])
        for i in contentlinks:
            content = rq.get(i)
            # print(i)
            # count += 1
            # if count == 20:
            #     break
            contentsoup = BeautifulSoup(content.text, "html.parser")

            name = contentsoup.findAll("dd",{"class":"physicalDescription-first"})
            if name: #checks for empy lists
                name = name[0].getText()
                name = name.strip()
            else:
                name = None
            culture = contentsoup.findAll("dd",{"class":"name-first"})
            if culture:
                culture = culture[0].getText()
                culture = culture.strip()
                culture = culture.replace("Search this", "")
            # print('<p class="content"> CULTURE/PEOPLE:' + culture + '</p>' )

            media = contentsoup.findAll("dd",{"class":"physicalDescription"})
            if media:
                media = media[1].getText()
                media = media.strip()
                media = media.replace('"', '')
            # print('<p class="content"> MEDIA/MATERIALS:' + media + '</p>')

            otype = contentsoup.findAll("dd",{"class":"objectType-first"})
            if otype:
                otype = otype[0].getText()
                otype = otype.strip()
            # print('<p class="content"> OBJECT TYPE:' + otype + '</p>')

            place = contentsoup.findAll("dd",{"class":"place-first"})
            if place:
                place = place[0].getText()
                place = place.strip()
            # print('<p class="content"> PLACE:' + place + '</p>')

            history = contentsoup.findAll("dd",{"class":"notes-first"})
            if history:
                history = history[0].getText()
                history = history.strip()
                history = history.replace('"', '')
            # print('<p class="content"> COLLECTION HISTORY::' + history + '</p>')

            for div in contentsoup.find_all('div', 'media'):
                image = div.find('img')
                image = image['src'].replace("max=140","")
                # print(image)

            if name:
                writer.writerow([name, culture, media, otype, place, history, image])
