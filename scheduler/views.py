from django.shortcuts import redirect, render
from django.contrib import messages 
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail

from datetime import date, datetime
import pytz

# Models
from django.contrib.auth.models import User 
from .models import interview

# Create your views here.

##REMOVE PRINTS THREAD 5.0
#Clearing Error messages THREAD 6.1

def check_availability(participants, start_time, end_time):
    #Set of tuples of start time, end time of all the interviews
    ##NAMING CONVENTION !!! THREAD 1.4.3
    participant_timings = list(interview.objects.filter(id__in = participants).values_list('start_time', 'end_time'))
    
    for start, end in participant_timings:
        if start <= start_time < end or start < end_time < end or (start_time <= start < end <= end_time):
            return True
    
    return False

def convert_datetime(start_time, end_time):
    timezone = pytz.timezone("UTC")
    start_time = timezone.localize(datetime.strptime(start_time, '%Y-%m-%dT%H:%M'))
    end_time = timezone.localize(datetime.strptime(end_time, '%Y-%m-%dT%H:%M'))

    return (start_time, end_time)

def index(request):
    return render(request, 'scheduler/index.html')

def schedule_interview(request):
    if request.method == "POST":
        # Needs to be update THREAD 2.0
        new_interview = request.POST['meet_name']

        #Make it generic THREAD 2.1
        participants_email = request.POST.getlist('email')
        

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        #Converting input datetime field into django friendly type
        start_time, end_time = convert_datetime(start_time, end_time)

        #Checks
        #Validating email
        try:
            participants = set()

            for email in participants_email:
                participant = User.objects.get(email = email)
                participants.add(participant)
                
        except ObjectDoesNotExist:
            messages.error(request, "Oops! One or more invalid Email ID. Please try again")
            print("Woops! Invalid Email ID. Please try again.")
            print("Error")
            return redirect('/')
                
        
        #Check for the number of participants
        if len(participants) < 2:
            messages.error(request, "Please selecte more than 2 distinct participants.")
            return redirect('/')
        
        #Check the Availability of participants
        #All the Interview id of the participants
        participant_interviews = User.objects.filter(email__in = participants_email).values_list('interview', flat=True)
        
        if check_availability(participant_interviews, start_time, end_time):
            messages.error(request, "One or more participants will be busy during the selected time period. Please try a different time period.")
            print("Availability issues")
            print("Error")
            return redirect('/')

        #Add to Database
        meet = interview(interview_name = new_interview, start_time = start_time, end_time = end_time)
        meet.save()

        for participant in participants:
            meet.participant.add(participant)

        
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
    interviews = interview.objects.filter(end_time__date__gt = date.today())

    context ={
        'interviews': interviews
    }

    return render(request, 'scheduler/timeline.html', context)

def interview_page(request, interview_id):
    interviews = interview.objects.get(id = interview_id)

    #THREAD 4.0
    #Converting Python datetime into HTML
    interviews.start_time, interviews.end_time = str(interviews.start_time), str(interviews.end_time)
    interviews.start_time = interviews.start_time[:10] + "T" + interviews.start_time[11:-6]
    interviews.end_time = interviews.end_time[:10] + "T" + interviews.end_time[11:-6]

    context = {
        'interview': interviews
    }
    return render(request, 'scheduler/interview.html', context)

def edit_interview(request):
    if request.method == "POST":
        # Needs to be update THREAD 2.0
        interview_id = request.POST['interview_id']
        edit_interview = request.POST['meet_name']

        #Make it generic THREAD 2.1
        participants_email = request.POST.getlist('email')

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        #Converting input datetime field into django friendly type
        start_time, end_time = convert_datetime(start_time, end_time)
        
        #Checks
        #Validating email
        try:
            participants = set()

            for email in participants_email:
                participant = User.objects.get(email = email)
                participants.add(participant)
                
        except ObjectDoesNotExist:
            messages.error(request, "Oops! One or more invalid Email ID. Please try again")
            print("Woops! Invalid Email ID. Please try again.")
            print("Error")
            return redirect('/timeline')
                
        
        #Check for the number of participants
        if len(participants) < 2:
            messages.error(request, "Please selecte more than 2 distinct participants.")
            return redirect('/timeline')

        #Check the Availability of participants
        #All the Interview id of the participants
        participant_interviews = set(User.objects.filter(email__in = participants_email).values_list('interview', flat=True))
        
        #Remove the Interview user is editing
        participant_interviews.remove(int(interview_id))
        
        if check_availability(participant_interviews, start_time, end_time):
            messages.error(request, "One or more participants will be busy during the selected time period. Please try a different time period.")
            return redirect('/timeline')

        #Adding to Database
        meet = interview.objects.get(id = interview_id)
        meet.interview_name = edit_interview
        meet.start_time = start_time
        meet.end_time = end_time

        meet.participant.clear()
        for participant in participants:
            meet.participant.add(participant)
        
        meet.save()

        messages.success(request, "Interview edited successfully")
        
        send_mail(
            subject = "Your scheduled interview has an update!",
            message = "Your interview is updated.",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = participants_email
        )

        return redirect('/timeline')

    return redirect('/timeline')



        ##Two way -- Show the USER which has confliciting schedule as well THREAD 1.4
        ##Or just show a general error. T
        ##Going with second flow right now
            ##Throw some error message and return. THREAD 1.0.1

        ##Update with "__in" THREAD 1.4.2
            ##Throw some error message and return. THREAD 1.4.1#
            # Extra Feauture
        #Send common time period of all person THRAD 101


        ##Update with "__in" THREAD 1.4.2
        # #Valid Number of participants THREAD 1.1