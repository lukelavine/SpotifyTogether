import os
import uuid
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import User

import spotipy
import analyzer as taste_analyzer
import numpy as np
import pickle

# Create your views here.

def index(request):
	cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)
	auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read user-library-read playlist-modify-private',
												cache_handler=cache_handler,
												show_dialog=True)
	signed_in = False
	if auth_manager.validate_token(cache_handler.get_cached_token()):
		signed_in = True
	context = {'auth_url' : auth_manager.get_authorize_url(),
				'signed_in' : signed_in}
	return render(request, 'main/index.html', context)

def home(request):
	cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)
	auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read user-library-read playlist-modify-private',
												cache_handler=cache_handler,
												show_dialog=True)
	if request.GET.get('code', False):
		auth_manager.get_access_token(request.GET.get('code'))
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
		return redirect('index')
	spotify = spotipy.Spotify(auth_manager=auth_manager)
	context = { 'user' : spotify.me()["display_name"]}
	return render(request, 'main/home.html', context)

def analyze(request):
	cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)
	auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read user-library-read playlist-modify-private',
												cache_handler=cache_handler,
												show_dialog=True)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
		return redirect('index')
	sp = spotipy.Spotify(auth_manager=auth_manager)
	if request.method == "GET":
		#Pick playlists and stuff
		context = { 'playlists' : sp.current_user_playlists()["items"] }
		return render(request, 'main/analyze.html', context)
	if request.method == "POST":
		#They entered playlists, run analysis
		#Worry about other playlists later
		'''savedmusic = False
		playlists = []
		for playlist in request.POST.keys:
			if playlist != "csrfmiddlewaretoken" and playlist != "savedmusic":
				playlists.append(plalylist)
			if playlist == "savedmusic":
				savedmusic = True
		tracks = []
		top = sp.current_user_top_tracks(limit=50, time_range='medium_term')
		for track in top["items"]
			tracks.append(track["id"])
		if savedmusic:	
			sp.'''
		tracks = []
		current = 0
		top = sp.current_user_top_tracks(limit=50, time_range='short_term')
		for track in top["items"]:
			tracks.append(track["id"])
		clfs = analyzer(sp, tracks)
		user = User(user_id=sp.me()["id"], display_name=sp.me()["display_name"], clf1=pickle.dumps(clfs[0]), clf2=pickle.dumps(clfs[1]), clf3=pickle.dumps(clfs[2]), clf4=pickle.dumps(clfs[3]))
		user.save()
		return render(request, 'main/analysis.html')
	return

def combine(request):
	cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)
	auth_manager = spotipy.oauth2.SpotifyOAuth(scope='user-top-read user-library-read playlist-modify-private',
												cache_handler=cache_handler,
												show_dialog=True)
	if not auth_manager.validate_token(cache_handler.get_cached_token()):
		return redirect('index')
	if request.method == "GET":
		#Show them users to combine
		users = User.objects.all()
		context = { 'users' : users }
		return render(request, 'main/combine.html', context)
	if request.method == "POST":
		#Generate playlist, add a button to add it
		#sp = spotipy.Spotify(auth_manager=auth_manager)
		#me = User.objects.get(sp.me()["id"])
		#other = User.objects.get(request.POST.get('user'))
		return render(request, 'main/playlist_preview.html')
	return

def analyzer(sp, tracks):
	clfs = taste_analyzer.runprog(sp, tracks)
	return clfs