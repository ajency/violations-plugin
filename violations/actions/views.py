from django.shortcuts import render

from django.http import JsonResponse#, HttpResponseRedirect
from datetime import datetime
import math, json
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Action
from .serializers import ActionSerializer

from violations.models import Violation

# Create your views here.

def data_serializer(data=None):
	response = {}
	status=200

	#import ipdb; ipdb.set_trace()
	serializer = ActionSerializer(data=data)

	if serializer.is_valid():
		serializer.save()
		
		response['message'] = json.loads(json.dumps(serializer.validated_data)) ## -- Dict to JSON -- ##
		status = 201
	else:
		if 'message' in serializer.errors:
			response['message'] = serializer.errors['message'][0]
			status = serializer.errors['status'][0]
		else:
			response['message'] = serializer.errors
			status = 400

	return {'response': response, 'status':status}

class ViewActionData(APIView):
	'''
		API to view `Action` of respective Violations
	'''
	def get(self, request, *args, **kwargs):
		response = {}
		status = 200
		
		if 'vio_id' in request.GET:
			query_data = Action.objects.filter(violation__id=request.GET.get('vio_id'))

			json_data = json.loads(serializers.serialize("json", query_data))

			for data in json_data:
				data['fields']['who_meta'] = eval(data['fields']['who_meta']) ## -- Convert string to JSON -- ##

				data.pop('model') ## -- Pop/Remove certain details -- ##

			response = {'data':json_data}
		else:
			response = {'message': "Please pass the vio_id Param"}
			status = 417

		return JsonResponse(response,status=200)

	def post(self, request):
		return JsonResponse({'message':'Invalid request type'}, status=405) ## -- Method not allowed -- ##


class SetActionData(APIView):
	''' 
	API to get `Action`, or add new `Comment`
	'''

	def get(self, request, *args, **kwargs):
		return JsonResponse({'message':'Invalid request type'}, status=405) ## -- Method not allowed -- ##
	

	def post(self, request, *args, **kwargs):
		response = {}
		status=200

		if request.body:
			data = json.loads(request.body)
		else:
			data = {}

		resp = data_serializer(data=data)
		response = resp['response']
		status = resp['status']

		return JsonResponse(response, status=status)