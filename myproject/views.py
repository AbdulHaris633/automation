from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_py  # This automatically manages the ChromeDriver 
import time

def open_chrome(request):
    url = request.GET.get('url', 'https://fmovies.ps/home')  
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  

    # Get the path to ChromeDriver provided by chromedriver-py
    chromedriver_path = chromedriver_py.binary_path

    try:
        # Initialize the Chrome WebDriver
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        time.sleep(10)  
        # Navigate to the provided URL
        driver.get(url)
        time.sleep(30)   
        driver.quit() 
    
        return HttpResponse(f"Opened Chrome and navigated to: {url}")
    except Exception as e:
        return HttpResponse(f"Failed to open Chrome: {str(e)}")  
