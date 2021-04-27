import json
import requests
from collections import Counter

result = {}

log_list = open('input.txt').readlines()

for idx, log in enumerate(log_list):
    r = requests.get('https://dps.report/getJson?permalink=' + log)
    if r.status_code != 200:
        print("Could not parse log with url: " + str(log) + " . Status code " + str(r.status_code))
    else:
        c = r.content
        j = json.loads(c)

        if j['fightName'] == "Dhuum CM":
            echo_pu_data = []
            f_echo_data = []

        mechanic_per_player = {}
        mechanic_name = "Damage Taken"

        for p in j['players']:
            acc = p['account']
            damage_taken = p['defenses'][0]['damageTaken']

            copy_dict = {}

            mechanic_per_player[acc] = damage_taken

        if mechanic_name in result.keys():
            c = Counter(result[mechanic_name])
            c2 = Counter(mechanic_per_player)
            r = c + c2

            result[mechanic_name] = r
        else:
            result[mechanic_name] = mechanic_per_player

        for mechanic in j['mechanics']:
            # generate mechanics for this log
            mechanic_per_player = {}
            mechanic_name = mechanic['name']
            for i in mechanic.get('mechanicsData'):
                if j['fightName'] == "Dhuum CM":
                    if mechanic_name == "Echo PU":
                        temp_list = [i['actor'], i['time']]
                        echo_pu_data.append(temp_list)
                    elif mechanic_name == "F Echo":
                        temp_list = [i['actor'], i['time']]
                        f_echo_data.append(temp_list)

                        if mechanic_per_player.get(i['actor']) is None:
                            mechanic_per_player[i['actor']] = 1
                        else:
                            mechanic_per_player[i['actor']] += 1
                    else:
                        if mechanic_per_player.get(i['actor']) is None:
                            mechanic_per_player[i['actor']] = 1
                        else:
                            mechanic_per_player[i['actor']] += 1
                else:
                    if mechanic_per_player.get(i['actor']) is None:
                        mechanic_per_player[i['actor']] = 1
                    else:
                        mechanic_per_player[i['actor']] += 1

            accounts = j['players']

            copy_dict = {}

            for m in mechanic_per_player:
                for a in accounts:
                    if a['name'] == m:
                        copy_dict[a['account']] = mechanic_per_player[m]

            mechanic_per_player = copy_dict

            if mechanic_name in result.keys():
                c = Counter(result[mechanic_name])
                c2 = Counter(mechanic_per_player)
                r = c + c2

                result[mechanic_name] = r
            else:
                result[mechanic_name] = mechanic_per_player

        if j['fightName'] == "Dhuum CM" and len(echo_pu_data) > 0:
            mechanic_per_player = {}
            mechanic_name = "Echo PU"
            if len(f_echo_data) == 0:
                for e in echo_pu_data:
                    if mechanic_per_player.get(e[0]) is None:
                        mechanic_per_player[e[0]] = 1
            else:
                for f in f_echo_data:
                    if mechanic_per_player.get(f[0]) is None:
                        mechanic_per_player[f[0]] = 1
                    else:
                        mechanic_per_player[f[0]] += 1

                last_free_tick = f_echo_data[-1][1]
                pu_left_overs = []
                pu_left_overs_players = []

                for e in echo_pu_data:
                    if e[1] > last_free_tick:
                        pu_left_overs.append(e)

                for p in pu_left_overs:
                    if p[0] not in pu_left_overs_players:
                        pu_left_overs_players.append(p[0])

                for pu in pu_left_overs_players:
                    if mechanic_per_player.get(pu) is None:
                        mechanic_per_player[pu] = 1
                    else:
                        mechanic_per_player[pu] += 1

            accounts = j['players']

            copy_dict = {}

            for m in mechanic_per_player:
                for a in accounts:
                    if a['name'] == m:
                        copy_dict[a['account']] = mechanic_per_player[m]

            mechanic_per_player = copy_dict

            if mechanic_name in result.keys():
                c = Counter(result[mechanic_name])
                c2 = Counter(mechanic_per_player)
                r = c + c2

                result[mechanic_name] = r
            else:
                result[mechanic_name] = mechanic_per_player

    print(str(idx + 1) + "/" + str(len(log_list)))

for r in result:
    try:
        result[r] = result[r].most_common()
    except:
        result[r] = result[r]


# write result to file
f = open("output.txt", "a")
for r in result:
    f.write("\n" + r + ":\n")
    for player in result[r]:
        f.write(str(player[0]) + ": " + str(player[1]) + str("\n"))
f.close()
