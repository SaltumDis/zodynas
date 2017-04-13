import string
import urllib.request as request

import requests
from bs4 import BeautifulSoup
from bs4 import Tag

class WordParser(object):

    def getHtmlWords(self, letter):
        try:
            with request.urlopen('http://ims.mii.lt/ALK%C5%BD/'+letter+'.html') as response:
                webPage = response.read()
            soup = BeautifulSoup(webPage)
            listsOfP=[]
            for tr in soup.findAll('tr'):
                dict = []
                for p in tr.findAll('p'):
                    text=p.text
                    if type(p.next) is Tag:
                        if p.next.has_attr("href"):
                            text={p.text:"http://ims.mii.lt" + p.next["href"][2:]}
                    dict.append(text)
                listsOfP.append(dict)
            self.removeFirstLast(listsOfP)
            formatedList=self.formatValues(listsOfP)
            print("done with letter: "+ letter)
            return formatedList
        except request.HTTPError:
            print("HTTP ERROR!")
        except request.URLError:
            print("URL ERROR!")


    def formatValues(self, listOfWords):
        removable=[]
        for i in range(0, len(listOfWords)):
            if listOfWords[i][0].isspace():
                removable.append(i)
        for i in range(len(removable)-1,-1,-1):
            listOfWords[removable[i]-1]+=(listOfWords[removable[i]][1:])
        for i in range(len(removable)-1,-1,-1):
            listOfWords.pop(removable[i])
        return listOfWords


    def removeFirstLast(self, list):
        list.pop(0)
        list.pop(len(list)-1)

    def populateDB(self, url):
        import time
        start = time.time()
        for char in list(string.ascii_lowercase):
            parsed=self.getHtmlWords(char)
            for words in parsed:
                eng=words[0]
                for word in words[1:]:
                    if isinstance(word, dict):
                        ltWord, link = word.popitem()
                        r = requests.post(url, data={'engWord': eng, 'ltWord': ltWord, 'link': link})
                    else:
                        r = requests.post(url, data={'engWord': eng, 'ltWord': word})
                    if r.status_code != 200:
                        print("Error with word "+ word)
        end = time.time()
        elapsed = end - start
        print("took "+ str(elapsed))

WordParser().populateDB("http://127.0.0.1:5000/add")