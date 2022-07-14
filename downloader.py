import requests
from bs4 import BeautifulSoup
import os
import re

url = input("inserisci il link del primo capitolo: ")

r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

lista_capitoli = soup.find('select', class_ = 'chapter custom-select')

def ottieni_link_capitolo(id_attuale, id_successivo, url):

    #separo l'id dal resto del link
    index_id = url.index('read/')
    index_pagine = (url[index_id+5:]).index('/')
    
    id_url = url[index_id+5:]
    id_url = id_url[:index_pagine]

    #sostituisco l'id con quello del prossimo capitolo da scaricare    
    url = url.replace(id_attuale, id_successivo)

    return url

def ottieni_link_immagine(soup):
    link_immagine = soup.find_all('img')
    immagine = []
    
    for immagini in link_immagine:
        immagine.append((format(immagini['src'])))

    del immagine[0]
    link_immagine = str(immagine)

    return link_immagine

def contapagine(soup):
    pagine_totali = soup.find('select', class_ = 'page custom-select')
    pagine = pagine_totali.text
    copia_pagine = pagine
    
    pagine = pagine.replace('/','')
    pagine = pagine[2]

    if '/' in pagine:
        pagine = pagine.replace('/','')

    #verifico se effettivamente le pagine sono giuste, se non lo sono probabilente è perchè le pagine sono troppe, provo a correggerle (funziona con il 90% dei manga)
    if '1/' + pagine not in copia_pagine:
        pagine = copia_pagine
        pagine = pagine.replace('1/','')
        pagine = pagine[:2]

    return pagine

def download_file(url, cartella):
    req = requests.get(url)
    filename = ''
    try:
        if filename:
            pass            
        else:
            filename = cartella + '/' + req.url[url.rfind('/')+1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None
    
#   url = link della prima pagina del capitolo
def download_capitolo(url, cartella, pagine):
    
    l_counter = 1


    while l_counter <= int(pagine):
        download_file(url, cartella)

        l_counter = l_counter + 1
        l_decounter = l_counter - 1

        if '.jpg' not in url:
            url = url.replace(str(l_decounter) + '.png', str(l_counter) + '.png')
        else:
            url = url.replace(str(l_decounter) + '.jpg', str(l_counter) + '.jpg')
    
    
    
#splitto tutte le stringhe in 1 array, eliminando la parola 'Capitolo'
    
id_manga = []
for option in lista_capitoli.find_all('option'):
      id_manga.append((format(option['value'])))


#prima che il programma parta:
cartella = input("in quale cartella vuoi salvare il capitolo?: ")

if not os.path.exists(cartella):
    os.makedirs(cartella)
    print('creo la cartella ' + str(cartella))

#questo array conterrà la lista dei capitoli
capitoli = re.split(r'Capitolo ',str(lista_capitoli.text))
del capitoli[0] #nello slot '0' si trova [''], quidni lo elimino

#I vari counter:
counter = 0
counter_successivo = counter + 1

while counter < len(id_manga):

    #ogni volta che il ciclo si ripete salverà i capitoli in cartelle diverse numerate
    cartella_capitoli = cartella + '/' + capitoli[counter]
    if not os.path.exists(cartella_capitoli):
        os.makedirs(cartella_capitoli)
        print('creo la cartella ' + str(cartella_capitoli))

    #ogni volta che il link cambia mando una richiesta a quello nuovo
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    if counter + 1 > len(id_manga):
        x = input('download completato!')
        exit()

    if counter == (len(id_manga) - 1):
        counter_successivo = 1
    
    id_attuale = id_manga[counter]
    id_successivo = id_manga[counter_successivo]

    url = ottieni_link_capitolo(id_attuale, id_successivo, url)
    link_immagine = str(ottieni_link_immagine(soup))
    link_immagine = link_immagine.replace("['",'')
    link_immagine = link_immagine.replace("']",'')
    pagine_totali = contapagine(soup)

    
    download_capitolo(link_immagine, cartella_capitoli, pagine_totali)
    print('scarico il capitolo ' + capitoli[counter])
    
    
    counter = counter + 1
    counter_successivo = counter + 1

x = input('download completato!')
exit()
