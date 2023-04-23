import os
from dotenv import load_dotenv
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.views import View
from django.urls import reverse, reverse_lazy
from .forms import SearchForm,ReviewForm,MyForm
from .models import MyModel, Review, MyList, Tag
import json
import requests
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse


load_dotenv()
API_KEY = os.getenv('API_KEY')

def login(request):
    return render(request, 'app/login.html')

SEARCH_URL = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=ja-jp&page=1&include_adult=false&format=json'

SEARCH_URL2 = f'https://api.themoviedb.org/3/movie/{{movie_id}}?api_key={API_KEY}&language=ja-JP&format=json'

SEARCH_URL3 = f'https://api.themoviedb.org/3/movie/{{movie_id}}/credits?api_key={API_KEY}&language=ja-JP'

SEARCH_URL4 = f'https://api.themoviedb.org/3/person/{{person_id}}?api_key={API_KEY}&language=en-US'

SEARCH_URL5 = f'https://api.themoviedb.org/3/person/{{person_id}}/movie_credits?api_key={API_KEY}&language=ja-JP'

POPULAR_URL = f'https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=ja-JP&page=1&region=JP'

RESEMBLE_URL = f'https://api.themoviedb.org/3/movie/{{movie_id}}/similar?api_key={API_KEY}&language=ja-JP&page=1'


def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result["results"]
    return items


def get_api_data2(movie_id):
    url = SEARCH_URL2.format(movie_id=movie_id)
    api = requests.get(url).text
    result = json.loads(api)
    return result


def get_api_data3(movie_id):
    url = SEARCH_URL3.format(movie_id=movie_id)
    api = requests.get(url).text
    result = json.loads(api)
    cast_i = result["cast"]
    return cast_i


def get_api_data4(movie_id):
    url = SEARCH_URL3.format(movie_id=movie_id)
    api = requests.get(url).text
    result = json.loads(api)
    crew_i = result["crew"]
    return crew_i


def get_api_data5(person_id):
    url = SEARCH_URL4.format(person_id=person_id)
    api = requests.get(url).text
    result = json.loads(api)
    return result


def get_api_data6(person_id):
    url = SEARCH_URL5.format(person_id=person_id)
    api = requests.get(url).text
    result = json.loads(api)
    cast_film = result["cast"]
    return cast_film


def get_api_data7():
    url = POPULAR_URL
    api = requests.get(url).text
    result = json.loads(api)
    popular_film = result["results"]
    return popular_film


def get_api_data8(movie_id):
    url = RESEMBLE_URL.format(movie_id=movie_id)
    api = requests.get(url).text
    result = json.loads(api)
    resemble_film = result["results"]
    return resemble_film


class IndexListView(LoginRequiredMixin,ListView):
    # 検索フォームのview


    def get(self, request):
        form = SearchForm(request.POST or None)
        reviewform = ReviewForm(request.POST or None)
        reviews = Review.objects.filter(
            user=request.user).order_by("-datetime")
        popular_film = get_api_data7()
        popular_film_data = []
        for p in popular_film:
            title = p["title"]
            image = p['poster_path']
            if image:
                image = 'https://image.tmdb.org/t/p/w185/' + image
            else:
                image = 'https://7869-7973-8327-01.s3.amazonaws.com/static/cinelog/148959.jpg'

            release_date = p['release_date']
            id = p['id']
            data = {
                "title": title,
                "image": image,
                "release_date": release_date,
                "id": id
            }
            popular_film_data.append(data)

        return render(request, 'app/index.html', {
            'form': form,
            'reviewform': reviewform,
            'reviews': reviews,
            'popular_film_data': popular_film_data,
        })

class CinemaResultView(LoginRequiredMixin,ListView):
  
    def post(self, request):

        form = SearchForm(request.POST or None)

        if form.is_valid():
            query = form.cleaned_data['title']

            params = {
                'query': query,
                'hits': 50,
            }
            items = get_api_data(params)
            cinema_data = []
            for i, item in enumerate(items):
                if i == 30:
                   break
            for item in items:
                title = item['title']
                image = item['poster_path']
                if image:
                    image = 'https://image.tmdb.org/t/p/w342/' + image
                else:
                    image = 'https://7869-7973-8327-01.s3.amazonaws.com/static/cinelog/148959.jpg'

                release_date = item['release_date']
                id = item['id']

                cinema = {
                    'title': title,
                    'image': image,
                    'release_date': release_date,
                    'id': id
                }
                cinema_data.append(cinema)

               


            return render(request, 'app/cinema.html', {
                'cinema_data': cinema_data,
                'keyword': query,
            })
            
        return render(request, 'app/index.html', {
            'form': form
        })

@login_required
# 検索のapiデータをとってくる
def movie_search(request):
    query = request.GET.get('query', '')
    if query:
        params = {
            'query': query,
            'hits': 5,
        }
        items = get_api_data(params)

        return JsonResponse({"movies": items})
    return JsonResponse({"movies": []})

class DetailCinemaView(LoginRequiredMixin, DetailView):
    # 映画の詳細を呼び出すview(cinema,cast,crewそれぞれをとってくる)
    def get(self, request, *args, **kwargs):
        movie_id = self.kwargs["id"]
        items = get_api_data2(movie_id)
        cast = get_api_data3(movie_id)
        crew = get_api_data4(movie_id)
        resemble = get_api_data8(movie_id)

        cinema_data = {
            'title': items['title'],
            'overview': items['overview'],
            'image': items['poster_path'],
            'release_date': items['release_date'],
            'id': items['id']
        }

        cast_datalist = []
        for i, item in enumerate(cast):
            if i == 30:
                break
            cast_name = item['name']
            cast_image = item['profile_path']
            if cast_image:
                cast_image = 'https://image.tmdb.org/t/p/w185/' + cast_image
            else:
                cast_image = 'https://7869-7973-8327-01.s3.amazonaws.com/static/cinelog/148959.jpg'

            cast_character = item['character']
            cast_id = item['id']

            cast_data = {
                'cast_name': cast_name,
                'cast_image': cast_image,
                'cast_character': cast_character,
                'cast_id': cast_id,
            }

            cast_datalist.append(cast_data)

        crew_datalist = []

        for i, item in enumerate(crew):
            if i == 8:
                break

            crew_name = item['name']
            crew_image = item['profile_path']
            if crew_image:
                crew_image = 'https://image.tmdb.org/t/p/w154/' + crew_image
            else:
                crew_image = 'https://7869-7973-8327-01.s3.amazonaws.com/static/cinelog/148959.jpg'

            crew_job = item['job']
            crew_id = item['id']

            crew_data = {
                'crew_name': crew_name,
                'crew_image': crew_image,
                'crew_job': crew_job,
                'crew_id': crew_id,
            }
            crew_datalist.append(crew_data)

            resemble_cinemalist = []
        for i, item in enumerate(resemble):
            if i == 8:
                break
            resemble_title = item['title']
            resemble_image = item['poster_path']
            if resemble_image:
                resemble_image = 'https://image.tmdb.org/t/p/w342/' + resemble_image
            else:
                resemble_image = 'https://7869-7973-8327-01.s3.amazonaws.com/static/cinelog/148959.jpg'
            resemble_release_date = item['release_date']
            resemble_id = item['id']

            resemble_cinema_data = {
                'resemble_title': resemble_title,
                'resemble_image': resemble_image,
                'resemble_release_date': resemble_release_date,
                'resemble_id': resemble_id,
            }

            resemble_cinemalist.append(resemble_cinema_data)

        return render(request, 'app/detail.html', {
            'cinema_data': cinema_data,
            'cast_datalist': cast_datalist,
            'crew_datalist': crew_datalist,
            'resemble_cinemalist': resemble_cinemalist,
        })


class DetailCastView(LoginRequiredMixin, DetailView):
    # キャスト詳細を呼び出すview
    def get(self, request, *args, **kwargs):
        person_id = self.kwargs["id"]
        cast_detail = get_api_data5(person_id)
        cast_detail_film = get_api_data6(person_id)

        cast_detail_list = {
            'name': cast_detail['name'],
            'birthday': cast_detail['birthday'],
            'image': cast_detail['profile_path'],
            'biography': cast_detail['biography'],

        }

        cast_film_list = []
        for i, item in enumerate(cast_detail_film):
            if i == 8:
                break
            film_title = item['title']
            relesedate = item['release_date']
            image = item['poster_path']
            cinema_id = item['id']

            cast_detail_film_data = {
                'film_title': film_title,
                'releasedate': relesedate,
                'image': image,
                'cinema_id': cinema_id,
            }
            cast_film_list.append(cast_detail_film_data)

        return render(request, 'app/cast-detail.html', {
            'cast_detail_list': cast_detail_list,
            'cast_film_list': cast_film_list
        })


class MyCreateView(LoginRequiredMixin, CreateView):
    # 登録のview(タイトル、ナンバー、画像を取得)
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        number = request.POST.get('number')
        image = request.POST.get('image')
        user = request.user
        tag = request.POST.get('tags')
        if tag == '':
            tag == None
        if MyModel.objects.filter(number=number, user=user).exists():
   
            return redirect('index')
        else:
            my_model = MyModel.objects.create(
                title=title, number=number, image=image, user=user)
            if tag:
                tags = tag.split(",")
                for t in tags:
                    tag_obj, created = Tag.objects.get_or_create(name=t)
                    my_model.tags.add(tag_obj)
            MyList.objects.create(user=user, movie=my_model)
 
            messages.success(self.request, '登録しました。')
            return redirect('list')



# 登録した映画のリスト
class CinemaListView(LoginRequiredMixin, ListView):
    template_name = 'app/cinema-list.html'
    model = MyModel

    def get_queryset(self):
        order = self.request.GET.get('order', 'desc')
        if order == 'desc':
            order_field = '-id'
        else:
            order_field = 'id'

        return MyModel.objects.filter(user=self.request.user).order_by(order_field)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = []
        for i in context['object_list']:
            review = Review.objects.filter(user=self.request.user,cinema=i.id)
            reviews.append(review)
        context['reviews'] = reviews
        return context

# マイリストから外すview
class MyListDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'app/list-delete.html'
    model = MyModel
    success_url = reverse_lazy('list')

# レビューを作るview
class CinemaReviewView(LoginRequiredMixin, CreateView):  
    model = Review
    fields = ('cinema', 'review', 'datetime', 'user')
    template_name = 'app/review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mymodel'] = MyModel.objects.get(pk=self.kwargs['cinema_id'])
        return context

    def get_success_url(self):
        return reverse('list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# TOPページから直接レビューを作成するview
class TopCinemaReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('cinema', 'review', 'datetime', 'user')
    template_name = 'app/top-review.html'

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, movie_id=None):
        self.form = SearchForm(request.POST or None)
        mymodel = None
        if movie_id:
            mymodel = MyModel.objects.get(id=movie_id)

        return render(request, 'app/top-review.html', {
            'form': self.form,
            'mymodel': mymodel,
        })

    def post(self, request, *args, **kwargs):
        self.form = SearchForm(request.POST or None)

        if 'search' in request.POST and self.form.is_valid():
            query = self.form.cleaned_data['title']

            params = {
                'query': query,
                'hits': 28,
            }
            items = get_api_data(params)
            cinema_data = []
            for i in items:
                title = i['title']
                image = i['poster_path']
                release_date = i['release_date']
                id = i['id']
                cinema = {
                    'title': title,
                    'image': image,
                    'release_date': release_date,
                    'id': id
                }
                cinema_data.append(cinema)

            return render(request, 'app/search-cinema.html', {
                'cinema_data': cinema_data,
            })
        elif 'submit' in request.POST:
            review_form = self.get_form()
            if review_form.is_valid():
                return self.form_valid(review_form)
            else:
                return self.form_invalid(review_form)

# 登録のview(タイトル、ナンバー、画像を取得)
class TopCinemaAddView(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        number = request.POST.get('number')
        image = request.POST.get('image')
        user = request.user

        if MyModel.objects.filter(number=number, user=user).exists():
            my_model = MyModel.objects.get(number=number, user=user)

            return redirect(reverse_lazy('review', kwargs={'cinema_id': my_model.pk}))
        else:
            my_model = MyModel.objects.create(
                title=title, number=number, image=image, user=user)
            MyList.objects.create(user=user, movie=my_model)
            return redirect(reverse_lazy('top-review', kwargs={'movie_id': my_model.id}))

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

# レビューを更新するview
class CinemaReviewUpdateView(LoginRequiredMixin, UpdateView):

    model = Review
    fields = ('cinema', 'review', 'datetime')
    template_name = 'app/review-update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mymodel'] = MyModel.objects.get(pk=self.kwargs['cinema_id'])
        return context

    def get_success_url(self):
        return reverse('mycinema_detail', kwargs={'cinema_id': self.kwargs['cinema_id']})

# レビューを削除するview
class CinemaReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('list')


# タグでまとまった映画のリスト
class CinemaTagListView(LoginRequiredMixin, ListView):
    template_name = 'app/cinema-tag-list.html'

    def get_queryset(self):
        tag = self.kwargs['tag']

        order = self.request.GET.get('order', 'desc')
        if order == 'desc':
            order_field = '-id'
        else:
            order_field = 'id'

        return MyModel.objects.filter(tags=tag).order_by(order_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(Tag, pk=self.kwargs["tag"])
        context['tag_name'] = tag.name
        return context

# 映画にタグを追加するview
class TagCreateView(LoginRequiredMixin, CreateView):
    def post(self, request, cinema_id):
        tag = request.POST.get('tags')
        user = request.user
        my_model = MyModel.objects.get(id=cinema_id, user=user)
        tags = tag.split(',')
        for t in tags:
            if my_model.tags.count() >= 6:
                break
                
            tag_obj, created = Tag.objects.get_or_create(name=t)
            my_model.tags.add(tag_obj)
        return redirect('list')


# タグを外すview
class RemoveTagFromCinemaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cinema = get_object_or_404(MyModel, pk=request.POST.get('cinema'))
        tag = get_object_or_404(Tag, pk=kwargs['tag'])

        if cinema.user == request.user:
            cinema.tags.remove(tag)
        return redirect('list')


# レビュー一覧を見る
def review_list(request):
    if request.user.is_authenticated:
        reviews = Review.objects.filter(
            user=request.user).order_by("-datetime")
    else:
        reviews = Review.objects.none()
    return render(request, 'app/index.html', {'reviews': reviews})



@login_required
def mycinema_detail(request, cinema_id):
    cinema = MyModel.objects.get(id=cinema_id)
    reviews = Review.objects.filter(cinema=cinema)
    context = {'cinema': cinema, 'reviews': reviews}
    return render(request, 'app/mycinema_detail.html', context)

