import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from time import sleep



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
    product_data['product_description'] = product.find('p', class_="").text
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




base_url = "http://books.toscrape.com/"
all_urls = get_all_url_product(base_url)
collected_data = []
for url in all_urls:
    collected_data.append(get_data_from_product_page(url))
    sleep(1.5)
print(collected_data[18])