"""SP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^AddUser/', views.AddUser),
    url(r'^AddUserTeacher/', views.AddUserTeacher),
    url(r'^ClassList/(?P<sections>.*)/', views.ClassList),
    url(r'^Delete/(?P<data>.*)', views.DeleteStudent),
    url(r'^Deletes/(?P<data>.*)', views.DeleteProf),
    url(r'^InsertQuiz', views.InsertQuiz),
    url(r'^InsertUser/', views.InsertUser),
    url(r'^Search/', views.Search),
    url(r'^InsertUserTeacher/', views.ImserTeacher),
    url(r'^Items/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<item>.*)$', views.ItemView),
    # LogiHCI
    url(r'^login$', views.Login),
    url(r'^$', views.redirect),
    # Logo Session
    url(r'^Logout/$', views.Logout),
    # Login Backend
    url(r'^PostLogin', views.PostLogin),
    url(r'^Result', views.Result),
    #Quiz form
    url(r'^Quiz', views.Home),
    url(r'^UpdateQuiz/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})', views.Home1),
    url(r'^UpdateQuizData/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})', views.UpdateQuizData),
    url(r'^DeleteQuiz/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})', views.DeleteQuiz),
    url(r'^updateItem/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})/(?P<item>.*)/', views.updateItem),
    # quiz url
    # url(r'^QuizList/(?P<item>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})/$', views.Dates),
    url(r'^Graphs/(?P<item>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})/', views.Graphs),
    url(r'^StatsOfAllItems/(?P<section>.*)/(?P<subject>.*)/(?P<date>\d{4}-\d{2}-\d{2})/$', views.StatsOfAllItems),
    # url(r'^StatsOfAllItems/', views.StatsOfAllItems),
    url(r'^Send/(?P<date>\d{4}-\d{2}-\d{2})/$', views.SendRandomQuestion),
    url(r'^History/', views.ListQuiz),
    url(r'^UpdateTeacher/(?P<data>.*)', views.UpdateTeacher),
    url(r'^Upload/',views.Upload),
    url(r'^FeedBack/',views.FeedBack),
    url(r'^UpdateDataTeacher/(?P<data>.*)/',views.UpdateDataTeacher),
    url(r'^resetpass/(?P<data>.*)/',views.resetpass),
    url(r'^Profile/(?P<data>.*)/',views.Profile),
]
