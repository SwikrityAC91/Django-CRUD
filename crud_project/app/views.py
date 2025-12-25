from django.shortcuts import render,redirect
from django.http import HttpResponse
from app.models import Student
from django.contrib import messages

# Create your views here
def Home(request):
    stu_data=Student.objects.all()
    return render(request,'home.html',{'studata':stu_data})

# def Add_student(request):

def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if not all([name, age, email, address]):
            return render(request, 'form.html', {
                'error': 'All fields are required'
            })
        
        # if Student.objects.filter(email=email).exists():
        #     return render(request, 'error.html', {
        #         'error': 'Email already exists'
        #     })
       

        Student.objects.create(
            name=name,
            age=int(age),
            email=email,
            address=address 
        )

        return redirect('home')

    return render(request,'form.html')


def delete_student(request):
    if request.method == "POST":
        student_id = request.POST.get('id')
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            messages.success(request, "Student deleted successfully.")  # optional
        except Student.DoesNotExist:
            messages.error(request, "Student does not exist.")  # optional
        return redirect('/')  # Redirect to home or list page
    else:
        return redirect('/')
    
def edit_student(request, id):
    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        # Handle the case where the student is not found
        return render(request, 'edit.html', {
            'error': 'Student not found'
        })

    if request.method == "POST":
        name = request.POST.get('name')
        age = request.POST.get('age')
        email = request.POST.get('email')
        address = request.POST.get('address')

        if not all([name, age, email, address]):
            return render(request, 'edit.html', {
                'student': student,
                'error': 'All fields are required'
            })

        student.name = name
        student.age = int(age)
        student.email = email
        student.address = address
        student.save()
        return redirect('home')

    # GET request
    return render(request, 'edit.html', {'student': student})

