from django.db import models

# Importing Models
from django.contrib.auth.models import User

# Create your models here.
class interview(models.Model):
    interview_name = models.CharField(verbose_name = "Interview Name", max_length = 100)
    start_time = models.DateTimeField(verbose_name = "Start Time")
    end_time = models.DateTimeField(verbose_name = "End Time")
    participant = models.ManyToManyField(User)

    def __str__(self):
        return self.interview_name