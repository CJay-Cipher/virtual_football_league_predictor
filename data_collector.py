import pandas as pd
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

service = Service("chrome_driver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://vsmobile.bet9ja.com/mobile/themes/?sk=bet9ja&t=b61c29e6-9348-4c58-af90-378760a74693&game"
               "=league_premier&pid=14001,14003,14011,14012,14014,14015,14016,"
               "14017&v=0&text=Premier&lang=en_GB#resutls&ui_state=dialog")
# driver.maximize_window()
time.sleep(10)

action = ActionChains(driver)
record_list = []

print("Start data collection  ...\n")
while True:
    week_num = driver.find_element(By.XPATH, "//span[@id='leagueWeekNumber']").text
    counter = driver.find_element(By.XPATH, "//div[@id='bets-time-betContdown']").text

    if counter[:2] == "00" and int(counter[-2:]) < 58 and int(counter[-2:]) > 20:
        match_result = driver.find_element(By.XPATH, "//div[@id='tab_id_Match_Result']").text

        driver.find_element(By.XPATH, "//a[@id='ui-id-3']").click()
        over_one = driver.find_element(By.XPATH, "//div[@id='tab_id_Over_Under_1_5']").text

        market_select = driver.find_element(By.XPATH, "//select[@id='bet-select-market']")

        market_select.click()
        arrow_down = [ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform() for _ in range(3)]
        action.send_keys(Keys.ENTER).perform()
        over_two = driver.find_element(By.XPATH, "//div[@id='tab_id_Over_Under_2_5']").text

        market_select.click()
        arrow_down = [ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform() for _ in range(4)]
        action.send_keys(Keys.ENTER).perform()
        over_three = driver.find_element(By.XPATH, "//div[@id='tab_id_Over_Under_3_5']").text

        market_select.click()
        arrow_down = [ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform() for _ in range(5)]
        action.send_keys(Keys.ENTER).perform()
        over_four = driver.find_element(By.XPATH, "//div[@id='tab_id_Over_Under_4_5']").text

        while True:
            counter = driver.find_element(By.XPATH, "//div[@id='bets-time-betContdown']").text
            current_week = driver.find_element(By.XPATH, "//span[@id='leagueWeekNumber']").text
            if current_week == "01":
                current_week = 39
            if counter[:2] == "00" and int(counter[-2:]) < 58 and int(counter[-2:]) > 50 and int(current_week) == int(week_num) + 1:
                driver.find_element(By.XPATH, "//div[@class='ui-panel-wrapper']//i[@class='fa fa-bars icon-menu']").click()
                driver.find_element(By.XPATH, "//a[@id='a_bet_results']").click()
                time.sleep(8)
                score_result = driver.find_element(By.XPATH, "//table[@id='results-div-header-mainTable']").text
                driver.find_element(By.XPATH, "//div[@id='results']//i[@class='fa fa-bars icon-menu']").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//li[@class='li_bet']//a[@id='a_bet_bet']").click()
                time.sleep(3)
                break
            else:
                time.sleep(1)   

        match_result = match_result.split("\n")[2::2]
        over_one = over_one.split("\n")[2::2]
        over_two = over_two.split("\n")[2::2]
        over_three = over_three.split("\n")[2::2]
        over_four = over_four.split("\n")[2::2]
        score_result = score_result.split(f"WEEK {int(current_week) - 1}")[1].split("\n")[1:11]

        for hda, one, two, three, four, score in zip(match_result, over_one, over_two, over_three, over_four, score_result):
            data = (int(current_week) - 1,
                    hda[:3], hda[6:9], 
                    float(hda[-14:-10]), float(hda[-9:-5]), float(hda[-4:]),
                    float(one[-9:-5]), float(one[-4:]), 
                    float(two[-9:-5]), float(two[-4:]), 
                    float(three[-9:-5]), float(three[-4:]), 
                    float(four[-9:-5]), float(four[-4:]),
                    int(score[4]), int(score[6]))
            record_list.append(data)
            
        print("Week", int(current_week) - 1, "Data Collection Complete ...")

        if int(current_week) == 39:
            new_df = pd.DataFrame(record_list, columns=[
                "week",
                "HT", "HT", "home", "draw", "away", 
                "over_1", "under_1", 
                "over_2", "under_2",
                "over_3", "under_3",
                "over_4", "under_4",
                "H_score", "A_score"])
            new_df.to_csv("odds_data.csv", index=False)
    else:
        time.sleep(1)


# # Close the browser session
# driver.quit()