import pandas as pd
pd.set_option('display.max_columns', None)
# ------------------------------------------------------------------------------------------------------

teams = ['FOR', 'MNC', 'ASV', 'TOT', 'EVE', 'CHE', 'BRN', 'WHU', 'ARS', 'FUL',
         'NWC', 'BOU', 'LEI', 'LIV', 'WOL', 'MNU', 'LEE', 'SOU', 'BRI', 'CRY']

FIVE, FOUR, THREE, TWO, ONE = 5, 4, 3, 2, 1

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
            "HLS": home_score,
            "ALS": away_score
        }
    )
    return data_table


# --------------------------------------------------------------------------------------------
def update_match_result(table, home_team, away_team, home_score, away_score):
    # Update total played for both teams
    table.loc[table['Team'] == home_team, 'Total_Played'] += 1
    table.loc[table['Team'] == away_team, 'Total_Played'] += 1

    # Update total goals for both teams
    table.loc[table['Team'] == home_team, 'Goals'] += home_score
    table.loc[table['Team'] == away_team, 'Goals'] += away_score

    # Update total wins, losses, and draws for both teams based on the result
    if home_score > away_score:
        table.loc[table['Team'] == home_team, 'Total_Won'] += 1
        table.loc[table['Team'] == away_team, 'Total_Lost'] += 1
        home_points = 3
        away_points = 0
    elif home_score < away_score:
        table.loc[table['Team'] == away_team, 'Total_Won'] += 1
        table.loc[table['Team'] == home_team, 'Total_Lost'] += 1
        home_points = 0
        away_points = 3
    else:
        table.loc[table['Team'] == home_team, 'Total_Draw'] += 1
        table.loc[table['Team'] == away_team, 'Total_Draw'] += 1
        home_points = 1
        away_points = 1

    # Update total points for both teams based on the Premier League standard
    table.loc[table['Team'] == home_team, 'Total_Points'] += home_points
    table.loc[table['Team'] == away_team, 'Total_Points'] += away_points

    # Update goal difference for both teams
    table.loc[table['Team'] == home_team, 'Goal_Diff'] += home_score - away_score
    table.loc[table['Team'] == away_team, 'Goal_Diff'] += away_score - home_score

    # Sort the table by total points, goal difference and goals scored to get the current ranking
    updated_table = table.sort_values(by=['Total_Points', 'Goal_Diff', 'Goals'], ascending=False)

    # Assign positions to each team based on the ranking
    updated_table['Position'] = updated_table['Total_Points'].rank(method='dense', ascending=False).astype(int)

    # Get the updated info for the home team
    home_team_info = updated_table.loc[updated_table['Team'] == home_team]
    home_team_position = int(home_team_info['Position'].iloc[0])
    home_team_points = int(home_team_info['Total_Points'].iloc[0])

    # Get the updated info for the away team
    away_team_info = updated_table.loc[updated_table['Team'] == away_team]
    away_team_position = int(away_team_info['Position'].iloc[0])
    away_team_points = int(away_team_info['Total_Points'].iloc[0])

    # Return the updated points, position, and table for both teams
    return home_team_points, home_team_position, away_team_points, away_team_position, updated_table


# --------------------------------------------------------------------------------------------------
def add_features(dataframe):
    global table
    temp_df = dataframe.copy()

    team_dict = {team: [] for team in teams}
    team_status = {team: [] for team in teams}

    h5, h4, h3, h2, = 0, 0, 0, 0
    a5, a4, a3, a2, = 0, 0, 0, 0

    hs_3, hs_2, hs_1 = 0, 0, 0
    as_3, as_2, as_1 = 0, 0, 0

    for index, row in temp_df.iterrows():
        home_t = row["HT"]
        ht_score = row["HLS"]
        away_t = row["AT"]
        at_score = row["ALS"]

        ht_p, htp, at_p, atp, table = update_match_result(table, home_t, away_t, ht_score, at_score)
        ht_points.append(ht_p), at_points.append(at_p), ht_pos.append(htp), at_pos.append(atp)

        current_week = row["week"]
        for (a, b), c in zip(team_dict.items(), team_status.values()):
            if a == home_t:
                b.append(ht_score)
                c.append("W" if ht_score > at_score else "L" if ht_score < at_score else "D")
                if current_week >= FIVE:
                    h5 = b[current_week - FIVE]
                    h4 = b[current_week - FOUR]
                    h3, hs_3 = b[current_week - THREE], c[current_week - THREE]
                    h2, hs_2 = b[current_week - TWO], c[current_week - TWO]
                    hs_1 = c[current_week - ONE]
            elif a == away_t:
                b.append(at_score)
                c.append("W" if ht_score < at_score else "L" if ht_score > at_score else "D")
                if current_week >= FIVE:
                    a5 = b[current_week - FIVE]
                    a4 = b[current_week - FOUR]
                    a3, as_3 = b[current_week - THREE], c[current_week - THREE]
                    a2, as_2 = b[current_week - TWO], c[current_week - TWO]
                    as_1 = c[current_week - ONE]
        HL5S.append(h5), HL4S.append(h4), HL3S.append(h3), HL2S.append(h2)
        AL5S.append(a5), AL4S.append(a4), AL3S.append(a3), AL2S.append(a2)

        hl3_stat.append(hs_3), hl2_stat.append(hs_2), hl_stat.append(hs_1)
        al3_stat.append(as_3), al2_stat.append(as_2), al_stat.append(as_1)

    new_cols = {
        "HL2S": HL2S, "AL2S": AL2S, "HL3S": HL3S, "AL3S": AL3S,
        "HL4S": HL4S, "AL4S": AL4S, "HL5S": HL5S, "AL5S": AL5S,

        "hl_stat": hl_stat, "al_stat": al_stat,
        "hl2_stat": hl2_stat, "al2_stat": al2_stat,
        "hl3_stat": hl3_stat, "al3_stat": al3_stat,

        "ht_points": ht_points, "at_points": at_points,
        "ht_pos": ht_pos, "at_pos": at_pos
    }
    temp_df = temp_df.assign(**new_cols)

    return temp_df


# -----------------------------------------------------------------------------------------------------------

path = "league_data"
test_record = [f"{path}/league_9.txt"]
record = [f"{path}/L_6095.txt", f"{path}/L_6097.txt", f"{path}/L_6099.txt", f"{path}/L_6148.txt"]

f_paths = record

df_list = []
print(".txt files preprocessing --> \nPlease Wait ...")
for path in f_paths:
    # Create an initial league table with zero points for all teams
    table = pd.DataFrame(
        {'Team': teams, 'Total_Played': 0, 'Total_Won': 0, 'Total_Lost': 0,
         'Total_Draw': 0, 'Goals': 0, 'Goal_Diff': 0, 'Total_Points': 0, 'Position': 0})

    league_id, week, hour, minute = [], [], [], []
    home_team, away_team, home_score, away_score = [], [], [], []

    ht_points, at_points, ht_pos, at_pos = [], [], [], []

    HL5S, HL4S, HL3S, HL2S = [], [], [], []
    AL5S, AL4S, AL3S, AL2S = [], [], [], []

    hl3_stat, hl2_stat, hl_stat = [], [], []
    al3_stat, al2_stat, al_stat = [], [], []

    text_content = txt_reader(path)
    update_df = table_creator(text_content)
    update_df = add_features(update_df)

    df_list.append(update_df.drop(range(40)))

df = pd.concat(df_list, ignore_index=True)
df.to_csv("league_record.csv", index=False)
print("\n... Pre-processing Completed ...\nFiles Saved Successfully ")
# print(df.tail(50))

# print(table[["Team", "Goals", "Goal_Diff", "Total_Points", "Position"]])
