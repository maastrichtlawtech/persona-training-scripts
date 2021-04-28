#!/usr/bin/env python
# coding: utf-8

# ## Training bot

# In[ ]:


import pandas as pd
websites = pd.read_excel('websites_groups.xlsx')


# In[ ]:


websites['Category'].unique()


# In[ ]:


#websites.head(20)


# In[ ]:


group = 'Female, LGBTQ+'
proxies_list = websites[websites['Category'] == group]['Website'].to_list()


# In[ ]:


proxies_list


# In[ ]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--window-size=1620x1620")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver')

##------
url = 'https://www.google.nl/'
driver.get(url)
driver.implicitly_wait(4)
print(driver.current_url)
##------
for idx, proxy in enumerate(proxies_list):
    url = "'https://www."+str(proxy)+"'"
    print("Learning...", url)
    driver.execute_script("window.open("+url+")")
    driver.implicitly_wait(3)
    driver.switch_to_window(driver.window_handles[idx+1])

windows_open  = len(driver.window_handles)
print("Windows open:", windows_open)


# In[ ]:


# buttons
#driver.back() 
#driver.forward()
#driver.refresh()
#driver.switch_to.new_window('tab')
#driver.switch_to.new_window('window')
#driver.close()
#driver.switch_to.window(original_window)


# In[ ]:


from datetime import datetime
sttime = datetime.now().strftime('%Y%m%d_%Hh%M_')


# In[ ]:


url = "https://www.buienradar.nl/"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 100")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_buien.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://www.msn.com/nl-nl"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 101")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+1])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_msn.png")
print(driver.title, driver.current_window_handle)
#we have to reload after cookies acceptance


# In[ ]:


url = "https://www.bbc.com/news"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 102")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+2])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_bbc.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://www.weerplaza.nl/"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 103")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+3])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_weerplaza.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://www.nu.nl/"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 104")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+4])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_nunl.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://google.nl/search?q=fiets"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 105")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+5])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_google_fiets.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://google.nl/search?q=nieuws"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 106")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+6])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_google_nieuws.png")
print(driver.title, driver.current_window_handle)


# In[ ]:


url = "https://google.nl/search?q=kleding+online+kopen"
print("Saving...", url)
driver.execute_script('window.open("'+url+'","window 107")')
driver.implicitly_wait(3)
driver.switch_to_window(driver.window_handles[windows_open+7])


# In[ ]:


driver.save_screenshot("screenshots/"+str(sttime)+str(group)+"_google_kleding.png")
print(driver.title, driver.current_window_handle)


# In[ ]:





# In[ ]:




