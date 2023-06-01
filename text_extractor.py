import pandas as pd
pd.set_option('display.max_columns', None)

# Open the file in read mode
file = open('league_6097.txt', 'r')

# Read the contents of the file
contents = file.read()

# Close the file
file.close()

# league_id, week, hour, minute, ht, at, ht_point, at_point, ht_pos, at_pos,
# hl5ms, al5ms, hl4ms, al4ms, hl3ms, al3ms, hl2ms, al2ms, hlms, alms

# print()
# for a, b, c, d in zip(home_team, away_team, home_score, away_score):
#     print(a, c, "-", d, b)

teams = ['FOR', 'MNC', 'ASV', 'TOT', 'EVE', 'CHE', 'BRN', 'WHU', 'ARS', 'FUL',
         'NWC', 'BOU', 'LEI', 'LIV', 'WOL', 'MNU', 'LEE', 'SOU', 'BRI', 'CRY']

weeks = contents.split("WEEK")
pos = weeks[0].index("League")
league_no = int(weeks[0][(pos + 7): (pos + 11)])

record = []
league_id, week, hour, minute = [], [], [], []
home_team, away_team, home_score, away_score = [], [], [], []

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
        home_score.append(score[4])
        away_score.append(score[6])

df = pd.DataFrame(
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
HL5S, HL4S, HL3S, HL2S = [], [], [], []
AL5S, AL4S, AL3S, AL2S = [], [], [], []

num = 5
team_dict = {team: [] for team in teams}
h5, h4, h3, h2, = 0, 0, 0, 0
a5, a4, a3, a2, = 0, 0, 0, 0

for index, row in df.iterrows():
    current_week = row["week"]
    for a, b in team_dict.items():
        if a == row["HT"]:
            b.append(row["HLS"])
            if current_week >= num:
                h5 = b[current_week - 5]
                h4 = b[current_week - 4]
                h3 = b[current_week - 3]
                h2 = b[current_week - 2]

        elif a == row["AT"]:
            b.append(row["ALS"])
            if current_week >= num:
                a5 = b[current_week - 5]
                a4 = b[current_week - 4]
                a3 = b[current_week - 3]
                a2 = b[current_week - 2]

    HL5S.append(h5), HL4S.append(h4), HL3S.append(h3), HL2S.append(h2)
    AL5S.append(a5), AL4S.append(a4), AL3S.append(a3), AL2S.append(a2)

new_cols = {
    "HL5S": HL5S, "AL5S": AL5S, "HL4S": HL4S, "AL4S": AL4S,
    "HL3S": HL3S, "AL3S": AL3S, "HL2S": HL2S, "AL2S": AL2S
}
df = df.assign(**new_cols)
# for key, value in new_cols.items():
#     print(key, "-", value)

print(df.tail(60))

# df["ht_point"] = 0
# temp_df = df[(df['week'] >= 6) & (df['week'] <= 33)]
# new_df = df[df["week"] < 6]
# # print(new_df)
# for team in teams:
#     temp = df[(df["HT"] == team) | (df["AT"] == team)]
#     print(temp)
        # df["hl5ms"] = df[(df["HT"] == team) | (df["AT"] == team)][ if df["week"] > 5 else 0
#         teams_score = week.split("\n")
    # teams_score = teams_score[1:-1][count]
    # temp_dict["ht"] = teams_score[0:3]
    # temp_dict["at"] = week[8:11]

    # temp_dict["hlms"] = week[4]
    # temp_dict["alms"] = week[6]

    # "ht_point": 0,
    # "at_point": 0,
    # "ht_pos": 0,
    # "at_pos": 0,
    # "hl5ms": 0,
    # "al5ms": 0,
    # "hl4ms": 0,
    # "al4ms": 0,
    # "hl3ms": 0,
    # "al3ms": 0,
    # "hl2ms": 0,
    # "al2ms": 0,


