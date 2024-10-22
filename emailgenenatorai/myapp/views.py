from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.conf import settings
import requests
from json import dumps
from django.http import JsonResponse

def index(request):
    return render(request, 'myapp/index.html')

def dashboard(request):
    return render(request, 'myapp/dashboard.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username1')
        email = request.POST.get('email')
        password = request.POST.get('password1')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Create a new user
        user = User(username=username, password=make_password(password), email=email)
        user.save()

        messages.success(request, "Registration successful! You can now login.")
        return redirect('/')

    return render(request, 'myapp/index.html')

# Handle user login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username2']
        password = request.POST['password2']
        print(username, password)

        user = authenticate(username=username, password=password)
        print(password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard/')  # Redirect to home page after successful login
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/')

# Handle user logout
def logout_view(request):
    # Django's logout function clears the session
    logout(request)
    # Redirect to the login page after logout
    return redirect('/')  # Replace 'index' with your login page URL name

def generate_email(request):
    response_text = ""
    if request.method == 'POST':
        topic = request.POST.get('emailTopic', '')
        tone = request.POST.get('tone', 'neutral')
        writing_style = request.POST.get('writing-style', 'casual')
        recipient = request.POST.get('name','')
        additional_details = request.POST.get('details', '')
        print(topic)

        # Prepare the prompt based on the form data
        prompt = f'''
        Generate an email based on the following parameters:
        1. Topic: {topic}
        2. Tone: {tone}
        3. Writing Style: {writing_style}
        4. Additional Details: {additional_details}
        5. Recipient: {recipient}

        Please create a well-structured email that aligns with these inputs in detail of 3 paragraphs.
        '''
        api_url = "https://6ac2-35-225-193-27.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            email_start_index = response_text.find("Dear")
    
            if email_start_index != -1:
                response_text = response_text[email_start_index:]
            
            start_index = response_text.find("Respected")
            if start_index != -1:
                response_text = response_text[start_index:]
        else:
            response_text = "Error generating email."
        
        print(response_text)
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_subject(request):
    response_text = ""
    if request.method == 'POST':
        content = request.POST.get('subject', '')
        print(content)

        prompt=f'''Generate a formal and clear subject line based on the following email content:

        Email Content:{content}

        Please provide the subject line below:
        '''
        api_url = "https://6ac2-35-225-193-27.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            print(response_text)
            start_index = response_text.find("below:")
            if start_index != -1:
                response_text = response_text[start_index+6:]
        else:
            response_text = "Error generating subject."
        
        print(response_text)
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def generate_reply_email(request):
    response_text = ""
    if request.method == 'POST':
        topic = request.POST.get('emailBody', '')
        tone = request.POST.get('replytone', 'neutral')
        writing_style = request.POST.get('replywriting-style', 'casual')
        print(topic)

        # Prepare the prompt based on the form data
        prompt = f'''
        Generate a reply email based on the following email content:

        Email Content: {topic}
        Tone: {tone}
        Writing Style: {writing_style}

        Please provide email below:
        Dear/Respected 
        '''
        api_url = "https://6ac2-35-225-193-27.ngrok-free.app/generate"
        api_response = requests.post(api_url, json={"prompt": prompt})

        if api_response.status_code == 200:
            response_text = api_response.json()['response']
            print(response_text)
            email_start_index = response_text.find("Dear")
            second_index = response_text.find('Dear', email_start_index + 1)
    
            if second_index != -1:
                response_text = response_text[second_index:]
            
            start_index = response_text.find("Respected")
            s_index = response_text.find('Respected', start_index + 1)
            if s_index != -1:
                response_text = response_text[s_index:]
        else:
            response_text = "Error generating email."
        
        return JsonResponse({'response_text': response_text})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
