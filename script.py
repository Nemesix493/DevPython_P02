import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep
import csv



def get_all_url_product(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    products = soup.find_all("article", class_="product_pod")
    urls = []
    for product in products:
        urls.append(urljoin(url, product.find("a")['href']))
    return urls

def get_data_from_product_page(url):
    response = requests.get(url)
    product_data = {'product_page_url' : url}
    soup = BeautifulSoup(response.content, "html.parser")
    product = soup.find('div', class_="content")
    product_data['image_url'] = urljoin(url, product.find('img')['src'])
    product_data['product_description'] = product.find('p', class_="").text.replace('\n', '')
    table_lines = product.find('table').find_all('tr')
    product_data['universal_product_code'] = table_lines[0].find('td').text
    product_data['price_excluding_tax'] = table_lines[2].find('td').text.replace('£', '')
    product_data['price_including_tax'] = table_lines[3].find('td').text.replace('£', '')
    product_data['review_rating'] = table_lines[6].find('td').text
    product_data['title'] = product.find('h1').text
    availability = product.find('p', class_="availability")
    if 'instock' in availability['class']:
        product_data['number_available'] = availability.text.replace(' ','').replace('\n\n\nInstock(', '').replace('available)\n\n','')
    else:
        product_data['number_available'] = "0"
    product_data['review_rating'] = product.find('p', class_='star-rating')['class'][1]
    product_data['category'] = soup.find('ul', class_="breadcrumb").find_all('li')[2].text.replace('\n', '')
    return product_data

def get_all_categorys_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find('ul', class_="nav-list").find('ul').find_all('a')
    categorys_data = []
    for link in links:
        categorys_data.append({
            'link': urljoin(url,link['href']),
            'name': link.text.replace(' ', '').replace('\n', ''),
        })
    return categorys_data

def brows_category_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    books_number = int(soup.find('form', class_="form-horizontal").find('strong').text)
    pages_number = books_number//20
    if books_number%20 > 0 :
        pages_number += 1
    links = [url]
    for i in range(pages_number-1):
        links.append(urljoin(url,"page-" + str(i+2) + ".html"))
    return links


base_url = "http://books.toscrape.com/"

categorys = get_all_categorys_data(base_url)
print(brows_category_pages(categorys[3]['link']))

"""all_urls = get_all_url_product(base_url)
collected_data = []
for url in all_urls:
    collected_data.append(get_data_from_product_page(url))
    #sleep(1.5)

with open('datas.csv', 'w', newline='') as fichier_csv:
   # Créer un objet writer (écriture) avec ce fichier
   writer = csv.writer(fichier_csv, delimiter=',')
   writer.writerow(list(collected_data[0].keys()))
   for data in collected_data:
      writer.writerow(list(data.values()))
"""