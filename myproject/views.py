from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_py  # Automatically manages the ChromeDriver path
import time

def open_chrome(request):
    url = request.GET.get('url', 'http://54.221.153.85:8000/plant/productlist/')
    token = request.GET.get('token',"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM1ODUzMzYzLCJpYXQiOjE3MzU4MzUzNjMsImp0aSI6IjRkNWQyZTBjZTljYjRhZTE5OTE5MjcxMzEyNjBkZmFiIiwidXNlcl9pZCI6MTB9.Ezfx2JpbB_ZfH6ESThjDmhEM--5Ojm1RBJY8jUnuwIc")
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chromedriver_path = chromedriver_py.binary_path
    driver = None

    try: 
        # Setup Chrome WebDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {
            "headers": {"Authorization": f"Bearer {token}"}
        })

        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))

        fields = [
            ("name", "Sample Data"),
            ("description", "Sample Data"),
            ("image", "Sample Data"),
            ("days_to_maturity", "Sample Data"),
            ("mature_speed", "Sample Data"),
            ("mature_height", "Sample Data"),
            ("fruit_size", "Sample Data"),
            ("family", "Sample Data"),
            ("type", "Sample Data"),
            ("native", "Sample Data"),
            ("hardiness", "Sample Data"),
            ("exposure", "Sample Data"),
            ("plant_dimension", "Sample Data"),
            ("variety_info", "Sample Data"),
            ("attributes", "Sample Data")
        ]

        # Fill fields
        for field_name, value in fields:
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, field_name))
            )
            input_field.send_keys(value)

        # Select dropdown option
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "category"))
        )
        select = Select(dropdown)
        select.select_by_visible_text("New cat")

        # Click the button
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and text()='POST']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)

        time.sleep(5)  # Wait for potential server response after the click
        return HttpResponse(f"Opened Chrome, filled the form, and navigated to: {url}")

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")

    finally:
        if driver:
            time.sleep(5)
            driver.quit() 
