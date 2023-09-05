# spotify_recommend
Sick of your same songs over and over? Use this program to get a new playlist of songs based off your favorite tracks!  
This is a Flask-based web application utilizing OAuth2 authentication to connect with the Spotify API and retrieve user-specific data seamlessly and securely, leveraging Flask’s routing capabilities to handle various endpoints methodically and efficiently.  
Using OAuth2 authentication, this app retrives user's top listening to tracks, then uses these tracks metadata to create multiple seeds to find tracks of similar genre, artist style, and track style. App then takes these similar tracks, adds them into a Spotify playlist under the user's account.
