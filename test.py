import requests
from bs4 import BeautifulSoup

url = "https://minfin.com.ua/currency/nbu/"

sourse = requests.get(url)
main_text = sourse.text
soup = BeautifulSoup(main_text)

table = soup.find('table', {'class' : 'data'})
tr = table.find('td', {'class' : 'responsive-collapsed'})
tr = tr.text

print(tr[:5])