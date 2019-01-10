from .models import *
from .views import *
import pyrebase

class QuizData:
    lq = None
    lq1 = None
    lq2 = None
    lq3 = None
    lq4 = None
    
    l_Accounts = None
    l_Accounts1 = None
    l_Accounts2 = None
    l_Accounts3 = None
    l_Accounts4 = None

    page = None
    page1 = None
    page2 = None
    page3 = None
    page4 = None

    contacts = None 
    contacts1 = None
    contacts2 = None
    contacts3 = None
    contacts4 = None

    AC1 = True
    AC2 = True
    AC3 = True
    AC4 = True
    AC5 = True

    def Test(self):
        try:
            request.session['email']
        except KeyError:
            print("No")
            return HttpResponseRedirect('/marlin/login')
    def If_Empty_Data(self):
        if not self.lq:
            self.AC1 = False
        if not self.lq1:
            self.AC2 = False
        if not self.lq2:
            self.AC3 = False
        if not self.lq3:
            self.AC4 = False
        if not self.lq4:
            self.AC5 = False
        return 0
    
    def Get_Pages(self,p1,p2,p3,p4,p5):
        self.page = p1
        self.page1 = p2
        self.page2 = p3
        self.page3 = p4
        self.page4 = p5
        print(p1)
    
    def Get_Data(self,Section1,Section2,Section3,Section4,Section5):
        self.lq = Section1
        self.lq1 = Section2
        self.lq2 = Section3
        self.lq3 = Section4
        self.lq4 = Section5
    
    def Distribute_Data(self,Page1,Page2,Page3,Page4,Page5):
        self.contacts = Page1.get_page(self.page)
        self.contacts1 = Page2.get_page(self.page1)
        self.contacts2 = Page3.get_page(self.page2)
        self.contacts3 = Page4.get_page(self.page3)
        self.contacts4 = Page5.get_page(self.page4)
    
    def Get_DB_Acounts_students(self):
        self.l_Accounts = accounts.objects.all().order_by('Lname').filter(section__contains="N1").filter(UserType__contains="S")
        self.l_Accounts1 = accounts.objects.all().order_by('Lname').filter(section__contains="ZC11").filter(UserType__contains="S")
        self.l_Accounts2 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT11").filter(UserType__contains="S")
        self.l_Accounts3 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT12").filter(UserType__contains="S")
        self.l_Accounts4 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT13").filter(UserType__contains="S")

def CheckData():
    quiz = databases.child("quiz").shallow().get().val()
    for sec in quiz:
        subject = databases.child("quiz").child(sec).shallow().get().val()
        for sub in subject:
            dates = databases.child("quiz").child(sec).child(sub).shallow().get().val()
            for date in dates:
                topic = databases.child("quiz").child(sec).child(sub).child(date).child("Quiz_Topic").get().val()
                if quizes.objects.filter(Quiz_Date__contains=date).filter(sections__contains=sec):
                    print(sec, date)
                else:
                    l = quizes(Quiz_Date=date,Quiz_Topic=topic,sections=sec,subjects=sub)
                    l.save()
    
    listUsers = databases.child("users").shallow().get().val()
    usersList = []
    sect = ''
    for i in listUsers:
        if databases.child("users").child(i).child('Details').child("Type").get().val() == "Student":
            usersList.append(i)

    for a in usersList:
        if databases.child("users").child(a).child('Details').child("Type").get().val() == "Student":
            if accounts.objects.filter(UserToken__contains=a):
                None
            else:
                fname = databases.child("users").child(a).child('Details').child("Student_Fname").get().val()
                lname = databases.child("users").child(a).child('Details').child("Student_Lname").get().val()
                sec = databases.child("users").child(a).child('Details').child("Classes").shallow().get().val()
                for s in sec:
                    sections = s
                # sec =
                l = accounts(UserToken=a,UserType="S",Fname=fname,Lname=lname,section=sections)
                l.save()