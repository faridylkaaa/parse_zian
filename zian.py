import requests
import lxml
from bs4 import BeautifulSoup
from time import sleep

headers = {'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

url = 'https://ulyanovsk.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=4736&offer_type=flat&p=1&type=4'

lst = []

def get_page():
    i = 1
    while True:
        response = requests.get(f'https://ulyanovsk.cian.ru/cat.php?deal_type=rent&engine_version=2&location%5B0%5D=4736&offer_type=flat&p={i}&type=4')
        if i != 1 and response.url == url:
            break
        else:
            i += 1
            yield response
            
def get_flat(url_flat):
    sleep(1)
    response = requests.get(url_flat, headers=headers)
    response_text = response.text
    soup = BeautifulSoup(response_text, 'lxml')
    all_inf = soup.find('div', class_='a10a3f92e9--center--b3Pm0')
    cost = soup.find('div', class_='a10a3f92e9--container--MWnM2 a10a3f92e9--container--sticky--H1UBn a10a3f92e9--container--not-hidden--_a5YN')
    rooms = all_inf.find('h1', class_='a10a3f92e9--title--vlZwT').text.split(',')[0]
    s = all_inf.find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text.split('&')[0]
    url = response.url
    i = all_inf.find_all('div', class_='a10a3f92e9--item--Jp5Qv')
    for para in i:
        fl = para.find('span', class_='a10a3f92e9--color_gray60_100--mYFjS a10a3f92e9--lineHeight_4u--E1SPG a10a3f92e9--fontWeight_normal--JEG_c a10a3f92e9--fontSize_12px--pY5Xn a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY a10a3f92e9--text_letterSpacing__0--cQxU5')
        if fl.text == 'Этаж':
            floor = para.find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text.replace(' из ', '/')
    price = cost.find('div', class_='a10a3f92e9--amount--ON6i1').find('span', class_='a10a3f92e9--color_black_100--Ephi7 a10a3f92e9--lineHeight_9u--limEs a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_28px--P1gR4 a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY').text
    
    # lst.append([rooms, cost, s, floor, price, url])
    return rooms, s, floor, price, url
    
def flat():
    for response in get_page():
        res_text = response.text
        soup = BeautifulSoup(res_text, 'lxml')
        cards = soup.find('div', class_='_93444fe79c--wrapper--W0WqH').find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
        for card in cards:
            url_flat = card.find('a').get('href')
            yield get_flat(url_flat)