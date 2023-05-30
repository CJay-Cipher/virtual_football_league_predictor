# Open the file in read mode
file = open('league_6095.txt', 'r')

# Read the contents of the file
contents = file.read()

# Close the file
file.close()

# league_id, week, hour, minute, ht, at, ht_point, at_point, ht_pos, at_pos, hl5ms, al5ms, hl4ms, al4ms, hl3ms, al3ms, hl2ms, al2ms, hlms, alms

# Print the contents of the file
weeks = contents.split("WEEK")
pos = weeks[0].index("League")
league_id = int(weeks[0][(pos + 7): (pos + 11)])
print("League -", league_id)

sample = ' 1   12:52:00\nEVE\t1-2\tMNC\nBRN\t0-1\tTOT\nBRI\t1-0\tFUL\nLEI\t2-1\tWHU\nWOL\t0-0\tARS\nASV\t2-3\tLIV\nCRY\t3-1\tFOR\nCHE\t3-3\tMNU\nLEE\t2-2\tBOU\nSOU\t0-2\tNWC\n'
sample.split("\n")[1:-1]

record = []
for week in weeks[1:]:
    temp_dict  = {}
    temp_dict["league_id"] = league_id
    temp_dict["week"] = int((week[:3]).strip())
    temp_dict["hour"] = int(week[5:7])
    temp_dict["minute"] = int(week[8:10])

    record.append(temp_dict)
    
print(record)
    # teams_score = week.split("\n")
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