
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from datetime import datetime, timezone, timedelta

from rest_framework.response import Response
from .serializers import RegisterTimeSerializer
from .models import TimeSlot

from users.models import CustomUser

class RegisterTimeView(generics.CreateAPIView):
    queryset = TimeSlot.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterTimeSerializer

class TimeSlotView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        now = datetime.now() 
        now = now.replace(tzinfo=timezone.utc)
        next = now.replace(hour=23, minute=59) + timedelta(days=1)
        res = []
        if user.type == 'manager':
            slots = TimeSlot.objects.filter(start__gte=now,end__lte=next)
            candidateTimeSlots = slots.filter(user_id=int(request.data['candidate']))
            for slot in candidateTimeSlots:
                overlapping_slots = slot.get_overlapping_slots(int(request.data['interviewer']))
                for event in overlapping_slots:
                    later_start = max(slot.start, event.start)
                    earlier_end = min(slot.end, event.end)
                    while later_start <= earlier_end:
                        later_start_plus_on = later_start + timedelta(minutes=60)
                        if later_start_plus_on <= earlier_end:
                            res.append((later_start.strftime("%I:%M %p"), later_start_plus_on.strftime("%I:%M %p")))
                        later_start = later_start_plus_on
            return Response(res)
        else:
            slots = TimeSlot.objects.filter(user=user)
        slots = slots.values('start', 'end', 'user')
        return Response(slots)

class TestView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        return Response({'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name, 'type': user.type})