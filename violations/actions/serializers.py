from rest_framework import serializers
from .models import Action

class ActionSerializer(serializers.Serializer):
	vio_id = serializers.IntegerField(min_value=1)
	who_id = serializers.IntegerField(required=True, min_value=1)
	who_meta = serializers.JSONField(binary=False)
	what = serializers.CharField(required=True, allow_blank=False, max_length=100)
	what_meta = serializers.JSONField(binary=False)

	def validate(self, data):
		list_param = ['vio_id', 'who_id', 'what', 'what_meta']

		if not all (k in data for k in list_param):
			raise serializers.ValidationError({
				'status': 417, ## -- Expectation Failed -- ##
				'message': "'vio_id', 'who_id', 'what' and 'what_meta' parameters are required"
			})
		else:
			data_obj = Action.objects.filter(violation__id=data['vio_id'], who_id=data['who_id'], what=data['what'])
			
			if data_obj.exists():
				raise serializers.ValidationError({
					'status': 409, ## -- Conflict -- ##
					'message': 'This user already taken an action on this violation'
				})
		return data

	def create(self, validated_data):
		"""
		Create and return a new `Action` instance, given the validated data.
		"""
		from violations.models import Violation

		violation_data = Violation.objects.get(id=validated_data.pop('vio_id')) ## -- Get Violation Details using Vioaltion ID -- ##
		return Action.objects.create(violation=violation_data, **validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Action` instance, given the validated data.
		"""
		#instance.vio_id = validated_data.get('vio_id', instance.vio_id)
		#instance.who_id = validated_data.get('who_id', instance.who_id)
		instance.who_meta = validated_data.get('who_meta', instance.who_meta)
		instance.what = validated_data.get('what', instance.what)
		instance.what_meta = validated_data.get('what_meta', instance.what_meta)
		instance.save()

		return instance

	class Meta:
		model = Action
		fields = ('id', 'violation', 'who_id', 'who_meta', 'what', 'what_meta', 'timestamp')