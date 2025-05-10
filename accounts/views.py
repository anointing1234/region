from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from .models import PasswordResetCode
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import json
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.db import transaction
from django.db.models import F,Sum
from django.contrib.auth.decorators import login_required
import logging
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from .models import Account
import string
import random


def authenticate_view(request):
    return render(request, 'auth/authenticate.html',)



def generate_unique_username(base_name):
    """Generate a unique username by appending random digits to the base name."""
    while True:
        random_suffix = ''.join(random.choices(string.digits, k=4))
        username = f"{base_name.lower()}{random_suffix}"
        if not Account.objects.filter(username=username).exists():
            return username


def register(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
            first_name = data.get('firstname')
            last_name = data.get('lastname')
            email = data.get('Email')
            password = data.get('password')

            errors = {}

            if not first_name:
                errors['firstname'] = ['First name is required.']
            if not last_name:
                errors['lastname'] = ['Last name is required.']
            if not email:
                errors['Email'] = ['Email is required.']
            elif Account.objects.filter(email=email).exists():
                errors['Email'] = ['This email address is already in use.']
            if not password:
                errors['password'] = ['Password is required.']

            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors,
                    'message': 'Registration failed. Please correct the errors below.'
                }, status=400)

            # Generate unique username
            base_username = f"{first_name}{last_name}".replace(" ", "").lower()
            unique_username = generate_unique_username(base_username)

            user = Account.objects.create_user(
                email=email,
                username=unique_username,
                first_name=first_name,
                last_name=last_name,
                password=password,
            )

            return JsonResponse({
                'success': True,
                'message': 'Registration successful!',
                'redirect_url': reverse('authenticate')
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data received.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Registration failed: {str(e)}'
            }, status=500)

    return render(request, 'auth/authenticate.html')



def login_view(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            password = data.get('password')

            errors = {}

            if not email:
                errors['email'] = ['Email is required.']
            if not password:
                errors['password'] = ['Password is required.']

            if errors:
                return JsonResponse({'success': False, 'errors': errors, 'message': 'Login failed. Please correct the errors below.'}, status=400)
            else:
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    auth_login(request, user)
                    return JsonResponse({
                        'success': True,
                        'message': 'Login successful!',
                        'redirect_url': reverse('home')  # Use the redirect URL from your commented-out code
                    })
                else:
                    errors['non_field_errors'] = ['Invalid email or password.']
                    return JsonResponse({'success': False, 'errors': errors, 'message': 'Login failed. Invalid email or password.'}, status=401) # 401 Unauthorized

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data received.'}, status=400)

    else:
        return render(request, 'auth/authenticate.html') # Or your actual login form template
 
 
 

def contact_form(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        name = request.POST.get('cname')
        email = request.POST.get('cemail')
        phone = request.POST.get('cphone', 'Not provided')
        subject = request.POST.get('csubject', 'No Subject')
        message = request.POST.get('cmessage')

        if not name or not email or not message:
            return JsonResponse({'success': False, 'message': 'Please fill in all required fields.'})

        # Construct email message
        email_subject = f"New Contact Form Submission: {subject}"
        email_body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message:
        {message}
        """

        try:
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,  # Ensure this is a valid sender
                recipient_list=['yakubudestiny9@gmail.com'],  # Send to the user
                fail_silently=False,
            )
            return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error sending email: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)




def send_reset_code_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({'success': False, 'message': 'Email field is required.'})

        # Check if email exists
        User = get_user_model()
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'This email address is not registered.'})

        # Generate and save reset code
        reset_code = get_random_string(length=7)
        PasswordResetCode.objects.update_or_create(
            email=email,
            defaults={'reset_code': reset_code}
        )

        # Send reset code email
        send_mail(
            'Password Reset Code',
            f'Your password reset code is: {reset_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({'success': True, 'message': 'A password reset code has been sent to your email.',  'redirect_url': '/accounts/reset-password'  })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

def logout_view(request):
    auth_logout(request)
    # register_form = RegisterForm()
    # login_form = LoginForm()
    # return render(request, 'auth/authenticate.html', {
    #     'login_form': login_form,
    #     'register_form': register_form,
    # })

def reset_password_view(request):
    # Check if the request is a POST request
    if request.method == 'POST':
        try:
            # Parse the request body
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('email')
            reset_code = data.get('reset_code')
            new_password = data.get('new_password')

            # Check if all fields are provided
            if not email or not reset_code or not new_password:
                return JsonResponse({'success': False, 'message': 'Missing required fields.'})

            # Check if the reset code is valid
            try:
                reset_entry = PasswordResetCode.objects.get(email=email, reset_code=reset_code)
            except PasswordResetCode.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Invalid reset code or email.'})

            # Update the user's password
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                reset_entry.delete()  # Delete the reset entry after successful password change

                return JsonResponse({'success': True, 'message': 'Your password has been reset successfully.'})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'User not found.'})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid data format.'})

    else:
        # Redirect to the reset password page if the request method is not POST
         return render(request,'auth/reset_password.html',)

def forgot_password(request):
    return render(request,'auth/send_password.html',)