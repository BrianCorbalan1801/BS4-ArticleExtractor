from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re

# Configuración de Selenium
options = Options()
options.headless = False  # Cambia a True si querés que no se abra el navegador
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

def initialize_driver():
    """Inicializa y devuelve un WebDriver con manejo de errores."""
    try:
        return webdriver.Chrome(options=options)
    except Exception as e:
        print(f"🚨 Error al iniciar WebDriver: {e}")
        return None

def clean_price(price):
    """Limpia el precio eliminando caracteres no numéricos."""
    return re.sub(r"[^\d,\.]", "", price)

def get_products(url, supermarket, product_selector, name_class, price_class, link_tag="a"):
    """Extrae productos de una tienda online con parámetros genéricos."""
    driver = initialize_driver()
    if not driver:
        return []

    driver.get(url)
    products = []

    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, product_selector))
        )
        product_elements = driver.find_elements(By.CSS_SELECTOR, product_selector)

        for product in product_elements[:8]:  # 🟡 Solo 8 productos
            try:
                name = product.find_element(By.CSS_SELECTOR, name_class).text.strip()
                price = product.find_element(By.CSS_SELECTOR, price_class).text.strip()
                link = product.find_element(By.TAG_NAME, link_tag).get_attribute('href')

                products.append({
                    'Supermercado': supermarket,
                    'Producto': name,
                    'Precio': clean_price(price),
                    'URL': link
                })
            except Exception as e:
                print(f"⚠️ Error al extraer datos de {supermarket}: {e}")
    except Exception as e:
        print(f"❌ No se pudieron cargar los productos de {supermarket}: {e}")
    finally:
        driver.quit()

    return products

def save_to_csv(products, filename="precios_productos_supermercados.csv"):
    """Guarda los datos en un archivo CSV."""
    if not products:
        print("⚠️ No hay productos para guardar.")
        return

    df = pd.DataFrame(products)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Datos guardados en {filename}")

def main():
    """Función principal."""
    print("📦 Iniciando la extracción de datos de productos...")

    all_products = []

    # 🔹 Supermercado DIA
    all_products.extend(get_products(
        url='https://www.supermercadosdia.com.ar/',
        supermarket='DIA',
        product_selector="section[class^='vtex-product-summary-2-x-container']",
        name_class="span.vtex-product-summary-2-x-productBrand",
        price_class="span.diaio-store-5-x-sellingPriceValue"
    ))

    # 🔹 Supermercado COTO
    all_products.extend(get_products(
        url='https://www.cotodigital.com.ar/sitios/cdigi/nuevositio',
        supermarket='COTO',
        product_selector='div.card-container',
        name_class='h3.nombre-producto',
        price_class='h4.card-title'
    ))

    # 🔹 Supermercado Carrefour
    all_products.extend(get_products(
    url='https://www.carrefour.com.ar/Almacen/Snacks/Papas-fritas-y-snacks-de-maiz',
    supermarket='Carrefour',
    product_selector="div.vtex-product-summary-2-x-container",
    name_class="span.vtex-product-summary-2-x-productBrand",
    price_class="span.vtex-product-price-1-x-sellingPrice",
    link_tag="a"
))


    save_to_csv(all_products)

if __name__ == "__main__":
    main()
