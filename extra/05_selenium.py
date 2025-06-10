# --- SCRIPT INTENTION: Web Automation with Selenium (Headless Linux - Python Docs Links & Screenshots - Corrected) ---
# This script robustly navigates the official Python 'os' module documentation.
# It correctly extracts internal links by stripping anchor tags and ensuring uniqueness of the base URLs,
# then visits a few of these distinct links, taking a screenshot of each visited page.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import datetime
import urllib.parse # To parse URLs

# --- Helper function to take a screenshot ---
def take_screenshot_on_error(driver, error_name="selenium_error"):
    """
    Takes a screenshot and saves it with a timestamped filename.
    Args:
        driver: The Selenium WebDriver instance.
        error_name: A base name for the screenshot file.
    Returns:
        The path to the saved screenshot file, or None if failed.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_filename = f"{error_name}_{timestamp}.png"
    try:
        driver.save_screenshot(screenshot_filename)
        print(f"   Screenshot saved to: {screenshot_filename}")
        return screenshot_filename
    except Exception as e:
        print(f"   Failed to take screenshot: {e}")
        return None

def selenium_python_docs_screenshots_corrected_example():
    print("--- Selenium Web Automation (Headless Linux - Python Docs Links & Screenshots - Corrected) Example ---")

    # --- 1. Configure Chrome Options for Headless Mode ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    chrome_options.add_argument("--lang=en-US,en")
    
    print("\n1. Configured Chrome for headless execution.")

    # --- 2. Setup WebDriver ---
    driver = None
    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("   Launched Chrome browser in headless mode using WebDriver Manager.")
    except Exception as e:
        print(f"\nError using WebDriver Manager: {e}")
        print("Falling back to manual driver path (ensure chromedriver is in PATH or specify full path).")
        driver_path = None
        if os.path.exists('./chromedriver'):
            driver_path = './chromedriver'
        
        if driver_path:
            try:
                service = ChromeService(executable_path=driver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
                print(f"   Launched Chrome browser from local path: {driver_path}")
            except Exception as e_manual:
                print(f"   Failed to launch browser even with manual path: {e_manual}")
                print("   Please ensure 'chromedriver' is correctly installed and accessible.")
                return
        else:
            print("   Could not find 'chromedriver' in current directory. Please ensure it's in PATH or specified.")
            return

    wait = WebDriverWait(driver, 10)

    # --- 3. Navigate to the target webpage (Python os module docs) ---
    target_url = "https://docs.python.org/3/library/os.html"
    print(f"\n3. Navigating to initial page: {target_url}")
    driver.get(target_url)
    
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.body[role='main']")))
        print("   Python documentation main content loaded successfully.")
    except Exception as e:
        print(f"   Error waiting for Python docs content: {e}")
        take_screenshot_on_error(driver, "initial_docs_page_load_error")
        driver.quit()
        return

    # --- 4. Find links within a specific section (e.g., the main body of the docs) ---
    print("\n4. Finding links within the main documentation body...")
    
    all_links_elements = driver.find_elements(By.CSS_SELECTOR, "div.body a")
    
    # Use a set to store unique URLs after stripping anchors
    unique_found_links = set() 
    base_url_prefix = "https://docs.python.org/3/library/" 

    for link_element in all_links_elements:
        href = link_element.get_attribute('href')
        if href:
            # Parse the URL to easily remove the fragment (the # part)
            parsed_href = urllib.parse.urlparse(href)
            
            # Reconstruct the URL without the fragment
            clean_href = urllib.parse.urlunparse(parsed_href._replace(fragment=''))

            # Ensure it's an internal link within the Python docs library section
            if clean_href.startswith(base_url_prefix):
                unique_found_links.add(clean_href)
            elif clean_href.startswith('/') and '/library/' in clean_href:
                # Handle relative paths, ensure it's within the 'library' section
                full_href = f"https://docs.python.org{clean_href}"
                unique_found_links.add(full_href)
            # else:
            #     print(f"   Skipping external or unhandled link: {href}") # Uncomment for debugging filtered links

    # Convert the set back to a list for iteration
    found_links_list = list(unique_found_links)
    
    if not found_links_list:
        print("   No suitable unique internal links found on the page after filtering.")
        take_screenshot_on_error(driver, "no_docs_links_found")
        driver.quit()
        return

    print(f"   Found {len(found_links_list)} unique suitable links. Processing up to 5 unique links for demonstration.")

    # --- 5. Navigate to each link and take a screenshot ---
    import random
    random.shuffle(found_links_list) # Shuffle to get different links each run

    for i, link_to_visit in enumerate(found_links_list[:5]): # Process first 5 unique links
        print(f"\n5.{i+1}. Navigating to linked Python docs page: {link_to_visit}")
        try:
            driver.get(link_to_visit)
            time.sleep(2) # Give page time to load content
            
            # Generate a more descriptive screenshot name using the page's path segment
            # e.g., 'os.path.join' from '.../os.html#os.path.join' or 'io.html' from '.../io.html'
            path_segment = link_to_visit.split('/')[-1] # Gets 'os.html' or 'io.html'
            page_name = path_segment.replace('.html', '').replace('.', '_') # Clean up for filename
            
            take_screenshot_on_error(driver, f"python_doc_{page_name}_screenshot_{i+1}")
            print(f"   Successfully navigated to and screenshotted: {link_to_visit}")
        except Exception as e:
            print(f"   Error navigating to or screenshottng {link_to_visit}: {e}")
            take_screenshot_on_error(driver, f"python_doc_error_{i+1}")
            # Continue to next link even if one fails
            
    # --- 6. Close the browser ---
    if driver:
        print("\n6. Closing the browser...")
        driver.quit()
        print("   Browser closed. --- Selenium Web Automation (Python Docs Links & Screenshots - Corrected) Example Finished ---")

if __name__ == "__main__":
    selenium_python_docs_screenshots_corrected_example()