import pandas as pd
import statistics as st
# pd.set_option('display.max_columns', None)
# ------------------------------------------------------------------------------------------------------

FIVE, FOUR, THREE, TWO, ONE, ZERO = 5, 4, 3, 2, 1, 0

def txt_reader(_path):
    file = open(_path, 'r')  # Open the file in read mode
    contents = file.read()  # Read the contents of the file
    file.close()  # Close the file

    return contents

def table_creator(contents):

    weeks = contents.split("WEEK")
    pos = weeks[0].index("League")
    league_no = int(weeks[0][(pos + 7): (pos + 11)])
    for val in weeks[1:]:
        scores = val.split("\n")[1:-1]
        for score in scores:
            # print(score)
            league_id.append(league_no)
            week.append(int((val[:3]).strip()))
            hour.append(int(val.split("\n")[0][-8:-6]))
            minute.append(int(val.split("\n")[0][-5:-3]))

            home_team.append(score[0:3])
            away_team.append(score[8:11])
            home_score.append(int(score[4]))
            away_score.append(int(score[6]))

    data_table = pd.DataFrame(
        {
            "league_id": league_id,
            "week": week,
            "hour": hour,
            "minutes": minute,
            "HT": home_team,
            "AT": away_team,
            "HCS": home_score,
            "ACS": away_score
        }
    )
    return data_table


# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------
def add_features(dataframe):
    def update_match_result(home_team, away_team, home_score, away_score, premier_league_table):
        home_index = -1
        away_index = -1
        for i, team in enumerate(premier_league_table):
            if team['team'] == home_team:
                home_index = i
            elif team['team'] == away_team:
                away_index = i

        premier_league_table[home_index]['played'] += 1
        premier_league_table[home_index]['goals_for'] += home_score
        premier_league_table[home_index]['goals_agst'] += away_score
        premier_league_table[away_index]['played'] += 1
        premier_league_table[away_index]['goals_for'] += away_score
        premier_league_table[away_index]['goals_agst'] += home_score

        premier_league_table[home_index]['goal_diff'] = \
            premier_league_table[home_index]['goals_for'] - premier_league_table[home_index]['goals_agst']

        premier_league_table[away_index]['goal_diff'] = \
            premier_league_table[away_index]['goals_for'] - premier_league_table[away_index]['goals_agst']

        if home_score > away_score:
            premier_league_table[home_index]['wins'] += 1
            premier_league_table[home_index]['points'] += 3
            premier_league_table[away_index]['losses'] += 1
        elif home_score < away_score:
            premier_league_table[away_index]['wins'] += 1
            premier_league_table[away_index]['points'] += 3
            premier_league_table[home_index]['losses'] += 1
        else:
            premier_league_table[home_index]['draws'] += 1
            premier_league_table[home_index]['points'] += 1
            premier_league_table[away_index]['draws'] += 1
            premier_league_table[away_index]['points'] += 1

        # Sort table by points, then alphabetically if multiple teams have the same points
        premier_league_table.sort(key=lambda x: (-x['points'], x['team']))

        # Assign positions to teams
        for i, team in enumerate(premier_league_table):
            team['position'] = i + 1

        return premier_league_table

    global table
    temp_df = dataframe.copy()

    # Initialize dictionaries and variables
    team_dict = {team: [] for team in teams}  # Dictionary to store scores for each team
    team_status = {team: [] for team in teams}  # Dictionary to store results (W/D/L) for each team

    h3, h2, h1= 0, 0, 0  # Variables to store home team scores from previous matches
    a3, a2, a1= 0, 0, 0  # Variables to store away team scores from previous matches
    hs_3, hs_2, hs_1 = 0, 0, 0  # Variables to store home team result (W/D/L) from previous matches
    as_3, as_2, as_1 = 0, 0, 0  # Variables to store away team result (W/D/L) from previous matches

    hsa, asa = 0, 0  # variables to store home & awat team scoring average
    hwr, hlr, hdr = 0, 0, 0  # store home and away win ratio
    awr, alr, adr = 0, 0, 0  # store home and away win, lose & draw ratio

    # Loop through each row in the dataframe
    for _, row in temp_df.iterrows():
        home_t = row["HT"]
        ht_score = row["HCS"]
        away_t = row["AT"]
        at_score = row["ACS"]

        # Update the league table with the match result
        table = update_match_result(home_t, away_t, ht_score, at_score, premier_league_table)
        temp = pd.DataFrame(table)

        # Add home team points and position to ht_points and ht_pos lists
        ht_points.append(temp.loc[temp['team'] == home_t, "points"].iloc[0])
        ht_pos.append(temp.loc[temp['team'] == home_t, "position"].iloc[0])

        # Add away team points and position to at_points and at_pos lists
        at_points.append(temp.loc[temp['team'] == away_t, "points"].iloc[0])
        at_pos.append(temp.loc[temp['team'] == away_t, "position"].iloc[0])

        # Add home & away wins, draws, losses, goals for, goals against, and goal diff to corresponding lists
        val_list = ["wins", "draws", "losses", "goals_for", "goals_agst", "goal_diff"]
        home_list = [h_wins, h_draws, h_loss, h_gf, h_ga, h_gd]
        away_list = [a_wins, a_draws, a_loss, a_gf, a_ga, a_gd]
        for home, away, val in zip(home_list, away_list, val_list):
            home.append(temp.loc[temp['team'] == home_t, val].iloc[0])
            away.append(temp.loc[temp['team'] == away_t, val].iloc[0])

        # Update home and away team dictionaries and status dictionaries with scores and results
        current_week = row["week"]
        for (a, b), c in zip(team_dict.items(), team_status.values()):
            
            if a == home_t:
                if current_week >= FIVE:
                    hsa = st.mean(b[-THREE:])
                    h3, hs_3 = b[-THREE], c[-THREE]
                    h2, hs_2 = b[-TWO], c[-TWO]
                    h1, hs_1 = b[-ONE], c[-ONE]
                    
                    hwr = c.count(ONE) / len(c)
                    hlr = c.count(-ONE) / len(c)
                    hdr = c.count(ZERO) / len(c)

                b.append(ht_score)

                # mapping "W" = 1, "D" = 0, "L" = -1
                c.append(ONE if ht_score > at_score else -ONE if ht_score < at_score else ZERO)

            elif a == away_t:
                if current_week >= FIVE:
                    asa = st.mean(b[-THREE:])
                    a3, as_3 = b[-THREE], c[-THREE]
                    a2, as_2 = b[-TWO], c[-TWO]
                    a1, as_1 = b[-ONE], c[-ONE]
                    
                    awr = c.count(ONE) / len(c)
                    alr = c.count(-ONE) / len(c)
                    adr = c.count(ZERO) / len(c)

                b.append(at_score)

                # mapping "W" = 1, "D" = 0, "L" = -1
                c.append(ONE if ht_score < at_score else -ONE if ht_score > at_score else ZERO)

        hs_avg.append(hsa), as_avg.append(asa)  # Adding scoring average

        # Adding win, lose and draw ratio
        hw_rat.append(hwr), hl_rat.append(hlr), hd_rat.append(hdr)
        aw_rat.append(awr), al_rat.append(alr), ad_rat.append(adr)

        # Add home and away team scores from previous matches to corresponding lists
        HL3S.append(h3), HL2S.append(h2), HL1S.append(h1)
        AL3S.append(a3), AL2S.append(a2), AL1S.append(a1)

        # Add home and away team result (W/D/L) from previous matches to corresponding lists
        hl3_stat.append(hs_3), hl2_stat.append(hs_2), hl1_stat.append(hs_1)
        al3_stat.append(as_3), al2_stat.append(as_2), al1_stat.append(as_1)

    # Create a new dictionary with the additional columns
    new_cols = {
        "HL1S": HL1S, "AL1S": AL1S, "HL2S": HL2S, 
        "AL2S": AL2S, "HL3S": HL3S, "AL3S": AL3S,

        "hl1_stat": hl1_stat, "al1_stat": al1_stat,
        "hl2_stat": hl2_stat, "al2_stat": al2_stat,
        "hl3_stat": hl3_stat, "al3_stat": al3_stat,

        "h_wins": h_wins, "a_wins": a_wins, "h_draws": h_draws, "a_draws": a_draws,
        "h_loss": h_loss, "a_loss": a_loss, "h_gf": h_gf, "a_gf": a_gf,
        "h_ga": h_ga, "a_ga": a_ga, "h_gd": h_gd, "a_gd": a_gd,

        "hs_avg": hs_avg, "as_avg": as_avg,

        # "H_ADV": H_ADV, #"A_ADV": A_ADV,

        "hw_rat": hw_rat, "aw_rat": aw_rat, 
        "hl_rat": hl_rat, "al_rat": al_rat, 
        "hd_rat": hd_rat, "ad_rat": ad_rat,

        "ht_points": ht_points, "at_points": at_points,
        "ht_pos": ht_pos, "at_pos": at_pos
    }
    # Add the new columns to the dataframe
    temp_df = temp_df.assign(**new_cols)

    return temp_df


# -----------------------------------------------------------------------------------------------------------

path = "league_data"
test_record = [f"{path}/L_18.txt"]
record = [
    f"{path}/L_6095.txt", f"{path}/L_6097.txt", f"{path}/L_6099.txt",
    f"{path}/L_6148.txt", f"{path}/L_6152.txt", f"{path}/L_6153.txt",
    f"{path}/L_6155.txt", f"{path}/L_6155.txt", f"{path}/L_6166.txt",
    f"{path}/L_6169.txt", f"{path}/L_6170.txt", f"{path}/L_6171.txt",
    f"{path}/L_6173.txt", f"{path}/L_6180.txt", f"{path}/L_6181.txt",
    f"{path}/L_6189.txt", f"{path}/L_6192.txt", f"{path}/L_6211.txt",
    f"{path}/L_6212.txt", f"{path}/L_6213.txt", f"{path}/L_6214.txt",
    f"{path}/L_6215.txt", f"{path}/L_6216.txt", f"{path}/L_6226.txt", 
    f"{path}/L_6227.txt", f"{path}/L_6230.txt"
]

f_paths = record

df_list = []
print(".txt files preprocessing --> \nPlease Wait ...")
for path in f_paths:
    teams = ['FOR', 'MNC', 'ASV', 'TOT', 'EVE', 'CHE', 'BRN', 'WHU', 'ARS', 'FUL',
             'NWC', 'BOU', 'LEI', 'LIV', 'WOL', 'MNU', 'LEE', 'SOU', 'BRI', 'CRY']
    premier_league_table = []

    for team in teams:
        team_dict = {
            'team': team,
            'played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_for': 0,
            'goals_agst': 0,
            'goal_diff': 0,
            'points': 0,
            'position': 0
        }
        premier_league_table.append(team_dict)

    league_id, week, hour, minute = [], [], [], []
    home_team, away_team, home_score, away_score = [], [], [], []

    ht_points, at_points, ht_pos, at_pos = [], [], [], []

    h_wins, h_draws, h_loss, h_gf, h_ga, h_gd = [], [], [], [], [], []
    a_wins, a_draws, a_loss, a_gf, a_ga, a_gd = [], [], [], [], [], []

    hs_avg, as_avg = [], []  # home & away Scoring averagae column
    # H_ADV = []
    hw_rat, hl_rat, hd_rat = [], [], []
    aw_rat, al_rat, ad_rat = [], [], []

    HL1S, HL2S, HL3S = [], [], []
    AL1S, AL2S, AL3S = [], [], []

    hl3_stat, hl2_stat, hl1_stat = [], [], []
    al3_stat, al2_stat, al1_stat = [], [], []

    text_content = txt_reader(path)
    update_df = table_creator(text_content)
    update_df = add_features(update_df)

    df_list.append(update_df)

df = pd.concat(df_list, ignore_index=True)
print(f"All {len(f_paths)} .txt Files Successfully Processed ...\n{df.shape[0]} Observations")

df.to_csv("league_record.csv", index=False)
print("\n... Pre-processing Completed ...\nCSV Saved Successfully \n")

# print(df.tail(10))

# print(pd.DataFrame(premier_league_table))
