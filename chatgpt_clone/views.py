from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User  # This gives acces to django's user model which is a table which django has for one to be able to create users from.
import openai
from .models import Chat

from django.utils import timezone


openai_api_key = "Put the API key here"
openai.api_key = openai_api_key

    



def ask_openai(message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a personal AI health adviser. You are not allowed to give any information unrelated to health and medical issues. You do not also serve as a replacement to professional medical practitioners."},
            {"role": "user", "content": message},
        ]
    )
    answer = response.choices[0].message.content
    return answer



def chatbot(request):
    chats = Chat.objects.filter(user=request.user)
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        context = {'message': message, 'response': response}
        return JsonResponse(context)
    context = {'chats': chats}
    return render(request, 'chatgpt.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')              
    else:                                                                                           
        return render(request, 'login.html')                                                                                                                                                                                                                        


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)  # creating a new user from django's in-built user model
                user.save()
                auth.login(request, user)   
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                context = {'error_message': error_message}
                return render(request, 'register.html', context)
        else:
            error_message = "Passwords don't match"
            context = {'error_message': error_message}
            return render(request, 'register.html', context)
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')