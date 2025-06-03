import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Función para extraer datos de un supermercado
def extraer_datos_dia():
    url = "https://diaonline.supermercadosdia.com.ar/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
   
    productos = []
   
    # Aquí debes ajustar el selector según la estructura HTML de la página
    for item in soup.select('.product-item'):
        nombre = item.select_one('.product-name').text.strip()
        precio = item.select_one('.product-price').text.strip()
        enlace = item.select_one('a')['href']
        productos.append(['DIA', nombre, precio, enlace])
   
    return productos

def extraer_datos_coto():
    url = "https://www.cotodigital3.com.ar/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
   
    productos = []
   
    # Ajusta el selector según la estructura HTML de la página
    for item in soup.select('.product-item'):
        nombre = item.select_one('.product-name').text.strip()
        precio = item.select_one('.product-price').text.strip()
        enlace = item.select_one('a')['href']
        productos.append(['COTO', nombre, precio, enlace])
   
    return productos

def extraer_datos_carrefour():
    url = "https://www.carrefour.com.ar/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
   
    productos = []
   
    # Ajusta el selector según la estructura HTML de la página
    for item in soup.select('.product-item'):
        nombre = item.select_one('.product-name').text.strip()
        precio = item.select_one('.product-price').text.strip()
        enlace = item.select_one('a')['href']
        productos.append(['Carrefour', nombre, precio, enlace])
   
    return productos

def main():
    print("🚀 Iniciando la extracción de datos...")
   
    # Extraer datos de cada supermercado
    datos_dia = extraer_datos_dia()
    datos_coto = extraer_datos_coto()
    datos_carrefour = extraer_datos_carrefour()
   
    # Combinar todos los datos
    todos_los_datos = datos_dia + datos_coto + datos_carrefour
    df = pd.DataFrame(todos_los_datos, columns=['Supermercado', 'Producto', 'Precio', 'URL'])
    df['Precio'] = df['Precio'].str.replace('$', '').str.replace('.', '').astype(float)
    df.to_csv('productos_supermercados.csv', index=False)
   
    print("✅ La extracción ha finalizado exitosamente. Los datos se han guardado en 'productos_supermercados.csv'.")

if __name__ == "__main__":
    main()