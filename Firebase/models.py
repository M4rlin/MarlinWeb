from django.db import models

# Create your models here.
class quizes(models.Model):
    # Qid = models.IntegerField(primary_key =True)
    Quiz_Topic = models.CharField(max_length=20,null=False,blank=True)
    Quiz_Date =  models.CharField(max_length=20,null=False,blank=True)
    sections =  models.CharField(max_length=20,null=False,blank=True)
    subjects =  models.CharField(max_length=20,null=False,blank=True)

class feedback(models.Model):
    email = models.EmailField(max_length=75,)
    subject = models.CharField(max_length=50, blank=False, null=False)
    suggestion = models.CharField(max_length=150, blank=False, null=False)

class accounts(models.Model):
    UserToken = models.CharField(max_length=50, blank=False, null=False)
    UserType = models.CharField(max_length=5, blank=False, null=True)
    Fname = models.CharField(max_length=50, blank=False, null=False)
    Lname = models.CharField(max_length=50, blank=False, null=False)
    section = models.CharField(max_length=50, blank=False, null=False)
    subject = models.CharField(max_length=50, blank=False, null=True)
    
    def __str__(self):
        return self.UserToken