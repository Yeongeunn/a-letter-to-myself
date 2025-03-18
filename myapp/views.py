from django.shortcuts import render, redirect,get_object_or_404
from django.http import JsonResponse
from .models import Letters, LetterRoutine, SpecialDateRoutine
from myapp.forms import LetterForm,SpecialDateRoutineForm
from commons.forms import UserForm
from django.utils.timezone import now  # 현재 날짜 가져오기
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


# Create your views here.
def home(request):
    return render(request, 'myapp/index.html')

# 1️⃣ 편지 작성 뷰
def write_letter(request):
    if request.method == 'POST':
        form = LetterForm(request.POST, request.FILES)
        if form.is_valid():
            letter = form.save(commit=False)  # ✅ 데이터 저장 전에 추가 설정
            letter.user = request.user  # 🔥 작성자를 현재 로그인한 사용자로 설정
            if not letter.open_date:  # open_date가 없으면 오늘 날짜로 설정
                letter.open_date = now().date()
            letter.save()
            return redirect('letter_list')  # 편지 목록 페이지로 이동
    else:
        form = LetterForm()
        
    return render(request, 'myapp/writing.html', {'form': form})

def postbox(request):
    return render(request, 'myapp/postbox.html')

# 2️⃣ 작성된 편지 목록 보기
@login_required
def letter_list(request):
    letters = Letters.objects.all()
    past_letters = Letters.objects.filter(category="past")
    today_letters = Letters.objects.filter(category="today")
    future_letters = Letters.objects.filter(category="future")
    
    return render(request, 'myapp/letter_list.html', {
        'letters': letters,
        'past_letters': past_letters,
        'today_letters': today_letters,
        'future_letters': future_letters,
    })

@login_required
def past_letters(request):
    """ 과거의 편지 목록 (오늘 이전 날짜) """
    today = now().date()
    letters = Letters.objects.filter(open_date__lt=today)
    return render(request, 'myapp/letter_past.html', {'letters': letters})

@login_required
def today_letters(request):
    """ 오늘의 편지 목록 """
    today = now().date()  # 오늘 날짜 가져오기
    letters = Letters.objects.filter(open_date=today)
    
    print(f"오늘 날짜: {today}")
    print(f"오늘의 편지 개수: {letters.count()}")

    for letter in letters:
        print(f"Letter ID: {letter.id}, Title: {letter.title}, Open Date: {letter.open_date}")

    return render(request, 'myapp/letter_today.html', {'letters': letters})

@login_required
def future_letters(request):
    """ 미래의 편지 목록 (오늘 이후 날짜) """
    today = now().date()
    letters = Letters.objects.filter(open_date__gt=today)
    return render(request, 'myapp/letter_future.html', {'letters': letters})

#개별 편지 상세보기api
@login_required
def letter_json(request, letter_id):
    letter = get_object_or_404(Letters, id=letter_id)
    data = {
        'id':letter.id,
        'title': letter.title,
        'content': letter.content,
        'letter_date': letter.open_date.strftime("%Y-%m-%d"),
    }
    return JsonResponse(data)

#편지 루틴 만들기
@login_required
@csrf_exempt
def save_routine(request):
    days = range(1, 32)
    routine = None  # ✅ 기본값 설정
    special_routine = None  # ✅ 기본값 설정

    if "title" in request.POST:
        title = request.POST.get("title") or "기본 루틴 제목"
        routine_type = request.POST.get("routine_type")
        day_of_week = request.POST.get("day_of_week") if routine_type == "weekly" else None
        day_of_month = request.POST.get("day_of_month") if routine_type == "monthly" else None
        time = request.POST.get("routine_time")

        routine = LetterRoutine.objects.create(
            user=request.user,
            title=title,
            routine_type=routine_type,
            day_of_week=day_of_week,
            day_of_month=day_of_month,
            time=time
        )

    elif "name" in request.POST:
        name = request.POST.get("name")
        date = request.POST.get("date")

        special_routine = SpecialDateRoutine.objects.create(
            user=request.user,
            name=name,
            date=date
        )

    # ✅ 내 루틴 보기
    routines = LetterRoutine.objects.filter(user=request.user)
    specialDays = SpecialDateRoutine.objects.filter(user=request.user)

    lists = {
        "days": days,
        "routines": routines,
        "specialDays": specialDays,
        "routine_id": routine.id if routine else None,  # ✅ `None` 체크 추가
        "special_routine_id": special_routine.id if special_routine else None  # ✅ `None` 체크 추가
    }

    return render(request, "myapp/routine.html", lists)

   
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # 로그인 후 홈으로 이동
    return render(request, 'commons/login.html')

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'commons/signup.html', {'form': form})

# @login_required
# def get_routine_events(request):
#     """편지 루틴 정보를 JSON 데이터로 반환"""
#     routines = LetterRoutine.objects.all()
#     events = []

#     for routine in routines:
#         events.append({
#             "title": f"📜 {routine.routine_type} 루틴",
#             "start": routine.date.strftime("%Y-%m-%d")
#         })

#     return JsonResponse(events, safe=False)
WEEKDAYS = {
    "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6
}
@login_required
def get_routine_events(request):
    """ 사용자의 편지 루틴을 JSON 데이터로 반환 """
    user = request.user
    routines = LetterRoutine.objects.filter(user=user)

    events = []
    for routine in routines:
        if routine.routine_type == "weekly":
            today = datetime.today()
            weekday_str = routine.day_of_week  # ✅ 문자열 요일 (예: "Monday")
            
            if weekday_str not in WEEKDAYS:
                continue  # ✅ 유효하지 않은 요일 값이 있으면 스킵
            
            weekday_num = WEEKDAYS[weekday_str]  # ✅ 요일을 숫자로 변환 (0~6)
            next_date = today + timedelta(days=(weekday_num - today.weekday() + 7) % 7)  # ✅ 다음 해당 요일 찾기

            # 주간 루틴 → 매주 같은 요일에 발생
            events.append({
                "title": routine.title,
                "start": next_date.strftime("%Y-%m-%d"),  # ✅ YYYY-MM-DD 형식
                "allDay": True
            })
        elif routine.routine_type == "monthly":
            # 월간 루틴 → 매월 특정 날짜에 발생
            for month in range(1, 13):  # 1월~12월 반복
                events.append({
                    "title": routine.title,
                    "start": f"2025-{month:02d}-{routine.day_of_month:02d}",  # ✅ YYYY-MM-DD 형식
                    "allDay": True
                })

    return JsonResponse(events, safe=False)

#기념일 루틴 추가 
# @login_required
# def save_specialDateRoutine(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         date = request.POST.get("date")
       

#         special_routine = SpecialDateRoutine.objects.create(
#             user=request.user,
#             name = name,
#             date = date
#         )
#         return JsonResponse({"message":"기념일이 성공적으로 저장되었습니다!", "id":special_routine.id})

#     return render(request, "myapp/routine.html")


# def routine_list(request):
#    #print(f"현재 로그인한 사용자: {request.user}")  # ✅ request.user 확인용 디버깅
#     routines = LetterRoutine.objects.filter(user=request.user)
#    #print(f"가져온 루틴 개수: {routines.count()}")  # ✅ 루틴 개수 확인
#     specialDays = SpecialDateRoutine.objects.filter(user=request.user)

#     lists = {
#         "routines": routines,
#         "specialDays":specialDays

#     }
#     return render(request, "myapp/routine.html", lists)


