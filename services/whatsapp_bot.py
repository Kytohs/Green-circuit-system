from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ✅ Specify the path to ChromeDriver
chrome_driver_path = "C:/path/to/chromedriver.exe"  # Change this to your actual path

# ✅ Set up WebDriver service
service = Service(chrome_driver_path)
options = webdriver.ChromeOptions()

# ✅ Use your logged-in Chrome profile to avoid scanning QR every time
options.add_argument("--user-data-dir=C:/Users/YourUser/AppData/Local/Google/Chrome/User Data")  # Change YourUser to your username
options.add_argument("--profile-directory=Default")  

# ✅ Launch Chrome
driver = webdriver.Chrome(service=service, options=options)

# ✅ Open WhatsApp Web
driver.get("https://web.whatsapp.com")
input("🔹 Scan the QR code, then press ENTER to continue...")

# ✅ Function to send WhatsApp message
def send_whatsapp_message(contact, message):
    try:
        search_box = driver.find_element(By.XPATH, "//div[@contenteditable='true']")
        search_box.click()
        search_box.send_keys(contact)
        search_box.send_keys(Keys.ENTER)
        time.sleep(2)

        message_box = driver.find_element(By.XPATH, "//div[@title='Type a message']")
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)

        print(f"✅ Message sent to {contact}")

    except Exception as e:
        print(f"❌ Error sending message: {e}")

# ✅ Example Usage
send_whatsapp_message("John Doe", "Hello! This is an automated message.")

# Keep browser open for a while
time.sleep(5)
driver.quit()
