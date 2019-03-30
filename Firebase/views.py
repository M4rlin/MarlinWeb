from django.shortcuts import render
from itertools import chain
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import *
from .models import *
import datetime
from .class_function import *
from datetime import datetime
# from datetime
import pyrebase
import csv
# Create your views here.
config = {
    'apiKey': "AIzaSyB88uhl-6syFZY4QVniD9SaBDTA79UYxj4",
    'authDomain': "lastlysp.firebaseapp.com",
    'databaseURL': "https://lastlysp.firebaseio.com",
    'projectId': "lastlysp",
    'storageBucket': "",
    'messagingSenderId': "806949477402"

}

firebase = pyrebase.initialize_app(config)
authed = firebase.auth()
database = firebase.database()
def redirect(request):
    return HttpResponseRedirect('/marlin/login')    

def Login(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
    else:
        return HttpResponseRedirect('/marlin/Quiz/')

    context = {
        "form": LoginForm(),
        "error":False,
        "suggest":FeedBackForm(),
        "t":False,
    }

    return render(request,"login2.html",context)

def FeedBack(request):
    f_User_Info = FeedBackForm(request.POST)
    if f_User_Info.is_valid():
        obj1 = f_User_Info.save()
        obj1.save()
    return HttpResponseRedirect('/Login/')


def Upload(request):
    data = []
    csv_file = request.FILES["file"]
    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(reverse("myapp:upload_csv"))

    file_data = csv_file.read().decode("utf-8")

    lines = file_data.split("\n")
    #loop over the lines and save them in db. If error , store as string and then display
    for line in lines:
        fields = line.split(",")
        # data_dict = {}
        # data_dict["name"] = fields[0]
        # data_dict["start_date_time"] = fields[1]
        # data_dict["end_date_time"] = fields[2]
        print (len(fields[0]))


    return HttpResponse(" ")

def PostLogin(request):

    email = request.POST.get('email')
    passw = request.POST.get('password')
    try:
        user = authed.sign_in_with_email_and_password(email,passw)
    except:
        message = "Invalid Email or Password!!"
        context = {
            "form": LoginForm(),
            "suggest":FeedBackForm(),
            "error":True,
            "t":False,
            "message":message
        }
        return render(request,"login2.html",context)

    if database.child("users").child(user['localId']).child("Details").child("Type").get().val() == "Student":
        return HttpResponseRedirect('/marlin/Logout/')

    session_id = user['idToken']
    request.session['user'] = str(user)
    request.session['uid'] = str(session_id)
    request.session['local'] = str(user['localId'])
    request.session['email'] = str(email)
    request.session['type'] = database.child("users").child(user['localId']).child("Details").child("Type").get().val()
    request.session['section'] = 0
    listSection = []


    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(user['localId']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    if database.child("users").child(user['localId']).child("Details").child("Type").get().val() == "Admin":
        request.session['fname'] = database.child("users").child(user['localId']).child("Details").child("Teacher_Fname").get().val()
        request.session['lname'] = database.child("users").child(user['localId']).child("Details").child("Teacher_Lname").get().val()
    else:
        request.session['fname'] = database.child("users").child(user['localId']).child("Details").child("Teacher_Fname").get().val()
        request.session['lname'] = database.child("users").child(user['localId']).child("Details").child("Teacher_Lname").get().val()

    quiz = database.child("quiz").shallow().get().val()
    for sec in quiz:
        subject = database.child("quiz").child(sec).shallow().get().val()
        for sub in subject:
            dates = database.child("quiz").child(sec).child(sub).shallow().get().val()
            for date in dates:
                topic = database.child("quiz").child(sec).child(sub).child(date).child("Quiz_Topic").get().val()
                if quizes.objects.filter(Quiz_Date__contains=date).filter(sections__contains=sec):
                    # print(sec, date)
                    None
                else:
                    l = quizes(Quiz_Date=date,Quiz_Topic=topic,sections=sec,subjects=sub)
                    l.save()

    listUsers = database.child("users").shallow().get().val()
    usersList = []
    sect = ''
    for i in listUsers:
        if database.child("users").child(i).child('Details').child("Type").get().val() == "Student":
            usersList.append(i)

    for a in usersList:
        if database.child("users").child(a).child('Details').child("Type").get().val() == "Student":
            if accounts.objects.filter(UserToken__contains=a):
                None
            else:
                fname = database.child("users").child(a).child('Details').child("Student_Fname").get().val()
                lname = database.child("users").child(a).child('Details').child("Student_Lname").get().val()
                sec = database.child("users").child(a).child('Details').child("Classes").shallow().get().val()
                for s in sec:
                    sections = s
                    sub = database.child("users").child(a).child('Details').child("Classes").child(sections).child("Subject_Code").get().val()
                    print (sub)
                # sec =
                l = accounts(UserToken=a,UserType="S",Fname=fname,Lname=lname,section=sections,subject=sub)
                l.save()


    return HttpResponseRedirect('/marlin/Quiz')

def Profile(request,data):
    fname = accounts.objects.filter(UserToken__contains=data)
    topic = []
    dates = []
    item1 = []
    item2 = []
    item3 = []
    item4 = []
    item5 = []
    Ans1 = []
    Ans2 = []
    Ans3 = []
    Ans4 = []
    Ans5 = []
    Type1 = []
    Type2 = []
    Type3 = []
    Type4 = []
    Type5 = []
    ctr = []
    score_count=0
    dis_count=0
    result1 = []
    result2 = []
    result4 = []
    result3 = []
    result5 = []
    dissmis1 = []
    dissmis2 = []
    dissmis3 = []
    dissmis4 = []
    dissmis5 = []
    
    for i in database.child("users").child(data).child("Details").child("Classes").get().val():
        section = i
        sub = database.child("users").child(data).child('Details').child("Classes").child(i).child("Subject_Code").get().val()
        
    for date in database.child("quiz").child(section).child(sub).shallow().get().val():
        dates.append(date)

    dates.sort(reverse=True)
    for d in dates:
        topic.append(database.child("quiz").child(section).child(sub).child(d).child("Quiz_Topic").get().val())
        item1.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item1").child("Question").get().val())
        item2.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item2").child("Question").get().val())
        item3.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item3").child("Question").get().val())
        item4.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item4").child("Question").get().val())
        item5.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item5").child("Question").get().val())
        Type1.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item1").child("Type").get().val())
        Type2.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item2").child("Type").get().val())
        Type3.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item3").child("Type").get().val())
        Type4.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item4").child("Type").get().val())
        Type5.append(database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item5").child("Type").get().val())

        times1 = database.child("Dismiss_Record").child(section).child(sub).child(d).child(data).child("Item1").shallow().get().val()
        times2 = database.child("Dismiss_Record").child(section).child(sub).child(d).child(data).child("Item2").shallow().get().val()
        times3 = database.child("Dismiss_Record").child(section).child(sub).child(d).child(data).child("Item3").shallow().get().val()
        times4 = database.child("Dismiss_Record").child(section).child(sub).child(d).child(data).child("Item4").shallow().get().val()
        times5 = database.child("Dismiss_Record").child(section).child(sub).child(d).child(data).child("Item5").shallow().get().val()

        # print (times1)
        if times1 is not None:
            for t in times1:
                dis_count = dis_count + 1  
            dissmis1.append(dis_count)
            dis_count = 0
        else:
            dissmis1.append(dis_count)

        if times2 is not None:
            for t in times2:
                dis_count = dis_count + 1  
            dissmis2.append(dis_count)
            dis_count = 0
        else:
            dissmis2.append(dis_count)

        if times3 is not None:
            for t in times3:
                dis_count = dis_count + 1  
            dissmis3.append(dis_count)
            dis_count = 0
        else:
            dissmis3.append(dis_count)     
        
        if times4 is not None:
            for t in times4:
                dis_count = dis_count + 1  
            dissmis4.append(dis_count)
            dis_count = 0
        else:
            dissmis4.append(dis_count)
        
        if times5 is not None:
            for t in times5:
                dis_count = dis_count + 1  
            dissmis5.append(dis_count)
            dis_count = 0
        else:
            dissmis5.append(dis_count)

        if database.child("Answer").child(section).child(sub).child(d).child(data).child("Item1").child("Answer").get().val() == database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item1").child("Answer").get().val():
            result1.append("Correct")
            score_count = score_count + 1
        elif database.child("Answer").child(section).child(sub).child(d).child(data).child("Item1").child("Answer").get().val() != database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item1").child("Answer").get().val():
            result1.append("Incorrect")            
        else:
            result1.append("No Answer")    

        if database.child("Answer").child(section).child(sub).child(d).child(data).child("Item2").child("Answer").get().val() == database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item2").child("Answer").get().val():
            result2.append("Correct")
            score_count = score_count + 1
        elif database.child("Answer").child(section).child(sub).child(d).child(data).child("Item2").child("Answer").get().val() != database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item2").child("Answer").get().val():
            result2.append("Incorrect")            
        else:
            result2.append("No Answer")  
        
        
        if database.child("Answer").child(section).child(sub).child(d).child(data).child("Item3").child("Answer").get().val() == database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item3").child("Answer").get().val():
            result3.append("Correct")
            score_count = score_count + 1
        elif database.child("Answer").child(section).child(sub).child(d).child(data).child("Item3").child("Answer").get().val() != database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item3").child("Answer").get().val():
            result3.append("Incorrect")            
        else:
            result3.append("No Answer")  

        if database.child("Answer").child(section).child(sub).child(d).child(data).child("Item4").child("Answer").get().val() == database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item4").child("Answer").get().val():
            result4.append("Correct")
            score_count = score_count + 1
        elif database.child("Answer").child(section).child(sub).child(d).child(data).child("Item4").child("Answer").get().val() != database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item4").child("Answer").get().val():
            result4.append("Incorrect")            
        else:
            result4.append("No Answer")  
        
        if database.child("Answer").child(section).child(sub).child(d).child(data).child("Item5").child("Answer").get().val() == database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item5").child("Answer").get().val():
            result5.append("Correct")
            score_count = score_count + 1
        elif database.child("Answer").child(section).child(sub).child(d).child(data).child("Item5").child("Answer").get().val() != database.child("quiz").child(section).child(sub).child(d).child("Items").child("Item5").child("Answer").get().val():
            result5.append("Incorrect")            
        else:
            result5.append("No Answer") 

        ctr.append(score_count)
        score_count = 0

    Quiz_Data = zip(topic,item1,item2,item3,item4,item5,Type1,Type2,Type3,Type4,Type5,result1,result2,result3,result4,result5,ctr,dissmis1,dissmis2,dissmis3,dissmis4,dissmis5)
    context ={ 
        "t":True,
        "fname":fname.values_list("Fname", flat=True),
        "lname":fname.values_list("Lname", flat=True),
        "email": request.session['email'],
        "topic": Quiz_Data,
        # "date":date,
    }
    return render(request,"Profile.html",context)

    # return HttpResponse(data)


def DeleteStudent(request,data):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")
    database.child("users").child(data).remove()
    row = accounts.objects.all().filter(UserToken__contains=data).delete()

    
    return HttpResponseRedirect('/marlin/AddUser/')
    # return HttpResponse(data)

def DeleteProf(request,data):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")
    database.child("users").child(data).remove()
    row = accounts.objects.all().filter(UserToken__contains=data).delete()

    
    return HttpResponseRedirect('/marlin/AddUserTeacher/')

def updateItem (request,section,subject,date,item):
    type1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).child("Type").get().val()
    if type1 == 'I':
        question = request.POST.get('Q1')
        answeri = request.POST.get('Answer')
        if question != "" and question is not None:
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Question": question})
        if answeri is not None and answeri != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Answer":answeri})
    elif type1 == 'TF':
        question = request.POST.get('Q1')
        answertf = request.POST.get('Tf_Answer1')
        if question != "" and question is not None:
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Question": question})
        if answertf is not None and answertf != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Answer":answertf})

    elif type1 == 'MC':
        question = request.POST.get('Q1')
        answer = request.POST.get('optradio5')
        Option1 = request.POST.get('item2Op1')
        Option2 = request.POST.get('item2Op2')
        Option3 = request.POST.get('item2Op3')
        if question != "" and question is not None:
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Question": question})
        if answer is not None and answer != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Answer":answer})
        if Option1 is not None and Option1 != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Option1":Option1})
        if Option3 is not None and Option3 != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Option3":Option3})
        if Option2 is not None and Option2 != "":
            database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).update({"Option2":Option2})

    topic = database.child("quiz").child(section).child(subject).child(date).child("Quiz_Topic").get().val()
    Question1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Question").get().val()
    Question2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Question").get().val()
    Question3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Question").get().val()
    Question4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Question").get().val()
    Question5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Question").get().val()

    type1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Type").get().val()
    type2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Type").get().val()
    type3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Type").get().val()
    type4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Type").get().val()
    type5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Type").get().val()

    Answer1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Answer").get().val()
    Answer2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Answer").get().val()
    Answer3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Answer").get().val()
    Answer4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Answer").get().val()
    Answer5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Answer").get().val()

    Option1in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option1").get().val()
    Option1in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option2").get().val()
    Option1in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option3").get().val()

    Option2in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option1").get().val()
    Option2in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option2").get().val()
    Option2in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option3").get().val()

    Option3in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option1").get().val()
    Option3in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option2").get().val()
    Option3in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option3").get().val()

    Option4in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option1").get().val()
    Option4in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option2").get().val()
    Option4in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option3").get().val()

    Option5in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option1").get().val()
    Option5in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option2").get().val()
    Option5in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option3").get().val()

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    print (listSection)
    context = {
        "t":True,
        "error":False,
        "title":"Marlin: Update Quiz",
        "quizform":QuizInfoForm(),
        "form":QuizInfoForm(),
        "Item_form1":ItemNum1_InfoForm(),
        "Tralse_form1":TF1(),
        "Tralse_form2":TF2(),
        "email": request.session['email'],
        "section":section,
        "listSection":listSection,
        "topic":topic,
        "sub":subject,
        "q1":Question1,
        "q2":Question2,
        "q3":Question3,
        "q4":Question4,
        "q5":Question5,
        "t1":type1,
        "t2":type2,
        "t3":type3,
        "t4":type4,
        "t5":type5,
        "A1":Answer1,
        "A2":Answer2,
        "A3":Answer3,
        "A4":Answer4,
        "A5":Answer5,
        "subject":subject,
        "date":date,
        # first 3 options
        "Option1in1":Option1in1,
        "Option1in2":Option1in2,
        "Option1in3":Option1in3,
        # second 3
        "Option2in1":Option2in1,
        "Option2in2":Option2in2,
        "Option2in3":Option2in3,
        # third 3
        "Option3in1":Option4in1,
        "Option3in2":Option4in2,
        "Option3in3":Option4in3,
        # fourth 3
        "Option4in1":Option4in1,
        "Option4in2":Option4in2,
        "Option4in3":Option4in3,
        # fifth 3
        "Option5in1":Option5in1,
        "Option5in2":Option5in2,
        "Option5in3":Option5in3,
    }
    return render(request,"EditQuiz.html",context)


def Home1(request,section,subject,date):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    topic = database.child("quiz").child(section).child(subject).child(date).child("Quiz_Topic").get().val()
    Question1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Question").get().val()
    Question2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Question").get().val()
    Question3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Question").get().val()
    Question4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Question").get().val()
    Question5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Question").get().val()

    type1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Type").get().val()
    type2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Type").get().val()
    type3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Type").get().val()
    type4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Type").get().val()
    type5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Type").get().val()

    Answer1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Answer").get().val()
    Answer2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Answer").get().val()
    Answer3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Answer").get().val()
    Answer4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Answer").get().val()
    Answer5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Answer").get().val()

    Option1in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option1").get().val()
    Option1in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option2").get().val()
    Option1in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option3").get().val()

    Option2in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option1").get().val()
    Option2in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option2").get().val()
    Option2in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option3").get().val()

    Option3in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option1").get().val()
    Option3in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option2").get().val()
    Option3in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option3").get().val()

    Option4in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option1").get().val()
    Option4in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option2").get().val()
    Option4in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option3").get().val()

    Option5in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option1").get().val()
    Option5in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option2").get().val()
    Option5in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option3").get().val()

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    print (listSection)
    context = {
        "t":True,
        "error":False,
        "title":"Marlin: Update Quiz",
        "form":QuizInfoForm(),
        "Item_form1":ItemNum1_InfoForm(),
        "Tralse_form1":TF1(),
        "Tralse_form2":TF2(),
        "email": request.session['email'],
        "section":section,
        "listSection":listSection,
        "topic":topic,
        "q1":Question1,
        "q2":Question2,
        "q3":Question3,
        "q4":Question4,
        "q5":Question5,
        "t1":type1,
        "t2":type2,
        "t3":type3,
        "t4":type4,
        "t5":type5,
        "A1":Answer1,
        "A2":Answer2,
        "A3":Answer3,
        "A4":Answer4,
        "A5":Answer5,
        "subject":subject,
        "date":date,
        # first 3 options
        "Option1in1":Option1in1,
        "Option1in2":Option1in2,
        "Option1in3":Option1in3,
        # second 3
        "Option2in1":Option2in1,
        "Option2in2":Option2in2,
        "Option2in3":Option2in3,
        # third 3
        "Option3in1":Option4in1,
        "Option3in2":Option4in2,
        "Option3in3":Option4in3,
        # fourth 3
        "Option4in1":Option4in1,
        "Option4in2":Option4in2,
        "Option4in3":Option4in3,
        # fifth 3
        "Option5in1":Option5in1,
        "Option5in2":Option5in2,
        "Option5in3":Option5in3,
    }
    return render(request,"EditQuiz.html",context)

def DeleteQuiz(request,section,subject,date):
    database.child("quiz").child(section).child(subject).child(date).remove()
    row = quizes.objects.all().filter(Quiz_Date__contains=date).filter(sections__contains=section).filter(subjects__contains=subject).delete()
    # return HttpResponse("hi")
    return HttpResponseRedirect('/marlin/History')

def ItemView(request,section,subject,date,item):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")
    lis_id = database.child("users").shallow().get().val()
    question = database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).child('Question').get().val()
    Qtype = database.child("quiz").child(section).child(subject).child(date).child("Items").child(item).child('Type').get().val()
    Topic = database.child("quiz").child(section).child(subject).child(date).child('Quiz_Topic').get().val()

    fname = []
    lname = []
    C1 = []
    C2 = []
    ctr = 0
    ctr_students = 0
    Names = database.child('quiz').child(section).child(subject).child(date).child("Quiz_Topic").get().val()

    for i in lis_id:
        sections = database.child("users").child(i).child("Details").child("Classes").child(section).get().val()
        # print (sections)
        if sections is not None:
            if database.child("users").child(i).child('Details').child("Type").get().val() == "Student":
                ctr = 0
                fname.append(database.child("users").child(i).child('Details').child("Student_Fname").get().val())
                lname.append(database.child("users").child(i).child('Details').child("Student_Lname").get().val())

                listofdismissed = database.child('Dismiss_Record').child(section).child(subject).child(date).child(i).child(item).shallow().get().val()
                answer1 = database.child('Answer').child(section).child(subject).child(date).child(i).child(item).child("Answer").get().val()
                Oanswer1 = database.child('quiz').child(section).child(subject).child(date).child("Items").child(item).child("Answer").get().val()
                if listofdismissed is None:
                    C1.append(0)
                else:
                    print(i)
                    for n in listofdismissed:
                        ctr = ctr + 1
                    C1.append(ctr)
                if answer1 is None:
                    C2.append('-')
                else:
                    if answer1.lower() == Oanswer1.lower():
                        C2.append('0')
                    elif answer1 is not Oanswer1:
                        C2.append('1')

    # fullname = zip(fname,lname,C1,C2,C3,C4,C5)
    name = zip(fname,lname,C1,C2)
    print(datetime.now().strftime('%H:%M'))

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    context = {
        "t":True,
        "email": request.session['email'],
        "date":date,
        "item":item,
        # "user":fullname,
        "names":name,
        "question":question,
        "title":"Marlin: Item View",
        "Qtype":Qtype,
        "Topic":Topic,
        "Dismissed":sum(C1),
        "section":request.session['section'],
        "sections":section,
        "subject":subject,
        "listSection":listSection,

    }


    return render(request,"statistics_students.html",context)
    # print (item)
    # print (date)
    # return HttpResponse(date)


def StatsOfAllItems(request,section,subject,date):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")
    lis_id = database.child("users").shallow().get().val()
    myDate = datetime.now()
    fname = []
    lname = []
    quid = []
    C1 = []
    C2 = []
    C3 = []
    C4 = []
    C5 = []
    Names = database.child('quiz').child(section).child(subject).child(date).child("Quiz_Topic").get().val()


    for i in lis_id:
        sections = database.child("users").child(i).child("Details").child("Classes").child(section).get().val()
        print (sections)
        if sections is not None:
            if database.child("users").child(i).child('Details').child("Type").get().val() == "Student":
                quid.append(i)

    quid.sort(reverse=True)
    for i in quid:
        fname.append(database.child("users").child(i).child('Details').child("Student_Fname").get().val())
        lname.append(database.child("users").child(i).child('Details').child("Student_Lname").get().val())
        Item1 = database.child("Answer").child(section).child(subject).child(date).child(i).child("Item1").child("Answer").get().val()
        Item2 = database.child("Answer").child(section).child(subject).child(date).child(i).child("Item2").child("Answer").get().val()
        Item3 = database.child("Answer").child(section).child(subject).child(date).child(i).child("Item3").child("Answer").get().val()
        Item4 = database.child("Answer").child(section).child(subject).child(date).child(i).child("Item4").child("Answer").get().val()
        Item5 = database.child("Answer").child(section).child(subject).child(date).child(i).child("Item5").child("Answer").get().val()

        Answer1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Answer").get().val()
        Answer2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Answer").get().val()
        Answer3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Answer").get().val()
        Answer4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Answer").get().val()
        Answer5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Answer").get().val()

        if Item1 is not None:
            if Item1 == Answer1:
                C1.append("1")
            elif Item1 != Answer1:
                C1.append("0")
        else:
            C1.append("2")

        if Item2 is not None:
            if Item2 == Answer2:
                C2.append("1")
                print(1)
            elif Item2 != Answer2:
                C2.append("0")
        else:
            C2.append("2")

        if Item3 is not None:
            if Item3 == Answer3:
                print(1)
                C3.append("1")
            elif Item3 != Answer3:
                C3.append("0")
        else:
            C3.append("2")

        if Item4 is not None:
            if Item4 == Answer4:
                C4.append("1")
            elif Item4 != Answer4:
                C4.append("0")
        else :
            C4.append("2")

        if Item5 is not None:
            if Item5 == Answer5:
                print(1)
                C5.append("1")
            elif Item5 != Answer5:
                C5.append("0")
        else:
            C5.append("2")


    fullname = zip(fname,lname,C1,C2,C3,C4,C5)
    name = zip(fname,lname)

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    context = {
        "t":True,
        "email": request.session['email'],
        "title":"Marlin: Item Statistics",
        "date":date,
        "user":fullname,
        "names":Names,
        "section":section,
        "subject":subject,
        "sections":request.session['section'],
        "listSection":listSection,
        "dates":myDate,

    }

    return render(request,"tallyofstudents.html",context)
    # return HttpResponse("hi")
    

def Graphs(request,item,subject,date):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        # print("Yes")
        None

    Name = database.child('quiz').child(item).child(subject).child(date).child("Quiz_Topic").get().val()
    item1 = database.child('quiz').child(item).child(subject).child(date).child("Items").child("Item1").child("Question").get().val()
    item2 = database.child('quiz').child(item).child(subject).child(date).child("Items").child("Item2").child("Question").get().val()
    item3 = database.child('quiz').child(item).child(subject).child(date).child("Items").child("Item3").child("Question").get().val()
    item4 = database.child('quiz').child(item).child(subject).child(date).child("Items").child("Item4").child("Question").get().val()
    item5 = database.child('quiz').child(item).child(subject).child(date).child("Items").child("Item5").child("Question").get().val()
    t1_ctr = 0
    ctr = 0
    t1_ans = 0
    print (item1)
    listUserItem1 = 0
    listUserItem2 = 0
    listUserItem3 = 0
    listUserItem4 = 0
    listUserItem5 = 0

    totalUn1 = 0
    totalUn2 = 0
    totalUn3 = 0
    totalUn4 = 0
    totalUn5 = 0

    CorrectAns1 = 0
    CorrectAns2 = 0
    CorrectAns3 = 0
    CorrectAns4 = 0
    CorrectAns5 = 0

    NotCorrectAns1 = 0
    NotCorrectAns2 = 0
    NotCorrectAns3 = 0
    NotCorrectAns4 = 0
    NotCorrectAns5 = 0

    dis1 = 0
    dis2 = 0
    dis3 = 0
    dis4 = 0
    dis5 = 0

    # print( database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item1").child("Question").get().val())
    if database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item1").child("Question").get().val() is not None:
        ctr = ctr +1
    if database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item2").child("Question").get().val() is not None:
        ctr = ctr +1
    if database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item3").child("Question").get().val() is not None:
        ctr = ctr +1
    if database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item4").child("Question").get().val() is not None:
        ctr = ctr +1
    if database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item5").child("Question").get().val() is not None:
        ctr = ctr +1

    list_users = database.child("users").shallow().get().val()
    for i in list_users:
        sections = database.child("users").child(i).child("Details").child("Classes").child(item).get().val()
        if sections is not None:
            if database.child("users").child(i).child("Details").child("Type").get().val() == 'Student':
                listAnswer1 = database.child("Answer").child(item).child(subject).child(date).child(i).child("Item1").child("Answer").get().val()
                listAnswer2 = database.child("Answer").child(item).child(subject).child(date).child(i).child("Item2").child("Answer").get().val()
                listAnswer3 = database.child("Answer").child(item).child(subject).child(date).child(i).child("Item3").child("Answer").get().val()
                listAnswer4 = database.child("Answer").child(item).child(subject).child(date).child(i).child("Item4").child("Answer").get().val()
                listAnswer5 = database.child("Answer").child(item).child(subject).child(date).child(i).child("Item5").child("Answer").get().val()

                TrueAnswer1 = database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item1").child("Answer").get().val()
                TrueAnswer2 = database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item2").child("Answer").get().val()
                TrueAnswer3 = database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item3").child("Answer").get().val()
                TrueAnswer4 = database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item4").child("Answer").get().val()
                TrueAnswer5 = database.child("quiz").child(item).child(subject).child(date).child("Items").child("Item5").child("Answer").get().val()

                dimissed1 = database.child("Dismiss_Record").child(item).child(subject).child(date).child(i).child("Item1").shallow().get().val()
                dimissed2 = database.child("Dismiss_Record").child(item).child(subject).child(date).child(i).child("Item2").shallow().get().val()
                dimissed3 = database.child("Dismiss_Record").child(item).child(subject).child(date).child(i).child("Item3").shallow().get().val()
                dimissed4 = database.child("Dismiss_Record").child(item).child(subject).child(date).child(i).child("Item4").shallow().get().val()
                dimissed5 = database.child("Dismiss_Record").child(item).child(subject).child(date).child(i).child("Item5").shallow().get().val()

                if listAnswer1 is not None:
                    listUserItem1 = listUserItem1 +1
                    if TrueAnswer1.lower() == listAnswer1.lower():
                        CorrectAns1 = CorrectAns1 +1
                    else:
                        NotCorrectAns1 = NotCorrectAns1 + 1
                else:
                    totalUn1 = totalUn1 + 1
                if listAnswer2 is not None:
                    listUserItem2 = listUserItem2 +1
                    if TrueAnswer2.lower() == listAnswer2.lower():
                        CorrectAns2 = CorrectAns2 +1
                    else:
                        NotCorrectAns2 = NotCorrectAns2 + 1
                else:
                    totalUn2 = totalUn2 + 1
                if listAnswer3 is not None:
                    listUserItem3 = listUserItem3 +1
                    if TrueAnswer3.lower() == listAnswer3.lower():
                        CorrectAns3 = CorrectAns3 +1
                    else:
                        NotCorrectAns3 = NotCorrectAns3 + 1
                else:
                    totalUn3 = totalUn3 + 1
                if listAnswer4 is not None:
                    listUserItem4 = listUserItem4 +1
                    if TrueAnswer4.lower() == listAnswer4.lower():
                        CorrectAns4 = CorrectAns4 +1
                    else:
                        NotCorrectAns4 = NotCorrectAns4 + 1
                else:
                    totalUn4 = totalUn4 + 1

                if listAnswer5 is not None:
                    listUserItem5 = listUserItem5 +1
                    if TrueAnswer5.lower() == listAnswer5.lower():
                        CorrectAns5 = CorrectAns5 +1
                    else:
                        NotCorrectAns5 = NotCorrectAns5 + 1
                else:
                    totalUn5 = totalUn5 + 1

                if dimissed1 is not None:
                    for q in dimissed1:
                        dis1 = dis1 +1
                if dimissed2 is not None:
                    for q in dimissed2:
                        dis2 = dis2 +1
                if dimissed3 is not None:
                    for q in dimissed3:
                        dis3 = dis3 +1
                if dimissed4 is not None:
                    for q in dimissed4:
                        dis4 = dis4 +1
                if dimissed5 is not None:
                    for q in dimissed5:
                        dis5 = dis5 +1


    answered = t1_ctr - t1_ans

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    context = {
        "t":True,
        "ctr":ctr,
        "email": request.session['email'],
        "title":"Marlin: Item Statistics",
        "Name":Name,
        "item1":item1,
        "item2":item2,
        "item3":item3,
        "item4":item4,
        "item5":item5,
        "date":date,
        "list1":listUserItem1,
        "list2":listUserItem2,
        "list3":listUserItem3,
        "list4":listUserItem4,
        "list5":listUserItem5,
        "Ulist1": totalUn1,
        "Ulist2": totalUn2,
        "Ulist3": totalUn3,
        "Ulist4": totalUn4,
        "Ulist5": totalUn5,
        "dimissed1": dis1,
        "dimissed2": dis2,
        "dimissed3": dis3,
        "dimissed4": dis4,
        "dimissed5": dis5,
        "CorrectAns1":CorrectAns1,
        "CorrectAns2":CorrectAns2,
        "CorrectAns3":CorrectAns3,
        "CorrectAns4":CorrectAns4,
        "CorrectAns5":CorrectAns5,
        "NotCorrectAns1":NotCorrectAns1,
        "NotCorrectAns2":NotCorrectAns2,
        "NotCorrectAns3":NotCorrectAns3,
        "NotCorrectAns4":NotCorrectAns4,
        "NotCorrectAns5":NotCorrectAns5,
        "section":item,
        "subject":subject,
        "date":date,
        "sections":request.session['section'],
        "listSection":listSection,
    }

    # return render(request,"statistics.html",context)
    return render(request,"statistics.html",context)

def ClassList(request,sections):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        # print("Yes")
        None
    
    AC = True

    l_Accounts = accounts.objects.all().filter(section__contains=sections).order_by("Lname").filter(UserType__contains="S")
    if not l_Accounts:
        AC = False

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)
    context = {
        "t":True,
        "accounts":l_Accounts,
        "email":request.session['email'],
        "section":sections,
        "title":"Marlin: Classlist",
        "sections":request.session['section'],
        "listSection":listSection,
        "AC":AC,
    }

    return render(request,"classlist.html",context)

def ListQuiz(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    # q_list = zip(quiz_list,Quiz_Topic)
    lq = quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11')
    lq1 = quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12')
    lq2 = quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13')
    lq3 = quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11')
    lq4 = quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1')

    myDate = datetime.now()

    paginator1 = Paginator(lq, 10) # Show 25 contacts per page
    paginator2 = Paginator(lq1, 10) # Show 25 contacts per page
    paginator3 = Paginator(lq2, 10) # Show 25 contacts per page
    paginator4 = Paginator(lq3, 10) # Show 25 contacts per page
    paginator5 = Paginator(lq4, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    page1 = request.GET.get('page1')
    page2 = request.GET.get('page2')
    page3 = request.GET.get('page3')
    page4 = request.GET.get('page4')

    contacts = paginator1.get_page(page)
    contacts1 = paginator2.get_page(page1)
    contacts2 = paginator3.get_page(page2)
    contacts3 = paginator4.get_page(page3)
    contacts4 = paginator5.get_page(page4)

    AC1 = True
    AC2 = True
    AC3 = True
    AC4 = True
    AC5 = True
    
    if not lq:
        AC1 = False
    if not lq1:
        AC2 = False
    if not lq2:
        AC3 = False
    if not lq3:
        AC4 = False
    if not lq4:
        AC5 = False


    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            listSection.append(i)

    context = {
        "title":"Marlin: Quiz History",
        "t":True,
        "email": request.session['email'],
        "date":contacts,
        "date1":contacts1,
        "date2":contacts2,
        "date3":contacts3,
        "date4":contacts4,
        "section":request.session['section'],
        "listSection":listSection,
        "dates":myDate,
        "AC1": AC1,
        "AC2": AC2,
        "AC3": AC3,
        "AC4": AC4,
        "AC5": AC5,
    }

    return render(request,"list.html",context)

def Search(request):
    All_Context = accounts.objects.all().order_by('Lname').filter(UserType__contains='s')
    context = {
        "form": UserForm(),
        "title":"Marlin: Search",
        "t":True,
        "email": request.session['email'],
        "all": All_Context,
    }
    return render(request,"Search.html",context)

def Result(request):
    text = request.POST.get('term')
    Section = request.POST.get('Student_Section')
    Subject = request.POST.get('Student_Subject')

    if text is not None:
        All_Context = accounts.objects.all().order_by('Lname').filter(UserType__contains='s').filter(Lname__contains=text)
    
    if Section != "" :
        All_Context = accounts.objects.all().order_by('Lname').filter(UserType__contains='s').filter(section__contains=Section)
        print(Section)

    if Subject != "":
        All_Context = accounts.objects.all().order_by('Lname').filter(UserType__contains='s').filter(subject__contains=Subject)
        print(Subject)
    
    if Section != "" and Subject != "":
        All_Context = accounts.objects.all().order_by('Lname').filter(UserType__contains='s').filter(subject__contains=Subject).filter(section__contains=Section)


    context = {
        "title":"Marlin: Search",
        "form": UserForm(),
        "t":True,
        "email": request.session['email'],
        "all": All_Context,
    }
    # return HttpResponse(Section)
    return render(request,"Search.html",context)


def AddUser(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    
    else:
        print("Yes")

    l_Accounts = accounts.objects.all().order_by('Lname').filter(section__contains="N1").filter(UserType__contains="S")
    l_Accounts1 = accounts.objects.all().order_by('Lname').filter(section__contains="ZC11").filter(UserType__contains="S")
    l_Accounts2 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT11").filter(UserType__contains="S")
    l_Accounts3 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT12").filter(UserType__contains="S")
    l_Accounts4 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT13").filter(UserType__contains="S")
    AC1 = True
    AC2 = True
    AC3 = True
    AC4 = True
    AC5 = True
    
    if not l_Accounts:
        AC1 = False
    if not l_Accounts1:
        AC2 = False
    if not l_Accounts2:
        AC3 = False
    if not l_Accounts3:
        AC4 = False
    if not l_Accounts4:
        AC5 = False

    listSection = []

    context = {
        "file":upload(),
        "t":True,
        "title":"Marlin: Students Accounts",
        "form": LoginForm(),
        "form2": UserForm(),
        "form3": PreferedTimeForm(),
        "email": request.session['email'],
        "fullname": l_Accounts,
        "fullname1": l_Accounts1,
        "fullname2": l_Accounts2,
        "fullname3": l_Accounts3,
        "fullname4": l_Accounts4,
        "section":request.session['section'],
        # "listSection":listSection,
        "error":False,
        "AC1": AC1,
        "AC2": AC2,
        "AC3": AC3,
        "AC4": AC4,
        "AC5": AC5,
    }
    return render(request,"create_acc.html",context)

def AddUserTeacher(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    list_Accounts = accounts.objects.all().filter(UserType__contains="T")

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    context = {
        "t":True,
        "form": LoginForm(),
        "title":"Marlin: Add Instructor Account",
        "Sec":TeacherForm(),
        "list_Accounts":list_Accounts,
        "form2": UserForm(),
        "form3": PreferedTimeForm(),
        "email": request.session['email'],
        "section":request.session['section'],
        "listSection":listSection,
        "title":"Marlin: Instructor Account"
    }
    return render(request,"create_acc_teacher.html",context)

def InsertUser(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    email = request.POST.get('email')
    passw = request.POST.get('password')
    Student_Age = request.POST.get('Student_Age')
    Student_Fname = request.POST.get('Student_Fname')
    Student_Lname = request.POST.get('Student_Lname')
    preferedTime1 = request.POST.get('preferedTime1')
    preferedTime2 = request.POST.get('preferedTime2')
    preferedTime3 = request.POST.get('preferedTime3')
    preferedTime4 = request.POST.get('preferedTime4')
    preferedTime5 = request.POST.get('preferedTime5')
    Student_Section = request.POST.get('Student_Section')
    Student_Subject = request.POST.get('Student_Subject')


    try:
        user = authed.create_user_with_email_and_password(email,passw)
    except:
        message = "Email was taken or Weak Password!!"
        list_Accounts = accounts.objects.all().filter(UserType__contains="T")

        l_Accounts = accounts.objects.all().order_by('Lname').filter(section__contains="N1").filter(UserType__contains="S")
        l_Accounts1 = accounts.objects.all().order_by('Lname').filter(section__contains="ZC11").filter(UserType__contains="S")
        l_Accounts2 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT11").filter(UserType__contains="S")
        l_Accounts3 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT12").filter(UserType__contains="S")
        l_Accounts4 = accounts.objects.all().order_by('Lname').filter(section__contains="ZT13").filter(UserType__contains="S")
        AC1 = True
        AC2 = True
        AC3 = True
        AC4 = True
        AC5 = True
        
        if not l_Accounts:
            AC1 = False
        if not l_Accounts1:
            AC2 = False
        if not l_Accounts2:
            AC3 = False
        if not l_Accounts3:
            AC4 = False
        if not l_Accounts4:
            AC5 = False

        
        listSection = []

        context = {
            "file":upload(),
            "t":True,
            "title":"Marlin: Students Accounts",
            "form": LoginForm(),
            "form2": UserForm(),
            "form3": PreferedTimeForm(),
            "email": request.session['email'],
            "fullname": l_Accounts,
            "fullname1": l_Accounts1,
            "fullname2": l_Accounts2,
            "fullname3": l_Accounts3,
            "fullname4": l_Accounts4,
            "section":request.session['section'],
            # "listSection":listSection,
            "error":False,
            "AC1": AC1,
            "AC2": AC2,
            "AC3": AC3,
            "AC4": AC4,
            "AC5": AC5,
            "error": True,
            "msg": "Weak Password or email has been taken"
        }
        return render(request,"create_acc.html",context)

        return render(request,"create_acc.html",context)
    uid = user['localId']

    #initial data from the student
    data = {'Student_Fname':Student_Fname,'Student_Lname':Student_Lname,'Student_Age':Student_Age,'Type':'Student'}
    data_time = {'preferedTime1':preferedTime1,'preferedTime2':preferedTime2,'preferedTime3':preferedTime3,'preferedTime4':preferedTime4,'preferedTime5':preferedTime5}
    database.child("users").child(uid).child("Details").set(data)
    database.child("users").child(uid).child("Details").child('Prefered Time').set(data_time)
    #class of the p
    section =  {'Subject_Code':Student_Subject}
    database.child("users").child(uid).child("Details").child('Classes').child(Student_Section).set(section)

    listUsers = database.child("users").shallow().get().val()
    usersList = []
    sections = ''
    for i in listUsers:
        if database.child("users").child(i).child('Details').child("Type").get().val() == "Student":
            usersList.append(i)

    for a in usersList:
        if database.child("users").child(a).child('Details').child("Type").get().val() == "Student":
            if accounts.objects.filter(UserToken__contains=a):
                None
            else:
                fname = database.child("users").child(a).child('Details').child("Student_Fname").get().val()
                lname = database.child("users").child(a).child('Details').child("Student_Lname").get().val()
                sec = database.child("users").child(a).child('Details').child("Classes").shallow().get().val()
                for s in sec:
                    sections = s
                # sec =
                l = accounts(UserToken=a,UserType="S",Fname=fname,Lname=lname,section=sections)
                l.save()


    return HttpResponseRedirect('/marlin/AddUser/')

def Logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/marlin/login')

def Home(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    # q_list = zip(quiz_list,Quiz_Topic)
    data = QuizData()
    data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
    data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
    data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
    data.If_Empty_Data()

    sec = []
    if request.session['type'] == "Teacher":
        lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
        for o in lists:
            sec.append(o)

    listSection = []

    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
        for i in secs:
            request.session['section'] = i
            listSection.append(i)

    print (listSection)
    context = {
        "t":True,
        "error":False,
        "title":"Marlin: Quiz Creation",
        "date":data.contacts,
        "date1":data.contacts1,
        "date2":data.contacts2,
        "date3":data.contacts3,
        "date4":data.contacts4,
        "form":QuizInfoForm(),
        "Item_form1":ItemNum1_InfoForm(),
        "Item_form2":ItemNum2_InfoForm(),
        "Item_form3":ItemNum3_InfoForm(),
        "Item_form4":ItemNum4_InfoForm(),
        "Item_form5":ItemNum5_InfoForm(),
        "Identity_form1":Identity1(),
        "Identity_form2":Identity2(),
        "Identity_form3":Identity3(),
        "Identity_form4":Identity4(),
        "Identity_form5":Identity5(),
        "Mutlitple_form1":Multiple1(),
        "Mutlitple_form2":Multiple2(),
        "Mutlitple_form3":Multiple3(),
        "Mutlitple_form4":Multiple4(),
        "Mutlitple_form5":Multiple5(),
        "Tralse_form1":TF1(),
        "Tralse_form2":TF2(),
        "Tralse_form3":TF3(),
        "Tralse_form4":TF4(),
        "Tralse_form5":TF5(),
        "email": request.session['email'],
        "section":sec,
        "listSection":listSection,
        "AC1": data.AC1,
        "AC2": data.AC2,
        "AC3": data.AC3,
        "AC4": data.AC4,
        "AC5": data.AC5,
    }
    return render(request,"quiz_form.html",context)

def InsertQuiz(request):
    try:
        request.session['email']
    except KeyError:
        print("No")
        return HttpResponseRedirect('/marlin/login')    

    else:
        print("Yes")

    Quiz_Date = request.POST.get('Quiz_Date')
    Quiz_Topic = request.POST.get('Quiz_Topic')
    Subject = request.POST.get('Subjects')
    if request.session['type'] == "Admin":
        Section = request.POST.get('Sections')
    else:
        Section = request.POST.get('section')

    ctr = 0
    print (Section)
    ItemNum1_1 = request.POST.get('ItemNum1_1')
    ItemNum1_2 = request.POST.get('ItemNum1_2')
    ItemNum1_3 = request.POST.get('ItemNum1_3')
    ItemNum1_4 = request.POST.get('ItemNum1_4')
    ItemNum1_5 = request.POST.get('ItemNum1_5')

    Tf_Question1 = request.POST.get('Tf_Question1')
    Tf_Question2 = request.POST.get('Tf_Question2')
    Tf_Question3 = request.POST.get('Tf_Question3')
    Tf_Question4 = request.POST.get('Tf_Question4')
    Tf_Question5 = request.POST.get('Tf_Question5')

    Tf_Answer1 = request.POST.get('Tf_Answer1')
    Tf_Answer2 = request.POST.get('Tf_Answer2')
    Tf_Answer3 = request.POST.get('Tf_Answer3')
    Tf_Answer4 = request.POST.get('Tf_Answer4')
    Tf_Answer5 = request.POST.get('Tf_Answer5')

    MultipleChoice_Question1 = request.POST.get('MultipleChoice_Question1')
    MultipleChoice_Question2 = request.POST.get('MultipleChoice_Question2')
    MultipleChoice_Question3 = request.POST.get('MultipleChoice_Question3')
    MultipleChoice_Question4 = request.POST.get('MultipleChoice_Question4')
    MultipleChoice_Question5 = request.POST.get('MultipleChoice_Question5')

    MultipleChoice_Option1_1 = request.POST.get('item1Op1')
    MultipleChoice_Option1_2 = request.POST.get('item1Op2')
    MultipleChoice_Option1_3 = request.POST.get('item1Op3')

    MultipleChoice_Option2_1 = request.POST.get('item2Op1')
    MultipleChoice_Option2_2 = request.POST.get('item2Op2')
    MultipleChoice_Option2_3 = request.POST.get('item2Op3')

    MultipleChoice_Option3_1 = request.POST.get('item3Op1')
    MultipleChoice_Option3_2 = request.POST.get('item3Op2')
    MultipleChoice_Option3_3 = request.POST.get('item3Op3')

    MultipleChoice_Option4_1 = request.POST.get('item4Op1')
    MultipleChoice_Option4_2 = request.POST.get('item4Op2')
    MultipleChoice_Option4_3 = request.POST.get('item4Op3')

    MultipleChoice_Option5_1 = request.POST.get('item5Op1')
    MultipleChoice_Option5_2 = request.POST.get('item5Op2')
    MultipleChoice_Option5_3 = request.POST.get('item5Op3')

    MultipleChoice_Answer5 = request.POST.get('optradio5')
    MultipleChoice_Answer4 = request.POST.get('optradio4')
    MultipleChoice_Answer3 = request.POST.get('optradio3')
    MultipleChoice_Answer2 = request.POST.get('optradio2')
    MultipleChoice_Answer1 = request.POST.get('optradio1')

    IdentNum1_1 = request.POST.get('IdentNum1_1')
    IdentNum1_2 = request.POST.get('IdentNum1_2')
    IdentNum1_3 = request.POST.get('IdentNum1_3')
    IdentNum1_4 = request.POST.get('IdentNum1_4')
    IdentNum1_5 = request.POST.get('IdentNum1_5')

    IdentAnswer_1 = request.POST.get('IdentAnswer_1')
    IdentAnswer_2 = request.POST.get('IdentAnswer_2')
    IdentAnswer_3 = request.POST.get('IdentAnswer_3')
    IdentAnswer_4 = request.POST.get('IdentAnswer_4')
    IdentAnswer_5 = request.POST.get('IdentAnswer_5')


    if ItemNum1_1 == 'I':
        if IdentNum1_1 ==  "" or IdentAnswer_1 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item1 = {'Question':IdentNum1_1,'Answer':IdentAnswer_1.lower(),'Type':'I'}
            ctr = ctr + 1

    elif ItemNum1_1 == 'M':
        if MultipleChoice_Question1 ==  "" or MultipleChoice_Answer1 == None or MultipleChoice_Option1_1 == "" or MultipleChoice_Option1_2 == "" or  MultipleChoice_Option1_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item1 = {'Question':MultipleChoice_Question1,'Answer':MultipleChoice_Answer1,'Option1':MultipleChoice_Option1_1,'Option2':MultipleChoice_Option1_2,'Option3':MultipleChoice_Option1_3,'Type':'MC'}
            ctr = ctr + 1

    elif ItemNum1_1 == "T":
        if  Tf_Question1 ==  "" or Tf_Answer1 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item1 = {'Question':Tf_Question1,'Answer':Tf_Answer1,'Type':'TF'}
            ctr = ctr + 1

    if ItemNum1_2 == 'I':
        if IdentNum1_2 ==  "" or IdentAnswer_2 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item2 = {'Question':IdentNum1_2,'Answer':IdentAnswer_2.lower(),'Type':'I'}
            ctr = ctr + 1
    elif ItemNum1_2 == 'M':
        if MultipleChoice_Question2 ==  "" or MultipleChoice_Answer2 == None or MultipleChoice_Option2_1 == "" or MultipleChoice_Option2_2 == "" or  MultipleChoice_Option2_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item2 = {'Question':MultipleChoice_Question2,'Answer':MultipleChoice_Answer2,'Option1':MultipleChoice_Option2_1,'Option2':MultipleChoice_Option2_2,'Option3':MultipleChoice_Option2_3,'Type':'MC'}
            ctr = ctr + 1

    elif ItemNum1_2 == "T":
        if  Tf_Question2 ==  "" or Tf_Answer2 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item2 = {'Question':Tf_Question2,'Answer':Tf_Answer2,'Type':'TF'}
            ctr = ctr + 1

    if ItemNum1_3 == 'I':
        if IdentNum1_3 ==  "" or IdentAnswer_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item3 = {'Question':IdentNum1_3,'Answer':IdentAnswer_3.lower(),'Type':'I'}
            ctr = ctr + 1
    elif ItemNum1_3 == 'M':
        if MultipleChoice_Question3 ==  "" or MultipleChoice_Answer3 == None or MultipleChoice_Option3_1 == "" or MultipleChoice_Option3_2 == "" or  MultipleChoice_Option3_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item3 = {'Question':MultipleChoice_Question3,'Answer':MultipleChoice_Answer3,'Option1':MultipleChoice_Option3_1,'Option2':MultipleChoice_Option3_2,'Option3':MultipleChoice_Option3_3,'Type':'MC'}
            ctr = ctr + 1
    elif ItemNum1_3 == "T":
        if  Tf_Question3 ==  "" or Tf_Answer3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item3 = {'Question':Tf_Question3,'Answer':Tf_Answer3,'Type':'TF'}
            ctr = ctr + 1

    if ItemNum1_4 == 'I':
        if IdentNum1_4 ==  "" or IdentAnswer_4 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item4 = {'Question':IdentNum1_4,'Answer':IdentAnswer_4.lower(),'Type':'I'}
            ctr = ctr + 1
    elif ItemNum1_4 == 'M':
        if MultipleChoice_Question4 ==  "" or MultipleChoice_Answer4 == None or MultipleChoice_Option4_1 == "" or MultipleChoice_Option4_2 == "" or  MultipleChoice_Option4_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item4 = {'Question':MultipleChoice_Question4,'Answer':MultipleChoice_Answer4,'Option1':MultipleChoice_Option4_1,'Option2':MultipleChoice_Option4_2,'Option3':MultipleChoice_Option4_3,'Type':'MC'}
            ctr = ctr + 1
    elif ItemNum1_4 == "T":
        if  Tf_Question4 ==  "" or Tf_Answer4 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item4 = {'Question':Tf_Question4,'Answer':Tf_Answer4,'Type':'TF'}
            ctr = ctr + 1

    if ItemNum1_5 == 'I':
        if IdentNum1_5 ==  "" or IdentAnswer_5 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item5 = {'Question':IdentNum1_5,'Answer':IdentAnswer_5.lower(),'Type':'I'}
            ctr = ctr + 1
    elif ItemNum1_5 == 'M':
        if MultipleChoice_Question5 ==  "" or MultipleChoice_Answer5 == None or MultipleChoice_Option5_1 == "" or MultipleChoice_Option5_2 == "" or  MultipleChoice_Option5_3 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item5 = {'Question':MultipleChoice_Question5,'Answer':MultipleChoice_Answer5,'Option1':MultipleChoice_Option5_1,'Option2':MultipleChoice_Option5_2,'Option3':MultipleChoice_Option5_3,'Type':'MC'}
            ctr = ctr + 1
    elif ItemNum1_5 == "T":
        if  Tf_Question5 ==  "" or Tf_Answer5 == "":
            data = QuizData()
            data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
            data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
            data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
            data.If_Empty_Data()

            sec = []
            if request.session['type'] == "Teacher":
                lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                for o in lists:
                    sec.append(o)

            listSection = []

            if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                for i in secs:
                    request.session['section'] = i
                    listSection.append(i)

            print (listSection)
            context = {
                "t":True,
                "error":False,
                "title":"Marlin: Quiz Creation",
                "date":data.contacts,
                "date1":data.contacts1,
                "date2":data.contacts2,
                "date3":data.contacts3,
                "date4":data.contacts4,
                "form":QuizInfoForm(),
                "Item_form1":ItemNum1_InfoForm(),
                "Item_form2":ItemNum2_InfoForm(),
                "Item_form3":ItemNum3_InfoForm(),
                "Item_form4":ItemNum4_InfoForm(),
                "Item_form5":ItemNum5_InfoForm(),
                "Identity_form1":Identity1(),
                "Identity_form2":Identity2(),
                "Identity_form3":Identity3(),
                "Identity_form4":Identity4(),
                "Identity_form5":Identity5(),
                "Mutlitple_form1":Multiple1(),
                "Mutlitple_form2":Multiple2(),
                "Mutlitple_form3":Multiple3(),
                "Mutlitple_form4":Multiple4(),
                "Mutlitple_form5":Multiple5(),
                "Tralse_form1":TF1(),
                "Tralse_form2":TF2(),
                "Tralse_form3":TF3(),
                "Tralse_form4":TF4(),
                "Tralse_form5":TF5(),
                "email": request.session['email'],
                "section":sec,
                "listSection":listSection,
                "error":True,
                "AC1": data.AC1,
                "AC2": data.AC2,
                "AC3": data.AC3,
                "AC4": data.AC4,
                "AC5": data.AC5,
                "msg":"Some of the Items are blank or have been forgotten to fill out",
            }
            return render(request,"quiz_form.html",context)
        else:
            item5 = {'Question':Tf_Question5,'Answer':Tf_Answer5,'Type':'TF'}
            ctr = ctr + 1

    print (ctr)

    now = datetime.now()
    if Quiz_Date <= now.strftime("%Y-%m-%d"):
        data = QuizData()
        data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
        data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
        data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
        data.If_Empty_Data()

        sec = []
        if request.session['type'] == "Teacher":
            lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
            for o in lists:
                sec.append(o)

        listSection = []

        if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
            secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
            for i in secs:
                request.session['section'] = i
                listSection.append(i)

        print (listSection)
        context = {
            "t":True,
            "error":False,
            "title":"Marlin: Quiz Creation",
            "date":data.contacts,
            "date1":data.contacts1,
            "date2":data.contacts2,
            "date3":data.contacts3,
            "date4":data.contacts4,
            "form":QuizInfoForm(),
            "Item_form1":ItemNum1_InfoForm(),
            "Item_form2":ItemNum2_InfoForm(),
            "Item_form3":ItemNum3_InfoForm(),
            "Item_form4":ItemNum4_InfoForm(),
            "Item_form5":ItemNum5_InfoForm(),
            "Identity_form1":Identity1(),
            "Identity_form2":Identity2(),
            "Identity_form3":Identity3(),
            "Identity_form4":Identity4(),
            "Identity_form5":Identity5(),
            "Mutlitple_form1":Multiple1(),
            "Mutlitple_form2":Multiple2(),
            "Mutlitple_form3":Multiple3(),
            "Mutlitple_form4":Multiple4(),
            "Mutlitple_form5":Multiple5(),
            "Tralse_form1":TF1(),
            "Tralse_form2":TF2(),
            "Tralse_form3":TF3(),
            "Tralse_form4":TF4(),
            "Tralse_form5":TF5(),
            "email": request.session['email'],
            "section":sec,
            "listSection":listSection,
            "error":True,
            "AC1": data.AC1,
            "AC2": data.AC2,
            "AC3": data.AC3,
            "AC4": data.AC4,
            "AC5": data.AC5,
            "msg":"Quizzes must be prepared prior to the class discussion!!",
        }
        return render(request,"quiz_form.html",context)

    # if Quiz_Date == database
    quiz = database.child("quiz").shallow().get().val()
    quiz1 = database.child("quiz").shallow().get().val()

    for sec1 in quiz:
        subject1 = database.child("quiz").child(sec1).shallow().get().val()
        for sub1 in subject1:
            dates1 = database.child("quiz").child(sec1).child(sub1).shallow().get().val()
            for date1 in dates1:
                if Quiz_Date == date1 and Section == sec1:
                    data = QuizData()
                
                    data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
                    data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
                    data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
                    data.If_Empty_Data()

                    sec = []
                    if request.session['type'] == "Teacher":
                        lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
                        for o in lists:
                            sec.append(o)

                    listSection = []

                    if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
                        secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
                        for i in secs:
                            request.session['section'] = i
                            listSection.append(i)

                    print (listSection)
                    context = {
                        "t":True,
                        "error":False,
                        "title":"Marlin: Quiz Creation",
                        "date":data.contacts,
                        "date1":data.contacts1,
                        "date2":data.contacts2,
                        "date3":data.contacts3,
                        "date4":data.contacts4,
                        "form":QuizInfoForm(),
                        "Item_form1":ItemNum1_InfoForm(),
                        "Item_form2":ItemNum2_InfoForm(),
                        "Item_form3":ItemNum3_InfoForm(),
                        "Item_form4":ItemNum4_InfoForm(),
                        "Item_form5":ItemNum5_InfoForm(),
                        "Identity_form1":Identity1(),
                        "Identity_form2":Identity2(),
                        "Identity_form3":Identity3(),
                        "Identity_form4":Identity4(),
                        "Identity_form5":Identity5(),
                        "Mutlitple_form1":Multiple1(),
                        "Mutlitple_form2":Multiple2(),
                        "Mutlitple_form3":Multiple3(),
                        "Mutlitple_form4":Multiple4(),
                        "Mutlitple_form5":Multiple5(),
                        "Tralse_form1":TF1(),
                        "Tralse_form2":TF2(),
                        "Tralse_form3":TF3(),
                        "Tralse_form4":TF4(),
                        "Tralse_form5":TF5(),
                        "email": request.session['email'],
                        "section":sec,
                        "listSection":listSection,
                        "error":True,
                        "AC1": data.AC1,
                        "AC2": data.AC2,
                        "AC3": data.AC3,
                        "AC4": data.AC4,
                        "AC5": data.AC5,
                        "msg":" A quiz has already been prepared for that date. Please delete the quiz to be taken before creating a new one.",

                    }
                    return render(request,"quiz_form.html",context)


    if ctr == 5:
        data = {'Quiz_Topic':Quiz_Topic,'Quiz_Start_Time':'08:00','Quiz_End_Time':'00:00',"Quiz_Date":Quiz_Date}
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).set(data)
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).child('Items').child('Item1').set(item1)
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).child('Items').child('Item2').set(item2)
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).child('Items').child('Item3').set(item3)
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).child('Items').child('Item4').set(item4)
        database.child("quiz").child(Section).child(Subject).child(Quiz_Date).child('Items').child('Item5').set(item5)
    
    if ctr != 5:
        data = QuizData()
        data.Get_Data(quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT12'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZT13'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='ZC11'),quizes.objects.all().order_by('-Quiz_Date').filter(sections__contains='N1'))
        data.Get_Pages(request.GET.get('page'),request.GET.get('page1'),request.GET.get('page2'),request.GET.get('page3'),request.GET.get('page4'))
        data.Distribute_Data(Paginator(data.lq, 10),Paginator(data.lq1, 10),Paginator(data.lq2, 10),Paginator(data.lq3, 10),Paginator(data.lq4, 10))
        data.If_Empty_Data()

        sec = []
        if request.session['type'] == "Teacher":
            lists = database.child("users").child(request.session['local']).child("Details").child("Classes").shallow().get().val()
            for o in lists:
                sec.append(o)

        listSection = []

        if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
            secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
            for i in secs:
                request.session['section'] = i
                listSection.append(i)

        print (listSection)
        context = {
            "t":True,
            "error":False,
            "title":"Marlin: Quiz Creation",
            "date":data.contacts,
            "date1":data.contacts1,
            "date2":data.contacts2,
            "date3":data.contacts3,
            "date4":data.contacts4,
            "form":QuizInfoForm(),
            "Item_form1":ItemNum1_InfoForm(),
            "Item_form2":ItemNum2_InfoForm(),
            "Item_form3":ItemNum3_InfoForm(),
            "Item_form4":ItemNum4_InfoForm(),
            "Item_form5":ItemNum5_InfoForm(),
            "Identity_form1":Identity1(),
            "Identity_form2":Identity2(),
            "Identity_form3":Identity3(),
            "Identity_form4":Identity4(),
            "Identity_form5":Identity5(),
            "Mutlitple_form1":Multiple1(),
            "Mutlitple_form2":Multiple2(),
            "Mutlitple_form3":Multiple3(),
            "Mutlitple_form4":Multiple4(),
            "Mutlitple_form5":Multiple5(),
            "Tralse_form1":TF1(),
            "Tralse_form2":TF2(),
            "Tralse_form3":TF3(),
            "Tralse_form4":TF4(),
            "Tralse_form5":TF5(),
            "email": request.session['email'],
            "section":sec,
            "listSection":listSection,
            "error":True,
            "AC1": data.AC1,
            "AC2": data.AC2,
            "AC3": data.AC3,
            "AC4": data.AC4,
            "AC5": data.AC5,
            "msg":"Please complete the 5 item quiz form. Thank you.",

        }
        return render(request,"quiz_form.html",context)

    # for sec in quiz1:
    #     subject = database.child("quiz").child(sec).shallow().get().val()
    #     for sub in subject:
    #         dates = database.child("quiz").child(sec).child(sub).shallow().get().val()
    #         for date in dates:
    #             topic = database.child("quiz").child(sec).child(sub).child(date).child("Quiz_Topic").get().val()
    #             if quizes.objects.filter(Quiz_Date__contains=date).filter(sections__contains=sec):
    #                 print(sec, date)
    #             else:
    #                 l = quizes(Quiz_Date=date,Quiz_Topic=topic,sections=sec,subjects=sub)
    #                 l.save()

    l = quizes(Quiz_Date=Quiz_Date,Quiz_Topic=Quiz_Topic,sections=Section,subjects=Subject)
    l.save()
    return HttpResponseRedirect('/marlin/Quiz')
    # return HttpResponse(Section)

def UpdateTeacher(request,data):
    context = {
            "form": LoginForm(),
            "title":"Marlin: Edit Profile",
            "t":True,
            "Tform":TeacherForm,
            "data":data,
            "email": request.session['email'],
        }
    return render(request,"EditTeacher.html",context)

def UpdateDataTeacher(request,data):
    Teacher_Age = request.POST.get('Student_Age')
    Teacher_Fname = request.POST.get('Student_Fname')
    Teacher_Lname = request.POST.get('Student_Lname')
    Teacher_Section = request.POST.get('Sections')
    Teacher_Subject = request.POST.get('Student_Subject')

    print(Teacher_Subject)
    if Teacher_Age is None:
        None
    else:
        database.child('users').child(data).child("Details").update({"Teacher_Age": Teacher_Age})
    if Teacher_Fname is None:
        None
    else:
        database.child('users').child(data).child("Details").update({"Teacher_Fname": Teacher_Fname})
    if Teacher_Lname is None:
        None
    else:
        database.child('users').child(data).child("Details").update({"Teacher_Lname": Teacher_Lname})

    if database.child('users').child(data).child("Details").child("Type").get().val() == "Admin":
        if Teacher_Age == "" and Teacher_Lname == "":
            None
        else:
            request.session['fname'] = database.child("users").child(data).child("Details").child("Teacher_Fname").get().val()
            request.session['lname'] = database.child("users").child(data).child("Details").child("Teacher_Lname").get().val()
    else:
        if Teacher_Age is None and Teacher_Lname is None:
            None
        else:
            request.session['fname'] = database.child("users").child(data).child("Details").child("Teacher_Fname").get().val()
            request.session['lname'] = database.child("users").child(data).child("Details").child("Teacher_Lname").get().val()

    context = {
            "form": LoginForm(),
            "t":True,
            "Tform":TeacherForm,
            "data":data,
            "email": request.session['email'],
        }
    return render(request,"EditTeacher.html",context)


def resetpass(request,data):
    authed.send_password_reset_email(data)
    # return HttpResponseRedirect('/marlin/AddUserTeacher/')
    msg="Your request for password reset has been sent to your email."
    context = {
            "form": LoginForm(),
            "title":"Marlin: Edit Profile",
            "t":True,
            "Tform":TeacherForm,
            "data":data,
            "email": request.session['email'],
            "msg":msg,
            "error":True,
        }
    return render(request,"EditTeacher.html",context)



def ImserTeacher(request):
    email = request.POST.get('email')
    passw = request.POST.get('password')
    Teacher_Age = request.POST.get('Student_Age')
    Teacher_Fname = request.POST.get('Student_Fname')
    Teacher_Lname = request.POST.get('Student_Lname')
    Teacher_Section = request.POST.get('Sections')
    Student_Section = request.POST.get('Student_Section')
    Student_Subject = request.POST.get('Student_Subject')

    try:
        user = authed.create_user_with_email_and_password(email,passw)
        uid = user['localId']
    except:
        message = "Invalid Email or Weak Password!!"
        list_Accounts = accounts.objects.all().filter(UserType__contains="T")

        listSection = []

        if database.child("users").child(request.session['local']).child("Details").child("Type").get().val() == "Teacher":
            secs = database.child("users").child(request.session['local']).child("Details").child('Classes').shallow().get().val()
            for i in secs:
                request.session['section'] = i
                listSection.append(i)

            context = {
                "t":True,
                "form": LoginForm(),
                "Sec":TeacherForm(),
                "list_Accounts":list_Accounts,
                "form2": UserForm(),
                "form3": PreferedTimeForm(),
                "email": request.session['email'],
                "section":request.session['section'],
                "title":"Marlin: Instructor Account",
                "listSection":listSection,
                "error":True,
                "msg":message

            }
            return render(request,"create_acc_teacher.html",context)
    
        

    print(uid)
    data = {'Teacher_Fname':Teacher_Fname,'Teacher_Lname':Teacher_Lname,'Teacher_Age':Teacher_Age,'Type':'Teacher','Section':Teacher_Section,'Department':'DCS'}
    database.child("users").child(uid).child("Details").set(data)
    section =  {'Subject_Code':Student_Subject}
    database.child("users").child(uid).child("Details").child('Classes').child(Student_Section).set(section)


    listUsers = database.child("users").shallow().get().val()
    usersList = []
    sections = ''
    for i in listUsers:
        if database.child("users").child(i).child('Details').child("Type").get().val() == "Teacher":
            usersList.append(i)

    for a in usersList:
        if database.child("users").child(a).child('Details').child("Type").get().val() == "Teacher":
            if accounts.objects.filter(UserToken__contains=a):
                None
            else:
                fname = database.child("users").child(a).child('Details').child("Teacher_Fname").get().val()
                lname = database.child("users").child(a).child('Details').child("Teacher_Lname").get().val()
                sec = database.child("users").child(a).child('Details').child("Classes").shallow().get().val()
                for s in sec:
                    sections = s
                # sec =
                l = accounts(UserToken=a,UserType="T",Fname=fname,Lname=lname,section=sections)
                l.save()
    return HttpResponseRedirect('/marlin/AddUserTeacher/')

def SendRandomQuestion(request,date):
    lis_id = database.child("users").shallow().get().val()

    for i in lis_id:
        if database.child("users").child(i).child('Details').child("Type").get().val() == "Student":
            database.child('users').child(i).child('Details').child("Prefered Time").child('preferedTime1').set(datetime.datetime.now().strftime('%H:%M'))
    return HttpResponseRedirect('/marlin/Quiz/')


def UpdateQuizData(request,section,subject,date):
    top = request.POST.get('topic')
    sub = request.POST.get('sub')
    sec = request.POST.get('sec')
    date_1 = request.POST.get('dates')
    topic = database.child("quiz").child(section).child(subject).child(date).child(date).get().val()

    if topic != top :
        data={"Quiz_Topic":top}
        database.child("quiz").child(section).child(subject).child(date).update(data)
        row = quizes.objects.all().filter(sections__contains=section).filter(subjects__contains=subject).filter(Quiz_Date__contains=date).delete()
        l = quizes(Quiz_Date=date,Quiz_Topic=top,sections=section,subjects=subject)
        l.save()
    
    Question1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Question").get().val()
    Question2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Question").get().val()
    Question3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Question").get().val()
    Question4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Question").get().val()
    Question5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Question").get().val()

    type1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Type").get().val()
    type2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Type").get().val()
    type3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Type").get().val()
    type4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Type").get().val()
    type5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Type").get().val()

    Answer1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Answer").get().val()
    Answer2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Answer").get().val()
    Answer3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Answer").get().val()
    Answer4 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Answer").get().val()
    Answer5 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Answer").get().val()

    Option1in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option1").get().val()
    Option1in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option2").get().val()
    Option1in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item1").child("Option3").get().val()

    Option2in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option1").get().val()
    Option2in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option2").get().val()
    Option2in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item2").child("Option3").get().val()

    Option3in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option1").get().val()
    Option3in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option2").get().val()
    Option3in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item3").child("Option3").get().val()

    Option4in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option1").get().val()
    Option4in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option2").get().val()
    Option4in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item4").child("Option3").get().val()

    Option5in1 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option1").get().val()
    Option5in2 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option2").get().val()
    Option5in3 = database.child("quiz").child(section).child(subject).child(date).child("Items").child("Item5").child("Option3").get().val()

    if date != date_1:
        print("Rer")
        database.child("quiz").child(section).child(subject).child(date).remove()

        if type1 == "MC":
            item1 = {'Question':Question1,'Answer':Answer1,'Option1':Option1in1,'Option2':Option1in2,'Option3':Option1in3,'Type':'MC'}        
        else:
            item1 = {'Question':Question1,'Answer':Answer1,'Type':type1} 

        if type2 == "MC":
            item2 = {'Question':Question2,'Answer':Answer2,'Option1':Option2in1,'Option2':Option2in2,'Option3':Option2in3,'Type':'MC'}        
        else:
            item2 = {'Question':Question2,'Answer':Answer2,'Type':type2}
        
        if type3 == "MC":
            item3 = {'Question':Question3,'Answer':Answer3,'Option1':Option3in1,'Option2':Option3in2,'Option3':Option3in3,'Type':'MC'}        
        else:
            item3 = {'Question':Question3,'Answer':Answer3,'Type':type3}
        
        if type4 == "MC":
            item4 = {'Question':Question4,'Answer':Answer4,'Option1':Option4in1,'Option2':Option4in2,'Option3':Option4in3,'Type':'MC'}        
        else:
            item4 = {'Question':Question4,'Answer':Answer4,'Type':type4} 

        if type5 == "MC":
            item5 = {'Question':Question5,'Answer':Answer5,'Option1':Option5in1,'Option2':Option5in2,'Option3':Option5in3,'Type':'MC'}        
        else:
            item5 = {'Question':Question5,'Answer':Answer5,'Type':type5}

        data = {"Quiz_Topic":top,"Quiz_Date":date_1,"Quiz_End_Time":"00:00","Quiz_Start_Time":"08:00"}
        database.child("quiz").child(section).child(subject).child(date_1).set(data)
        database.child("quiz").child(section).child(subject).child(date_1).child('Items').child('Item1').set(item1)
        database.child("quiz").child(section).child(subject).child(date_1).child('Items').child('Item2').set(item2)
        database.child("quiz").child(section).child(subject).child(date_1).child('Items').child('Item3').set(item3)
        database.child("quiz").child(section).child(subject).child(date_1).child('Items').child('Item4').set(item4)
        database.child("quiz").child(section).child(subject).child(date_1).child('Items').child('Item5').set(item5)

        row = quizes.objects.all().filter(sections__contains=section).filter(subjects__contains=subject).filter(Quiz_Date__contains=date).delete()
        l = quizes(Quiz_Date=date_1,Quiz_Topic=top,sections=sec,subjects=sub)
        l.save()

    if subject != sub:
        print("Rer")
        database.child("quiz").child(section).child(subject).remove()

        if type1 == "MC":
            item1 = {'Question':Question1,'Answer':Answer1,'Option1':Option1in1,'Option2':Option1in2,'Option3':Option1in3,'Type':'MC'}        
        else:
            item1 = {'Question':Question1,'Answer':Answer1,'Type':type1} 

        if type2 == "MC":
            item2 = {'Question':Question2,'Answer':Answer2,'Option1':Option2in1,'Option2':Option2in2,'Option3':Option2in3,'Type':'MC'}        
        else:
            item2 = {'Question':Question2,'Answer':Answer2,'Type':type2}
        
        if type3 == "MC":
            item3 = {'Question':Question3,'Answer':Answer3,'Option1':Option3in1,'Option2':Option3in2,'Option3':Option3in3,'Type':'MC'}        
        else:
            item3 = {'Question':Question3,'Answer':Answer3,'Type':type3}
        
        if type4 == "MC":
            item4 = {'Question':Question4,'Answer':Answer4,'Option1':Option4in1,'Option2':Option4in2,'Option3':Option4in3,'Type':'MC'}        
        else:
            item4 = {'Question':Question4,'Answer':Answer4,'Type':type4} 

        if type5 == "MC":
            item5 = {'Question':Question5,'Answer':Answer5,'Option1':Option5in1,'Option2':Option5in2,'Option3':Option5in3,'Type':'MC'}        
        else:
            item5 = {'Question':Question5,'Answer':Answer5,'Type':type5}

        data = {"Quiz_Topic":top,"Quiz_Date":date_1,"Quiz_End_Time":"00:00","Quiz_Start_Time":"08:00"}
        database.child("quiz").child(section).child(sub).child(date_1).set(data)
        database.child("quiz").child(section).child(sub).child(date_1).child('Items').child('Item1').set(item1)
        database.child("quiz").child(section).child(sub).child(date_1).child('Items').child('Item2').set(item2)
        database.child("quiz").child(section).child(sub).child(date_1).child('Items').child('Item3').set(item3)
        database.child("quiz").child(section).child(sub).child(date_1).child('Items').child('Item4').set(item4)
        database.child("quiz").child(section).child(sub).child(date_1).child('Items').child('Item5').set(item5)

        row = quizes.objects.all().filter(sections__contains=section).filter(subjects__contains=subject).filter(Quiz_Date__contains=date).delete()
        l = quizes(Quiz_Date=date_1,Quiz_Topic=top,sections=sec,subjects=sub)
        l.save()

    if section != sec:
        print("Rer")
        database.child("quiz").child(section).child(subject).remove()

        if type1 == "MC":
            item1 = {'Question':Question1,'Answer':Answer1,'Option1':Option1in1,'Option2':Option1in2,'Option3':Option1in3,'Type':'MC'}        
        else:
            item1 = {'Question':Question1,'Answer':Answer1,'Type':type1} 

        if type2 == "MC":
            item2 = {'Question':Question2,'Answer':Answer2,'Option1':Option2in1,'Option2':Option2in2,'Option3':Option2in3,'Type':'MC'}        
        else:
            item2 = {'Question':Question2,'Answer':Answer2,'Type':type2}
        
        if type3 == "MC":
            item3 = {'Question':Question3,'Answer':Answer3,'Option1':Option3in1,'Option2':Option3in2,'Option3':Option3in3,'Type':'MC'}        
        else:
            item3 = {'Question':Question3,'Answer':Answer3,'Type':type3}
        
        if type4 == "MC":
            item4 = {'Question':Question4,'Answer':Answer4,'Option1':Option4in1,'Option2':Option4in2,'Option3':Option4in3,'Type':'MC'}        
        else:
            item4 = {'Question':Question4,'Answer':Answer4,'Type':type4} 

        if type5 == "MC":
            item5 = {'Question':Question5,'Answer':Answer5,'Option1':Option5in1,'Option2':Option5in2,'Option3':Option5in3,'Type':'MC'}        
        else:
            item5 = {'Question':Question5,'Answer':Answer5,'Type':type5}

        data = {"Quiz_Topic":top,"Quiz_Date":date_1,"Quiz_End_Time":"00:00","Quiz_Start_Time":"08:00"}
        database.child("quiz").child(sec).child(sub).child(date_1).set(data)
        database.child("quiz").child(sec).child(sub).child(date_1).child('Items').child('Item1').set(item1)
        database.child("quiz").child(sec).child(sub).child(date_1).child('Items').child('Item2').set(item2)
        database.child("quiz").child(sec).child(sub).child(date_1).child('Items').child('Item3').set(item3)
        database.child("quiz").child(sec).child(sub).child(date_1).child('Items').child('Item4').set(item4)
        database.child("quiz").child(sec).child(sub).child(date_1).child('Items').child('Item5').set(item5)

        row = quizes.objects.all().filter(sections__contains=section).filter(subjects__contains=subject).filter(Quiz_Date__contains=date).delete()
        l = quizes(Quiz_Date=date_1,Quiz_Topic=top,sections=sec,subjects=sub)
        l.save()
    
    return HttpResponseRedirect('/marlin/History/')
    
