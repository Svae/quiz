from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import *
from django import forms


# class QuestionInLine(admin.TabularInline):
# 	model = Question.quiz.through
# 	filter_horizontal = ('content',)


class AnswerInLine(admin.TabularInline):
	model = Answer


class QuizAdminForm(forms.ModelForm):
	question = forms.ModelMultipleChoiceField(queryset=Question.objects.all(),
	                                          required=False,
	                                          widget=FilteredSelectMultiple(verbose_name='Questions', is_stacked=False))

	def __init__(self, *args, **kwargs):
		super(QuizAdminForm, self).__init__(*args, **kwargs)
		if self.instance.pk:
			self.fields['question'].inital = self.instance.question_set.all()

	def save(self, commit=True):
		quiz = super(QuizAdminForm, self).save(commit=False)
		if commit:
			quiz.save()
		if quiz.pk:
			quiz.question_set = self.cleaned_data['questions']
			self.save_m2m()
		return quiz


class QuizAdmin(admin.ModelAdmin):
	form = QuizAdminForm
	list_display = ('title', )
	list_filter = ('title',)
	search_fields = ('description', )


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('content', )
	fields = ('content', 'quiz',)
	filter_horizontal = ('quiz', )
	inlines = [AnswerInLine]


#class ParticipantAdmin(admin.ModelAdmin):
	#list_display = ('firstname', 'lastname', 'email', 'phonenumber')
	#search_fields = ('firstname', 'lastname',  'phonenumber','email',)


class AnswerAdmin(ModelAdmin):
	list_display = ('question', 'answer', 'is_correct')


class SittingAdmin(admin.ModelAdmin):
	search_fields = ('user', 'admin')
	list_display = ('user', 'current_score')


admin.site.register(Quiz, QuizAdmin)
#admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Sitting, SittingAdmin)
#admin.site.register(Result, ResultAdmin)

