from rest_framework import serializers
from .models import Violation

class ViolationSerializer(serializers.Serializer):
	vio_id = serializers.IntegerField(required=False, min_value=1)
	vio_type = serializers.CharField(required=True, allow_blank=False, max_length=100)
	who_id = serializers.IntegerField(min_value=1)
	who_type = serializers.CharField(required=True, allow_blank=False, max_length=100)
	who_meta = serializers.JSONField(binary=False)
	whom_id = serializers.IntegerField(min_value=1)
	whom_type = serializers.CharField(required=True, allow_blank=False, max_length=100)
	whom_meta = serializers.JSONField(binary=False)
	cc_list = serializers.ListField(child=serializers.IntegerField(min_value=0), min_length=0)
	cc_list_meta = serializers.ListField(child=serializers.JSONField(binary=False), min_length=0)
	bcc_list = serializers.ListField(child=serializers.IntegerField(min_value=0), min_length=0)
	bcc_list_meta = serializers.ListField(child=serializers.JSONField(binary=False), min_length=0)
	status = serializers.CharField(required=True, allow_blank=False, max_length=100)
	violation_nature = serializers.CharField(required=False, allow_blank=False, max_length=100)

	def validate(self, data):
		list_param = ['who_id', 'who_type', 'whom_id', 'whom_type', 'status', 'vio_type']

		if not all (k in data for k in list_param):
			raise serializers.ValidationError({
				'status': 417, ## -- Expectation Failed -- ##
				'message': "Respective Params required -> 'who_id', 'who_type', 'whom_id', 'whom_type', 'status', 'vio_type'"
			})
		else:
			try:
				if 'vio_id' in data and data['vio_id']:
					data['instance'] = Violation.objects.get(id=data['vio_id'])
			except:
				pass

		return data

	def create(self, validated_data):
		"""
		Create and return a new `Type` instance, given the validated data.
		"""
		from types_vio.models import Type
		
		type_data = Type.objects.get(shortcode=validated_data.pop('vio_type')) ## -- Get Type Details using Type ID -- ##
		return Violation.objects.create(vio_type=type_data, **validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Type` instance, given the validated data.
		"""
		#instance.vio_type = validated_data.get('vio_type', instance.vio_type)
		#instance.who_id = validated_data.get('who_id', instance.who_id)
		#instance.who_type = validated_data.get('who_type', instance.who_type)
		instance.who_meta = validated_data.get('who_meta', instance.who_meta)
		#instance.whom_id = validated_data.get('whom_id', instance.whom_id)
		#instance.whom_type = validated_data.get('whom_type', instance.whom_type)
		instance.whom_meta = validated_data.get('whom_meta', instance.whom_meta)
		instance.cc_list = validated_data.get('cc_list', instance.cc_list)
		instance.cc_list_meta = validated_data.get('cc_list_meta', instance.cc_list_meta)
		instance.bcc_list = validated_data.get('bcc_list', instance.bcc_list)
		instance.bcc_list_meta = validated_data.get('bcc_list_meta', instance.bcc_list_meta)
		instance.status = validated_data.get('status', instance.status)
		instance.violation_nature = validated_data.get('violation_nature', instance.violation_nature)
		instance.save()

		return instance

	class Meta:
		model = Violation
		fields = ('id', 'who_id', 'who_type', 'who_meta', 'whom_id', 'whom_type', 'whom_meta', 'cc_list', 'cc_list_meta', 'bcc_list', 'bcc_list_meta', 'status', 'violation_nature')