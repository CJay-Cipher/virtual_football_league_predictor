import pandas as pd
import math
import datetime
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time
import sys
service = Service("chrome_driver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Create an instance of ActionChains
actions = ActionChains(driver)

# Open the specified URL
driver.get("https://logigames.bet9ja.com/Games/Launcher?gameId=11000&provider=0&pff=1&skin=201")
# driver.maximize_window()
time.sleep(5)

start_time = time.time()  # Record the start time 
max_running_hours = 3000  # Set the maximum running hours  
max_running_time = max_running_hours * 60 * 60

# Initialize an empty list to store records
record_list = []
start_trade = False
pause_trade = False
end_trade = False

capital = 120_000   #  
print(f"Capital = {capital}")
win_count_target = 1000 # Win times 
win_count = 0
max_loss = []
loss_count = 0
green_last_draw, red_last_draw, blue_last_draw = [], [], []
draw_counter = 0
loss_count_list = []

# MARTINGALE LIST GENERATOR --------
target_percentage = 0.1  # %
if target_percentage >= 0.12:
    print(f"Target Percentage is too high - {target_percentage}")
    sys.exit()
target = round(capital * (target_percentage / 100))
print(f"Profit Target = {target}")
odd = 1.5
martingale_levels = 8
martingale_loss = 0
martingale_stakes = []
for x in range(martingale_levels):
    stake = math.ceil((target + martingale_loss) / (odd - 1))
    martingale_stakes.append(stake)
    martingale_loss += stake
print(f"Martingale Levels = {martingale_stakes}")
print(f"Martingale Sum = {sum(martingale_stakes)}\n{'-'*50}")
Initial_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
print(f"Initial Balance = {Initial_balance}")

def reloadResult(click_string="//div[@class='stats__toggle ']"):
    green_last_draw.pop(), red_last_draw.pop(), blue_last_draw.pop()
    driver.find_element(By.XPATH, click_string).click()  # Click on stats
    time.sleep(1)
    driver.find_element(By.XPATH, "//a[contains(text(),'Rainbow')]").click()  # Click on the "Total Colour" option in the dropdown menu
    time.sleep(0.5)
    driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='All time']").click()
    time.sleep(2)

    # This gets the Last Drawn values on the Statistics page
    green_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[2]/td[4]").text))
    red_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[8]/td[4]").text))
    blue_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[14]/td[4]").text))

    # to confirm draw result
    green_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(6) td:nth-child(4)").text
    red_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(12) td:nth-child(4)").text
    blue_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(18) td:nth-child(4)").text
    result_check = f"{green_6_ld}-{red_6_ld}-{blue_6_ld}"
    return result_check

while True:
    # Get the counter value from the webpage
    counter = driver.find_element(By.XPATH, "//div[@class='timeline__value-txt']").text

    draw_error = False
    if int(counter) < 41 and int(counter) > 37:
        draw_counter += 1
        trade_status = ""
        # Click on the statistics button
        try:
            driver.find_element(By.XPATH, "//div[@class='stats__toggle ']").click()     # -error check 1
        except Exception as e:  # handle any exception error
            print("---> Draw or Network error <---")
            draw_error = True
            driver.refresh()
            time.sleep(2)
            driver.find_element(By.XPATH, "//div[@class='stats__toggle ']").click()

        time.sleep(0.5)
        # Click on the "Rainbow" option in the dropdown menu
        driver.find_element(By.XPATH, "//a[contains(text(),'Rainbow')]").click()
        # Click on the "All time" option in the dropdown menu
        driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='All time']").click()
        time.sleep(5)

        # This gets the Last Drawn values on the Statistics page
        green_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[2]/td[4]").text))
        red_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[8]/td[4]").text))
        blue_last_draw.append(int(driver.find_element(By.XPATH, "//tbody/tr[14]/td[4]").text))
        # last_drawn_record = [green_last_draw[-1], red_last_draw[-1], blue_last_draw[-1]]

        # to confirm draw result
        green_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(6) td:nth-child(4)").text
        red_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(12) td:nth-child(4)").text
        blue_6_ld = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(18) td:nth-child(4)").text
        result_check = f"{green_6_ld}-{red_6_ld}-{blue_6_ld}"
        # print("Result check --> ", result_check)

        if draw_counter > 1 and previous_stats_record == result_check:
            print("...... Draw correction ......")
            result_check = reloadResult(click_string="//a[normalize-space()='History']")
            if previous_stats_record == result_check:
                print(".... 2nd Draw correction ....")
                driver.refresh()
                time.sleep(1.5)
                result_check = reloadResult()
                if (previous_stats_record == result_check) and draw_error == True:
                    time.sleep(5)
                    while True:
                        counter = driver.find_element(By.XPATH, "//div[@class='timeline__value-txt']").text
                        if int(counter) < 43 and int(counter) > 33:
                            print(".... 3rd Draw correction ....")
                            driver.refresh()
                            time.sleep(1.5)
                            result_check = reloadResult()
                            break
                        else:
                            time.sleep(1)
        previous_stats_record = result_check

        # Check if result is a Win or Loss 
        result_colours = [green_last_draw[-1], red_last_draw[-1], blue_last_draw[-1]]
        if start_trade == True:
            if result_colours[colour_index] == 0:
                start_trade = False
                win_count += 1
                max_loss.append(loss_count)
                loss_count = 0
                print(f"------------------------------->-------------------------------> {colour_string} WIN = {win_count} Loss_levels = {max_loss[-1]} Max Loss = {max(max_loss)}")

            else:
                loss_count += 1
   

        # Click on the "History" tab
        driver.find_element(By.XPATH, "//a[normalize-space()='History']").click()
        time.sleep(2)
        
        # Get the history text from the webpage
        history = driver.find_element(By.XPATH, "//div[@class='p-stats__content']").text
        
        # This gets the number of times each colour appears from RED, GREEN and BLUE respectively
        # E.g '213' means 2 reds, 1 green and 3 blues
        colours_count = history.split(" ")[9:][0].split("\n")[-1]

        # This gets the Total number count for all six balls
        # E.g 148 means total sum for the given balls - 22, 14, 4, 35, 26, 47 
        sum_colours = int(history.split(" ")[9:][1].split("\n")[0])

        # Get the numbers for all 6 balls
        ball_path = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[4]/div[2]/table[1]/tbody[1]/tr[1]/td[2]/div[1]/span["
        ball_1 = int(driver.find_element(By.XPATH, f"{ball_path}1]").text)
        ball_2 = int(driver.find_element(By.XPATH, f"{ball_path}2]").text)
        ball_3 = int(driver.find_element(By.XPATH, f"{ball_path}3]").text)
        ball_4 = int(driver.find_element(By.XPATH, f"{ball_path}4]").text)
        ball_5 = int(driver.find_element(By.XPATH, f"{ball_path}5]").text)
        ball_6 = int(driver.find_element(By.XPATH, f"{ball_path}6]").text)
        
        last_5_colours = [num[-3:] for num in history.split(" ")[9:][0:-1:2][:5]]
        last_5_green, last_5_red, last_5_blue = [], [], []
        for numbers in last_5_colours:
            last_5_green.append(int(numbers[1]))
            last_5_red.append(int(numbers[0]))
            last_5_blue.append(int(numbers[2]))
        # print(last_5_red, last_5_green, last_5_blue)

        # Record all collected results in a listed tuple
        all_balls = (ball_1, ball_2, ball_3, ball_4, ball_5, ball_6)
        all_record = all_balls + (colours_count, sum_colours)
        record_list.append(all_record)
        # print(all_record)

        # To open trading page
        driver.find_element(By.XPATH, "//div[@class='stats__toggle active']").click()
        time.sleep(1)

        if loss_count >= martingale_levels:
            print(f"\n      *** SORRY ***\n---> {loss_count} Losses Reached")
            # email_notification("TRADING STOPPED \nMAXIMUM LOSS REACHED ...")
            final_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            print(f"Initial Balance = {Initial_balance}")
            print(f"Final Balance = {final_balance}")
            print(f"Lost Amount = {final_balance - Initial_balance}")
            break

        if start_trade == False and (win_count >= win_count_target):
            driver.refresh()  # Reload webpage to get updated final balance
            time.sleep(2)
            print(f"\n    *** !!! CONGRATULATIONS !!! ***\n        {win_count} Wins Target Achieved")
            final_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            print(f"Initial Balance = {Initial_balance}")
            print(f"End Balance = {final_balance}")
            print(f"Profit = {final_balance - Initial_balance}")
            break

        if start_trade == False and ((time.time() - start_time) > max_running_time):  # Check if run time has exceeded the allocated trading time
            driver.refresh()  # Reload webpage to get updated final balance
            time.sleep(2)
            print(f"\n               *** ! PAUSE TRADING ! ***\n        {max_running_hours} hours Allocated Trading time exceeded")
            final_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            print(f"Initial Balance = {Initial_balance}")
            print(f"End Balance = {final_balance}")
            print(f"Profit = {final_balance - Initial_balance}")
            break

        # START TRADING CONDITION ------------------------------------------------------------------------------------------------------------------------.    
        colours = ("green", "red", "blue")#                                                                                                               |
        for pick in ["22442", "12424", "41042", "32231"]:  # "41042", "12424", "22442", "32231", "23432"                                                  |
            n1, n2, n3, n4, n5 = map(int, pick)  # 41042, 22432, 32231, 12424                                                                             |
            if start_trade:  #                                                                                                                            |
                break  #                                                                                                                                  |
            colour_index = -1  #                                                                                                                          |
            for color in [last_5_green, last_5_red, last_5_blue]:  #                                                                                      |
                colour_index += 1  #                                                                                                                      |
                if (color[0] >= n1) and (color[1] >= n2) and (color[2] >= n3) and (color[3] >= n4) and (color[4] >= n5):#                                 |
                    start_trade = True  #                                                                                                                 |
                    colour_string = colours[colour_index]  #                                                                                              |
                    trade_status = f"---> stake {colour_string.upper()} - {pick}"#                                                                        |
                    break  #                                                                                                                              |
                # if notification_start == False:  # For sending email notification to start trading -----------------------.                             |
                #     email_notification("AUTO TRADING STARTED")#                                                           |                             |
                #     notification_start = True  # -------------------------------------------------------------------------'                             |
        #                                                                                                                                                 |
        last_5 = f'[{"".join(map(str, last_5_red))} {"".join(map(str, last_5_green))} {"".join(map(str, last_5_blue))}]'
        print(f"R.G.B - {colours_count}-{last_5}-{red_last_draw[-1], green_last_draw[-1], blue_last_draw[-1]} {trade_status}")#                           |
        #                                                                                                                                                 |
        # ------------------------------------------------------------------------------------------------------------------------------------------------'


        # START TRADING if trade condition is True --------------------------------------------------------------------------------------------------------
        if start_trade:
            green_string = "//div[contains(@class,'game__ts')]//div[3]//div[2]//div[1]//div[1]"
            red_string = "//div[contains(@class,'rainbow-grid')]//div[1]//div[2]//div[1]//div[1]"
            blue_string = "//div[contains(@class,'game__content')]//div[2]//div[2]//div[1]//div[1]"
            colors_string_list = [green_string, red_string, blue_string]
            color_select = colors_string_list[colour_index]
            color_unselect = f"div[class='rainbow__ball {colour_string} available active'] div[class='rainbow__ball-value']"

            # print("START TRADE HERE ...")
            before_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            driver.find_element(By.XPATH, "//a[4]").click()  # Total Colour
            time.sleep(1)

            stake_amount = martingale_stakes[loss_count]
            # Click on selected colour
            driver.find_element(By.XPATH, color_select).click()
            time.sleep(0.5)

            stake_box = driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/input[1]")
            stake_box.click()  # Click on stake box
            stake_box.send_keys(Keys.CONTROL + "a")  # Highlight the existing value in the stake box
            stake_box.send_keys(Keys.BACKSPACE)  # Clear the highlighted value
            time.sleep(0.5)
            
            stake_box.send_keys(stake_amount)  # Enter stake amount
            time.sleep(2)
            try:
                driver.find_element(By.XPATH, "//a[@class='place-bet']").click()  # Place bet
            
            # if there was a problem with PLACE BET button -------------------------------------------------------------------------------------------
            except ElementClickInterceptedException:
                print("Place bet button delay ---------------------------------->>>")
                driver.refresh()  # Reload the current webpage
                time.sleep(1)
                driver.find_element(By.XPATH, "//a[4]").click()  # Total Colour
                driver.find_element(By.XPATH, color_select).click()
                time.sleep(1)

                stake_box = driver.find_element(By.XPATH, "//body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[2]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/input[1]")
                stake_box.click()  # Click on stake box
                stake_box.send_keys(Keys.CONTROL + "a")  # Highlight the existing value in the stake box
                stake_box.send_keys(Keys.BACKSPACE)  # Clear the highlighted value
                # time.sleep(0.5)
                
                stake_box.send_keys(stake_amount)  # Enter stake amount
                time.sleep(2)
                driver.find_element(By.XPATH, "//a[@class='place-bet']").click()  # Place bet
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, color_unselect).click()  # to unselect the last picked colour
            time.sleep(8)
            after_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            if before_balance != after_balance:
                # stake_status = True
                print("success -------------------->")
            else:
                print("!!! stake error !!!")
                driver.find_element(By.XPATH, color_select).click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//a[@class='place-bet']").click()  # Place bet
                time.sleep(5)
                after_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
                if before_balance != after_balance:
                    # stake_status = True
                    print("stake success --------------------> 2")
                driver.find_element(By.CSS_SELECTOR, color_unselect).click()  # to unselect
            # -----------------------------------------------------------------------------------------------------------------------------------------

    else: 
        time.sleep(1)  # 1 seconds counter delay

print(f"\nTotal Draws = {draw_counter}")
total_minutes = (draw_counter * 50) // 60
print(f"Total Wins = {win_count}")
print(f"Total Loss = {loss_count}")
print(f"Time Taken = {total_minutes // 60}hrs {total_minutes % 60}mins -----------------------------------------------")

# Compile the collected data
cols = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'colours', 'total']
df = pd.DataFrame(record_list, columns=cols)
df['colours'] = df['colours'].astype(str)

# Save the data as a CSV file
df.to_csv('new_data.csv', index=False)
print("Data Saved Successfully ...")

# Close the browser session
driver.quit()