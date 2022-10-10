from django.db import models

# Importing Models
from django.contrib.auth.models import User

# Create your models here.
class interview(models.Model):
    meet_name = models.CharField(verbose_name = "Meet Name", max_length = 100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.meet_name

class schedule(models.Model):
    meet = models.ForeignKey(interview, on_delete = models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.meet.meet_name