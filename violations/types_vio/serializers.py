from rest_framework import serializers
from .models import Type

class TypeSerializer(serializers.Serializer):
	shortcode = serializers.CharField(required=True, allow_blank=False, max_length=100)
	display = serializers.CharField(required=False, allow_blank=True, max_length=100)
	severity = serializers.CharField(required=False, allow_blank=True, max_length=100)
	group = serializers.CharField(required=False, allow_blank=True, max_length=100)
	configurable_counts = serializers.CharField(required=False, allow_blank=True, max_length=100)

	def validate(self, data):

		if 'shortcode' in data:
			if 'display' not in data:
				data['display'] = data['shortcode'].replace('_',' ').title()
			try:
				data['instance'] = Type.objects.get(shortcode=data['shortcode']) ## -- If data exist, then execute Update of it -- ##
				data['id'] = data['instance'].id ## -- Pass  ID if data exist or not -- ##
			except:
				pass
		else:
			raise serializers.ValidationError({
				'status': 417, ## -- Expectation Failed -- ##
				'message': 'Required Params not passed -> shortcode, display'
			})
		return data

	def create(self, validated_data):
		"""
		Create and return a new `Type` instance, given the validated data.
		"""
		return Type.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Type` instance, given the validated data.
		"""
		#instance.shortcode = validated_data.get('shortcode', instance.shortcode)
		instance.display = validated_data.get('display', instance.display)
		instance.severity = validated_data.get('severity', instance.severity)
		instance.group = validated_data.get('group', instance.group)
		instance.configurable_counts = validated_data.get('configurable_counts', instance.configurable_counts)
		instance.save()

		return instance

	class Meta:
		model = Type
		fields = ('id', 'shortcode', 'display', 'severity', 'group', 'configurable_counts')