from django.shortcuts import render
from django.http import JsonResponse#, HttpResponseRedirect
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import math, json

from .models import Type
from .serializers import TypeSerializer

# Create your views here.

def data_serializer(data=None): ## -- Method called for saving/updating data in DB -- ##
	response = {}
	status=200


	serializer = TypeSerializer(data=data)

	if serializer.is_valid():
		if 'id' in serializer.validated_data and serializer.validated_data['id']: ## -- If the data exist, then update, else save -- ##
			serializer.update(serializer.validated_data['instance'], serializer.data) ## -- <Class>.update(<Model/DB_Object_dict>, {Validated_data}) -- ##
		else:
			serializer.save()
		response['message'] = serializer.data
		status = 201
	else:
		if 'message' in serializer.errors:
			response['message'] = serializer.errors['message'][0]
			status = serializer.errors['status'][0]
		else:
			response['message'] = serializer.errors
			status = 400
	return {'response': response, 'status':status}


@csrf_exempt
def violation_types(request): ## -- Add/Edit Types in the DB - API format -- ##

	response = {}
	status = 200

	if request.method == 'POST':
		if request.body:
			data = json.loads(request.body)
		else:
			data = {}

		resp = data_serializer(data=data)
		response = resp['response']
		status = resp['status']
	else:
		response = {'message':'Invalid request type'}
		status = 405 ## -- Method not allowed -- ##

	return JsonResponse(response, status=status)

def view_types(request): ## -- View certain / all the Types from the DB - API format -- ##
	from django.core import serializers

	response = {}
	status = 200

	if request.method == 'GET':
		if 'id' in request.GET:
			query_data = Type.objects.filter(id=request.GET.get('id'))
		else:
			query_data = Type.objects.all()

		if query_data.exists():
			json_data = json.loads(serializers.serialize("json", query_data))

			response = {'data':json_data}
		else:
			response = {'message':'Invalid request type'}
			status = 404 ## -- Not Found -- ##	
	else:
		response = {'message':'Invalid request type'}
		status = 405 ## -- Method not allowed -- ##

	return JsonResponse(response, status=status)