import csv
import json
import requests
from datetime import datetime

result = [['Date', 'Encounter', 'Profession', 'Alive', 'DPS', 'Breakbar Damage', 'Log']]

account_name = 'Visceryn.5429'

log_list = open('visc_input.txt').readlines()

for log in log_list:
    result_dict = []
    r = requests.get('https://dps.report/getJson?permalink=' + log)
    if r.status_code != 200:
        print("Could not parse log with url: " + str(log) + " . Status code " + str(r.status_code))
    else:
        c = r.content
        j = json.loads(c)

        alive = 100
        dps = 0
        breakbar_damage = 'None'
        s_banner_uptime = 0
        d_banner_uptime = 0

        for p in j['players']:
            if p['account'] == account_name and p['profession']:
                # player name
                player_name = p['name']

                # class
                player_class = p['profession']

                # dps
                dps = p['dpsAll'][0]['dps']

                # get breakbar damage
                if 'breakbarDamage1S' in p:
                    breakbar_damage = p['breakbarDamage1S'][0]
                    breakbar_damage = breakbar_damage[-1]

        # find death
        for m in j['mechanics']:
            if m['name'] == 'Dead':
                for d in m['mechanicsData']:
                    if d['actor'] == player_name:
                        time_of_death = int(d['time'])
                        duration = datetime.strptime(j['duration'], "%Mm %Ss %fms")
                        duration = int((duration.minute * 60 + duration.second) * 1000 + duration.microsecond / 1000)

                        alive = round(time_of_death / duration * 100, 2)

        date = j['timeStart']

        result_dict.append(date[:-4])
        result_dict.append(j['fightName'])
        result_dict.append(player_class)
        result_dict.append(alive if alive < 100 else 100)
        result_dict.append(dps)
        result_dict.append(breakbar_damage)
        result_dict.append(log[:-1])

        result.append(result_dict)

for r in result:
    print(r)

with open('visc_output.csv', 'w', newline='') as output:
    wr = csv.writer(output)
    for r in result:
        wr.writerow(r)
