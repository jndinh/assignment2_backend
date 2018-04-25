# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User
from rest_framework.decorators import api_view

import requests
import json
import time
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyCVsFWhJzGfxcs1vr98chFN0w5dcSPh_Tc')


# Create your views here.
@api_view(['POST', 'GET', 'PATCH', 'DELETE'])
@csrf_exempt
def user_crud(request):

    #Send to the proper function
    if request.method == 'POST':
        response = make_user(request)
    elif request.method == 'GET':
        response = get_user(request)
    elif request.method == 'PATCH':
        response = update_user(request)
    else:
        response = JsonResponse({"detail": "Invalid Request"}, content_type = "application/json", status = 400) 
    return response
	

# Create a user
def make_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
		
        # Optional parameters
       	longitude = request.POST.get('longitude')
       	latitude = request.POST.get('latitude')
        timestamp = request.POST.get('timestamp')

	user = User.objects.filter(username=username).first()
		
	# username already exists
        if user:
		return JsonResponse({'detail' : False}, content_type = "application/json", status = 400)

	user = User.objects.create(username=username, password=password)

	if longitude:
		user.longitude = longitude
	if latitude:
		user.latitude = latitude
	if timestamp:
		user.timestamp = long(timestamp)

	user.save()

        return JsonResponse({'detail' : 'User created', 'status' : True}, content_type = "application/json", status = 200)
    except Exception as e:
        return JsonResponse({'detail' : 'Failed to create account', 'status' : False, 'error' : str(e)}, content_type = "application/json", status = 400)        


# Get a single user
def get_user(request):
    try:
        username = request.GET.get('username')

	user = User.objects.filter(username=username).first()

	# user doesn't exist
	if not user:
        	return JsonResponse({'user' : {}}, content_type = "application/json", status = 200)

        data = {}
        data['username'] = user.username
        data['longitude'] = user.longitude
        data['latitude'] = user.latitude
        data['timestamp'] = user.timestamp

        return JsonResponse({'user' : data}, content_type = "application/json", status = 200)

    except Exception as e:
	return JsonResponse({'detail' : 'Failed to get user', 'error' : str(e)}, content_type = "application/json", status = 400)


# Get all user
@api_view(['GET'])
def get_all_users(request):
    try:
    	users = User.objects.all()
	data = {}

	# format every user
	for user in users:
		location = {}
		location['longitude'] = user.longitude
		location['latitude'] = user.latitude
		location['timestamp'] = user.timestamp

		data[user.username] = location


        return JsonResponse(data, content_type = "application/json", status = 200)
    except Exception as e:
    	return JsonResponse({'detail' : 'Failed to get all users', 'error' : str(e)}, content_type = "application/json", status = 400)


# Log in
@api_view(['POST'])
def login(request):
    try:

        username = request.POST.get('username')
        password = request.POST.get('password')

	# Missing parameters
	if not username or not password:
		return JsonResponse({'detail' : 'Missing username or password', 'status' : False}, content_type = "application/json", status = 200)

	user = User.objects.filter(username=username, password=password).first()

	# User DNE
	if not user:
		return JsonResponse({'detail' : 'User DNE.', 'status' : False}, content_type = "application/json", status = 200)

        return JsonResponse({'detail' : 'Logged in.', 'status' : True}, content_type = "application/json", status = 200)
    except Exception as e:
        return JsonResponse({'detail' : 'Failed to login.', 'status' : False, 'error' : str(e)}, content_type = "application/json", status = 400)


# Update user
@api_view(['PATCH'])
def update_user(request):
    try:
	username = request.POST.get('username')
	longitude = request.POST.get('longitude')
	latitude = request.POST.get('latitude')
	timestamp = request.POST.get('timestamp')

	#Missing parameters
	if not username or not longitude or not latitude:
	        return JsonResponse({'detail' : 'Missing parameteri(s): username, longitude, latitude.'}, content_type = "application/json", status = 400)		

	user = User.objects.filter(username=username).first()
	
	# User doesn't exist
	if not user:
                return JsonResponse({'detail' : 'User does not exist.', 'status' : False}, content_type = "application/json", status = 400)		

	# Update location & time
	if longitude:
		user.longitude = float(longitude)
	if latitude:
		user.latitude = float(latitude)
	if timestamp:
		user.timestamp = long(timestamp)
	else:	
		user.timestamp = time.time() * 1000

	user.save()

        return JsonResponse({'detail' : 'User updated.', 'status' : True}, content_type = "application/json", status = 200)
    except Exception as e:
        return JsonResponse({'detail' : 'Failed to update user.', 'status' : False, 'error' : str(e)}, content_type = "application/json", status = 400)


# Get all friends in 1km radius
@api_view(['GET'])
def get_radius(request):
    try:
    	username = request.GET.get('username')

        # Missing parameters
        if not username:
                return JsonResponse({'detail' : 'Missing parameter: username'}, content_type = "application/json", status = 400)

	user = User.objects.filter(username=username).first()

        # User doesn't exist
        if not user:
                return JsonResponse({'detail' : 'User does not exist.', 'status' : False}, content_type = "application/json", status = 400)
	
	friends = User.objects.exclude(username=username)
       
	origin = [{'lat' : user.latitude, 'lng' : user.longitude}]
	radius = {}

	# Get distance between user and friend
        for friend in friends:
		# does friend havea location?
		if not friend.latitude or not friend.longitude:
			continue

		dest = [{'lat' : friend.latitude, 'lng' : friend.longitude}]

		distance = gmaps.distance_matrix(origins=origin, destinations=dest)

		# Something didn't work
		if distance["status"] != "OK":
	        	return JsonResponse({'detail' : distance["status"], 'status' : False}, content_type = "application/json", status = 400)

		# Does distance even exist? skip if it doesnt
		if distance["rows"][0]["elements"][0]["status"] != "OK":
			continue

		# Friend within 1km or 1000 meters?
		if distance["rows"][0]["elements"][0]["distance"]["value"] <= 1000:
                	location = {}
                	location['longitude'] = float(friend.longitude)
                	location['latitude'] = float(friend.latitude)
                	location['timestamp'] = long(friend.timestamp)

                	radius[friend.username] = location
		
	return JsonResponse(radius, content_type = "application/json", status = 200)
    except Exception as e:
        return JsonResponse({'detail' : 'Failed to get friends in radius', 'status' : False, 'error' : str(e)}, content_type = "application/json", status = 400)





