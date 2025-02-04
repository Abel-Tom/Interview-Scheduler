
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from datetime import datetime, timezone, timedelta

from rest_framework.response import Response
from .serializers import RegisterTimeSerializer
from .models import TimeSlot
from django.db.models import Q, F
from django.db import connection

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
        # now = now.replace(hour=00, minute=00)
        next = now.replace(hour=23, minute=59)
        # next = now.replace(hour=23, minute=59) + timedelta(days=1)
        res = []
        if user.type == 'manager':
            slots = TimeSlot.objects.filter(start__gte=now,end__lte=next)
            candidate_slots = slots.filter(user_id=int(request.data['candidate']))
            for slot in candidate_slots:
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

class OverlappingTimeSlots(APIView):
    def get(self, request):
        now = datetime.now() 
        now = now.replace(tzinfo=timezone.utc)
        end = now.replace(hour=23, minute=59)
        end_str = end.strftime("%Y-%m-%d %H:%M:%S")
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        res = []
        try:
            candidate_id = int(request.GET.get('candidate'))
            interviewer_id = int(request.GET.get('interviewer'))
        except:
            return Response({'error': 'Please provide candidate and interviewer id', 'status': 400})
        if not candidate_id and not interviewer_id:
            return Response({'error': 'Please provide candidate and interviewer id', 'status': 400})
        with connection.cursor() as cursor:
            
            sql = """
                SELECT t1.*, t2.*
                FROM scheduler_timeslot t1
                JOIN scheduler_timeslot t2 ON t1.id <> t2.id  -- Avoid comparing a row to itself
                WHERE t1.user_id = %s AND t2.user_id=%s AND t1.start BETWEEN %s AND %s AND t2.start BETWEEN %s AND %s AND t1.start < t2.end AND t1.end > t2.start
                ORDER BY t1.start ASC;
            """
            params = [candidate_id, interviewer_id, now_str, end_str, now_str, end_str]  
            cursor.execute(sql,params)  

            rows = cursor.fetchall()
            for row in rows:
                later_start = max(row[1], row[5])
                earliest_day = later_start.date().day
                earlier_end = min(row[2], row[6])
                while later_start <= earlier_end and later_start.date().day == earliest_day:
                    later_start_plus_one = later_start + timedelta(minutes=60)
                    if later_start_plus_one <= earlier_end:
                        res.append((later_start.strftime("%I:%M %p"), later_start_plus_one.strftime("%I:%M %p")))
                    later_start = later_start_plus_one
        return Response(res)
    
