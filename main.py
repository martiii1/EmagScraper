import requests
from bs4 import BeautifulSoup
import re


class ProductInfo:
    def __init__(self):
        self.price = 0.0
        self.link = ""
        self.description = ""

    def encode_product_info_uft8(self):
        """ Returns a new object with all parameters encoded in UTF-8. """

        encoded_product = ProductInfo()

        encoded_product.description = self.description.encode('utf-8', 'ignore')
        encoded_product.link = self.link.encode('utf-8', 'ignore')
        encoded_product.price = str(self.price).encode('utf-8', 'ignore')
        return encoded_product


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
            current_product = ProductInfo()

            info = product.select('.card-section-mid')

            # Price = numbers / 100 because the number is the price and the last 2 digits are 'Stotinki'
            current_product.price = leave_only_numbers(product.select('.product-new-price')[0].getText()) / 100

            # Gets the link to the page of the current product
            current_product.link = info[0].select('a[href^="https"]')[0].get('href', None)

            # Gets the basic card description of the current product
            current_product.description = info[0].select('a')[0].get('title', None)

            # Adds the current product to the list of all products as a dict
            all_products.append(current_product)
        except IndexError:
            # print("End of page!")
            break

    return all_products


def write_info_to_file(file_name, raw_data_list):
    with open(file_name, 'ab') as file:
        for item in raw_data_list:
            encoded_item = item.encode_product_info_uft8()

            file.write(encoded_item.description)
            file.write("\n".encode('utf-8', 'ignore'))

            file.write(encoded_item.link)
            file.write("\n".encode('utf-8', 'ignore'))

            file.write(encoded_item.price)
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
text_file_name = "testNew.txt"

number_of_pages = int(input('Pages: '))

for number in range(number_of_pages + 1):
    products_collected = get_items_form_emag(get_next_link(my_link, number))
    write_info_to_file(text_file_name, products_collected)

print(f"The data from the site was saved on a text file: {text_file_name}")
