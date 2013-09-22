import re
from django.db import models
from django.contrib.auth.models import User



class Quiz(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
	url = models.CharField(max_length=10)
	random_order = models.BooleanField()
	numnber_of_question = models.IntegerField()

	def save(self, force_insert=False, force_update=False):
		self.url = self.url.replace(' ', '-').lower()
		super(Quiz, self).save(force_insert, force_update)

	class Meta:
		verbose_name = 'Quiz'

	def __unicode__(self):
		return self.title


# class Participant(models.Model):
# 	firstname = models.CharField(max_length=20)
# 	lastname = models.CharField(max_length=20)
# 	email = models.EmailField(unique=True)
# 	phonenumber = models.CharField(max_length=8)
#
# 	def __unicode__(self):
# 		return (self.firstname + ' ' + self.lastname)


class Question(models.Model):

	quiz = models.ManyToManyField(Quiz, blank = True)
	content = models.TextField(max_length=300, verbose_name='Question')

	class Meta:
		verbose_name = "Question"

	def __unicode__(self):
		return self.content

class Answer(models.Model):
	question = models.ForeignKey(Question)
	answer = models.TextField(max_length=300)
	is_correct = models.BooleanField(verbose_name='Is correct')

	def __unicode__(self):
		return self.answer


#class ResultManager(models.Manager):
	#def new_result(self, user, score):
	#	new_result = self.create(user=user, score=score)
	#	if self.score > 7:
	#		self.valid = True
	#	else:
	#		False
	#	return new_result



class SittingManager(models.Manager):

	def new_sitting(self, user, quiz):
		if quiz.random_order:
			question_set = quiz.question_set.all().order_by('?')
		else:
			question_set = quiz.question_set.all()

		questions = []
		number_of_question = quiz.numnber_of_question
		for question in question_set:
			questions.append(str(question.id))

		while len(questions) > number_of_question:
			questions.pop

		questions_list = ','.join(questions)

		new_sitting = self.create(user=user, quiz=quiz,
		                          question_list=questions_list, current_score =0, complete=False)
		new_sitting.save()
		return new_sitting


class Sitting(models.Model):
	user = models.ForeignKey('auth.User')
	quiz = models.ForeignKey(Quiz)
	question_list = models.TextField()
	current_score = models.IntegerField(default=0)
	complete = models.BooleanField(default=False)
	objects = SittingManager()

	def add_score(self, points):
		self.current_score = points
		self.save()

	def get_current_score(self):
		return self.current_score

	def mark_quiz_complete(self):
		self.complete = True
		self.save()

	def get_question_list(self):
		return self.question_list
