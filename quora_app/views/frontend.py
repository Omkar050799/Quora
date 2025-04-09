from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

from ..model.questions import Questions
from ..model.answers import Answers
from ..model.users import User
from .login import LoginViewSet
from .questions import QuestionsView
from .answers import AnswersView

def home(request):
    """View for the home page showing all questions"""
    # Create a DRF request object
    factory = APIRequestFactory()
    drf_request = factory.get('/')
    drf_request.user = request.user
    drf_request.session = request.session
    
    # Create QuestionsView instance and call list method
    questions_view = QuestionsView()
    questions_view.request = drf_request
    questions_view.kwargs = {}
    response = questions_view.list(drf_request)
    
    if response.status_code == 200:
        questions_data = response.data.get('data', [])
        questions = []
        for q_data in questions_data:
            try:
                question = Questions.objects.get(id=q_data.get('id'))
                questions.append(question)
            except Questions.DoesNotExist:
                pass
    else:
        questions = []
    
    return render(request, 'home.html', {'questions': questions})

@login_required
def create_question(request):
    """View for creating a new question"""
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if question_text:
            # Create a DRF request object
            factory = APIRequestFactory()
            drf_request = factory.post('/', {'question': question_text})
            drf_request.user = request.user
            drf_request.session = request.session
            
            questions_view = QuestionsView()
            questions_view.request = drf_request
            questions_view.kwargs = {}
            
            response = questions_view.create(drf_request)
            
            if response.status_code == 201:
                messages.success(request, 'Question created successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Failed to create question. Please try again.')
    
    return render(request, 'create_question.html')

def question_detail(request, id):
    """View for displaying a question and its answers"""
    # Create a DRF request object
    factory = APIRequestFactory()
    drf_request = factory.get(f'/{id}/')
    drf_request.user = request.user
    drf_request.session = request.session
    
    questions_view = QuestionsView()
    questions_view.request = drf_request
    questions_view.kwargs = {'id': id}
    
    response = questions_view.retrieve(drf_request, id=id)
    
    if response.status_code == 200:
        question_data = response.data.get('data', {})
        question = get_object_or_404(Questions, id=id)
        
        # Get answers for this question
        factory = APIRequestFactory()
        drf_request = factory.get('/')
        drf_request.user = request.user
        drf_request.session = request.session
        
        answers_view = AnswersView()
        answers_view.request = drf_request
        answers_view.kwargs = {}
        
        # Filter answers by question_id
        drf_request.query_params = {'question_id': id}
        
        answers_response = answers_view.list(drf_request)
        
        if answers_response.status_code == 200:
            answers_data = answers_response.data.get('data', [])
            answers = []
            for a_data in answers_data:
                try:
                    answer = Answers.objects.get(id=a_data.get('id'))
                    answers.append(answer)
                except Answers.DoesNotExist:
                    pass
        else:
            answers = []
        
        return render(request, 'question_detail.html', {
            'question': question,
            'answers': answers
        })
    else:
        messages.error(request, 'Question not found.')
        return redirect('home')

@login_required
def create_answer(request, question_id):
    """View for creating a new answer to a question"""
    if request.method == 'POST':
        answer_text = request.POST.get('answer')
        if answer_text:
            # Create a DRF request object
            factory = APIRequestFactory()
            drf_request = factory.post('/', {
                'answer': answer_text,
                'question_id': question_id
            })
            drf_request.user = request.user
            drf_request.session = request.session
            
            answers_view = AnswersView()
            answers_view.request = drf_request
            answers_view.kwargs = {}
            
            response = answers_view.create(drf_request)
            
            if response.status_code == 201:
                messages.success(request, 'Answer posted successfully!')
            else:
                messages.error(request, 'Failed to post answer. Please try again.')
    
    return redirect('question_detail', id=question_id)

@login_required
@csrf_exempt
def like_answer(request, answer_id):
    """View for liking/unliking an answer"""
    if request.method == 'POST':
        # Create a DRF request object
        factory = APIRequestFactory()
        drf_request = factory.post(f'/{answer_id}/like/')
        drf_request.user = request.user
        drf_request.session = request.session
        
        answers_view = AnswersView()
        answers_view.request = drf_request
        answers_view.kwargs = {'id': answer_id}
        
        response = answers_view.like(drf_request, id=answer_id)
        
        if response.status_code == 200:
            likes_count = response.data.get('data', {}).get('likes_count', 0)
            return JsonResponse({'success': True, 'likes_count': likes_count})
        else:
            return JsonResponse({'success': False, 'message': 'Failed to like answer'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def login_view(request):
    """View for handling login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        login_viewset = LoginViewSet()
        login_viewset.request = request
        
        # Prepare data for API
        data = {
            'username': username,
            'password': password
        }
        
        # Call API login method
        response = login_viewset.post(request, data=data)
        
        if response.status_code == 200:
            # Get user from response
            user_data = response.data.get('data', {})
            user_id = user_data.get('id')
            
            try:
                user = User.objects.get(id=user_id)
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            error_msg = response.data.get('message', 'Login failed.')
            messages.error(request, error_msg)
    
    return render(request, 'login.html')

def register_view(request):
    """View for user registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        
        # Create new user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        # Log the user in
        auth_login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('home')
        
    return render(request, 'register.html')

def logout_view(request):
    """View for handling logout"""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def forget_password_view(request):
    """View for handling forget password"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Create a DRF request object
        factory = APIRequestFactory()
        drf_request = factory.post('/', {'email': email})
        drf_request.user = request.user
        drf_request.session = request.session
        
        # Use the API view
        from ..views.forget_password import ForgotPasswordView
        forget_password_api = ForgotPasswordView()
        forget_password_api.request = drf_request
        forget_password_api.kwargs = {}
        
        response = forget_password_api.post(drf_request)
        
        if response.status_code == 200:
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
        else:
            error_msg = response.data.get('message', 'Failed to process request.')
            messages.error(request, error_msg)
    
    return render(request, 'forget_password.html') 