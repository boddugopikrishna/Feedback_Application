from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from .admin import QuestionMasterResource
import math
from .models import *
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(userId= request.user.username)
        print(user_profile.firstName)
        student = Student.objects.filter(studentId = request.user.username).values()
        semester = student[0]['semester']
        department = student[0]['department_id']
        subjects = Subject.objects.filter(semester = semester,department = department)
        teacher_list = []
        for subject in subjects:
            teacher = Teacher.objects.filter(subject = subject.id)
            teacher_list.append(teacher)

        combined_list = []
        for val in range(subjects.count()):
            feedback_object = Feedback.objects.filter(username = request.user.username,subject=subjects[val],teacher=teacher_list[val][0])
            if feedback_object:
                status = "Done"
            else:
                status = "Pending"
            print("Feedback object : {0} and status is {1}".format(feedback_object,status))
            combined_list.append((subjects[val],teacher_list[val][0],status))
        if request.method == "POST":
            for key in request.POST:
                if key.startswith('testname'):
                    pk = int(key[-1])
                    request.session['recordIndex'] = int(key[-1])
                    break
            return redirect('feedback')
        context = {'userName':user_profile.firstName,'subject_list': combined_list,}
        return render(request,'FeedbackApp/dashboard.html',context= context)
    else:
        return redirect('login')

@login_required
def logOut(request):
    logout(request)
    return redirect('login')

def logIn(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_profile = UserProfile.objects.filter(userId = username,password = password)
        if user_profile.count() != 0:
            role = " "
            for data in user_profile:
                role = data.role
            user_query = User.objects.filter(username = username)
            if user_query.count() == 0:
                user = User.objects.create_user(
                        username= username,
                        password= password
                        )
                user.save()

            else:
                user = User.objects.get(username = username)
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if role == "Student":
                    return redirect('index')
                elif role == "TIC":
                    return redirect('teacher_analytics')
                else:
                    return redirect('principle_analytics')
            else:
                return render(request,'FeedbackApp/login.html',{'i':'Incorrect Password/ User ID'})
        else:
            return render(request, 'FeedbackApp/login.html', {'i': 'Incorrect Password/ User ID'})
    return render(request, 'FeedbackApp/login.html', {'i': ''})

def teacher_analytics(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(userId=request.user.username)
        tic = TIC.objects.get(tic_name__contains = user_profile.values()[0]['firstName'])
        print("Teacher in Charge Name:{0} and his department:{1}".format(tic,tic.department))
        subjects = Subject.objects.filter(department = tic.department)
        teacher_list = []
        for subject in subjects:
            teacher = Teacher.objects.get(subject=subject.id)
            teacher_list.append(teacher)
        teachers = []
        for teacher in teacher_list:
            teachers.append(teacher)
        print(teacher_list)
        course_list = Course.objects.filter( department = tic.department)
        context = {
            'TicName' : tic,
            'subjects':subjects,
            'teachers':teachers,
            'course_list':course_list,
        }
        if request.method == "POST":
            subject = request.POST.get('Subjects')
            course = request.POST.get('Courses')
            teacher = request.POST.get('Teachers')
            # sessin variables to store data
            request.session['teacher_subject'] = subject
            request.session['teacher_course'] = course
            request.session['teacher_teacher'] = teacher

            return redirect('teacher_view')

    return render(request,'FeedbackApp/teacher_analytics.html',context = context)

def teacher_view(request):
    if request.user.is_authenticated:
        print(request.user.username)
        tic_profile = UserProfile.objects.get(userId = request.user.username)
        tic_object = TIC.objects.get(tic_name__contains = tic_profile.firstName)
        print(tic_object.department)
        subject = request.session['teacher_subject']
        course = request.session['teacher_course']
        teacher = request.session['teacher_teacher']
        department_object = Department.objects.get(departmentName__contains = tic_object.department)
        department_id = department_object.id
        if course == 'All':
            if subject != 'All':
                subject_object = Subject.objects.get(name__contains=subject)
                subject_id = subject_object.id
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],
                                                         lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id,subject = subject_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id,subject = subject_id)
            else:
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0], lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id)
        else:
            course_object = Course.objects.get(courseName__contains=course)
            course_id = course_object.id
            if subject != 'All':
                subject_object = Subject.objects.get(name__contains=subject)
                subject_id = subject_object.id
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                    subject=subject_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                subject=subject_id)
            else:
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id)

        context = {
            'department': department_object,
            'subject' : subject,
            'course' : course,
            'teacher' : teacher,
            'feedback_objects':feedback_objects,
        }
        if request.method == "POST":
            return redirect('teacher_analytics')
        return render(request, 'FeedbackApp/teacher_view.html', context=context)


def principle_analytics(request):
    if request.user.is_authenticated:
        principal_object = UserProfile.objects.get(userId = request.user.username)

        teachers = Teacher.objects.all()
        departments = Department.objects.all()
        courses = Course.objects.all()
        context = {
            'principle_name':principal_object.firstName,
            'teachers':teachers,
            'departments': departments,
            'courses' : courses
        }
        if request.POST:
            department = request.POST.get('Department')
            course = request.POST.get('courses')
            teachers = request.POST.get('Teachers')
            # sessin variables to store data
            request.session['department'] = department
            request.session['course'] = course
            request.session['teachers'] = teachers

            return redirect('analytics')
        else:
            return render(request,'FeedbackApp/principle_analytics.html',context = context)
        return render(request, 'FeedbackApp/principle_analytics.html', context=context)

def analytics(request):
    department = request.session['department']
    course = request.session['course']
    teacher = request.session['teachers']

    if department == 'All':
        if course != 'All':
            course_object = Course.objects.get(courseName__contains=course)
            course_id = course_object.id
            if teacher != 'All':
                teacher_list = teacher.split(" ")
                teacher_object = Teacher.objects.get(fname__contains=teacher_list[0], lname__contains=teacher_list[-1])
                teacher_id = teacher_object.id
                feedback_objects = Feedback_data.objects.filter(course=course_id,
                                                                teacher=teacher_id)
            else:
                feedback_objects = Feedback_data.objects.filter(course=course_id)
        else:
            if teacher != 'All':
                teacher_list = teacher.split(" ")
                teacher_object = Teacher.objects.get(fname__contains=teacher_list[0], lname__contains=teacher_list[-1])
                teacher_id = teacher_object.id
                feedback_objects = Feedback_data.objects.filter(teacher=teacher_id)
            else:
                feedback_objects = Feedback_data.objects.all()
    else:
        department_object = Department.objects.get(departmentName__contains=department)
        department_id = department_object.id
        if course != 'All':
            course_object = Course.objects.get(courseName__contains=course)
            course_id = course_object.id
            if teacher != 'All':
                teacher_list = teacher.split(" ")
                teacher_object = Teacher.objects.get(fname__contains=teacher_list[0], lname__contains=teacher_list[-1])
                teacher_id = teacher_object.id
                feedback_objects = Feedback_data.objects.filter(department=department_id,course=course_id,
                                                                teacher=teacher_id)
            else:
                feedback_objects = Feedback_data.objects.filter(department=department_id,course=course_id)
        else:
            if teacher != 'All':
                teacher_list = teacher.split(" ")
                teacher_object = Teacher.objects.get(fname__contains=teacher_list[0], lname__contains=teacher_list[-1])
                teacher_id = teacher_object.id
                feedback_objects = Feedback_data.objects.filter(department=department_id,
                                                                teacher=teacher_id)
            else:
                feedback_objects = Feedback_data.objects.filter(department=department_id)
    context = {
        'department':department,
        'course':course,
        'teacher':teacher,
        'feedback_objects':feedback_objects
    }
    if request.method == "POST":
        return redirect("principle_analytics")
    return render(request,'FeedbackApp/analytics.html',context=context)

def feedbackStatus(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(userId=request.user.username)
        # print(user_profile.values()[0]['firstName'])
        tic = TIC.objects.get(tic_name__contains=user_profile.values()[0]['firstName'])
        print("Teacher in Charge Name:{0} and his department:{1}".format(tic, tic.department))
        # subject_objects = Subject.objects.filter(department = tic.department)
        subjects = Subject.objects.filter(department=tic.department)
        teacher_list = []
        for subject in subjects:
            teacher = Teacher.objects.get(subject=subject.id)
            teacher_list.append(teacher)
        teachers = []
        for teacher in teacher_list:
            teachers.append(teacher)
        print(teacher_list)
        course_list = Course.objects.filter(department=tic.department)
        context = {
            'TicName': tic,
            'subjects': subjects,
            'teachers': teachers,
            'course_list': course_list,
        }
        if request.method == "POST":
            subject = request.POST.get('Subjects')
            course = request.POST.get('Courses')
            teacher = request.POST.get('Teachers')
            # sessin variables to store data
            request.session['feedbackStatus_subject'] = subject
            request.session['feedbackStatus_course'] = course
            request.session['feedbackStatus_teacher'] = teacher

            return redirect('feedbackStatus_view')

    return render(request,"FeedbackApp/feedbackStatus.html",context= context)

def feedbackStatus_view(request):
    if request.user.is_authenticated:
        print(request.user.username)
        tic_profile = UserProfile.objects.get(userId = request.user.username)
        #print(tic_profile.firstName)
        tic_object = TIC.objects.get(tic_name__contains = tic_profile.firstName)
        print(tic_object.department)
        subject = request.session['feedbackStatus_subject']
        course = request.session['feedbackStatus_course']
        teacher = request.session['feedbackStatus_teacher']

        department_object = Department.objects.get(departmentName__contains = tic_object.department)
        department_id = department_object.id
        if course == 'All':
            if subject != 'All':
                subject_object = Subject.objects.get(name__contains=subject)
                subject_id = subject_object.id
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],
                                                         lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id,subject = subject_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id,subject = subject_id)
            else:
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    # print(teacher_list[0])
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id)
        else:
            course_object = Course.objects.get(courseName__contains=course)
            course_id = course_object.id
            if subject != 'All':
                subject_object = Subject.objects.get(name__contains=subject)
                subject_id = subject_object.id
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    # print(teacher_list[0])
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                    subject=subject_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                    subject=subject_id)
            else:
                if teacher != 'All':
                    teacher_list = teacher.split(" ")
                    # print(teacher_list[0])
                    teacher_object = Teacher.objects.get(fname__contains=teacher_list[0],lname__contains=teacher_list[-1])
                    teacher_id = teacher_object.id
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id,
                                                                    teacher=teacher_id)
                else:
                    feedback_objects = Feedback_data.objects.filter(department=department_id, course=course_id)

        context = {
            'department': department_object,
            'subject' : subject,
            'course' : course,
            'teacher' : teacher,
            'feedback_objects':feedback_objects,
        }
        if request.method == "POST":
            return redirect('feedbackStatus')
        return render(request, 'FeedbackApp/feedbackStatus_view.html', context=context)

def change_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('currentpassword')
        new_password = request.POST.get('newpassword')
        reenter_password = request.POST.get('Reenterpassword')

        if new_password == reenter_password:
            print("Password Matches")

            user_profile = UserProfile.objects.filter(userId=username, password=password)
            if user_profile.count() != 0:
                profile = UserProfile.objects.get(userId=username)
                profile.password = new_password
                profile.save()
                return render(request, 'FeedbackApp/change_password.html',{"i":"Password successfully Updated/Please login"})
            else:
                return render(request, 'FeedbackApp/change_password.html',
                              {"i": "User profile doesn't exist/Please Enter valid Details"})
        else:
            return render(request, 'FeedbackApp/change_password.html',
                          {"i": "Please enter valid New Password/ Re enter Password Details"})
    return render(request, 'FeedbackApp/change_password.html',
                  {"i": ""})

def feedback(request):
    if request.user.is_authenticated:
        current_user = request.user.username
        questions = QuestionMaster.objects.all()
        context = {
            'questions':questions
        }
        if request.method == "POST":
            if 'submitFeedback' in request.POST:
                current_student = Student.objects.get(studentId = request.user)
                rating = 0
                no_of_question = 0
                rating_vals = []
                for val in range(1,15):
                    no_of_question = no_of_question + 1
                    current_rating = int(request.POST.get(str(val)))
                    rating = rating + current_rating
                    rating_vals.append(current_rating)
                avg_rating = round(rating / no_of_question,2)
                subjects = Subject.objects.filter(department = current_student.department,semester = current_student.semester)
                current_record = request.session['recordIndex']
                current_subject = subjects[current_record-1]
                current_teacher = Teacher.objects.get(subject = current_subject )
                feedbackId = 0
                feedbacks = Feedback.objects.all().count()
                if feedbacks == 0:
                    feedback_object = Feedback.objects.create(
                        username = request.user.username,
                        department=current_student.department,
                        course=current_student.course,
                        semester=current_student.semester,
                        subject=current_subject,
                        teacher=current_teacher,
                        avg_rating= avg_rating,
                        feedbackId= 1
                    )
                    feedback_object.save()
                    feedback_data_object = Feedback_data.objects.create(
                        department=current_student.department,
                        course=current_student.course,
                        semester=current_student.semester,
                        subject=current_subject,
                        teacher=current_teacher,
                        avg_rating=avg_rating,
                        value_1=rating_vals[0],
                        value_2=rating_vals[1],
                        value_3=rating_vals[2],
                        value_4=rating_vals[3],
                        value_5=rating_vals[4],
                        value_6=rating_vals[5],
                        value_7=rating_vals[6],
                        value_8=rating_vals[7],
                        value_9=rating_vals[8],
                        value_10=rating_vals[9],
                        value_11=rating_vals[10],
                        value_12=rating_vals[11],
                        value_13=rating_vals[12],
                        value_14=rating_vals[13],
                        count=1,
                    )
                    feedback_data_object.save()
                    return redirect('index')
                else:
                    feedback_object = Feedback.objects.filter(
                        username = request.user.username,
                        department=current_student.department,
                        course=current_student.course,
                        semester=current_student.semester,
                        subject=current_subject,
                        teacher=current_teacher
                    )
                    if feedback_object.count() !=0:
                        print("Feedback already provided with this data")
                        return redirect('index')
                    else:
                        current_object = Feedback.objects.create(
                            username=request.user.username,
                            department=current_student.department,
                            course=current_student.course,
                            semester=current_student.semester,
                            subject=current_subject,
                            teacher=current_teacher,
                            avg_rating=avg_rating,
                            feedbackId= feedbacks + 1
                        )
                        current_object.save()
                        data_object = Feedback_data.objects.filter(
                            department=current_student.department,
                            course=current_student.course,
                            semester=current_student.semester,
                            subject=current_subject,
                            teacher=current_teacher,
                        )
                        if data_object.count() != 0:
                            data_ = Feedback_data.objects.get(
                                department=current_student.department,
                                course=current_student.course,
                                semester=current_student.semester,
                                subject=current_subject,
                                teacher=current_teacher,
                            )
                            cur_avg = data_.avg_rating * (data_.count) + avg_rating
                            data_.count += 1
                            data_.value_1 = round(((data_.value_1 * (data_.count - 1)) + rating_vals[0]) / data_.count,2)
                            data_.value_2 = round(((data_.value_2 * (data_.count - 1)) + rating_vals[1]) / data_.count,2)
                            data_.value_3 = round(((data_.value_3 * (data_.count - 1)) + rating_vals[2]) / data_.count,2)
                            data_.value_4 = round(((data_.value_4 * (data_.count - 1)) + rating_vals[3]) / data_.count,2)
                            data_.value_5 = round(((data_.value_5 * (data_.count - 1)) + rating_vals[4]) / data_.count,2)
                            data_.value_6 = round(((data_.value_6 * (data_.count - 1)) + rating_vals[5]) / data_.count,2)
                            data_.value_7 = round(((data_.value_7 * (data_.count - 1)) + rating_vals[6]) / data_.count,2)
                            data_.value_8 = round(((data_.value_8 * (data_.count - 1)) + rating_vals[7]) / data_.count,2)
                            data_.value_9 = round(((data_.value_9 * (data_.count - 1)) + rating_vals[8]) / data_.count,2)
                            data_.value_10 = round(((data_.value_10 * (data_.count - 1)) + rating_vals[9]) / data_.count,2)
                            data_.value_11 = round(((data_.value_11 * (data_.count - 1)) + rating_vals[10]) / data_.count,2)
                            data_.value_12 = round(((data_.value_12 * (data_.count - 1)) + rating_vals[11]) / data_.count,2)
                            data_.value_13 = round(((data_.value_13 * (data_.count - 1)) + rating_vals[12]) / data_.count,2)
                            data_.value_14 = round(((data_.value_14 * (data_.count - 1)) + rating_vals[13]) / data_.count,2)
                            data_.avg_rating = round(cur_avg / data_.count,2)
                            data_.save()
                            return redirect('index')
                        else:
                            feedback_data_object = Feedback_data.objects.create(
                                department=current_student.department,
                                course=current_student.course,
                                semester=current_student.semester,
                                subject=current_subject,
                                teacher=current_teacher,
                                avg_rating=avg_rating,
                                value_1=rating_vals[0],
                                value_2=rating_vals[1],
                                value_3=rating_vals[2],
                                value_4=rating_vals[3],
                                value_5=rating_vals[4],
                                value_6=rating_vals[5],
                                value_7=rating_vals[6],
                                value_8=rating_vals[7],
                                value_9=rating_vals[8],
                                value_10=rating_vals[9],
                                value_11=rating_vals[10],
                                value_12=rating_vals[11],
                                value_13=rating_vals[12],
                                value_14=rating_vals[13],
                                count=1,
                            )
                            feedback_data_object.save()
                            return redirect('index')
            else:
                return redirect('index')
        return render(request,'FeedbackApp/feedback.html',context= context)
    else:
        return redirect('login')

def top_five_teachers(request):
    if request.user.is_authenticated:
        feedback_objects = Feedback_data.objects.order_by('-avg_rating')[:5]
        context = {
            'feedback_objects':feedback_objects,
        }
        return render(request,'FeedbackApp/top_five_teachers.html',context=context)

from tablib import Dataset

def simple_upload(request):
    if request.method == "POST":
        question_resource = QuestionMasterResource()
        dataset = Dataset()
        new_questions = request.FILES['myfile']

        imported_data = dataset.load(new_questions.read())
        result = question_resource.import_data(dataset,dry_run=True)

        if not result.has_errors():
            question_resource.import_data(dataset,dry_run=False)

    return render(request,'core/simple_upload.html')




