import streamlit as st
import requests
import json
import time
import datetime

api_token = st.secrets['api_token']
site_ID = st.secrets['site_id']
season = "2024"
saturday_league_competition_id = str(120234)
womens_league_competition_id = str(119033)
#Identify junior and women's indoor games by league ID (to accommodate for junior teams swapping divisions, cups vs league, finals days etc. All junior games will need same match fee)
womens_indoor_league_id = str(10936)
junior_league_id = str(10443)
# period_start = "01/01/2024"
# period_end = "31/12/2024"
saturday_match_fee = 12
womens_outdoor_match_fee = 0
womens_indoor_match_fee = 0
junior_match_fee = 0
other_match_fee = 6

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["pwd"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        password_entry_container.text_input(
            'Type the magic word in the box below. On a touch-screen device, tap the screen anywhere outside the box to enter the password', on_change=password_entered, key="password", help="If your mobile\'s on-screen Enter key doesn\'t work, simply tap the app screen after typing your password"
        )
        welcome_image_container.image('images/magic_word.png', use_column_width = True)
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        password_entry_container.text_input(
            'Type the magic word in the box below. On a touch-screen device, tap the screen anywhere outside the box to enter the password', on_change=password_entered, key="password", help="If your mobile\'s on-screen Enter key doesn\'t work, simply tap the app screen after typing your password"
        )
        st.error("😕 Incorrect password dumbass. Have another go")
        return False
    else:
        # Password correct.
        return True

st.image('images/Streamlit_title.png', use_column_width=True)

password_entry_container = st.empty()
submit_button_container = st.empty()
welcome_image_container = st.empty()

if check_password():
    st.write("You\'re in!")
    password_entry_container.empty()
    submit_button_container = st.empty()
    welcome_image_container.empty()

    # Get a listing of players and player IDs
    players_response = requests.get("http://play-cricket.com/api/v2/sites/" + site_ID + "/players?&api_token=" + api_token)

    #st.write(players_response.text)

    # Strip the "players" key values (which contains name and id dictionaries) from the api response
    players = players_response.json()['players']

    # Strip the player ids and names into separate lists.

    playeridlisting = []
    playernamelisting = []
    for p in players:
        playerid = p['member_id']
        playername = p['name']
        playeridlisting.append(playerid)
        playernamelisting.append(playername)

    sortedplayernamelisting = sorted(playernamelisting)

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    # NEW ENTRY
    # playername = st.selectbox('Who are you?', sortedplayernamelisting)

    # An option to produce a dropdown to allow calculating previous years
    # season = st.selectbox('Season', ('2022', '2023'))
    # period_start = "01/01/" + season
    # period_end = "31/12/" + season
    period_start = "01/01/" + season
    period_end = "31/12/" + season

    selectedmonth = st.selectbox('What month do you want to calculate match fees for?', months) 
    if selectedmonth == 'January':
        month_string = '/01/'
    elif selectedmonth == 'February':
        month_string = '/02/'
    elif selectedmonth == 'March':
        month_string = '/03/'
    elif selectedmonth == 'April':
        month_string = '/04/'
    elif selectedmonth == 'May':
        month_string = '/05/'
    elif selectedmonth == 'June':
        month_string = '/06/'
    elif selectedmonth == 'July':
        month_string = '/07/'
    elif selectedmonth == 'August':
        month_string = '/08/'
    elif selectedmonth == 'September':
        month_string = '/09/'
    elif selectedmonth == 'October':
        month_string = '10'
    elif selectedmonth == 'November':
        month_string = '11'
    else:
        month_string = '12'


    # Find the month using datetime to compare it to selected month
    today = datetime.datetime.now()
    month_now = (today.strftime("%B"))
    month_now_number = (today.strftime("%m"))
    # Cast month_now_number as an integer
    month_now_number = int(month_now_number)

    # Now turn month_string into a number to compare it to current month number
    month_calculated_number = month_string
    # Strip leading and trailing slashes
    month_calculated_number = month_calculated_number.strip("/")
    # Cast month_calculated_number as integer
    month_calculated_number = int(month_calculated_number)
    calculate = st.button('Calculate')    

    matchdates = []
    matchIDs = []
    competition = []

    if calculate:
        response = requests.get("http://play-cricket.com/api/v2/matches.json?&site_id=" + site_ID + "&from_entry_date=" + period_start + "&end_entry_date=" + period_end + "&api_token=" + api_token)

        matches = response.json()['matches']
        #extract the match dates

        #st.write(matches)
        
        for d in matches:
            date = d['match_date']
            ID = d['id']
            comp_type = d['competition_id']
            #for games identified by league id rather than competition (or division) id
            league_type = d['league_id']
            if month_string in date and season in date:
                matchdates.append(date)
                matchIDs.append(ID)
                if comp_type == saturday_league_competition_id:
                    competition.append('Saturday league')           
                elif comp_type == womens_league_competition_id:
                    competition.append("Women's outdoor league")
                elif league_type == womens_indoor_league_id:
                    competition.append("Women's indoor league")
                elif league_type == junior_league_id:
                    competition.append("Junior fixture")        
                else:
                    competition.append('Other')
        #st.write("Calculating subs for ", selectedmonth, '...\n')
        spinner_text = ('Calculating subs for ' + selectedmonth + '...  \n')
        with st.spinner(spinner_text):
            time.sleep(1) 
        st.success('') 
        # datelisting = ''
        # st.write('Match dates in ', selectedmonth, ':')
        # for date in matchdates:
            # datelisting += date + ',  '
        # st.markdown(datelisting)    
    
    # players is a list of dictionaries which at the moment contains the player id and name of each player
    # Loop through and add 'Saturday games', 'Womens games', 'Other games' and 'Subs' keys to each and initialise with a value of 0.
    # Then later we'll loop through the game players to match the ID and increment the games and subs
    
    for dictionary in players:
        dictionary['Saturday games'] = 0
        dictionary["Women's outdoor games"] = 0
        dictionary["Women's indoor games"] = 0
        dictionary["Junior games"] = 0
        dictionary['Other games'] = 0
        dictionary['Subs'] = 0

    for m in matchIDs:
        this_match = str(m)
        # print('Match id: ', m)
        matchdetailresponse = requests.get("http://play-cricket.com/api/v2/match_detail.json?&match_id=" + this_match + "&api_token=" + api_token)
        # The value for the 'match_details' key is a list so you need to tell it to look for the 'players' key
        # in the first index position of this list (the [0] after 'match_details').
        # Similarly, the home team is a list in index position 0 of list that is the value of the 'players' key
        # and the away team is a set of dictionaries in a list which is in the second index position of the 'players' value.
        # Confused? Well it took me till 1.30am to work it out.
        awayteamplayedingameids = matchdetailresponse.json()['match_details'][0]['players'][1]['away_team']
        hometeamplayedingameids = matchdetailresponse.json()['match_details'][0]['players'][0]['home_team']
        playedingame = []
        for p in awayteamplayedingameids:
            player = p['player_id']
            playedingame.append(player)
            #print(playedingame)
        for p in hometeamplayedingameids:
            player = p['player_id']
            playedingame.append(player)
            #print(playedingame)
        # Find the index number for this match ID in the matchIDs list
        ind_number = matchIDs.index(m)
        # print('Index number is: ', ind_number)
        # Use this index number to get the match date and whether it's a Saturday league game from their respective lists
    
        for player in players:
            if player['member_id'] in playedingame and competition  [ind_number] == 'Saturday league':
                player['Saturday games'] +=1
                player['Subs'] += saturday_match_fee
            elif player['member_id'] in playedingame and competition[ind_number] == "Women's outdoor league":
                player["Women's outdoor games"] +=1            
                player['Subs'] += womens_outdoor_match_fee
            elif player['member_id'] in playedingame and competition[ind_number] == "Women's indoor league":
                player["Women's indoor games"] +=1            
                player['Subs'] += womens_indoor_match_fee
            elif player['member_id'] in playedingame and competition[ind_number] == "Junior fixture":
                player["Junior games"] +=1            
                player['Subs'] += junior_match_fee        
            elif player['member_id'] in playedingame:
                player['Other games'] +=1
                player['Subs'] += other_match_fee
            if player['Subs'] > 40:
                player['Subs'] = 40   
    
    if calculate:  
        # Uncomment to debug
        # st.write(players)
        sat_games = next((item.get('Saturday games') for item in players if item['name'] == playername))
        womens_outdoor_games = next((item.get("Women's outdoor games") for item in players if item['name'] == playername))
        womens_indoor_games = next((item.get("Women's indoor games") for item in players if item['name'] == playername))
        junior_games = next((item.get("Junior games") for item in players if item['name'] == playername))
        other_games = next((item.get('Other games') for item in players if item['name'] == playername))
        subs = next((item.get('Subs') for item in players if item['name'] == playername))

        if month_calculated_number > month_now_number:
            st.markdown('**_Fairy Benmother is very cross with you!_**')
            st.image('images/Fuckwit.png', use_column_width=True)

        if selectedmonth == month_now:
            st.write("**That month hasn't finished yet but here's how we're looking so far:**")
    
        for i in range(1):
            st.write('Account name: North Kilworth Cricket Club  \nAccount number: ' + st.secrets['account_number'] + '  \nSort code: ' + st.secrets['sort_code']) 
            for p in players:
                if p['Subs'] != 0:
                    person = p['name']
                    owes = str(p['Subs'])
                    output_string = '<strong><p style=font-family:courier;color:black;>' + person + ' £' + owes +'</p></strong>'
                    st.markdown(output_string, unsafe_allow_html=True)
                    # st.write(p['name'], ' £', p['Subs'])
                    st.write('   Saturday games ', p['Saturday games'], "; Women's outdoor games ", p["Women's outdoor games"], "; Women's indoor games ", p["Women's indoor games"], '; Junior games ', p['Junior games'], '; Other games ', p['Other games'])
                    st.write('')
               
   
    


