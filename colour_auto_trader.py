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

# print("\nWaiting for Trade time ...")
# time.sleep(1400)  # waiting for Trade time

service = Service("chrome_driver/chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://casino.bet9ja.com/casino/category/popular")
# driver.maximize_window()
time.sleep(5)

# Create an instance of ActionChains
actions = ActionChains(driver)

# login 
username = "Nnabueze"
password = "cjval1610"
print("Logging in ...")
driver.find_element(By.XPATH, "//div[@title='Log In']").click()
time.sleep(1)
driver.find_element(By.XPATH, "//input[@id='01']").send_keys(username)
driver.find_element(By.XPATH, "//input[@id='02']").send_keys(password)
driver.find_element(By.XPATH, "//div[@class='btn-primary-l mt20']").click()
time.sleep(3)

element_to_hover = driver.find_element(By.XPATH, "//div[@id='11000']//div[@class='game__info']")
actions.move_to_element(element_to_hover).perform()

# # for real trading
# driver.find_element(By.XPATH, "//div[@id='11000']//div[@class='game__info']//button[@title='Play Now'][normalize-space()='Play Now']").click()

# for demo trading
driver.find_element(By.XPATH, "//div[@id='11000']//button[@title='Demo'][normalize-space()='Demo']").click()

time.sleep(5)

# Get the handles of all open windows
window_handles = driver.window_handles

# Switch to the new window
new_window_handle = window_handles[-1]  # Get the handle of the last window in the list
driver.switch_to.window(new_window_handle)
# print(len(window_handles))

# Now you are in the new window

# # Continue with actions or assertions in the new window
# driver.maximize_window()
time.sleep(1)

start_time = time.time()  # Record the start time 
max_running_hours = 23  # Set the maximum running hours <<-------------------------------------------------------------------
max_running_time = max_running_hours * 60 * 60

# Initialize an empty list to store records
record_list = []
start_trade = False
pause_trade = False
end_trade = False

capital = 100_000   # <<-------------------------------------------------------------------
print(f"Capital = {capital}")
win_count_target = 20 # Win times <<-------------------------------------------------------
win_count = 0
max_loss = []
loss_count = 0
max_num = 12
min_num = 6
# last_draw_num = 13
green_count, red_count, blue_count = [], [], []
colour_list = [green_count, red_count, blue_count]
green_last_draw, red_last_draw, blue_last_draw = [], [], []
last_draw_list = [green_last_draw, red_last_draw, blue_last_draw]
draw_counter = 0
loss_count_list = []

# MARTINGALE LIST GENERATOR --------
target_percentage = 1.0  # %  <<-------------------------------------------------------------------
if target_percentage >= 1.32:
    print(f"Target Percentage is too high - {target_percentage}")
    sys.exit()
target = round(capital * (target_percentage / 100))
print(f"Profit Target = {target}")
odd = 3.8
martingale_levels = 12
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
# -------------------------------------------------------

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
        driver.find_element(By.XPATH, "//a[contains(text(),'Total Colour')]").click()
        # Click on the "100 Draws" option in the dropdown menu
        driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='100 Draws']").click()
        time.sleep(5)

        # Get the statistics text from the webpage
        stats = driver.find_element(By.XPATH, "//div[@class='p-stats__content']").text

        total_stats = tuple([int(x[-2:]) for x in stats.split("%")[:-1]])
        green_count.append(total_stats[1]), red_count.append(total_stats[2]), blue_count.append(total_stats[3])

        # This gets the Last Drawn values on the Statistics page
        last_drawn_record = tuple([int(x.split(" ")[0].split("\n")[1]) for x in stats.split("%")[1:]])
        green_last_draw.append(last_drawn_record[1]), red_last_draw.append(last_drawn_record[2]), blue_last_draw.append(last_drawn_record[3])
        if draw_counter > 1 and previous_stats_record == last_drawn_record:
            print("...... Draw correction ......")
            green_count.pop(), red_count.pop(), blue_count.pop()
            green_last_draw.pop(), red_last_draw.pop(), blue_last_draw.pop()
            driver.find_element(By.XPATH, "//a[normalize-space()='History']").click()  # Click on the "History" tab
            time.sleep(1.5)
            driver.find_element(By.XPATH, "//a[contains(text(),'Total Colour')]").click()  # Click on the "Total Colour" option in the dropdown menu
            time.sleep(0.5)
            driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='100 Draws']").click()
            time.sleep(3)
            stats = driver.find_element(By.XPATH, "//div[@class='p-stats__content']").text
            total_stats = tuple([int(x[-2:]) for x in stats.split("%")[:-1]])
            green_count.append(total_stats[1]), red_count.append(total_stats[2]), blue_count.append(total_stats[3])
            last_drawn_record = tuple([int(x.split(" ")[0].split("\n")[1]) for x in stats.split("%")[1:]])
            green_last_draw.append(last_drawn_record[1]), red_last_draw.append(last_drawn_record[2]), blue_last_draw.append(last_drawn_record[3])
            if previous_stats_record == last_drawn_record:
                print(".... 2nd Draw correction ....")
                driver.refresh()
                time.sleep(1.5)
                green_count.pop(), red_count.pop(), blue_count.pop()
                green_last_draw.pop(), red_last_draw.pop(), blue_last_draw.pop()
                driver.find_element(By.XPATH, "//div[@class='stats__toggle ']").click()  # Click on stats
                time.sleep(1)
                driver.find_element(By.XPATH, "//a[contains(text(),'Total Colour')]").click()  # Click on the "Total Colour" option in the dropdown menu
                time.sleep(0.5)
                driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='100 Draws']").click()
                time.sleep(2)
                stats = driver.find_element(By.XPATH, "//div[@class='p-stats__content']").text
                total_stats = tuple([int(x[-2:]) for x in stats.split("%")[:-1]])
                green_count.append(total_stats[1]), red_count.append(total_stats[2]), blue_count.append(total_stats[3])
                last_drawn_record = tuple([int(x.split(" ")[0].split("\n")[1]) for x in stats.split("%")[1:]])
                green_last_draw.append(last_drawn_record[1]), red_last_draw.append(last_drawn_record[2]), blue_last_draw.append(last_drawn_record[3])
                if (previous_stats_record == last_drawn_record) and draw_error == True:
                    time.sleep(5)
                    while True:
                        counter = driver.find_element(By.XPATH, "//div[@class='timeline__value-txt']").text
                        if int(counter) < 43 and int(counter) > 33:
                            print(".... 3rd Draw correction ....")
                            driver.refresh()
                            time.sleep(1.5)
                            green_count.pop(), red_count.pop(), blue_count.pop()
                            green_last_draw.pop(), red_last_draw.pop(), blue_last_draw.pop()
                            driver.find_element(By.XPATH, "//div[@class='stats__toggle ']").click()  # Click on stats
                            time.sleep(1)
                            driver.find_element(By.XPATH, "//a[contains(text(),'Total Colour')]").click()  # Click on the "Total Colour" option in the dropdown menu
                            time.sleep(0.5)
                            driver.find_element(By.XPATH, "//div[@class='dd__trigger active dd__menu-open']//div[@class='dd__menu-item--value'][normalize-space()='100 Draws']").click()
                            time.sleep(2)
                            stats = driver.find_element(By.XPATH, "//div[@class='p-stats__content']").text
                            total_stats = tuple([int(x[-2:]) for x in stats.split("%")[:-1]])
                            green_count.append(total_stats[1]), red_count.append(total_stats[2]), blue_count.append(total_stats[3])
                            last_drawn_record = tuple([int(x.split(" ")[0].split("\n")[1]) for x in stats.split("%")[1:]])
                            green_last_draw.append(last_drawn_record[1]), red_last_draw.append(last_drawn_record[2]), blue_last_draw.append(last_drawn_record[3])
                            break
                        else:
                            time.sleep(1)
        previous_stats_record = last_drawn_record

        # Check if result is a Win or Loss ----------------------------------------------------------------------------
        result_colours = [last_drawn_record[1], last_drawn_record[2], last_drawn_record[3]]
        if start_trade == True:
            if result_colours[colour_index] == 0:
                start_trade = False
                win_count += 1
                max_loss.append(loss_count)
                loss_count = 0
                # print(f"Total Wins = {win_count} --> Selected Colour = {colour_string} --> Last Loss count = {max_loss[-1]} --> Max Loss = {max(max_loss)}")
                print(f"-------------------------------> {colour_string} WIN = {win_count} Loss_levels = {max_loss[-1]} Max Loss = {max(max_loss)}")

            else:
                loss_count += 1
        # --------------------------------------------------------------------------------------------------------------
   

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
        
        # Record all collected results in a listed tuple
        all_balls = (ball_1, ball_2, ball_3, ball_4, ball_5, ball_6)
        all_record = all_balls + total_stats + last_drawn_record + (colours_count, sum_colours)
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
            print(f"\n               *** ! TRADING PAUSE ! ***\n        {max_running_hours} hours Allocated Trading time exceeded")
            final_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            print(f"Initial Balance = {Initial_balance}")
            print(f"End Balance = {final_balance}")
            print(f"Profit = {final_balance - Initial_balance}")
            break

        # START TRADING CONDITION ------------------------------------------------------------------------------------------------------------------------.
        current_time = datetime.datetime.now().time()  # breaks the program if wrong trading time -------------------------------.                        |
        if (current_time >= datetime.time(23, 30) or current_time < datetime.time(1, 23)) and start_trade == False:#             |                        |
            print(f"\n     *** WRONG TRADING TIME ***\n     {win_count} Wins Achieved - We Continue Tomorrow ...")#              |                        |
            break  # ------------------------------------------------------------------------------------------------------------'                        |
        #                                                                                                                                                 |
        colours = ("green", "red", "blue")#                                                                                                               |
        temp = total_stats[1:] #                                                                                                                          |
        # mid_num = sorted(list(temp))[-2] #                                                                                                                |
        # if (draw_counter >= last_draw_num) and (temp.count(mid_num) == 1) and ((mid_num - min(temp)) <= 6) and (start_trade == False):#                   |
        #     colour_index = temp.index(mid_num)#                                                                                                           |
        #     colour_num = temp[colour_index]#                                                                                                              |
        #     colour_string = colours[colour_index]#                                                                                                        |
        #     if (max(colour_list[colour_index][-max_num:-2]) < colour_num) and ((last_draw_list[colour_index][-10:]).count(0) >= 3):#                      |
        #         trade_status = "---> mid TRADE"#                                                                                                          |
        #         start_trade = True    #                                                                                                                   |
                
        if (draw_counter >= max_num) and (temp.count(max(temp)) == 1) and ((max(temp) - (sorted(list(temp))[-2])) <= 3) and (start_trade == False):#|
            colour_index = temp.index(max(temp))#                                                                                                         |
            colour_num = temp[colour_index]#                                                                                                              |
            colour_string = colours[colour_index]#                                                                                                        |
            if (max(colour_list[colour_index][-max_num:-min_num]) < colour_num) and ((last_draw_list[colour_index][-10:]).count(0) >= 4)\
                and (max(last_draw_list[colour_index][-17:]) <= 5) and len(set(colour_list[colour_index][-4:])) > 1:#                                     |                      
                trade_status = "---> max TRADE"#                                                                                                          |
                start_trade = True    #                                                                                                                   |
                # if notification_start == False:  # For sending email notification to start trading -----------------------.                             |
                #     email_notification("AUTO TRADING STARTED")#                                                           |                             |
                #     notification_start = True  # -------------------------------------------------------------------------'                             |
        #                                                                                                                                                 |        
        print(f"{total_stats[0]} -- {temp} --> {last_drawn_record[1:]} {trade_status}")#                                                                  |
        #                                                                                                                                                 |
        # ------------------------------------------------------------------------------------------------------------------------------------------------'


        # START TRADING if trade condition is True --------------------------------------------------------------------------------------------------------
        if start_trade:
            # print("START TRADE HERE ...")
            before_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            driver.find_element(By.XPATH, "//a[5]").click()  # Total Colour
            time.sleep(1)
            
            stake_amount = martingale_stakes[loss_count]
            driver.find_element(By.XPATH, f"//div[@class='g-total__btn {colour_string} ']").click()  # Click on selected colour
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
                driver.find_element(By.XPATH, "//a[5]").click()  # Total Colour
                driver.find_element(By.XPATH, f"//div[@class='g-total__btn {colour_string} ']").click()
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
            driver.find_element(By.XPATH, f"//div[@class='g-total__btn {colour_string} active']").click()  # to unselect the last picked colour
            time.sleep(8)
            after_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
            if before_balance != after_balance:
                # stake_status = True
                print("success -------------------->")
            else:
                print("!!! stake error !!!")
                driver.find_element(By.XPATH, f"//div[@class='g-total__btn {colour_string} ']").click()
                time.sleep(2)
                driver.find_element(By.XPATH, "//a[@class='place-bet']").click()  # Place bet
                time.sleep(5)
                after_balance = round(float(driver.find_element(By.XPATH, "//div[@class='rs-menu__balance-value']").text))
                if before_balance != after_balance:
                    # stake_status = True
                    print("stake success --------------------> 2")
                driver.find_element(By.XPATH, f"//div[@class='g-total__btn {colour_string} active']").click()  # to unselect
            # -----------------------------------------------------------------------------------------------------------------------------------------

    else: 
        time.sleep(1)  # 1 seconds counter delay

print(f"\nTotal Draws = {draw_counter}")
total_minutes = (draw_counter * 50) // 60
print(f"Total Wins = {win_count}")
print(f"Total Loss = {loss_count}")
print(f"Time Taken = {total_minutes // 60}hrs {total_minutes % 60}mins -----------------------------------------------")

# Close the browser session
driver.quit()