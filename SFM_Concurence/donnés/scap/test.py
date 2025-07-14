from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def extract_competitors_selenium(crunchbase_url):
    options = Options()
    options.add_argument("--headless")  # Mode sans interface graphique
    driver = webdriver.Chrome(options=options)

    driver.get(crunchbase_url)
    time.sleep(5)  # Attendre que la page charge le contenu JS

    competitors = []
    try:
        # Trouver la section compétiteurs (exemple basé sur la structure visible)
        sections = driver.find_elements(By.TAG_NAME, 'section')
        for section in sections:
            header = section.find_element(By.TAG_NAME, 'h2')
            if header and ("Competitors" in header.text or "Alternatives" in header.text):
                links = section.find_elements(By.TAG_NAME, 'a')
                for a in links:
                    name = a.text.strip()
                    if name:
                        competitors.append(name)
                break
    except Exception as e:
        print("Erreur lors de l'extraction avec Selenium :", e)
    finally:
        driver.quit()

    return competitors

if __name__ == "__main__":
    company = "SFM Technologies"
    # Exemple de lien Crunchbase (à récupérer avec une autre méthode si besoin)
    url = "https://www.crunchbase.com/organization/sfm-technologies"
    concurrents = extract_competitors_selenium(url)
    print("Concurrents trouvés via Selenium :")
    for i, c in enumerate(concurrents, 1):
        print(f"{i}. {c}")
