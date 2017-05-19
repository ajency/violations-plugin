from rest_framework import serializers
from .models import Comment

from violations.models import Violation

class CommentSerializer(serializers.Serializer):
	violation_id = serializers.IntegerField(min_value=1)
	who_id = serializers.IntegerField(min_value=1)
	who_meta = serializers.JSONField(binary=False)
	comment = serializers.CharField(required=True, allow_blank=True, max_length=100)

	def validate(self, data):
		list_param = ['violation_id', 'who_id', 'comment']

		if not all (k in data for k in list_param):
			raise serializers.ValidationError({
				'status': 417, ## -- Expectation Failed -- ##
				'message': "'violation_id', 'who_id' and 'comment' parameters are required"
			})
		return data

	def create(self, validated_data):
		"""
		Create and return a new `Comment` instance, given the validated data.
		"""
		
		violation_data = Violation.objects.get(id=validated_data.pop('violation_id')) ## -- Get Violation Details using Vioaltion ID -- ##
		return Comment.objects.create(violation=violation_data, **validated_data)

	def update(self, instance, validated_data):
		"""
		Update and return an existing `Comment` instance, given the validated data.
		"""
		#instance.violation_id = validated_data.get('violation_id', instance.violation_id)
		instance.who_id = validated_data.get('who_id', instance.who_id)
		instance.who_meta = validated_data.get('who_meta', instance.who_meta)
		instance.comment = validated_data.get('comment', instance.comment)
		instance.save()

		return instance

	class Meta:
		model = Comment
		fields = ('id', 'violation_id', 'who_id', 'who_meta', 'comment', 'timestamp')