from django.shortcuts import render, redirect
from .forms import UserProfile, UserRegistration
from django.contrib.auth.models import User
from .models import Profile, Matching
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import random
from django.db.models import Q, QuerySet, Subquery, OuterRef, F, Func, IntegerField
from django.db.models import CharField
import time

# Create your views here.
#def home(request):
#    return render(request, 'web/home.html')


def home(request):
    if request.user.is_authenticated:
        return redirect('profile-detail')

    return render(request, 'web/home.html')

def ProfileDetailsView(request):
    user_id = request.user.pk  # текущий пользователь, пославший запрос

    # Получение списка отфильтрованных пользователей
    filtered_users_liked = Matching.objects.filter(user_id=user_id).values_list('like', flat=True)
    filtered_users_disliked = Matching.objects.filter(user_id=user_id).values_list('dislike', flat=True)

    # Объединение двух списков
    filtered_users_liked_and_disliked = list(filtered_users_liked) + list(filtered_users_disliked)
    print(list(map(type, filtered_users_liked_and_disliked)), list(map(lambda x: x, filtered_users_liked_and_disliked)))
    # Фильтрация пользователей
    filtered_users = Profile.objects.exclude(id__in=filtered_users_liked_and_disliked).exclude(id__in=[0, user_id]).values_list('id', flat=True)
    print(f'1 Первоначальная фильтрация {filtered_users} {len(filtered_users)}')

    # Выбор случайного пользователя из отфильтрованного списка
    if filtered_users:
        print(f'2 Вторичная фильтрация {filtered_users}')
        pk = filtered_users[0]
        pick_user = Profile.objects.filter(pk=pk).first()

        if request.method == 'POST':
            like = request.POST.get('like') 
            dislike = request.POST.get('dislike')
            print(f'Лайкнут дизлайкнут {like} {dislike}')

            like = like if len(like) != 0 else 0
            dislike = dislike if len(dislike) != 0 else 0

            # Проверка, существует ли уже Matching для этого пользователя и данных
            existing_match = Matching.objects.filter(user_id=request.user.pk, like=like, dislike=dislike).first()

            if existing_match is None:
                # Если нет, создаем новый экземпляр
                match_data = Matching(user_id=request.user.pk, dislike=dislike, like=like)
                match_data.save()
                time.sleep(0.1)
            print(f'Остаток после вычета активности{filtered_users}')
        if pick_user is not None:
            context = {
                'pick_user': pick_user,
                'user_id': user_id,
            }


            return render(request, 'web/profile_detail.html', context)
        else:
            return render(request, 'web/profile_detail.html', context={'limit': 'На сегодня лимит пользователей исчерпан, заходите завтра'})
    else:
        return render(request, 'web/profile_detail.html', context={'limit': 'На сегодня лимит пользователей исчерпан, заходите завтра'})




def profle(request):
    if request.method == 'POST':
        form = UserProfile(request.POST)
        if form.is_valid():
            form.save()
            #return redirect('success')
    else:
        form = UserProfile()
    return render(request, 'web/profile.html', {'form': form})














def registration(request):
    tsts = str
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        sub_form = UserProfile(request.POST)

        if form.is_valid() and sub_form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            
            user = User(username = email, email = email)
            user.set_password(password)
            user.save()

            #biografy = sub_form.cleaned_data['biografy']
            birth_date = sub_form.cleaned_data['birth_date']
            location = sub_form.cleaned_data['location']
            name = sub_form.cleaned_data['name']
            #photo = sub_form.cleaned_data['photo']
            
            #user.pk это pk пользователя

            #Собираем полученные данные в условную переменную
            sub_info = Profile(user_id = user.pk, birth_date = birth_date, location = location, name = name)
            #Сохраняем данные (пользователя = в модель)
            sub_info.save()
            return redirect('home')
    else:
        form = UserRegistration()
        sub_form = UserProfile()
    return render(request, 'registration/register.html', {'form': form, 'sub_form': sub_form, 'tsts': tsts})