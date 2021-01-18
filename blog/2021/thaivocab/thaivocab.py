from pythainlp import tokenize
from bs4 import BeautifulSoup
import requests
import re
import time

def getthaipbs():
    response = requests.get("https://news.thaipbs.or.th/archive", "html.parser")
    soup = BeautifulSoup(response.text)
    articles = soup.find_all('article')
    hrefs = []
    for article in articles:
        link = article.a
        if (link is None): continue
        href = link['href']
        hrefs.append(href)
    
    results = []
    for href in hrefs:
        # print(href)
        response = requests.get(href)
        soup = BeautifulSoup(response.text)
        article = soup.article
        # print(article.get_text())
        results.append(article.get_text())
    
    return results

languages = [
    "Pali", 
    "Sanskrit", 
    "Proto-Southwestern Tai", 
    "Proto-Tai", 
    "Chinese", 
    "Middle Chinese", 
    "Old Chinese", 
    "Teochew", 
    "Khmer", 
    "Modern Khmer", 
    "Middle Khmer", 
    "Old Khmer", 
    "English", 
    "French", 
    "Portuguese", 
    "Northern Thai", 
    "Lao", 
    "Lü", 
    "Shan", 
    "Tai Nüa", 
    "Ahom", 
    "Zhuang", 
    "Vietnamese", 
    "Burmese", 
]
origindict = {'ONA':0, 'Not Found':0}
def lookupwiktionary(words):
    print(words)
    nonword = r"[^A-Za-z\u0E01-\u0E4C]"
    langregex = "(" + "|".join(languages) + ")"
    for word in words:
        added = False
        if (re.search(nonword, word) is None):
            print(word)
            response = requests.get("https://en.wiktionary.org/wiki/" + word, "html.parser")
            soup = BeautifulSoup(response.text)
            lastline = None
            for line in soup.get_text().split('\n'):
                if (lastline is not None and re.search(r"Etymology.*\[edit\]", lastline) is not None):
                    print(line)
                    frompart = line[line.lower().find('from'):line.find('Cognate')]
                    print(frompart)
                    if (re.search(langregex, frompart) is not None): # first "From"
                        match = re.search(langregex, frompart)
                        print(match.group(0))
                        if (match.group(0) in origindict):
                            origindict[match.group(0)] += 1
                        else:
                            origindict[match.group(0)] = 1
                        added = True
                    elif (line.find('Cognate') != -1):
                        cognatepart = line[line.find('Cognate'):]
                        print(cognatepart)
                        if (re.search(langregex, cognatepart) is not None): # first "Cognate"
                            match = re.search(langregex, cognatepart)
                            print(match.group(0))
                            if (match.group(0) + ' Cognate' in origindict):
                                origindict[match.group(0) + ' Cognate'] += 1
                            else:
                                origindict[match.group(0) + ' Cognate'] = 1
                            added = True
                    else:
                        origindict['ONA'] += 1
                        added = True
                lastline = line
            if added is False:
                origindict['Not Found'] += 1
            print(origindict)
            # time.sleep(1)

def graph(origindict):
    print(origindict)
    return

if __name__ == "__main__":
    articles = getthaipbs()
    for article in articles:
        words = tokenize.word_tokenize(article, engine='attacut', keep_whitespace=False)
        lookupwiktionary(words)
    graph(origindict)