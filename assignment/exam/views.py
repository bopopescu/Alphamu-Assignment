from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from exam.models import *

from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser


def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))

    return db


class Home(ListView):
    model = Questions
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):

        """ connect to Mysql """
        db_config = read_db_config()
        db = None
        try:
            db = MySQLConnection(**db_config)
            if db.is_connected():
                cursor = db.cursor()
                query = "select questions.id, questions.question_text, answers.answer_text from questions join answers on (answers.id=questions.answer_id);"
                cursor.execute(query)
                questions_objs = cursor.fetchall()

                return render(request, self.template_name, {'questions_objs': questions_objs})
        except Error as e:
            print(e)
            return render(request, self.template_name)
        finally:
            if db is not None and db.is_connected():
                db.close()


class Add(CreateView):
    model = Questions
    template_name = "add.html"
    fields = ('question_text',)

    def post(self, request, *args, **kwargs):
        question_text = self.request.POST['question_text']
        answer_text = self.request.POST['answer_text']

        """ connect to Mysql """
        db_config = read_db_config()
        db = None
        try:
            db = MySQLConnection(**db_config)
            if db.is_connected():
                cursor = db.cursor()

                answer_insert_query = "insert into answers (answer_text) values ('%s')" % (answer_text)
                cursor.execute(answer_insert_query)
                answer_id = cursor.lastrowid
                db.commit()

                question_insert_query = "insert into questions (question_text, answer_id) values ('%s', %s)" % (question_text, answer_id)
                cursor.execute(question_insert_query)
                db.commit()

                return redirect(reverse('home'))
        except Error as e:
            print(e)
            return render(request, self.template_name)
        finally:
            if db is not None and db.is_connected():
                db.close()


class Edit(UpdateView):
    model = Questions
    template_name = "edit.html"

    def get(self, request, *args, **kwargs):
        question_id = self.kwargs['pk']

        """ connect to Mysql """
        db_config = read_db_config()
        db = None
        try:
            db = MySQLConnection(**db_config)
            if db.is_connected():
                cursor = db.cursor()
                query = "select questions.question_text, answers.answer_text from questions join answers on (questions.answer_id = answers.id) where questions.id = %s" % (question_id)
                cursor.execute(query)
                exam_obj = cursor.fetchone()

                return render(request, self.template_name, {'exam_obj': exam_obj})
        except Error as e:
            print(e)
            return render(request, self.template_name)
        finally:
            if db is not None and db.is_connected():
                db.close()

    def post(self, request, *args, **kwargs):
        question_id = self.kwargs['pk']
        question_text = self.request.POST['question_text']
        answer_text = self.request.POST['answer_text']

        """ connect to Mysql """
        db_config = read_db_config()
        db = None
        try:
            db = MySQLConnection(**db_config)
            if db.is_connected():
                cursor = db.cursor()

                query = "UPDATE questions, answers SET questions.question_text = '%s', answers.answer_text = '%s' where questions.id = %s and answers.id = questions.answer_id" % (question_text, answer_text, question_id)
                cursor.execute(query)
                db.commit()

                return redirect(reverse('home'))
        except Error as e:
            print(e)
            return render(request, self.template_name)
        finally:
            if db is not None and db.is_connected():
                db.close()


class Delete(DeleteView):
    model = Questions
    template_name = 'home.html'

    def delete(self, request, *args, **kwargs):
        question_id = self.kwargs['pk']

        """ connect to Mysql """
        db_config = read_db_config()
        db = None
        try:
            db = MySQLConnection(**db_config)
            if db.is_connected():
                cursor = db.cursor()

                query = "DELETE answers, questions FROM answers left join questions on (answers.id = questions.answer_id) WHERE questions.id = %s" % (question_id)
                cursor.execute(query)
                db.commit()

                return redirect(reverse('home'))
        except Error as e:
            print(e)
            return render(request, self.template_name)
        finally:
            if db is not None and db.is_connected():
                db.close()
