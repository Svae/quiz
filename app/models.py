
from django.db import models



class Quiz(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=300)
	random_order = models.BooleanField()
	number_of_question = models.IntegerField()

	class Meta:
		verbose_name = 'Quiz'

	def __unicode__(self):
		return self.title


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



class Sitting(models.Model):
	name = models.TextField(max_length=300)
	email = models.EmailField()
	phonenumber = models.CharField(max_length=12, unique=True)
	answers = models.TextField(default="")
	quiz = models.ForeignKey(Quiz)
	questions = models.TextField(default="")
	score = models.IntegerField(default=0)

	def get_quiz(self):
		return self.quiz.title


	def get_score(self):
		return self.score


	def get_questions(self):
		return self.question_list.split(",")

	def get_answers(self):
		return self.answers.split(",")


	def add_score(self, points):
		self.score = points
		self.save()

	def add_quiz(self):
		self.quiz = Quiz.objects.get(title='itDAGENE')
		self.save()

	def update_answers(self, answers):
		self.answers = answers.split(",")
		self.save()

	def create_questions(self):
		all_questions = self.quiz.question_set.all()
		question_list = []
		for i in range(self.quiz.number_of_question):
			question = all_questions.pop()
			question_list.add(question.id)
		questions = question_list.join(",")
		self.questions =questions
		
		return question_list


	def add_answer(self, answer_id):
		temp = self.answers
		self.answers = temp + "," + str(answer_id)
		self.save()
		return self.answers

	def new_sitting(self, name, email, phonenumber):
		self.name = name
		self.email = email
		self.phonenumber = phonenumber
		self.questions = self.create_questions()
		self.quiz = Quiz.objects.get(title='itDAGENE')
		self.save()
		return self




