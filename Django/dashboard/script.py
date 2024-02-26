from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

print("Start Script")
CONTAINER_SELENIUM = "selenium"
PORT_SELENIUM = "4444"
CONTAINER_WEB_APPLICATION = "django-application-dev"
PORT_WEB_APPLICATION = "8000"


# Options
options = webdriver.ChromeOptions()
options.add_argument('--headless')

try:
    ############################################
    # Start driver
    ############################################
    print("Starting driver...")
    driver = webdriver.Remote(f"http://{CONTAINER_SELENIUM}:{PORT_SELENIUM}/wd/hub", DesiredCapabilities.CHROME, options=options)
    print("Driver started")

    try:
        ############################################
        # Open page
        ############################################
        print("Opening page...")
        container_web_aplication = "django-application-dev"
        port_web_aplication = "8000"
        driver.get(f"http://{CONTAINER_WEB_APPLICATION}:{PORT_WEB_APPLICATION}/dashboard/current-datetime/")
        driver.implicitly_wait(500)
        print(f"Page opened - page title: {driver.title}")

        try:
            ############################################
            # take screenshot
            ############################################
            screenshot = driver.get_screenshot_as_png()
            DIR_MEDIA = "../media"
            # save screenshot
            with open(f"{DIR_MEDIA}/screenshot.png", "wb") as f:
                f.write(screenshot)
        except Exception as screenshot_error:
            print(f"Error taking screenshot: {screenshot_error}")
    except Exception as page_error:
        print(f"Error opening page: {page_error}")

finally:
    ############################################
    # Close driver
    ############################################
    try:
        driver.quit()
        print("Driver closed")
    except Exception as driver_close_error:
        print(f"Error closing driver: {driver_close_error}")