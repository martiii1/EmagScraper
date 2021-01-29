import requests
from bs4 import BeautifulSoup
import re


def leave_only_numbers(text):
    regex = r"\d"

    matches = re.findall(regex, text, re.MULTILINE)
    num = 0
    num_len = len(matches)
    for i in range(num_len):
        num = num + int(matches[i]) * (10 ** (num_len - i - 1))
    return num


def get_items_form_emag(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('.card')

    all_products = []

    for product in items:

        try:
            info = product.select('.card-section-mid')
            price = leave_only_numbers(product.select('.product-new-price')[0].getText()) / 100
            link = info[0].select('a[href^="https"]')[0].get('href', None)
            description = info[0].select('a')[0].get('title', None)

            all_products.append({'title': description, 'link': link, 'price': price})
        except IndexError:
            print("All data fetched!")
            break

    return all_products


def encode_dictionary(item_dict):
    try:
        for item in item_dict:
            item['title'] = item['title'].encode('utf-8', 'ignore')
            item['link'] = item['link'].encode('utf-8', 'ignore')
            item['price'] = str(item['price']).encode('utf-8', 'ignore')
        return item_dict
    except:
        return None


def write_info_to_file(file_name, raw_info):
    with open(file_name, 'ab') as file:
        encoded_dic = encode_dictionary(raw_info)

        if encoded_dic is None:
            return

        for item in encoded_dic:
            file.write(item['title'])
            file.write("\n".encode('utf-8', 'ignore'))
            file.write(item['link'])
            file.write("\n".encode('utf-8', 'ignore'))
            file.write(item['price'])
            file.write("\n".encode('utf-8', 'ignore'))
            file.write("\n".encode('utf-8', 'ignore'))
            file.write("\n".encode('utf-8', 'ignore'))


def get_next_link(link, page_num=0):
    if page_num == 0:
        link = link + r"/c"
    else:
        link = link + r"/p" + str(page_num) + r"/c"
    return link


my_link = r"https://www.emag.bg/slushalki-kompiutyr/filter/tip-f6328,gaming-v23004"

number_of_pages = int(input('Pages: '))

for number in range(number_of_pages + 1):
    products_collected = get_items_form_emag(get_next_link(my_link, number))
    write_info_to_file('test.txt', products_collected)
    
    
