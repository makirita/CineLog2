from django.urls import path,include
from cinelog import views
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.IndexListView.as_view(),name='index'),
    path('cinema/', views.CinemaResultView.as_view(),name='cinema'),
    path('login/', views.login,name='login'),
    path('logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('social-auth/', include('social_django.urls',namespace='social')),
    path('accounts/', include('django.contrib.auth.urls')),
        path('detail/<int:id>', views.DetailCinemaView.as_view(),name='detail'),
    #詳細
    path('review/<int:cinema_id>/', views.CinemaReviewView.as_view(),name='review'),
    #レビューする,cinema_idはmodels.pyのclass reviewを参照にしており、そのcinemaのidを元にレビュー作成するため。
    path('reviews/<int:cinema_id>/mycinema_detail', views.mycinema_detail,name='mycinema_detail'),
    #個々のレビューを表示する
    path('reviews/<int:pk>/mycinema_detail/<cinema_id>/update', views.CinemaReviewUpdateView.as_view(),name='review_update'),
    #レビューを更新する
    path('reviews/<int:pk>/mycinema_detail/delete', views.CinemaReviewDeleteView.as_view(),name='mycinema_detail_delete'),
    #レビューを削除する
    path('detailcast/<int:id>', views.DetailCastView.as_view(),name='cast'),
    #キャスト詳細表示
    path('create/', views.MyCreateView.as_view(),name='create'),
    #マイリスト登録(ボタンを押すと登録される)
    path('create/<int:id>/delete', views.MyListDeleteView.as_view(),name='create_delete'),
    #マイリストから登録を外す
    path('list/', views.CinemaListView.as_view(),name='list'),
    #映画リストを表示
    path('taglist/<str:tag>',views.CinemaTagListView.as_view(),name='tag-list'),
    #タグのリストを表示する
    path('tag/create/<int:cinema_id>',views.TagCreateView.as_view(),name='tag-create'),
    #タグを作成するview
    path('remove-tag/<str:tag>/', views.RemoveTagFromCinemaView.as_view(),name='remove_tag'),
    #タグを外すview
    path('', views.review_list,name='review_list'),
    #レビューリストの表示(タイムライン表示)
    path('api/movie-search/',views.movie_search,name='movie-search'),

    path('top-review/',views.TopCinemaReviewView.as_view(),name='top-review'),
    path('top-review/<int:movie_id>/',views.TopCinemaReviewView.as_view(),name='top-review'),
    path('top-review/add',views.TopCinemaAddView.as_view(),name='top-add'),
]

