import requests  # required for HTTP requests: pip install requests
from bs4 import BeautifulSoup  # required for HTML and XML parsing                                                              # required for HTML and XML parsing: pip install beautifulsoup4
import pandas as pd  # required for getting the data in dataframes : pip install pandas
import time  # to time the requests
from multiprocessing import Process, Queue, Pool, Manager
import threading
import sys
import re
from lxml.html import fromstring
from itertools import cycle
import traceback
from pymongo import MongoClient

# name
# brand
# price
# inches
# res
# tags
# show
# panel
# res_time
# frec

#def get_proxies():
#    url = 'https://free-proxy-list.net/'
#    response = requests.get(url)
#    parser = fromstring(response.text)
#    proxies = set()
#    for i in parser.xpath('//tbody/tr')[:10]:
#        if i.xpath('.//td[7][contains(text(),"yes")]'):
#            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
#                              i.xpath('.//td[2]/text()')[0]])
#            proxies.add(proxy)
#    return proxies

no_pages = 4  # no of pages to scrape in the website (provide it via arguments)




findingElement = 'li'
findingClass = 'product-block'

findingName = 'GTM-productClick'
findingBrand = 'c-product-card'
findingPrice = 'cart text-black addToCart GTM-addToCart add-to-cart-btn show-movil-land-up f-right cursor-pointer'
findingImage = 'img-product-list'
findingUrl = 'card-product-img'

# proxies = { # define the proxies which you want to use
#   'http': 'http://167.172.191.249:39193',
#   'https': 'http://195.22.121.13:443',
# }
# proxies = get_proxies()
# proxy_pool = cycle(proxies)


def get_data(pageNo, q, link):
    # proxy = next(proxy_pool)
    # proxies={"http": proxy, "https": proxy}
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    r = requests.get(link+'?pagina='+str(pageNo), headers=headers)
    #print(r.text)
    content = r.content
    soup = BeautifulSoup(content)
    print(soup.head.title)
    for d in soup.findAll(findingElement, attrs={'class': findingClass}):
        #print(d.text)
        name = d.find('div', attrs={'class': findingName})
        #brand = d.find('article', attrs={'class': findingBrand})
        price = d.find('a', attrs={'class': findingPrice})
        brand = d.find("meta", itemprop="brand")
        image = d.find('img', attrs={'class': findingImage})
        url = d.find('div', attrs={'class': findingUrl})
        id = d.find('div', attrs={'class': findingUrl})
        #print(name.text, price.text)

        all = []
        #all.append(re.findall(r"(?<=dp/)[A-Z0-9]{10}", url['href'])[0])
        if name is not None:
            all.append(name['data-name'])
        else:
          all.append("unknown-product")
        if brand is not None:
            all.append(brand['content'])
        else:
            all.append("unknown-brand")
        if price is not None:
            all.append(price['data-price'])
        else:
            all.append('0€')
        if image is not None:
            all.append(image['src'])
        else:
            all.append('')
            #all.append('')
        if url is not None:
            all.append('https://www.dynos.es/' + url['dirzone'])
        else:
            all.append('')
        if id is not None:
            all.append(name['data-id'])
        else:
            all.append('')
        q.put(all)
    print("---------------------------------------------------------------")
    results = []


if __name__ == "__main__":
    links = [
        'https://www.dynos.es/monitores/27-pulgadas/2560-x-1440',
        'https://www.dynos.es/monitores/27-pulgadas/2560-x-1440/1-ms',
        'https://www.dynos.es/monitores/31-5-pulgadas/2560-x-1440',
        
        'https://www.dynos.es/monitores/22-pulgadas/1920-x-1080-full-hd',
        'https://www.dynos.es/monitores/31-5-pulgadas/1920-x-1080-full-hd',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/24-pulgadas/gaming',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/24-pulgadas/gaming/altavoces',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/24-pulgadas/',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/24-pulgadas/altavoces',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/27-pulgadas/gaming',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/27-pulgadas/gaming/altavoces',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/27-pulgadas/altavoces',
        'https://www.dynos.es/monitores/1920-x-1080-full-hd/27-pulgadas/',
        'https://www.dynos.es/monitores/27-pulgadas/3840-x-2160-uhd',
        'https://www.dynos.es/monitores/28-pulgadas/3840-x-2160-uhd',
        'https://www.dynos.es/monitores/3840-x-2160-uhd/42-5-pulgadas',
        'https://www.dynos.es/monitores/10-41-pulgadas/15-pulgadas/19-5-pulgadas/21-5-pulgadas/22-pulgadas/23-6-pulgadas/23-8-pulgadas/23-pulgadas/2560-x-1440'
    ]
    attribs = [ {"inches":27, "res":1440, "tags": ["Audio", "Gaming"], "show": ["1440p", "Gaming", "Mediano"], "res_time": 5, "frec": 60},
                {"inches":27, "res":1440, "tags": ["Audio", "Gaming"], "show": ["1440p", "Gaming", "1ms", "Mediano"], "res_time": 10, "frec": 60},
                {"inches":31.5, "res":1440, "tags": ["Gaming"], "show": ["1440p", "Gaming", "Grande"], "res_time": 5, "frec": 60},

                {"inches":22, "res":1080, "tags": [], "show": ["Full HD", "Pequeño"], "res_time": 5, "frec": 60},
                {"inches":31.5, "res":1080, "tags": ["Gaming"], "show": ["Full HD", "Gaming", "Grande"], "res_time": 5, "frec": 165},
                {"inches":24, "res":1080, "tags": ["Gaming"], "show": ["Full HD", "Gaming", "Mediano"], "res_time": 5, "frec": 144},
                {"inches":24, "res":1080, "tags": ["Gaming", "Audio"], "show": ["Full HD", "Gaming", "Mediano"], "res_time": 5, "frec": 144},
                {"inches":24, "res":1080, "tags": [], "show": ["Full HD", "Mediano"], "res_time": 5, "frec": 60},
                {"inches":24, "res":1080, "tags": ["Audio"], "show": ["Full HD", "Mediano"], "res_time": 5, "frec": 75},
                {"inches":27, "res":1080, "tags": ["Gaming"], "show": ["Full HD", "Gaming", "Mediano"], "res_time": 5, "frec": 60},
                {"inches":27, "res":1080, "tags": ["Gaming", "Audio"], "show": ["Full HD", "Gaming", "Mediano"], "res_time": 3, "frec": 144},
                {"inches":27, "res":1080, "tags": ["Audio"], "show": ["Full HD", "Mediano"], "res_time": 8, "frec": 60},
                {"inches":27, "res":1080, "tags": [], "show": ["Full HD", "Mediano"], "res_time": 10, "frec": 60},
            



                {"inches": 27, "res": 2160, "tags": ["Audio"], "show": ["UHD", "Display Port"], "res_time": 5, "frec": 60},
                {"inches": 28, "res": 2160, "tags": ["Audio", "Gaming"], "show": ["UHD", "Gaming", "Grande"], "res_time": 1, "frec": 60},
                {"inches": 42.5, "res": 2160, "tags": ["Audio", "Gaming"], "show": ["UHD", "Gaming", "Grande"], "res_time": 8, "frec": 60},
                {"inches": 23, "res": 1440, "tags": [], "show": ["Pequeño", "1440p"], "res_time": 8, "frec": 60}
            ]
    linkIndex = 0
    lista_result = []
    while linkIndex < len(links):
        m = Manager()
        q = m.Queue()
        p = {}
        startTime = time.time()
        qcount = 0  # the count in queue used to track the elements in queue
        ids = []
        products = []  # List to store name of the product
        brands = []  # Brands
        prices = []  # List to store price of the product
        images = []  # Images
        urls = []  # URLS
        for i in range(1, no_pages):
            print("starting thread: ", i)
            p[i] = threading.Thread(target=get_data, args=(
                i, q, links[linkIndex]))
            p[i].start()
        for i in range(1, no_pages):  # join all the threads/processes
            p[i].join()
        while q.empty() is not True:
            qcount = qcount+1
            queue_top = q.get()
            products.append(queue_top[0])
            brands.append(queue_top[1])
            prices.append(queue_top[2])
            images.append(queue_top[3])
            urls.append(queue_top[4])
            ids.append(queue_top[5])
            result={"_id":ids[qcount-1], "name": products[qcount-1], "brand": brands[qcount-1], "price": float(prices[qcount-1]), "inches":attribs[linkIndex]["inches"], "res":attribs[linkIndex]["res"], "tags":attribs[linkIndex]["tags"], "show":attribs[linkIndex]["show"], "frec":attribs[linkIndex]["frec"], "res_time":attribs[linkIndex]["res_time"], "url":urls[qcount-1], "img":images[qcount-1]}
            if not any(d['_id'] == result["_id"] for d in lista_result):
                lista_result.append(dict(result))
        print("total time taken: ", str(
            time.time()-startTime), " qcount: ", qcount)
        print([len(products), len(brands), len(prices),
              len(images), len(urls)])
        # print([len(products), len(prices)])
        #df = pd.DataFrame({'name': products, 'brand': brands, 'Price': prices,
                            #'image': images, 'url': urls})
        # df = pd.DataFrame({'Product Name':prices})
        # df.to_csv('monitores.csv', mode='a',
                  # index=False, header=False, encoding='utf-8')
    
        linkIndex += 1
    print(ids)
    print(len(lista_result))
    client = MongoClient("mongodb+srv://chemon:CHEMON@cluster0.xx7nr.mongodb.net/monitorwatch?retryWrites=true&w=majority")
    # res_list = [i for n, i in enumerate(lista_result) if i not in lista_result[n + 1:]]
    db=client.monitorwatch
    monitores=db.monitores
    db.monitores.insert_many(lista_result, ordered=False)
