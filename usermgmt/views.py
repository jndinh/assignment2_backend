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

	user = User.objects.get(username=username)
		
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

	user = User.objects.get(username=username)

	data = {}
	data['username'] = user.username
	data['longitude'] = user.longitude
	data['latitude'] = user.latitude
	data['timestamp'] = user.timestamp

	# user doesn't exist
	if not user:
        	return JsonResponse({'user' : {}}, content_type = "application/json", status = 200)

        return JsonResponse({'user' : data}, content_type = "application/json", status = 200)

    except Exception as e:
	return JsonResponse({'detail' : 'Failed to get user', 'error' : str(e)}, content_type = "application/json", status = 400)


# Get all user
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


# Update user
@api_view(['PATCH'])
def update_user(request):
    try:
	username = request.POST.get('username')
	longitude = request.POST.get('longitude')
	latitude = request.POST.get('latitude')

	#Missing parameters
	if not username or not longitude or not latitude:
	        return JsonResponse({'detail' : 'Missing parameteri(s): username, longitude, latitude.'}, content_type = "application/json", status = 400)		

	user = User.objects.get(username=username)
	
	# User doesn't exist
	if not user:
                return JsonResponse({'detail' : 'User does not exist.', 'status' : False}, content_type = "application/json", status = 400)		

	# Update location & time
	if longitude:
		user.longitude = longitude
	if latitude:
		user.latitude = latitude
	
	user.timestamp = time.time()

	user.save()

        return JsonResponse({'detail' : 'User updated.', 'status' : True}, content_type = "application/json", status = 200)
    except Exception as e:
        return JsonResponse({'detail' : 'Failed to update user.', 'status' : False, 'error' : str(e)}, content_type = "application/json", status = 400)



