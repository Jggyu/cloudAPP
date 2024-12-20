from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
import hashlib
from .models import User

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def dashboard(request):
    return render(request, 'dashboard.html')

def signup(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = hash_password(request.POST.get('password'))
        name = request.POST.get('name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        programming_language = request.POST.get('programming_language')
        
        # 중복 체크
        if User.objects.filter(student_id=student_id).exists() or User.objects.filter(email=email).exists():
            return HttpResponse("이미 존재하는 학번 또는 이메일입니다.")
        
        try:
            # 새 사용자 생성
            User.objects.create(
                student_id=student_id,
                password=password,
                name=name,
                email=email,
                department=department,
                programming_language=programming_language
            )
            return redirect('login')
        except Exception as e:
            return HttpResponse(f"회원가입 중 오류가 발생했습니다: {str(e)}")
    
    departments = ['컴퓨터공학과', '소프트웨어학과', '정보통신공학과', '인공지능학과']
    languages = ['Python', 'Java', 'C++', 'JavaScript', 'C#']
    return render(request, 'signup.html', {'departments': departments, 'languages': languages})

def login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = hash_password(request.POST.get('password'))
        
        try:
            user = User.objects.get(student_id=student_id, password=password)
            
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            request.session['student_id'] = user.student_id
            request.session['department'] = user.department
            request.session['programming_language'] = user.programming_language
            return redirect('success')
        except User.DoesNotExist:
            return render(request, 'login.html', {'error_message': "잘못된 학번 또는 비밀번호입니다."})
        except Exception as e:
            return render(request, 'login.html', {'error_message': f"로그인 중 오류가 발생했습니다: {str(e)}"})
    
    return render(request, 'login.html')

def success(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    context = {
        'name': request.session['name'],
        'student_id': request.session['student_id'],
        'department': request.session['department'],
        'programming_language': request.session['programming_language']
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.flush()
    return redirect('dashboard')