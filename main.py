from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import undetected_chromedriver as uc
from time import sleep
import datetime
from create_csv import CsvManager
from upload import upload_csv_to_sheets

google_form = "https://forms.gle/hj7atTojEMec1NHz8"
URL = "https://www.airbnb.com/s/Pickering--ON/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=10&query=Pickering%2C%20ON&place_id=ChIJHY3o-qvZ1IkR2IYnsWJI0ks&date_picker_type=calendar&checkin=2023-04-04&checkout=2023-04-14&source=structured_search_input_header&search_type=filter_change&adults=2&federated_search_session_id=ab90fa63-b1c3-4381-a136-d6286349dc4a&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MiwiaXRlbXNfb2Zmc2V0Ijo0MCwidmVyc2lvbiI6MX0%3D"
PAGES = 5
# DATE_TIME = datetime.datetime.today().strftime("%d-%m-%Y, %H:%M:%S")

CHECK_IN = "2023-04-04"
CHECK_OUT = "2023-04-14"
DATE_RANGE = CHECK_IN + " to " + CHECK_OUT


class DataManager:
    def __init__(self):
        self.driver = uc.Chrome()
        self.driver.maximize_window()
        self.driver.get(URL)
        self.data = []
        self.daily_price = []
        self.total_price = []
        self.description = []
        self.links = []
        self.date_time = datetime.datetime.today().strftime("%d-%B-%Y, %H:%M:%S")

    def get_data(self):
        self.data = self.driver.find_elements(By.CLASS_NAME, "gh7uyir giajdwt g14v8520 dir dir-ltr")
        print(self.data)

    def get_links(self):
        a_tags = self.driver.find_elements(By.XPATH, "//a[contains(@aria-labelledby, 'title_')]")
        [self.links.append(tag.get_attribute('href')) for tag in a_tags]

    def get_prices(self):
        total_prices = self.driver.find_elements(By.CSS_SELECTOR, "._tt122m span")
        [self.total_price.append(price.text.split(' ')[0]) for price in total_prices]

        price_night = self.driver.find_elements(By.CLASS_NAME, "_tyxjp1")
        [self.daily_price.append(price.text) for price in price_night]

    def get_description(self):
        description = self.driver.find_elements(By.CLASS_NAME, 't6mzqp7')
        [self.description.append(d.text) for d in description]

    def next_page(self):
        next_page = self.driver.find_element(By.CLASS_NAME, '_1bfat5l')
        next_page.click()


if __name__ == '__main__':
    write = CsvManager()
    data = DataManager()
    for _ in range(0, PAGES):
        data.get_links()
        data.get_prices()
        data.get_description()
        sleep(2)
        data.next_page()
        sleep(5)
    print(f"length: {len(data.total_price)}")
    print(f"length: {len(data.daily_price)}")
    print(f"length: {len(data.description)}")
    print(f"length: {len(data.links)}")
    print(f"{DATE_RANGE}:{data.date_time} \n"
          f"{data.description} \n"
          f"{data.total_price} \n"
          f"{data.daily_price} \n"
          f"{data.links}")
    write.write_csv(data.date_time, DATE_RANGE,
                    data.description, data.total_price,
                    data.daily_price, data.links)
    sleep(3)
    upload_csv_to_sheets()
