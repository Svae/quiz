from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',
	(r'^$', views.index),
	#(r'^login/$', 'app.views.login'),
	#(r'^register/$', 'app.views.register'),
	url(r'^(?P<quiz_name>[\w-]+)/$', 'app.views.quiz_take'), #  quiz/
	url(r'^(?P<quiz_name>[\w-]+)$', 'app.views.quiz_take'), #  quiz
	url(r'^(?P<quiz_name>[\w-]+)/taken/$', 'app.views.quiz_taken'), #  quiz/take/
	url(r'^(?P<quiz_name>[\w-]+)taken$', 'app.views.quiz_take'), #  quiz/take
)