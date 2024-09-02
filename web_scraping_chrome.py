import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# Path to your manually downloaded Chrome WebDriver
webdriver_path = r"C:\Users\Xydis\OneDrive - Coty, Inc\Documents\Desktop\Various\Web Scraping\chromedriver.exe"


# Setup Chrome options
options = webdriver.ChromeOptions()
# Forces the browser to use English as the default language.
options.add_argument("--lang=en")
# Initialize WebDriver with the path to the manually downloaded WebDriver
driver = webdriver.Chrome(service=Service(webdriver_path), options=options)

# Airbnb search URL for Athens, Greece
airbnb_url='https://www.airbnb.com/s/Athens--Greece/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-10-01&monthly_length=3&monthly_end_date=2025-01-01&price_filter_input_type=0&channel=EXPLORE&query=Athens&place_id=ChIJ8UNwBh-9oRQR3Y1mdkU1Nic&location_bb=QhghpUG%2BUUpCF8uXQb1%2B8w%3D%3D&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'
driver.maximize_window()

# Data storage
data = []

while True:
       
        driver.get(airbnb_url)
        urls = list(set(a.get_attribute('href') for a in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'[itemprop="itemListElement"] a')))))
        try:
            next_page= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#site-content > div > div.pbmlr01.atm_h3_t9kd1m.atm_gq_n9wab5.dir.dir-ltr > div > div > div > nav > div > a.l1ovpqvx.atm_1he2i46_1k8pnbi_10saat9.atm_yxpdqi_1pv6nv4_10saat9.atm_1a0hdzc_w1h1e8_10saat9.atm_2bu6ew_929bqk_10saat9.atm_12oyo1u_73u7pn_10saat9.atm_fiaz40_1etamxe_10saat9.c1ytbx3a.atm_mk_h2mmj6.atm_9s_1txwivl.atm_h_1h6ojuz.atm_fc_1h6ojuz.atm_bb_idpfg4.atm_26_1j28jx2.atm_3f_glywfm.atm_7l_hkljqm.atm_gi_idpfg4.atm_l8_idpfg4.atm_uc_10d7vwn.atm_kd_glywfm.atm_gz_8tjzot.atm_uc_glywfm__1rrf6b5.atm_26_zbnr2t_1rqz0hn_uv4tnr.atm_tr_kv3y6q_csw3t1.atm_26_zbnr2t_1ul2smo.atm_3f_glywfm_jo46a5.atm_l8_idpfg4_jo46a5.atm_gi_idpfg4_jo46a5.atm_3f_glywfm_1icshfk.atm_kd_glywfm_19774hq.atm_70_glywfm_1w3cfyq.atm_uc_aaiy6o_9xuho3.atm_70_18bflhl_9xuho3.atm_26_zbnr2t_9xuho3.atm_uc_glywfm_9xuho3_1rrf6b5.atm_70_glywfm_pfnrn2_1oszvuo.atm_uc_aaiy6o_1buez3b_1oszvuo.atm_70_18bflhl_1buez3b_1oszvuo.atm_26_zbnr2t_1buez3b_1oszvuo.atm_uc_glywfm_1buez3b_1o31aam.atm_7l_1wxwdr3_1o5j5ji.atm_9j_13gfvf7_1o5j5ji.atm_26_1j28jx2_154oz7f.atm_92_1yyfdc7_vmtskl.atm_9s_1ulexfb_vmtskl.atm_mk_stnw88_vmtskl.atm_tk_1ssbidh_vmtskl.atm_fq_1ssbidh_vmtskl.atm_tr_pryxvc_vmtskl.atm_vy_1vi7ecw_vmtskl.atm_e2_1vi7ecw_vmtskl.atm_5j_1ssbidh_vmtskl.atm_mk_h2mmj6_1ko0jae.dir.dir-ltr')))
            airbnb_url = next_page.get_attribute('href')
        except TimeoutException:
            next_page = None
    

    
        for url in urls:
            try:
                driver.get(url)
                
                # Wait for the amenities button and click it
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-section-id="AMENITIES_DEFAULT"] button'))).click()
                
                # Parse the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
    
                # Extract price per night using XPath
                price_per_night = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[2]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/span/div/span[1]'))
                ).text.strip()
    
                # Extract number of bedrooms using XPath
                bedroom_class = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[2]'))
                ).text.strip()
    
                # Extract number of beds using XPath
                bed_class = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[3]'))
                ).text.strip()
    
                # Extract number of bathrooms using XPath
                # bath_class = WebDriverWait(driver, 10).until(
                #     EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/main/div/div[1]/div[3]/div/div[1]/div/div[1]/div/div/div/section/div[2]/ol/li[4]'))
                # ).text.strip()
    
                # Extract data
                d = {
                    'url': url,
                    'title': soup.h1.text,
                    'price_per_night': price_per_night,
                    'bedroom_class': bedroom_class,  # Number of bedrooms
                    'bed_class': bed_class,          # Number of beds
                    #'bath_class': bath_class,        # Number of bathrooms
                    'amenities': [i.text.split('\n')[0] for i in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="modal-container"] [id$="-row-title"]')))]
                }
    
    
                # if soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div'):
                #     sleep_areas = list(soup.select_one('[data-section-id="SLEEPING_ARRANGEMENT_DEFAULT"] div+div').stripped_strings)
                #     d.update(dict(zip(sleep_areas[0::2], sleep_areas[1::2])))
                # else:
                #     d.update({'Bedroom': None})
    
                data.append(d)
            
            except TimeoutException:
                print("TimeoutException: Skipping this listing.")
                continue  # Move to the next URL if there's a timeout
    
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                continue  # Log and move to the next URL if any other exception occurs
    
        if next_page == None:
            break
        
            

df=pd.DataFrame(data)
