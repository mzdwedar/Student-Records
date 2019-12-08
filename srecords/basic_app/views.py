from django.shortcuts import render
from . import forms
from django.core.files.uploadedfile import SimpleUploadedFile
import pyrebase
import pprint
 
config = {
  "apiKey": "AIzaSyAIb0_8_lwd3g8a0HwfP_mMyHzM8gtkzoA",
  "authDomain": "student-record-ca92e.firebaseapp.com",
  "databaseURL": "https://student-record-ca92e.firebaseio.com",
  "storageBucket": "student-record-ca92e.appspot.com",
   "serviceAccount": "basic_app/student-record-ca92e-firebase-adminsdk-n9z07-9b13bee757.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def index(request):
    return render(request, 'basic_app/index.html')

def info(request):
    main = True
    addinfo = False
    showinfo = False

    form = forms.newStudent()
    if request.method == 'POST':

        if request.POST['info'] == 'submit':
            form = forms.newStudent(request.POST)

            if (form.is_valid()):
                sid = form.cleaned_data['sid']
                firstname = form.cleaned_data['firstname']
                lastname = form.cleaned_data['lastname']
                data = {"firstname":firstname, "lastname":lastname, "totalRequired":0}
                
                # # Import
                # from google.cloud import storage

                # # Initialize
                # client = storage.Client()
                # bucket = client.get_bucket('bucket-id-here')

                # # Download
                # blob = bucket.get_blob('remote/path/to/file.txt')
                # print blob.download_as_string()

                # # Upload
                # blob2 = bucket.blob('remote/path/storage.txt')
                # blob2.upload_from_filename(filename='/local/path.txt')
                db.child("students").child(sid).set(data)
                
                return render(request, 'basic_app/index.html')

        elif request.POST['info'] == 'showinfo':
            showinfo = True
            addinfo = False
            main = False
            sid = request.POST.get('sid')        
            student = db.child("students").get()
            info = student.val()[sid]

            return render(request, 'basic_app/info.html', context={'main':main,
                                                            'info':info,'sid':sid,
                                                            'showinfo':showinfo, 
                                                            'addinfo':addinfo})

        elif request.POST['info'] == 'addinfo':
            main = False
            showinfo = False
            addinfo = True

            return render(request, 'basic_app/info.html', context={'main':main, 'form':form, 
                                                                    'showinfo':showinfo, 
                                                                    'addinfo':addinfo})

    return render(request,'basic_app/info.html', context={'main':main, 'showinfo':showinfo,
                                                          'addinfo':addinfo, 'form':form})

def grades(request):
    main=True
    newCourse = False
    showCourse = False

    form = forms.newCourse()
    
    if request.method == 'POST':
        sid = request.POST.get('sid')

        if request.POST['grades'] == 'Show Grades':
            main = False
            showCourse = True
            newCourse = False

            student = db.child("students").get()
            grades = student.val().sid.grades
            pprint.pprint(grades)
            return render(request,'basic_app/grades.html', context={'grades':grades,  
                                                                    'main':main,'sid':sid,
                                                                    'newCourse':newCourse, 
                                                                    'showCourse':showCourse})

        elif request.POST['grades'] == 'Add Grades':
            main = False
            newCourse = True
            showCourse = False
            return render(request,'basic_app/grades.html', context={'main':main,'sid':sid,
                                                                    'form':form,
                                                                    'newCourse':newCourse, 
                                                                    'showCourse':showCourse})

        elif request.POST ['grades'] =='Add Course':
            form = forms.newCourse(request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                semester = form.cleaned_data['semester']
                cid = form.cleaned_data['cid']
                name = form.cleaned_data['name']
                price = form.cleaned_data['price']
                grade = form.cleaned_data['grade']
                data = {'cid':cid, 'name':name, 'price':price, 'grade':grade}

                student = db.child("students").get().val()[sid]

                if 'grades' not in student.keys():
                    student['grades'] = {}
                    student['grades'][year] = {}
                    student['grades'][year][semester] ={}
            
                    student['grades'][year][semester]['total'] = 0
                    student['grades'][year][semester]['required'] = 0
                
                elif year not in student.grades.keys():
                    student['grades'][year] = {}
                    student['grades'][year][semester] ={}
                    student['grades'][year][semester]['total'] = 0
                    student['grades'][year][semester]['required'] = 0

                elif semester not in student.grades.year.keys():
                    student['grades'][year][semester] ={}
                    student['grades'][year][semester]['total'] = 0
                    student['grades'][year][semester]['required'] = 0
                    

                temptotal = student['grades'][year][semester]['total'] 
                temptotal += price

                temprequired = student['grades'][year][semester]['required']
                temprequired += price

                temptotalRequired = student['totalRequired']
                temptotalRequired += price
                
                db.child("students").child(sid).update({'totalRequired':temptotalRequired})
                
                db.child("students").child(sid).child('grades').child(year).child(semester).set({"total":temptotal,
                                                                                                "required":temprequired})
                db.child("students").child(sid).child('grades').child(year).child(semester).push(data)   
                
                return render(request,'basic_app/index.html')
    return render(request,'basic_app/grades.html', context={'main':main, 
                                                            'newCourse':newCourse, 
                                                            'showCourse':showCourse})

def financial(request):
    main = True
    addFin = False
    showFin = False

    if request.method == 'POST':
        sid = request.POST.get('sid')

        if request.POST['finance'] == 'View Financial Profile':
            main = False
            showFin = True
            addFin = False
            student = db.child("students").get().val()[sid]
            
            return render(request, 'basic_app/financial.html', context={'main':main,
                                                                        'showFin':showFin, 
                                                                        'addFin':addFin,
                                                                         'student':student,
                                                                        'sid':sid})
        
        elif request.POST['finance'] == 'Deposit Money':
            main = False
            showFin = False
            addFin = True

            return render(request, 'basic_app/financial.html', context={'main':main, 
                                                                        'showFin':showFin,
                                                                        'addFin':addFin,
                                                                        'sid':sid})
        
        elif request.POST['finance'] == 'Add Money':
            year = request.POST.get('year')
            semester = request.POST.get('semester')
            paid = int(request.POST.get('paid-amount'))

            
            required = db.child("students").get().val()[sid]['grades'][year][semester]['required']
            total = db.child("students").get().val()[sid]['totalRequired']

            required  -= paid
            print(total)
            total -= paid
            print(total)
            db.child("students").child(sid).update({'totalRequired':total})
            db.child("students").child(sid).child('grades').child(year).child(semester).update({'paid':paid})
            db.child("students").child(sid).child('grades').child(year).child(semester).update({'required':required})
            
            
            return render(request, 'basic_app/index.html')

    return render(request, 'basic_app/financial.html', context={'main':main, 
                                                                'addFin':addFin, 
                                                                'showFin':showFin})

def report(request):
    main = True

    if request.method == 'POST':
        main = False
        sid = request.POST.get('sid')
        students = db.child("students").get()
        report = students.val()[sid]
        
        return render(request, 'basic_app/report', context={'main':main, 'sid':sid, 'report':report})

    return render(request,'basic_app/report.html', context={'main':main})