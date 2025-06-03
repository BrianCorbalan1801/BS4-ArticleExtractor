from newspaper import Article
import csv

def extract_and_save(url, filename='articles.csv'):
    article = Article(url)
    article.download()
    article.parse()
   
    data = [
        {'field': 'Titulo', 'value': article.title},
        {'field': 'Autor', 'value': ' : '.join(article.authors)},
        {'field': 'Fecha_publicacion', 'value': article.publish_date},
        {'field': 'Contenido', 'value': article.text.replace('\n', ' ')}
    ]
   
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=':')
        for item in data:
            writer.writerow([item['field'], item['value']])
        writer.writerow([])

urls = ['https://tn.com.ar/']
for url in urls:
    extract_and_save(url)