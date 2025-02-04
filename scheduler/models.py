from django.db import models
from users.models import CustomUser
from django.db.models import Q

class TimeSlot(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='%(class)s_createdby')
    start = models.DateTimeField()
    end = models.DateTimeField()

    def get_overlapping_slots(self, interviewer_id):
        """
        Returns a QuerySet of slots that overlap with this slots.
        """
        
        slots = TimeSlot.objects.filter(user_id=interviewer_id)
        # return slots.filter(
        #     Q(start__lt=self.end) & Q(end__gt=self.start) | 
        #     Q(start__gt=self.start) & Q(start__lt=self.end) |
        #     Q(end__gt=self.start) & Q(end__lt=self.end)
        # ).exclude(pk=self.pk)
        return slots.filter(
            Q(start__range=(self.start, self.end)) | Q(end__range=(self.start, self.end)) 
            ).exclude(pk=self.pk)   

