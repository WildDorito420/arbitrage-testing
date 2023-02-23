import requests,json,os,math

csvArr = []
csvArr.append("id,sport_key,commence,home_team,away_team,home_odds,home_bookie,home_bet,away_odds,away_bookie,away_bet,draw_odds,draw_bookie,draw_bet,winnings")

allowed_groups = ["Baseball", "American Football", "Aussie Rules", "Basketball", "Soccer", "Rugby League", "Cricket"]

def Average(lst):
    return sum(lst) / len(lst)

def process(resp):
    for i in resp:

        if i["home_team"] == None or i["away_team"] == None:
            continue

        # print(str(i))
        dictArr = {}
        dictArr["details"] = {'id':str(i["id"]), 'sport_key':str(i["sport_key"]),'commence':str(i["commence_time"])}
        dictArr[str(i["home_team"])] = {'odds':0,'bookie':''}
        dictArr[str(i["away_team"])] = {'odds':0,'bookie':''}
        dictArr["Draw"] = {'odds':0,'bookie':''}
        # print(str(i["sport_title"]) + " " + str(i["home_team"]) + " " + str(i["away_team"]))

        for j in i["bookmakers"]:
            outcomes = j["markets"][0]["outcomes"]
            bookie = j["key"]

            for l in outcomes:
                ht = l["name"]
                ho = l["price"]

                dho = dictArr[ht]['odds']

                if ho > dho:
                    dictArr[ht]['odds'] = ho
                    dictArr[ht]['bookie'] = bookie
        
        if dictArr["Draw"]["odds"] == 0:
            test = (1/dictArr[str(i["home_team"])]["odds"]) + (1/dictArr[str(i["away_team"])]["odds"])
        else:
            test = (1/dictArr[str(i["home_team"])]["odds"]) + (1/dictArr[str(i["away_team"])]["odds"]) + (1/dictArr["Draw"]["odds"])

        if test < 1:
            print("PROFIT: " + str(i["home_team"]) + "(Odds: " + str(dictArr[i["home_team"]]["odds"]) + " Bookie: " + str(dictArr[i["home_team"]]["bookie"]) + ") v " + str(i["away_team"]) + "(Odds: " + str(dictArr[i["away_team"]]["odds"]) + " Bookie: " + str(dictArr[i["away_team"]]["bookie"]) + ") Draw Odds: " + str(dictArr["Draw"]["odds"]) + " Bookie: " + str(dictArr["Draw"]["bookie"]) + "" )
        # else:
        #     print("NO PROFIT: " + str(i["home_team"]) + " v " + str(i["away_team"]) + " " +  str(test))
        
        if dictArr["Draw"]["odds"] == 0 and test < 1:
            profit_2(dictArr, str(i["home_team"]), str(i["away_team"]))
        elif dictArr["Draw"]["odds"] > 0 and test < 1:
            profit_3(dictArr, str(i["home_team"]), str(i["away_team"]))

def profit_3(dictArr, home, away):
    total = 100
    odds_one = dictArr[home]["odds"]
    odds_two = dictArr[away]["odds"]
    odds_draw = dictArr["Draw"]["odds"]
    wage_one = total / (1 + ( odds_one / odds_two) + (odds_one / odds_draw))
    wage_two = total / (1 + ( odds_two / odds_one) + (odds_two / odds_draw))
    wage_draw = total / (1 + ( odds_draw / odds_one) + (odds_draw / odds_two))
    final_total = wage_one + wage_two + wage_two

    one_win = (wage_one * odds_one) - total
    two_win = (wage_two * odds_two) - total
    draw_win = (wage_draw * odds_draw) - total

    print("Out of $" + str(total) + ", place $" + str(wage_one) + " on " + str(home) + " through " + str(dictArr[home]["bookie"]) + " to win $" + str(one_win))
    print("Out of $" + str(total) + ", place $" + str(wage_two) + " on " + str(away) + " through " + str(dictArr[away]["bookie"]) + " to win $" + str(two_win))
    print("Out of $" + str(total) + ", place $" + str(wage_draw) + " on Draw through " + str(dictArr["Draw"]["bookie"]) + " to win $" + str(draw_win))

    csvArr.append(dictArr["details"]["id"] + "," + dictArr["details"]["sport_key"] + "," + str(dictArr["details"]["commence"]) + "," + home + "," + away + "," + str(odds_one) + "," + str(dictArr[home]["bookie"]) +  "," + str(wage_one) + "," + str(odds_two) + "," + str(dictArr[away]["bookie"]) + "," + str(wage_two) + "," + str(dictArr["Draw"]["odds"]) + "," + str(dictArr["Draw"]["bookie"]) + "," + str(wage_draw) + "," + str(Average([one_win, two_win, draw_win])))

def profit_2(dictArr, home, away):
    total = 100
    odds_one = dictArr[home]["odds"]
    odds_two = dictArr[away]["odds"]
    wage_one = total / ( odds_one / odds_two + 1)
    wage_two = total / ( odds_two / odds_one + 1)

    one_win = (wage_one * odds_one) - total
    two_win = (wage_two * odds_two) - total

    print("Out of $" + str(total) + ", place $" + str(wage_one) + " on " + str(home) + " through " + str(dictArr[home]["bookie"]) + " to win $" + str(one_win))
    print("Out of $" + str(total) + ", place $" + str(wage_two) + " on " + str(away) + " through " + str(dictArr[away]["bookie"]) + " to win $" + str(two_win))

    csvArr.append(dictArr["details"]["id"] + "," + dictArr["details"]["sport_key"] + "," + str(dictArr["details"]["commence"]) + "," + home + "," + away + "," + str(odds_one) + "," + str(dictArr[home]["bookie"]) +  "," + str(wage_one) + "," + str(odds_two) + "," + str(dictArr[away]["bookie"]) + "," + str(wage_two) + ",,,," + str(Average([one_win, two_win])))



key = "xxxxx"

url = "https://api.the-odds-api.com/v4/sports/?apiKey=" + key

resp1 = '[{"key":"americanfootball_ncaaf","group":"American Football","title":"NCAAF","description":"US College Football","active":true,"has_outrights":false},{"key":"americanfootball_nfl","group":"American Football","title":"NFL","description":"US Football","active":true,"has_outrights":false},{"key":"americanfootball_nfl_super_bowl_winner","group":"American Football","title":"NFL Super Bowl Winner","description":"Super Bowl Winner 2022/2023","active":true,"has_outrights":true},{"key":"aussierules_afl","group":"Aussie Rules","title":"AFL","description":"Aussie Football","active":true,"has_outrights":false},{"key":"baseball_mlb_world_series_winner","group":"Baseball","title":"MLB World Series Winner","description":"World Series Winner 2023","active":true,"has_outrights":true},{"key":"basketball_euroleague","group":"Basketball","title":"Basketball Euroleague","description":"Basketball Euroleague","active":true,"has_outrights":false},{"key":"basketball_nba","group":"Basketball","title":"NBA","description":"US Basketball","active":true,"has_outrights":false},{"key":"basketball_nba_championship_winner","group":"Basketball","title":"NBA Championship Winner","description":"Championship Winner 2022/2023","active":true,"has_outrights":true},{"key":"basketball_ncaab","group":"Basketball","title":"NCAAB","description":"US College Basketball","active":true,"has_outrights":false},{"key":"cricket_big_bash","group":"Cricket","title":"Big Bash","description":"Big Bash League","active":true,"has_outrights":false},{"key":"cricket_international_t20","group":"Cricket","title":"International Twenty20","description":"International Twenty20","active":true,"has_outrights":false},{"key":"cricket_test_match","group":"Cricket","title":"Test Matches","description":"International Test Matches","active":true,"has_outrights":false},{"key":"golf_masters_tournament_winner","group":"Golf","title":"Masters Tournament Winner","description":"2023 Winner","active":true,"has_outrights":true},{"key":"golf_pga_championship_winner","group":"Golf","title":"PGA Championship Winner","description":"2023 Winner","active":true,"has_outrights":true},{"key":"golf_the_open_championship_winner","group":"Golf","title":"The Open Winner","description":"2023 Winner","active":true,"has_outrights":true},{"key":"golf_us_open_winner","group":"Golf","title":"US Open Winner","description":"2023 Winner","active":true,"has_outrights":true},{"key":"icehockey_nhl","group":"Ice Hockey","title":"NHL","description":"US Ice Hockey","active":true,"has_outrights":false},{"key":"icehockey_nhl_championship_winner","group":"Ice Hockey","title":"NHL Championship Winner","description":"Stanley Cup Winner 2022/2023","active":true,"has_outrights":true},{"key":"icehockey_sweden_allsvenskan","group":"Ice Hockey","title":"HockeyAllsvenskan","description":"Swedish Hockey Allsvenskan","active":true,"has_outrights":false},{"key":"icehockey_sweden_hockey_league","group":"Ice Hockey","title":"SHL","description":"Swedish Hockey League","active":true,"has_outrights":false},{"key":"mma_mixed_martial_arts","group":"Mixed Martial Arts","title":"MMA","description":"Mixed Martial Arts","active":true,"has_outrights":false},{"key":"rugbyleague_nrl","group":"Rugby League","title":"NRL","description":"Aussie Rugby League","active":true,"has_outrights":false},{"key":"soccer_australia_aleague","group":"Soccer","title":"A-League","description":"Aussie Soccer","active":true,"has_outrights":false},{"key":"soccer_belgium_first_div","group":"Soccer","title":"Belgium First Div","description":"Belgian First Division A","active":true,"has_outrights":false},{"key":"soccer_denmark_superliga","group":"Soccer","title":"Denmark Superliga","description":"Danish Soccer","active":true,"has_outrights":false},{"key":"soccer_efl_champ","group":"Soccer","title":"Championship","description":"EFL Championship","active":true,"has_outrights":false},{"key":"soccer_england_efl_cup","group":"Soccer","title":"EFL Cup","description":"League Cup","active":true,"has_outrights":false},{"key":"soccer_england_league1","group":"Soccer","title":"League 1","description":"EFL League 1","active":true,"has_outrights":false},{"key":"soccer_england_league2","group":"Soccer","title":"League 2","description":"EFL League 2 ","active":true,"has_outrights":false},{"key":"soccer_epl","group":"Soccer","title":"EPL","description":"English Premier League","active":true,"has_outrights":false},{"key":"soccer_fa_cup","group":"Soccer","title":"FA Cup","description":"Football Association Challenge Cup","active":true,"has_outrights":false},{"key":"soccer_france_ligue_one","group":"Soccer","title":"Ligue 1 - France","description":"French Soccer","active":true,"has_outrights":false},{"key":"soccer_germany_bundesliga","group":"Soccer","title":"Bundesliga - Germany","description":"German Soccer","active":true,"has_outrights":false},{"key":"soccer_germany_bundesliga2","group":"Soccer","title":"Bundesliga 2 - Germany","description":"German Soccer","active":true,"has_outrights":false},{"key":"soccer_italy_serie_a","group":"Soccer","title":"Serie A - Italy","description":"Italian Soccer","active":true,"has_outrights":false},{"key":"soccer_italy_serie_b","group":"Soccer","title":"Serie B - Italy","description":"Italian Soccer","active":true,"has_outrights":false},{"key":"soccer_mexico_ligamx","group":"Soccer","title":"Liga MX","description":"Mexican Soccer","active":true,"has_outrights":false},{"key":"soccer_netherlands_eredivisie","group":"Soccer","title":"Dutch Eredivisie","description":"Dutch Soccer","active":true,"has_outrights":false},{"key":"soccer_norway_eliteserien","group":"Soccer","title":"Eliteserien - Norway","description":"Norwegian Soccer","active":true,"has_outrights":false},{"key":"soccer_poland_ekstraklasa","group":"Soccer","title":"Ekstraklasa - Poland","description":"Polish Soccer","active":true,"has_outrights":false},{"key":"soccer_portugal_primeira_liga","group":"Soccer","title":"Primeira Liga - Portugal","description":"Portugese Soccer","active":true,"has_outrights":false},{"key":"soccer_spain_la_liga","group":"Soccer","title":"La Liga - Spain","description":"Spanish Soccer","active":true,"has_outrights":false},{"key":"soccer_spain_segunda_division","group":"Soccer","title":"La Liga 2 - Spain","description":"Spanish Soccer","active":true,"has_outrights":false},{"key":"soccer_spl","group":"Soccer","title":"Premiership - Scotland","description":"Scottish Premiership","active":true,"has_outrights":false},{"key":"soccer_sweden_allsvenskan","group":"Soccer","title":"Allsvenskan - Sweden","description":"Swedish Soccer","active":true,"has_outrights":false},{"key":"soccer_sweden_superettan","group":"Soccer","title":"Superettan - Sweden","description":"Swedish Soccer","active":true,"has_outrights":false},{"key":"soccer_switzerland_superleague","group":"Soccer","title":"Swiss Superleague","description":"Swiss Soccer","active":true,"has_outrights":false},{"key":"soccer_turkey_super_league","group":"Soccer","title":"Turkey Super League","description":"Turkish Soccer","active":true,"has_outrights":false},{"key":"soccer_uefa_champs_league","group":"Soccer","title":"UEFA Champions","description":"European Champions League","active":true,"has_outrights":false},{"key":"soccer_uefa_europa_conference_league","group":"Soccer","title":"UEFA Europa Conference League","description":"UEFA Europa Conference League","active":true,"has_outrights":false},{"key":"soccer_uefa_europa_league","group":"Soccer","title":"UEFA Europa","description":"European Europa League","active":true,"has_outrights":false}]\n'

sport = "cricket_big_bash"

req1 = requests.get(url)

resp1 = json.loads(req1.text)

for i in resp1:
    if not i["group"] in allowed_groups:
        continue

    sport_key = i["key"]
    req2 = requests.get("https://api.the-odds-api.com/v4/sports/"+sport_key+"/odds/?regions=au&dateFormat=unix&apiKey=" + key)
    resp2 = json.loads(req2.text)
    try:
        process(resp2)
    except Exception as e:
        print("ERROR: " + str(e))
    # print(csvArr)

for i in csvArr:
    print(i)


