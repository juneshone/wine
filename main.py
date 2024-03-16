from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

import argparse
import datetime
import pandas
import collections


def get_product_categories(product_file):
    pd_product_file = pandas.read_excel(product_file, keep_default_na=False)
    products = pd_product_file.to_dict(orient='records')
    product_categories = collections.defaultdict(list)
    for product in products:
        product_categories[product['Категория']].append(product)
    return product_categories


def get_form_word(year):
    last_digit = year % 10
    last_two_digits = year % 100
    if 11 <= last_two_digits <= 14:
        return 'лет'
    else:
        if last_digit == 1:
            return 'год'
        elif last_digit >= 5 or last_digit == 0:
            return 'лет'
        else:
            return 'года'


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    parser = argparse.ArgumentParser(
        description='Выберите файл с товарами для загрузки на сайт'
    )
    parser.add_argument(
        '--product_file',
        default='wine.xlsx',
        help='Файл с товарами'
    )
    args = parser.parse_args()

    today = datetime.date.today()
    foundation_winery_year = 1920
    delta = today.year - foundation_winery_year

    rendered_page = template.render(
        winery_age=delta,
        form_word=get_form_word(delta),
        product_categories=get_product_categories(args.product_file)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
