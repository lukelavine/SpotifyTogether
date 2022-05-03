# SpotifyTogether
Using machine learning to combine users music taste

# DISCLAIMER
Although meant for a web application, this app isn't quite ready to be published to the public yet. Check back later in the week to see if it has been published and where it can be found.

It is possible to download this project and run it locally by running "python manage.py runserver", it will require the install of spotipy and sklearn


# Application
There are a lot of files that are mostly administrative, the ones to pay to attention to are spotifytogether/main/views.py and spotifytogether/analyzer.py

## Views.py
Handles routing of the web app, tracks users logging in to spotify, calls the analysis, compares the music taste of two users, and will then create a playlist based off of their taste.
Once it calls analyzer.py, it returns recieves classifiers and stores them into a database using pickle to convert them to binary
So when another user uses the website it has a database of users to compare music with, if their classifiers and the other users classifiers say that they both like a song the song is added tot the playlist
The user is then shown a preview of the playlist and asked if they want to save it.

## Analyzer.py
Takes a users top 50 songs and asks the spotify API for their audio features like "Danceability", "Loudness", "Tempo", "Valence", and more.
It then trains 4 classifiers on these features, Perceptron, Decision Tree, MLP, and Random Forest. These classifiers are supposed to represent the users music taste.
It returns these classifier to views.py where it stores them into a database using pickle to convert them to binary.

# Results
The classifiers would have really high accuracy values, but then performed poorly outside of training.
The reason for this is probably because it's training on susch a small dataset, and can be fixed by integrating the music that the user saves to their library and the playlists they follow.
