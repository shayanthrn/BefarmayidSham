from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
import random
from django.contrib.auth.hashers import make_password, check_password

class LandingPage(View):
    def get(self,request):
        return render(request, 'main/landing_page.html',context={})
    def post(self,request):
        competition_id = request.POST.get('competitionId')
        name = request.POST.get('name')
        email = request.POST.get('email')
        starter = request.POST.get('starter')
        main_course = request.POST.get('mainCourse')
        dessert = request.POST.get('dessert')
        theme = request.POST.get('theme')
        competition = Competition.objects.filter(competition_id=competition_id).first()
        if competition is not None:
            dates = [competition.date1, competition.date2, competition.date3, competition.date4]
            date = None
            index = 0
            while date == None:
                random_date = random.choice(dates)
                index+=1
                if Competitor.objects.filter(competition_id=competition_id, date=random_date).first() is None:
                    date = random_date
                if index>4:
                    break
            if date == None:
                return HttpResponse("No time for error page! fuck you! there is no such a competition!")
            entry = Competitor(
                name = name,
                competition_id=competition_id,
                email=email,
                starter=starter,
                main_course=main_course,
                dessert=dessert,
                theme=theme,
                date=date
            )
            entry.save()
            subject = 'Welcome to Meetup Cook-Off'
            message = f'Dear {name}! \n\n Thank you for signing up for our service. The menu and host name will be send to you through email at proper time. \n Enjoy your competition!! \n Meetup Cook-Off Team'
            email_from = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect("/")
        else:
            return HttpResponse("No time for error page! fuck you! there is no such a competition!")
        

class CompetitionPage(View):
    def get(self, request):
        return render(request, 'main/competition.html',context={})
    def post(self,request):
        competition_id = request.POST.get('competitionId')
        password = request.POST.get('password')
        dates = request.POST.getlist('dates')

        entry = Competition(
            competition_id=competition_id,
            date1=dates[0],
            date2=dates[1],
            date3=dates[2],
            date4=dates[3]
        )
        entry.set_password(password)  # Hash the password
        entry.save()
        return redirect("/")
    
class DirectorLogin(View):
    def get(self, request, id):
        return render(request, 'main/director_login.html',context={})
    
    def post(self,request,id):
        password = request.POST.get('password')
        competition = Competition.objects.filter(competition_id=id).first()
        if competition is not None:
            if competition.check_password(password):
                hashed_string = make_password(id+"123")
                response = HttpResponseRedirect(f'/manage/{id}/')  # Replace '/target-url/' with your redirect URL
                response.set_cookie('security', hashed_string, max_age=3600)  # Set the cookie
                return response
            else:
                return HttpResponse("No time for error page! fuck you! there is no such a competition!")
        else:
            return HttpResponse("No time for error page! fuck you! there is no such a competition!")
        
class DirectorManage(View):
    def get(self, request, id):
        cookie_value = request.COOKIES.get('security', 'default_value')
        if(check_password(id+"123", cookie_value)):
            entries = Competitor.objects.all()  # Fetch all entries of the model
            return render(request, 'main/director.html', {'entries': entries})
        else:
            return HttpResponse("No time for error page! fuck you! there is no such a competition!")
class SendEmail(View):
    def get(self, request, id, cid):
        cookie_value = request.COOKIES.get('security', 'default_value')
        if(check_password(cid+"123", cookie_value)):
            guests = Competitor.objects.exclude(id=id)
            host = Competitor.objects.filter(id=id).first()
            for entry in guests:
                subject = 'Menu of Tonight'
                message = f'Dear {entry.name}!\n Here is the menu of our host for tonight: {host.name}!! \n starter: {host.starter} \n main course: {host.main_course} \n dessert: {host.dessert} \n theme: {host.theme} \n Have Fun!'
                email_from = settings.DEFAULT_FROM_EMAIL
                recipient_list = [entry.email]
                send_mail(subject, message, email_from, recipient_list)
            return redirect(f"/manage/{cid}/")
        else:
            return HttpResponse("No time for error page! fuck you! there is no such a competition!")
    