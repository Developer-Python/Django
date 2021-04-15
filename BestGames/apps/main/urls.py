
# Import for work with paths
from django.urls import path

# Import for work with functions of views
from . import views

app_name = 'main'

urlpatterns = [
	path("", views.GameView.as_view(), name='game'),
	path('cart/', views.CartView.as_view(), name='cart'),
	path('search/', views.SearchResultView.as_view(), name='search_results'),
	path('news/', views.NewsGamesView.as_view(), name='news_games_view'),
	path('about/', views.about_view, name='about'),
	path('other/', views.other_view, name='other'),
	path('box_office/<int:user_id>/', views.BoxOfficeView.as_view(), name='box_office'),
	path('<int:main_id>/', views.GameDetailView.as_view(), name = 'detail'),
	path('<int:main_id>/rank_up/<int:user_id>', views.rank_up, name = 'rank_up'),
	path('<int:main_id>/rank_down/<int:user_id>', views.rank_down, name = 'rank_down'),
	path('<int:main_id>/like', views.like, name = 'like'),
    path('<int:main_id>/dislike', views.dislike, name = 'dislike'),
    path('<int:main_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
	path('category/<slug:url>/', views.GameCategoryView.as_view(), name='game_category_view'),
	path('userprofile/<int:user_id>', views.userprofile_get_info, name='userprofile_get_info'),
	path('userprofile/<int:user_id>/userprofile_set_info', views.userprofile_set_info, name='userprofile_set_info'),
	path('cart/product-remove/<int:main_id>/', views.RemoveToCartView.as_view(), name='remove_to_cart'),
	path('add-to-cart/<int:main_id>/', views.AddToCartView.as_view(), name='add-to-cart'),
	path('box_office/<int:user_id>/pay_online', views.pay_online, name='pay_online')
]
