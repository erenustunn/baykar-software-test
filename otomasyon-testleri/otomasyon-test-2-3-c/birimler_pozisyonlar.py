from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import re
import time

class WebScraper:
    def __init__(self, wait_time=15):
        chrome_service = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, wait_time)
        self.all_units = []
        self.all_positions = []

    def get_units(self, url):
        self.driver.get(url)
        unit_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="myUL2"]/div')))
        self.all_units = [
            re.sub(r'\d+', '', unit.text.replace('\n', '').strip()) for unit in unit_elements
        ]
        self.all_units = [unit.strip() for unit in self.all_units if unit.strip()]

    def get_positions(self, base_url, start_page=1):
        page = start_page
        while True:
            url = f"{base_url}?type=1&page={page}"
            self.driver.get(url)
            time.sleep(1)

            try:
                positions_element = self.wait.until(
                    EC.presence_of_element_located((By.ID, 'filterOpenPositions'))
                )
                positions = [position.text for position in positions_element.find_elements(By.TAG_NAME, "h3")]

                if not positions:
                    print(f"Sayfa {page}'de pozisyon bulunamadı, döngü sonlandırılıyor.")
                    break

                self.all_positions.extend(positions)
                print(f"Sayfa {page} tamamlandı.")
                page += 1

            except Exception as e:
                print(f"Hata: {e}")
                break

    def close(self):
        self.driver.quit()

    def open_unit_or_position_page(self, base_url, search_term):
        search_term_formatted = search_term.replace(' ', '%20')
        url = f"{base_url}?type=1&search={search_term_formatted}"
        print(f"Şu sayfaya gidiliyor: {url}")
        self.driver.get(url)
        self.wait.until(EC.title_contains("Baykar"))
        print("Sayfa başarıyla açıldı.")


class ResourceManager:
    @staticmethod
    def check_and_create_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def save_units_and_positions(scraper, unit_file, position_file):
        scraper.save_to_file(scraper.all_units, unit_file)
        scraper.save_to_file(scraper.all_positions, position_file)


def main():
    ResourceManager.check_and_create_directory("resources")
    scraper = WebScraper()


    scraper.get_units("https://kariyer.baykartech.com/tr/open-positions/?type=1&page=1")
    scraper.get_positions("https://kariyer.baykartech.com/tr/open-positions/")


    print("\nBirimler:")
    for idx, unit in enumerate(scraper.all_units):
        print(f"{idx + 1}. {unit}")

    print("\nPozisyonlar:")
    for idx, position in enumerate(scraper.all_positions):
        print(f"{idx + 1}. {position}")


    choice_type = input("\nBirim veya pozisyon açmak için 'b' ya da 'p' girin: ").lower()
    if choice_type == 'b':
        choice_index = int(input("Açmak istediğiniz birim numarasını girin: ")) - 1
        selected_term = scraper.all_units[choice_index]
    elif choice_type == 'p':
        choice_index = int(input("Açmak istediğiniz pozisyon numarasını girin: ")) - 1
        selected_term = scraper.all_positions[choice_index]
    else:
        print("Geçersiz seçim!")
        scraper.close()
        return


    scraper.open_unit_or_position_page("https://kariyer.baykartech.com/tr/open-positions/", selected_term)
    time.sleep(20)
    scraper.close()


if __name__ == "__main__":
    main()
