from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    departmentName = models.CharField(verbose_name="Department Name", max_length=150)

    def __str__(self):
        return "{0}".format(self.departmentName)


class Course(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    courseId = models.CharField(max_length=15,verbose_name="Course Id")
    courseName = models.CharField(max_length=150,verbose_name="Course Name")
    semester = models.IntegerField(default= 1)
    subject =  models.ManyToManyField('Subject')

    def __str__(self):
        return ("{0}".format(self.courseName))

class Subject(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False)
    semester = models.IntegerField(default=5)

    def __str__(self):
        return str(self.name)


class Principle(models.Model):
    name = models.CharField(verbose_name="Principle",max_length=150)

    def __str__(self):
        return str(self.principle_name)

class Teacher(models.Model):
    fname = models.CharField(max_length=50, blank=False)
    lname = models.CharField(max_length=50, blank=False)
    subject = models.ManyToManyField(Subject, related_name="subject_teachers")

    def __str__(self):
        return str(self.fname) + " " + str(self.lname)

class TIC(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    tic_name = models.CharField(max_length=120, verbose_name="Teacher Name")

    def __str__(self):
        return "{0}".format(self.tic_name)


class Student(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    semester = models.IntegerField(default= 1)
    studentId = models.CharField(max_length=20,verbose_name="Roll Number")
    fname = models.CharField(max_length=120, verbose_name="First Name")
    lname = models.CharField(max_length=120, verbose_name="Last Name")
    mname = models.CharField(max_length=120, verbose_name="Middle Name",blank=True)

    def __str__(self):
        return "{0}".format(self.studentId)

class QuestionMaster(models.Model):
    question_text = models.CharField(max_length=250,verbose_name="Question")

    def __str__(self):
        return "{0}".format(self.question_text)

class Feedback(models.Model):
    username = models.CharField(max_length=150,verbose_name="User Name")
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    semester = models.IntegerField(default= 1)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    feedbackId = models.IntegerField(default=0)
    avg_rating = models.FloatField(default=0.0)
    def __str__(self):
        return "{0}".format(self.feedbackId)

class Feedback_data(models.Model):
    department = models.ForeignKey(Department,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    semester = models.IntegerField(default= 1)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    value_1 = models.FloatField(default=0.0)
    value_2 = models.FloatField(default=0.0)
    value_3 = models.FloatField(default=0.0)
    value_4 = models.FloatField(default=0.0)
    value_5 = models.FloatField(default=0.0)
    value_6 = models.FloatField(default=0.0)
    value_7 = models.FloatField(default=0.0)
    value_8 = models.FloatField(default=0.0)
    value_9 = models.FloatField(default=0.0)
    value_10 = models.FloatField(default=0.0)
    value_11 = models.FloatField(default=0.0)
    value_12 = models.FloatField(default=0.0)
    value_13 = models.FloatField(default=0.0)
    value_14 = models.FloatField(default=0.0)

    avg_rating = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)

    def __str__(self):
        return "{0}".format(self.count)


class UserProfile(models.Model):
    userId = models.CharField(max_length=50,
                               verbose_name= "User Id")
    loginId = models.CharField(max_length=50,
                               verbose_name= "Login Id")
    password = models.CharField(max_length=50,
                                verbose_name="Password")
    role = models.CharField(max_length=50,
                            verbose_name="Role")
    firstName = models.CharField(max_length=100,
                                 verbose_name="First Name")
    lastName = models.CharField(max_length=100,
                                verbose_name="Last Name")
    middleName = models.CharField(max_length=100,
                                  verbose_name="Middle Name",blank=True)

    salutation = models.CharField(max_length=50,
                                  verbose_name="Salutation",blank=True)


    def __str__(self):
        return (("{0}"+" "+"{1}").format(self.firstName,self.lastName))






