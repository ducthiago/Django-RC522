from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Log, User1
from .serializers import LogSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, Nguoi_Dung
from django.contrib import messages

# Create your views here.
@login_required(login_url='signin')
def user(request):
    nguoidung = User1.objects.all()
    return render(request, 'user.html', {'nguoidung':nguoidung})
@login_required(login_url='signin')
def log(request):
    logs = Log.objects.all()
    log2 = []
    for item in logs:
        log2.append(item)
    log2.reverse()
    return render(request,'index.html',{'logs':log2})
def signup(request):
    form = UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Chào {username}, tài khoản của bạn đã tạo thành công!')
            return redirect('log')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form':form})
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'không tồn tại')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('log')
    return render(request, 'signin.html', {})
@login_required(login_url='signin')
def profile(request):
    return render(request, 'profile.html', {})
@login_required(login_url='signin')
def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', False)
        tim = Log.objects.filter(name__contains=searched)
        tim2 = []
        for item in tim:
            tim2.append(item)
        tim2.reverse()
        return render(request, 'search.html', {'searched':searched, 'tim2':tim2})
    else:
        return render(request, 'search.html', {})
@login_required(login_url='signin')
def adduser(request):
    addbook = Nguoi_Dung()
    if request.method == 'POST':
        addbook = Nguoi_Dung(request.POST, request.FILES)
        if addbook.is_valid():
            addbook.save()
            name = addbook.cleaned_data.get('name')
            messages.success(request, f'Thêm \"{name}\" vào danh sách thành công!')
            return redirect('user')
    else:
        addbook = Nguoi_Dung()
    return render(request, 'adduser.html', {'addbook':addbook})
@login_required(login_url='signin')
def edit_user(request, pk):
    change = User1.objects.get(id=pk)
    addbook = Nguoi_Dung(instance=change)
    if request.method == 'POST':
        addbook = Nguoi_Dung(request.POST, instance=change)
        if addbook.is_valid():
            addbook.save()
            bookName = addbook.cleaned_data.get('bookName')
            messages.success(request, f'Thay đổi thông tin người dùng \"{bookName}\" thành công!')
            return redirect('user')
    return render(request, 'edit_user.html', {'addbook':addbook})
@login_required(login_url='signin')
def delete_user(request, pk):
    change = User1.objects.get(id=pk)
    if request.method == 'POST':
        change.delete()
        return redirect('user')
    return render(request, 'delete_user.html', {'delete':change})
@api_view(['GET'])
def getData(request):
    log = Log.objects.all()
    serializer = LogSerializer(log, many=True)
    return Response(serializer.data)
@api_view(['POST'])
def postData(request):
    cardID1 = request.POST.get('cardID')
    name = User1.objects.filter(cardID=cardID1).values('name')
    x = name[0]['name']
    data = {
            'cardID': request.POST.get('cardID'),
            'name': x,
        }
    serializer = LogSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)