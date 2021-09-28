from django.db import models

# Create your models here.
class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    firstname = models.CharField(max_length=1024)
    lastname = models.CharField(max_length=1024)
    username = models.CharField(max_length=1024)
    email = models.CharField(max_length=1024)
    idnumber = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.username} {self.idnumber} {self.firstname} {self.lastname} {self.email}"
    class Meta:
        managed = False
        db_table = 'mdl_user'

class QuizGrade(models.Model):
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, db_column='userid', related_name='grades', on_delete=models.CASCADE)
    grade = models.FloatField()
    timemodified = models.IntegerField()
    quiz = models.BigIntegerField()
    class Meta:
        managed = False
        db_table= 'mdl_quiz_grades'

    def __str__(self):
        return f"id:{self.id} grade:{self.grade} time:{self.timemodified}"

# class QuizAttempt(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     userid = models.ForeignKey(User, related_name='attempts', on_delete=models.CASCADE)
#     timestart = models.BigIntegerField()
#     timefinish = models.BigIntegerField()
#     class Meta:
#         managed = False
#         db_table = 'mdl_quiz_attempts'

class MoodleRouter:

#    instances = [User, QuizGrade, QuizAttempt]
    instances = [User, QuizGrade]

    def db_for_read(self, model, **hints):
        if model in self.instances:
            return 'moodle'
        return None

    def db_for_write(self, model, **hints):
        if model in self.instances:
            return 'moodle'
        return None

    def allow_relation(self, o1, o2, **hints):
        if type(o1) in self.instances and type(o2) in self.instances:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(f"Migration : {db} {app_label} {model_name}")
        if app_label == 'quiz':
            return db == 'moodle'
        return None