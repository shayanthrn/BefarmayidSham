from django.db import models
from django.contrib.auth.hashers import make_password

class Competition(models.Model):
    competition_id = models.CharField(max_length=100)
    password_hash = models.CharField(max_length=255)  # Store the hashed password
    date1 = models.DateField(null=True,blank=True)
    date2 = models.DateField(null=True,blank=True)
    date3 = models.DateField(null=True,blank=True)
    date4 = models.DateField(null=True,blank=True)

    def set_password(self, password):
        self.password_hash = make_password(password)
    
    def check_password(self, password):
        from django.contrib.auth.hashers import check_password
        return check_password(password, self.password_hash)

    def __str__(self):
        return f"Competition {self.competition_id}"

class Competitor(models.Model):
    name = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(unique=True, null=True,blank=True)
    starter = models.CharField(max_length=255,null=True,blank=True)
    main_course = models.CharField(max_length=255,null=True,blank=True)
    dessert = models.CharField(max_length=255,null=True,blank=True)
    theme = models.CharField(max_length=255,null=True,blank=True)
    competition_id = models.CharField(max_length=255,null=True,blank=True)
    date = models.DateField()
    def __str__(self):
        return self.name