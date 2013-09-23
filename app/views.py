
from django.shortcuts import render_to_response
from forms import RegistrationForm, LoginForm
from django.template import RequestContext
from models import *

from django import forms
from django.http import HttpResponseRedirect


def index(request):
	return render_to_response('app.html')

def user_login(request):
	if request.method == 'GET':
		form = LoginForm(request.GET)
		print("hei")
		if form.is_valid():
			information = form.cleaned_data
			phonenumber = information['phonenumber']
			sitting = check_sitting(phonenumber)
			if sitting:
				return user_load_question(sitting)
			else:
				return render_to_response('app.html')
	else:
		form = LoginForm()
	return render_to_response('login.html', {'form': form})

#def toQuiz(request):



def register(request):
	if request.method == 'GET':
		form = RegistrationForm(request.GET)
		if form.is_valid():
			information = form.cleaned_data
			name = information['name']
			email = information['email']
			phonenumber = information['phonenumber']
			quiz = Quiz.objects.get(title='test')
			sitting = Sitting.objects.create(name=name, email=email, phonenumber=phonenumber, quiz=quiz)
			sitting.add_quiz()
			sitting.create_questions()
			print(sitting.questions)
			return user_load_question(sitting)
	else:
		form = RegistrationForm()
	return render_to_response('registration.html', {'form':form})

def check_sitting(phonenumber):
	try:
		sitting = Sitting.objects.get(phonenumber=phonenumber)
		return sitting
	except Sitting.DoesNotExist:
		return
	except Sitting.MultipleObjectsReturned:
		try:
			sitting = Sitting.objects.get(phonenumber=phonenumber)[0]
			return sitting
		except Sitting.DoesNotExist:
			return
	return

def check_user(phonenumber):
	sitting = check_sitting(phonenumber)
	if sitting:
		user_load_question(sitting)
	else:
		form = LoginForm
		return render_to_response('login.html', {'form': form})



def quiz_taken(request, phonenumber):
	sitting = check_sitting(phonenumber)
	print("inn")
	if sitting:
		score = score_for_quiz(request, sitting)
		sitting.add_score(score)
		answers = update_user_answers(request, sitting)
		sitting.update_answers(answers)
	print("riktig")
	return render_to_response('take/result.html')


def score_for_quiz(request, sitting):
	score = 0
	for answer in request.GET.values():
		try:
			id = answer.encode('ascii')
			if Answer.objects.get(id=id).is_correct:
				score += 1
		except Answer.DoesNotExist:
			user_load_question(sitting)
	return score

def update_user_answers(request, sitting):
	answers = []
	for answer in request.GET.values():
		try:
			id = answer.encode('ascii')
			if Answer.objects.get(id=id):
				answers.append(id)
		except Answer.DoesNotExist:
			user_load_question(sitting)
	return answers

def user_load_question(sitting):
	quiz = sitting.quiz
	all_questions = sitting.questions.split(",")
	answers = sitting.get_answers()
	questions = []
	for question in all_questions:
		try:
			questions.append(Question.objects.get(id=str(question)))
		except Question.DoesNotExist:
			print("ops")
	print(questions)
	return render_to_response('take/question.html', {'quiz': quiz, 'questions': questions, 'answers': answers, 'sitting': sitting},)


def get_question_list(sitting):
	questions = sitting.get_questions(sitting)
	question_array = []
	for question in questions:
		question_array.append(Question.objects.get(id=int(question)))
	return question_array


# def get_winner(quiz_name):
# 	quiz = Quiz.objects.get(url='itdagene')
# 	threshold = quiz.numnber_of_question
# 	participants = Sitting.objects.filter(quiz=quiz)
# 	valid = []
# 	for participant in participants:
# 		print(3312)
# 		if participant.get_current_score() > (threshold/2):
# 			valid.append(participant.user.first_name)
#
# 	return render_to_response('winner.html', {'winners':valid})
#
