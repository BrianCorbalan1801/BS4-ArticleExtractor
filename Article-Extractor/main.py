import requests
from bs4 import BeautifulSoupimport pandas as pd

# URL del artículo

url = 'https://tn.com.ar/politica/2025/03/11/temporal-en-bahia-blanca-la-justicia-recibio-mas-de-200-llamados-por-personas-incomunicadas/'

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

article_content = soup.find('article')

if article_content:    
	article_text = article_content.get_text(strip=True)
else:    
	article_text = "No se encontró contenido de artículo."

df = pd.DataFrame({'Article Content': [article_text]})

print(df)

