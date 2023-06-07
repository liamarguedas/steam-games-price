from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np
import time

# Function to pass Age Restriction
def PassAgeRestriction(Driver):
    
    Select(Driver.find_element(By.NAME, "ageYear")).select_by_value('2000')
    Driver.find_element(By.CLASS_NAME, "btnv6_blue_hoverfade.btn_medium").click()

# Function to scrape games    
def GetSteamGames(ToScrape = 10, ToWait = 0.5, verbose = True, Scroll = 5):
    
    # Storage list
    GameName = list()
    AgeRestriction = list()
    GameDescription = list()
    GameReviews = list()
    ReviewSentiment = list()
    ReleaseDate = list()
    GameDeveloper = list()
    GamePrice = list()
    DiscountedPrice = list()
    PEGIRating = list()
    Metacritic = list()
    GameType = list()
    LastUpdate = list()
    GamesLanguages = list()
    GamesFeatures = list()
    GameDRM = list()
    GameAchievements = list()
    CuratorReviews = list()
    
    # Selenium warnings options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
    
    # Getting top sellers games
    driver.get('https://store.steampowered.com/search/?filter=topsellers&ndl=1&ignore_preferences=1')
    
    # Scrolling "Scroll" times to get games
    for scroll in range(1, Scroll + 1):
        driver.execute_script(f"window.scrollTo(0, {2000 * scroll})")
        time.sleep(1) 
    
    # Scroll back to the first game
    driver.execute_script(f"window.scrollTo(0, 0)")
    time.sleep(1)
    
    # Find all listed games
    GamesBanner = driver.find_elements(By.CLASS_NAME, "search_result_row.ds_collapse_flag.app_impression_tracked")
    
    if len(GamesBanner) < ToScrape:
        
        raise ValueError(f"Games ToScrape ({ToScrape}) is higher than games found ({len(GamesBanner)}), try raising Scroll parameter")
        
    if verbose:
        print(f"Total Found games: {len(GamesBanner)}")
        print(f"Scraping: {ToScrape}")
        print('=' * 20)

        MeanTime = list()
    
    # For game in (Find all listed games)
    for number, item in enumerate(GamesBanner):
        
        if number < ToScrape:
            
            if verbose:
                t0 = time.time()
            
            # Get game URL to scrape
            GameDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
            GameDriver.get(f"{item.get_attribute('href')}")
            
            # Pass AgeRestriction if needed
            try: 
                PassAgeRestriction(Driver = GameDriver)
                AgeRestriction.append('Yes')
            except:
                AgeRestriction.append('No')
            
            time.sleep(ToWait)
            
            # SCRAPING GAME INFO 
            
            # Game name
            try: 
                GameName.append(GameDriver.find_element(By.CLASS_NAME, "apphub_AppName").text)   
            except: # In case of an error, introduced an NaN value.
                GameName.append(np.nan)
                
            # Game description
            try: 
                GameDescription.append(GameDriver.find_element(By.CLASS_NAME, "game_description_snippet").text)   
            except:
                GameDescription.append(np.nan)
                
            # Total reviews
            try: 
                GameReviews.append(GameDriver.find_element(By.CLASS_NAME, "user_reviews_summary_bar").text)   
            except:
                GameReviews.append(np.nan)
                
            # Reviews sentiment
            try: 
                ReviewSentiment.append(GameDriver.find_element(By.CLASS_NAME, "game_review_summary").text)   
            except:
                ReviewSentiment.append(np.nan)
                
            # Release date
            try: 
                ReleaseDate.append(GameDriver.find_element(By.CLASS_NAME, "date").text)   
            except:
                ReleaseDate.append(np.nan)
                
            # Game Developer
            try: 
                GameDeveloper.append(GameDriver.find_element(By.ID, "developers_list").text)   
            except:
                GameDeveloper.append(np.nan)
            
            # Original Price
            try:
                GamePrice.append(GameDriver.find_element(By.XPATH, "//div[@class='game_purchase_action_bg']/div[@class='game_purchase_price price']").text)   
            except:
                try:
                    GamePrice.append(GameDriver.find_element(By.XPATH, "//div[@class='discount_prices']/div[@class='discount_original_price']").text)
                except:
                    GamePrice.append(np.nan)
                    
            # Discounted price
            try:
                if GamePrice[-1] in ['Gratuito para jogar', 'Gratuito p/ Jogar']:
                    
                    raise ValueError('Execute except')
                else: 
                    DiscountedPrice.append(GameDriver.find_element(By.XPATH, "//div[@class='discount_block game_purchase_discount']//div[@class='discount_final_price']").text)   
            except:
                DiscountedPrice.append('0') 
                
            # Game Rating (PEGI)
            try: 
                PEGIRating.append(GameDriver.find_element(By.XPATH, "//div[@class='game_rating_icon']/img").get_attribute("src"))  
            except:
                PEGIRating.append(np.nan) 
                
            # MetacriticScore
            try: 
                Metacritic.append(GameDriver.find_element(By.CLASS_NAME, "score").text)  
            except:
                Metacritic.append(np.nan) 
                
            # Genero
            try: 
                GameType.append(GameDriver.find_element(By.XPATH, "//div[@id='genresAndManufacturer']//span").text)  
            except:
                GameType.append(np.nan)  
            
            # Last update
            try: 
                LastUpdate.append(GameDriver.find_element(By.CLASS_NAME, "partnereventwebrowembed_LatestUpdateButton_3F6YM.Focusable").text)  
            except:
                LastUpdate.append(np.nan) 
            
            # Game Available Languages
            try: 
                GamesLanguages.append(GameDriver.find_element(By.CLASS_NAME, "all_languages").text)  
            except:
                GamesLanguages.append(1)
                
            # Game Features
            try: 
                GamesFeatures.append(GameDriver.find_element(By.CLASS_NAME, "game_area_features_list_ctn").text)  
            except:
                GamesFeatures.append(np.nan) 
        
            # DRM notice
            try: 
                GameDRM.append(GameDriver.find_element(By.XPATH, "//div[@class='DRM_notice']/div").text)  
            except:
                GameDRM.append('Not required')
                
            # Number of achievements
            try: 
                GameAchievements.append(GameDriver.find_element(By.XPATH, "//div[@id='achievement_block']/div").text)  
            except:
                GameAchievements.append(0)
        
            # Number of curator reviews
            try: 
                CuratorReviews.append(GameDriver.find_element(By.CLASS_NAME, "no_curators_followed").text)  
            except:
                CuratorReviews.append(0)      

            GameDriver.quit()
            
            if verbose:
                t1 = time.time()
                MeanTime.append(t1-t0)
                print(f"Scraped: {number+1}/{ToScrape}")
                print(f"Total time: {round((t1-t0), 2)}s")
                print(f"Time To finish: {round((np.mean(MeanTime) * (ToScrape - (number+1))) / 60, 2)} minutes")
                print('-' * 20)
        
    driver.quit()
    
    # Return .csv file named "games.csv"      
    return pd.DataFrame({'Game' : GameName,
    'AgeRestriction': AgeRestriction,
    'GameDescription':GameDescription,
    'Reviews':GameReviews,
    'ReviewSentiment':ReviewSentiment,
    'ReleaseDate':ReleaseDate,
    'Developer':GameDeveloper,
    'FullPrice':GamePrice,
    'DiscountedPrice':DiscountedPrice,
    'PEGI': PEGIRating,
    'MetacriticScore': Metacritic,
    'Type':GameType,
    'LastUpdate': LastUpdate,
    'GamesLanguages':GamesLanguages,
    'GameFeatures':GamesFeatures,
    'DRM Notice':GameDRM,
    'GameAchievements':GameAchievements,
    'CuratorReviews':CuratorReviews}).to_csv('games.csv')