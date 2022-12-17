from bs4 import BeautifulSoup
import requests
url = 'http://127.0.0.1:8000/'
response = requests.get(url)
htmlContent = response.content
# print(htmlContent)
soup = BeautifulSoup(htmlContent)
# soup = soup.prettify
all_div = soup.find_all('div',attrs={'class':'card-body'})
img = soup.find_all('img')
for img in img:
    print(img.get('src'))
