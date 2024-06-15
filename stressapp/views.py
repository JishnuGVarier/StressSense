from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Recommendation
from django.views.decorators.csrf import csrf_protect   
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.validators import EmailValidator,RegexValidator
from .ml_model import predict
import numpy as np


# Create your views here.

def indexView(request):
    return render(request, 'index.html')

def loginView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('predict')
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'login.html')


def registerView(request):
    if request.method == 'POST':
        email = request.POST['email']
        new_pass = request.POST['new_pass']
        confirm_pass = request.POST['confirm_pass']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']

        if new_pass != confirm_pass:
            return HttpResponse("Your password and confirm password are not the same!!")
        else:
            # Validate password
            try:
                validate_password(new_pass)
            except ValidationError as e:
                return HttpResponse(str(e))
            # Validate email
            try:
                EmailValidator()(email)
            except ValidationError:
                return HttpResponse("Invalid email format")
            # Validate first name and last name
            name_validator = RegexValidator(r'^[a-zA-Z]*$', 'Only letters are allowed.')
            try:
                name_validator(first_name)
                name_validator(last_name)
            except ValidationError as e:
                return HttpResponse(str(e))
            # Validate username
            username_validator = RegexValidator(r'^[a-zA-Z][a-zA-Z0-9]*$', 'Username must start with a letter and contain only letters and numbers.')
            try:
                username_validator(username)
            except ValidationError as e:
                return HttpResponse(str(e))
            # Create a new user instance using the custom user model
            user = User.objects.create_user(username=username, email=email, password=new_pass)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            return redirect('login')
    return render(request, 'register.html')

def aboutView(request):
    return render(request, 'about.html')

def errorView(request):
    return render(request, 'error.html')

def servicesView(request):
    return render(request, 'services.html')

def whyView(request):
    return render(request, 'why.html')

def teamView(request):
    return render(request, 'team.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_protect
@login_required(login_url='/stress/login/')
def predictionView(request):
    if request.method == 'POST':
        try:
            # Get input data from the form
            snoring_rate = float(request.POST.get('snoring_rate', 0))
            respiration_rate = float(request.POST.get('respiration_rate', 0))
            body_temperature = float(request.POST.get('body_temperature', 0))
            limb_movement = float(request.POST.get('limb_movement', 0))
            blood_oxygen = float(request.POST.get('blood_oxygen', 0))
            eye_movement = float(request.POST.get('eye_movement', 0))
            sleeping_hours = float(request.POST.get('sleeping_hours', 0))
            heart_rate = float(request.POST.get('heart_rate', 0))
            # print(snoring_rate, respiration_rate, body_temperature, limb_movement, blood_oxygen, eye_movement, sleeping_hours, heart_rate)
            # Prepare input data for predictions
            input_data = np.array([[snoring_rate, respiration_rate, body_temperature, limb_movement, blood_oxygen, eye_movement, sleeping_hours, heart_rate]])
            # Make predictions using the ML model
            prediction = predict(input_data)
            val=int(prediction[0])

            recommendations = Recommendation.objects.filter(stress_level=val)

            recommendation = recommendations[0].recommend.split('.',2)
            # Render the prediction result in the template
            return render(request, 'prediction.html', {'prediction': prediction,'recommendation':recommendation if recommendations else None})

        except Exception as e:
            # Handle any exception that might occur during prediction
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'prediction.html', {'error_message': error_message})

    # Render the prediction form initially
    return render(request, 'prediction.html')