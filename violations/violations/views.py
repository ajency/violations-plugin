from django.shortcuts import render
from django.http import JsonResponse#, HttpResponseRedirect
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import math, json, ast
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from .models import Type, Violation, Comment, Action
from .serializers import TypeSerializer, ViolationSerializer, CommentSerializer, ActionSerializer


def type_serializer(data=None): ## -- Method called for saving/updating data in DB -- ##
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

		resp = type_serializer(data=data)
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


def violation_serializer(data=None): ## -- Method called for saving/updating `Violation` data in DB -- ##
	response = {}
	status=200

	serializer = ViolationSerializer(data=data)

	if serializer.is_valid():
		if 'vio_id' in serializer.validated_data and serializer.validated_data['vio_id']: ## -- If the data exist, then update, else save -- ##
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

class ViolationData(APIView):
	"""
    List all Violations, or create a new violation.
    """
	
	#permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	def get(self, request, *args, **kwargs):
		response = {}
		status = 200

		list_params = ['vio_types', 'who_ids', 'who_types', 'statuses', 'vio_date']
		
		if 'vio_id' in request.GET: ## -- If Violation ID is defined, then get that Violation data -- ##
			query_data = Violation.objects.filter(id=request.GET.get('vio_id'))
		elif request.GET and any (k in request.GET for k in list_params): ## -- If any of the above filters exist in params, then enter this condition-- ##
			query_data = Violation.objects
			if 'vio_types' in request.GET and eval(request.GET.get('vio_types')):
				query_data = query_data.filter(vio_type__shortcode__in=eval(request.GET.get('vio_types')))

			if 'who_ids' in request.GET and eval(request.GET.get('who_ids')):
				query_data = query_data.filter(who_id__in=eval(request.GET.get('who_ids')))

			if 'who_types' in request.GET and eval(request.GET.get('who_types')):
				query_data = query_data.filter(who_type__in=eval(request.GET.get('who_types')))

			if 'statuses' in request.GET and eval(request.GET.get('statuses')):
				query_data = query_data.filter(status__in=eval(request.GET.get('statuses')))

			if 'vio_date' in request.GET and eval(request.GET.get('vio_date')):
				query_data = query_data.filter(vio_date__range=eval(request.GET.get('vio_date')))

		else: ## -- If no filters nor violation ID is defined, then get all the data -- ##
			query_data = Violation.objects.filter(status='active')## -- Get oldest to new violations that are 'active'-- ##
			# query_data = Violation.objects.all()

		if 'orderBy' in request.GET:
			query_data = query_data.order_by(request.GET.get('orderBy')) ## -- Order the Violations data in that order -- ##
		else:
			query_data = query_data.order_by('vio_date') ## -- Order by Violation Date from old to new -- ##

		if 'start' in request.GET and 'length' in request.GET: ## -- If Pagination is defined, i.e. start Point & number of data -- ##
			start = int(request.GET.get('start'))
			length = int(request.GET.get('length'))
			sliced_data = query_data[start : start + length]
		else: ## -- If Pagination not defined, then get 1st 30 data -- ##
			sliced_data = query_data[:30]
		
		## Note: query_data after slicing is transferred to sliced_data as .filter() doesn't work on 'sliced data' i.e. query_data[ start : start + length]

		json_data = json.loads(serializers.serialize("json", sliced_data))

		for data in json_data:
			data['fields']['vio_type'] = json.loads(serializers.serialize("json", Type.objects.filter(id=data['fields']['vio_type'])))[0] ## -- Get the Type details -- ##
			data['fields']['vio_type'].pop('model')

			data['fields']['who_meta'] = eval(data['fields']['who_meta']) ## -- Convert string to JSON -- ##
			data['fields']['whom_meta'] = eval(data['fields']['whom_meta']) ## -- Convert string to JSON -- ##
			data['fields']['cc_list'] = eval(data['fields']['cc_list']) ## -- Convert from string to Array -- ##
			data['fields']['bcc_list'] = eval(data['fields']['bcc_list']) ## -- Convert from string to Array -- ##
			data['fields']['cc_list_meta'] = [ast.literal_eval(value) for value in eval(data['fields']['cc_list_meta'])] ## -- Convert from string to unicode to JSON -- ##
			data['fields']['bcc_list_meta'] = [ast.literal_eval(value) for value in eval(data['fields']['bcc_list_meta'])] ## -- Convert from string to unicode to JSON -- ##
			
			data['actions'] = json.loads(serializers.serialize("json", query_data.filter(id=data['pk'])[0].actions.all())) ## -- Get all the actions related to that Violations -- ##
			for action in data['actions']: ## -- convert String meta back to JSON meta -- ##
				action['fields']['who_meta'] = eval(action['fields']['who_meta'])
				action.pop('model') ## -- Remove the Model Info -- ##

			data['comments'] = json.loads(serializers.serialize("json", query_data.filter(id=data['pk'])[0].comments.all())) ## -- Get all the comments related to that Violations -- ##
			for comment in data['comments']: ## -- convert String meta back to JSON meta -- ##
				comment['fields']['who_meta'] = eval(comment['fields']['who_meta'])
				comment.pop('model') ## -- Remove the Model Info -- ##

			data.pop('model') ## -- Pop/Remove certain details -- ##

		response = {'data':json_data}

		return JsonResponse(response, status=status)

	def post(self, request, *args, **kwargs):
		response = {}
		status=200
		
		if request.body:
			data = json.loads(request.body)
		else:
			data = {}

		resp = violation_serializer(data=data)
		response = resp['response']
		status = resp['status']

		return JsonResponse(response, status=status)


@csrf_exempt
def violation_data(request):

	response = {}
	status=200
	
	if request.method == 'GET':
		list_params = ['vio_types', 'who_ids', 'who_types', 'statuses', 'vio_date']
		
		if 'vio_id' in request.GET: ## -- If Violation ID is defined, then get that Violation data -- ##
			query_data = Violation.objects.filter(id=request.GET.get('vio_id'))
		elif request.GET and any (k in request.GET for k in list_params): ## -- If any of the above filters exist in params, then enter this condition-- ##
			query_data = Violation.objects
			if 'vio_types' in request.GET and eval(request.GET.get('vio_types')):
				query_data = query_data.filter(vio_type__shortcode__in=eval(request.GET.get('vio_types')))

			if 'who_ids' in request.GET and eval(request.GET.get('who_ids')):
				query_data = query_data.filter(who_id__in=eval(request.GET.get('who_ids')))

			if 'who_types' in request.GET and eval(request.GET.get('who_types')):
				query_data = query_data.filter(who_type__in=eval(request.GET.get('who_types')))

			if 'statuses' in request.GET and eval(request.GET.get('statuses')):
				query_data = query_data.filter(status__in=eval(request.GET.get('statuses')))

			if 'vio_date' in request.GET and eval(request.GET.get('vio_date')):
				query_data = query_data.filter(vio_date__range=eval(request.GET.get('vio_date')))

		else: ## -- If no filters nor violation ID is defined, then get all the data -- ##
			query_data = Violation.objects.filter(status='active')## -- Get oldest to new violations that are 'active'-- ##
			# query_data = Violation.objects.all()

		if 'orderBy' in request.GET:
			query_data = query_data.order_by(request.GET.get('orderBy')) ## -- Order the Violations data in that order -- ##
		else:
			query_data = query_data.order_by('vio_date') ## -- Order by Violation Date from old to new -- ##

		if 'start' in request.GET and 'length' in request.GET: ## -- If Pagination is defined, i.e. start Point & number of data -- ##
			start = int(request.GET.get('start'))
			length = int(request.GET.get('length'))
			sliced_data = query_data[start : start + length]
		else: ## -- If Pagination not defined, then get 1st 30 data -- ##
			sliced_data = query_data[:30]
		
		## Note: query_data after slicing is transferred to sliced_data as .filter() doesn't work on 'sliced data' i.e. query_data[ start : start + length]

		json_data = json.loads(serializers.serialize("json", sliced_data))

		for data in json_data:
			data['fields']['type_vio'] = Type.objects.get(id=data['fields']['type_vio']).display if Type.objects.filter(id=data['fields']['type_vio']).exists() else ''

			data['fields']['who_meta'] = eval(data['fields']['who_meta']) ## -- Convert string to JSON -- ##
			data['fields']['whom_meta'] = eval(data['fields']['whom_meta']) ## -- Convert string to JSON -- ##
			data['fields']['cc_list'] = eval(data['fields']['cc_list']) ## -- Convert from string to Array -- ##
			data['fields']['bcc_list'] = eval(data['fields']['bcc_list']) ## -- Convert from string to Array -- ##
			data['fields']['cc_list_meta'] = [ast.literal_eval(value) for value in eval(data['fields']['cc_list_meta'])] ## -- Convert from string to unicode to JSON -- ##
			data['fields']['bcc_list_meta'] = [ast.literal_eval(value) for value in eval(data['fields']['bcc_list_meta'])] ## -- Convert from string to unicode to JSON -- ##
			
			data['actions'] = json.loads(serializers.serialize("json", query_data.filter(id=data['pk'])[0].actions.all())) ## -- Get all the actions related to that Violations -- ##
			for action in data['actions']: ## -- convert String meta back to JSON meta -- ##
				action['fields']['who_meta'] = eval(action['fields']['who_meta'])
				action.pop('model') ## -- Remove the Model Info -- ##

			data['comments'] = json.loads(serializers.serialize("json", query_data.filter(id=data['pk'])[0].comments.all())) ## -- Get all the comments related to that Violations -- ##
			for comment in data['comments']: ## -- convert String meta back to JSON meta -- ##
				comment['fields']['who_meta'] = eval(comment['fields']['who_meta'])
				comment.pop('model') ## -- Remove the Model Info -- ##

			data.pop('model') ## -- Pop/Remove certain details -- ##

		response = {'data':json_data}
	elif request.method == 'POST':
		if request.body:
			data = json.loads(request.body)
		else:
			data = {}

		resp = violation_serializer(data=data)
		response = resp['response']
		status = resp['status']
		
	else:
		response = {'message':'Invalid request type'}
		status = 405 ## -- Method not allowed -- ##
	return JsonResponse(response, status=status)


def action_serializer(data=None): ## -- Method called for saving/updating `Action` data in DB -- ##
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

		resp = action_serializer(data=data)
		response = resp['response']
		status = resp['status']

		return JsonResponse(response, status=status)

def comment_serializer(data=None): ## -- Method called for saving/updating `Comment` data in DB -- ##
	response = {}
	status=200

	serializer = CommentSerializer(data=data)

	if serializer.is_valid():
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


class ViewCommentData(APIView):
	'''
		API to get/View comments to respective Violations
	'''
	def get(self, request, *args, **kwargs):

		response = {}
		status = 200
		
		if 'vio_id' in request.GET:
			query_data = Comment.objects.filter(violation__id=request.GET.get('vio_id'))

			json_data = json.loads(serializers.serialize("json", query_data))

			for data in json_data:
				data['fields']['who_meta'] = eval(data['fields']['who_meta']) ## -- Convert string to JSON -- ##

				data.pop('model') ## -- Pop/Remove certain details -- ##

			response = {'data':json_data}
		else:
			response = {'message': "Please pass the vio_id Param"}
			status = 417

		return JsonResponse(response,status=200)

	def post(self, request, *args, **kwargs):
		return JsonResponse({'message':'Invalid request type'}, status=405) ## -- Method not allowed -- ##


class SetCommentData(APIView):
	''' 
		API to get `Comments`, or add new `Comment`
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

		if 'vio_id' in data:
			data['violation_id'] = data['vio_id']

		resp = comment_serializer(data=data)
		response = resp['response']
		status = resp['status']
		
		return JsonResponse(response, status=status)