from django.conf.urls.defaults import *
from django.contrib.auth.views import login
import views

urlpatterns = patterns('',
	(r'^$', views.index),
	(r'^login$', 'app.views.user_login'),
	(r'^registrer/$', 'app.views.register'),
	#url(r'^winner/$', 'app.views.get_winner'),
	url(r'^take/(?P<phonenumber>[\w-]+)/$', 'app.views.check_user'), #  quiz/
	url(r'^take/(?P<phonenumber>[\w-]+)$', 'app.views.check_user'), #  quiz
	url(r'^(?P<phonenumber>[\w-]+)/taken/$', 'app.views.quiz_taken'), #  quiz/take/
	url(r'^(?P<phonenumber>[\w-]+)/taken$', 'app.views.quiz_taken'), #  quiz/take
)