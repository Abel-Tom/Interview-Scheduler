from rest_framework import serializers
from .models import TimeSlot
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser

from datetime import datetime, timezone

class RegisterTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = ['start', 'end','user']

        extra_kwargs = {
            'start': {'required': True},
            'end': {'required': True},
            'user': {'required': False}
        }

    def validate(self, attrs):
        user = self.context['request'].user 
        
        if user.type == 'manager':
            raise serializers.ValidationError({"user": "Managers cannot create time slots."})
        if attrs['start'] >= attrs['end']:
            raise serializers.ValidationError({"start": "Start time cannot be after end time."})
        now = datetime.now() 
        now = now.replace(tzinfo=timezone.utc) 
        if attrs['start'] < now:
            raise serializers.ValidationError({"start": "Start time cannot be in the past."})
        if attrs['end'] < now: 
            raise serializers.ValidationError({"end": "End time cannot be in the past."})
        slots = TimeSlot.objects.filter(user=user)
        if slots.filter(start__gte=attrs['start'], end__lte=attrs['end']).exists():
            raise serializers.ValidationError({"start": "Time slot overlaps with existing time slot."})
        if slots.filter(start__lt=attrs['start'], end__gt=attrs['start']).exists():
            raise serializers.ValidationError({"start": "Time slot overlaps with existing time slot."})
        if slots.filter(start__lt=attrs['end'], end__gt=attrs['end']).exists():
            raise serializers.ValidationError({"end": "Time slot overlaps with existing time slot."})
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user        
        slot = TimeSlot.objects.create(
            user=user,
            start=validated_data['start'],
            end=validated_data['end'],
        )
        slot.save()
        return slot