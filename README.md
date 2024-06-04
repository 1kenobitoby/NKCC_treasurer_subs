# NKCC_streamlit_subs
Cricket club monthly match fee calculator calling the Play-Cricket API.
A streamlit python app to calculate a cricket club player's monthly match fees.
If you want to use it, you'll need to submit a request to ECB to get an API token and site ID for your club.
[see Play-Cricket API info page](https://play-cricket.ecb.co.uk/hc/en-us/articles/115004270145-Do-you-have-an-API-to-access-play-cricket-data-)
Calls the Play-Cricket match summary API to get a list of IDs for matches in target year.
Calls the Play-Cricket players API to get a listing of players and their IDs.
Calls the match details API and loops through the match IDs to find the player IDs that took part in that game.
Uses the competition ID in the match detail to work out what type of game it was and the corresponding match fee.
For each player ID found in the each match detail ID, matches that to the club's player listing and increments their number of games played and match fees.
