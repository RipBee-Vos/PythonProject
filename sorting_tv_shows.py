# Read filename from input
filename = input()

# Dictionary to hold seasons as keys and list of shows as values
season_dict = {}

# Read input file
with open(filename, 'r') as file:
    lines = [line.strip() for line in file.readlines()]

# Build dictionary from alternating lines
for i in range(0, len(lines), 2):
    seasons = int(lines[i])
    show = lines[i + 1]
    if seasons not in season_dict:
        season_dict[seasons] = []
    season_dict[seasons].append(show)

# Write output_keys.txt (sorted by season count)
with open('output_keys.txt', 'w') as f_keys:
    for key in sorted(season_dict.keys()):
        shows = '; '.join(season_dict[key])
        f_keys.write(f"{key}: {shows}\n")

# Write output_titles.txt (sorted alphabetically)
all_shows = []
for show_list in season_dict.values():
    all_shows.extend(show_list)

with open('output_titles.txt', 'w') as f_titles:
    for show in sorted(all_shows):
        f_titles.write(f"{show}\n")

