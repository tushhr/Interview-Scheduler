from django.shortcuts import redirect, render
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail

from datetime import date, datetime, timedelta
import pytz

# Models
from django.contrib.auth.models import User 
from .models import interview

# Create your views here.

#Function to check availability of all the participants
def check_availability(scheduled_interviews, start_time, end_time):
    #Set of tuples of start time, end time for all the scheduled interviews
    scheduled_timings = list(interview.objects.filter(id__in = scheduled_interviews).values_list('start_time', 'end_time'))
    
    for start, end in scheduled_timings:
        if start <= start_time < end or start < end_time < end or (start_time <= start < end <= end_time):
            return True
    
    return False

#Function to convert datetime from naive to offset
def convert_datetime_to_offset(naive_time):
    timezone = pytz.timezone("UTC")
    offset_time = timezone.localize(datetime.strptime(naive_time, '%Y-%m-%dT%H:%M'))

    return offset_time

#Function to convert datetime from offset to naive
def convert_datetime_to_naive(offset_time):
    offset_time = str(offset_time)
    naive_time = offset_time[:10] + "T" +  offset_time[11:-6]

    return naive_time

def index(request):
    return render(request, 'scheduler/index.html')

def schedule_interview(request):
    if request.method == "POST":
        # Needs to be update THREAD 2.0
        new_interview_name = request.POST['meet_name']
        participants_email = request.POST.getlist('email')
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        start_time = convert_datetime_to_offset(start_time)
        end_time = convert_datetime_to_offset(end_time)

        #Checks
        #Validating email
        try:
            participants = set()

            for email in participants_email:
                participant = User.objects.get(email = email)
                participants.add(participant)
                
        except ObjectDoesNotExist:
            messages.error(request, "Oops! One or more invalid Email ID. Please try again")
            return redirect('/')
                
        
        #Check for the number of participants
        if len(participants) < 2:
            messages.error(request, "Please select more than 2 distinct participants.")
            return redirect('/')
        

        #Check the Availability of participants
        #All the Interview id of the participants
        scheduled_interviews = User.objects.filter(email__in = participants_email).values_list('interview', flat=True)
        
        if check_availability(scheduled_interviews, start_time, end_time):
            messages.error(request, "One or more participants will be busy during the selected time period. Please try a different time period.")
            return redirect('/')

        #After validating all checks
        #Add to Database
        new_interview = interview(interview_name = new_interview_name, start_time = start_time, end_time = end_time)
        new_interview.save()

        for participant in participants:
            new_interview.participant.add(participant)

        messages.success(request, "Interview Scheduled successfully")
        
        send_mail(
            subject = "Interview Scheduled",
            message = "Your interview is scheduled.",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = participants_email
        )
        return redirect('/')

    return redirect('/')

def timeline(request):
    interviews = interview.objects.filter(end_time__date__gt = date.today() - timedelta(days = 1))
    
    context ={
        'interviews': interviews
    }

    return render(request, 'scheduler/timeline.html', context)

def interview_page(request, interview_id):
    schedule_interview = interview.objects.get(id = interview_id)

    schedule_interview.start_time = convert_datetime_to_naive(schedule_interview.start_time)
    schedule_interview.end_time = convert_datetime_to_naive(schedule_interview.end_time)

    context = {
        'interview': schedule_interview
    }
    return render(request, 'scheduler/interview.html', context)

def edit_interview(request):
    if request.method == "POST":
        if 'edit_interview' in request.POST:
            interview_id = request.POST['interview_id']
            edit_interview = request.POST['meet_name']
            participants_email = request.POST.getlist('email')

            start_time = request.POST['start_time']
            end_time = request.POST['end_time']

            #Converting naive datetime to offset
            start_time = convert_datetime_to_offset(start_time)
            end_time = convert_datetime_to_offset(end_time)
            
            #Checks
            #Validating email
            try:
                participants = set()

                for email in participants_email:
                    participant = User.objects.get(email = email)
                    participants.add(participant)
                    
            except ObjectDoesNotExist:
                messages.error(request, "Oops! One or more invalid Email ID. Please try again")
                return redirect('/')
                    
            
            #Check for the number of participants
            if len(participants) < 2:
                messages.error(request, "Please select more than 2 distinct participants.")
                return redirect('/')
            

            #Check the Availability of participants
            #All the Interview id of the participants
            scheduled_interviews = User.objects.filter(email__in = participants_email).values_list('interview', flat=True)
            
            if check_availability(scheduled_interviews, start_time, end_time):
                messages.error(request, "One or more participants will be busy during the selected time period. Please try a different time period.")
                return redirect('/')

            #After validating all checks
            #Modify the database
            meet = interview.objects.get(id = interview_id)
            meet.interview_name = edit_interview
            meet.start_time = start_time
            meet.end_time = end_time

            meet.participant.clear()
            for participant in participants:
                meet.participant.add(participant)
            
            meet.save()
            
            send_mail(
                subject = "Your scheduled interview has an update!",
                message = "Your interview is updated.",
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = participants_email
            )

            messages.success(request, "Interview edited successfully")
            return redirect('/timeline')

        elif 'delete_interview' in request.POST:
            interview_id = request.POST['interview_id']
            meet = interview.objects.get(id = interview_id)

            participants_email = list()
            for participant in meet.participant.all():
                participants_email.append(participant.email)

            meet.delete()

            send_mail(
                subject = "Your scheduled interview has an update!",
                message = "Your interview is updated.",
                from_email = settings.EMAIL_HOST_USER,
                recipient_list = participants_email
            )

            messages.success(request, "Interview deleted successfully")
            return redirect('/timeline')


    return redirect('/timeline')