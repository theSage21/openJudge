from django.test import TestCase
from question import models

def create_question():
    q=models.Question()
    q.title='qwe'
    return q
def create_profile():
    u=models.User()
    u.username='asd'
    p=models.Profile()
    p.user=u
    return p
def create_answer_type():
    t=models.AnswerType()
    t.name='answer_type1'
    return t
def create_answer():
    a=models.Answer()
    a.question=create_question()
    a.question_number=0
    a.answer_type=create_answer_type()
    return a
def create_language():
    l=models.Language()
    l.name='asd'
    return l

class ProfileTest(TestCase):    
    def test_str_function(self):
        p=create_profile()
        self.assertEqual(type(p.__str__()),type(''))
class LanguageTest(models.Model):
    def test_str_function(self):
        l=create_language()
        self.assertEqual(l.name,l.__str__())
class AttemptTest(TestCase):
    def test_str_function(self)
        a=models.Attempt()
        a.question=create_question()
        a.player=create_profile()
        self.assertEqual(a.__str__(),q.__str__()+' - '+p.__str__())
class QuestionTest(TestCase):
    def test_str_function(self)
        q=create_question()
        self.assertEqual(q.__str__(),q.title)
    def test_get_score(self)
class AnswerTest(TestCase):
    def test_str_function(self)
        a=create_answer()
        self.assertEqual(a.__str__(),a.question.__str__())
class AnswerTest(TestCase):
    def test_str_function(self)
        t=create_answer_type()
        self.assertEqual(t.__str__(),t.name)
class LanguageTest(TestCase):
    def test_str_function(self):
        l=models.Language()
        l.name='language1'
        self.assertEqual(l.__str__(),l.name)
