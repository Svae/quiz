
from django.shortcuts import render_to_response, redirect
from forms import RegistrationForm, LoginForm
from django.template import RequestContext
from models import *

from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


def index(request):
	return render_to_response('app.html')

def user_login(request):
	if request.method == 'GET':
		form = LoginForm(request.GET)
		if form.is_valid():
			information = form.cleaned_data
			epost = information['epost']
			new_user = authenticate(username=epost, password=epost)
			login(request, new_user)
			return render_to_response('registration_complete.html')
	else:
		form = LoginForm()
	return render_to_response('login.html', {'form': form})


def register(request):
	if request.method == 'GET':
		form = RegistrationForm(request.GET)
		if form.is_valid():
			information = form.cleaned_data
			fornavn = information['fornavn']
			etternavn = information['etternavn']
			epost = information['epost']
			new_user = User.objects.create_user(epost, epost, epost)
			new_user.first_name = fornavn
			new_user.last_name = etternavn
			new_user.is_active = True
			new_user.save()
			new_user = authenticate(username=epost, password=epost)
			login(request, new_user)

			return render_to_response('registration_complete.html',
			                          {'fornavn':fornavn, 'etternavn':etternavn, 'epost':epost},
			                          context_instance=RequestContext(request))
	else:
		form = RegistrationForm()
	return render_to_response('registration.html', {'form':form})


def quiz_take(request,quiz_name):
	if request.user.is_authenticated():
		quiz = Quiz.objects.get(url=quiz_name.lower())

		try:
			sitting = Sitting.objects.get(user=request.user, quiz=quiz)
		#if sitting.complete:
		#	index(request)
		#else:
			return user_load_question(request, sitting, quiz)
		except Sitting.DoesNotExist:
			sitting = Sitting.objects.new_sitting(request.user, quiz)
			return user_load_question(request, sitting, quiz)
		except Sitting.MultipleObjectsReturned:
			sitting = Sitting.objects.get(user=request.user, quiz=quiz, complete=False)[0]
			return user_load_question(request, sitting, quiz)

	print(1123)
	return index(request)


def quiz_taken(request, quiz_name):
	quiz = Quiz.objects.get(url=quiz_name.lower())
	if request.user.is_authenticated():  #  logged in user
		try:
			sitting = Sitting.objects.get(user=request.user,
			                              quiz=quiz,
			                              complete=False,
			                              )
		except Sitting.DoesNotExist:
			sitting = Sitting.objects.new_sitting(request.user, quiz)
	score = score_for_quiz(request, quiz_name)
	sitting.add_score(score)
	sitting.mark_quiz_complete()
	return render_to_response('take/result.html', {'quiz':quiz_name}, context_instance = RequestContext(request))


def score_for_quiz(request, quiz_name):
	points = 0
	for answer in request.GET.values():
		try:
			id = answer.encode('ascii')
			if Answer.objects.get(id=id).is_correct:
				points += 1
		except Answer.DoesNotExist:
			quiz_take(request, quiz_name)
	return points


def user_load_question(request, sitting, quiz):
	question_list = get_question_list(sitting)
	return render_to_response('take/question.html', {'quiz':quiz, 'questions':question_list},
	                          context_instance=RequestContext(request))


def get_question_list(sitting):
	questions = sitting.question_list
	question_list = questions.split(",")
	question_array = []
	for question in question_list:
		q_id = int(question)
		question_array.append(Question.objects.get(id=q_id))
	return question_array


