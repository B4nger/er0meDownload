# %%
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re


# %%
url = input('Paste URL: ')
req = Request(url)
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

# %%
usableLinks = []
if url[21:24] == '/a/':
    usableLinks.append(url)
else:
    allPages = []
    if url[21:24] != '/a/':
        for i in links:
            if i[i.find('='):][0] == '=':
                allPages.append(int(i[i.find('=')+1:]))
    try:
        maxPage = max(allPages)
    except:
        maxPage = 0
    for i in links:
        if i[21:24] == '/a/':
            usableLinks.append(i)
    if maxPage != 0:
        for page in range(0,maxPage):
            newLink =  url+'?page='+str(page)
            req = Request(newLink)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            linksOnPage = []
            for l in soup.findAll('a'):
                linksOnPage.append(l.get('href'))
            for l in linksOnPage:
                if l[21:24] == '/a/':
                    usableLinks.append(l)
        

# %%
import os

# %%
allFiles = []
for l in usableLinks:
    allFiles += os.popen('gallery-dl'+' -g '+l).read().split('\n')
for i in allFiles:
    if i[-4:] != '.mp4':
        allFiles.remove(i)
allFiles = list(dict.fromkeys(allFiles))

# %%
def save_to_file(text):

    with open('urls', mode='wt', encoding='utf-8') as myfile:
        myfile.write('\n'.join(text))
        myfile.write('\n')


        

# %%
save_to_file(allFiles)

# %%
print('Now run: wget --referer "er0me.com" --no-check-certificate  --input-file=urls')
print('End of script.')


