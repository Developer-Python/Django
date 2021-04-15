
# Import for work with payments
import pyqiwi

# Import for work with сrypts
from django.contrib.auth.hashers import make_password, check_password

# Import for work with requests and redirect

from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

# Import for work with class-based views are designed to display data
from django.views.generic.base import View
from django.views.generic import ListView

# Import for work with Pagination and Search
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Import models
from . models import Customer, Category, Game, Cart, CartProduct, Comment
from django.contrib.auth.models import User



class CartView(View):

	'''=============='''
	'''    Корзина   '''
	'''=============='''

	def get(self, request, *args, **kwargs):

		cart, created = Cart.objects.get_or_create(
			owner=Customer.objects.get(user_id=request.user), 
		)

		cart.final_price = sum([ int(i.final_price * i.qty) for i in cart.products.all() ])
		cart.save()

		return render(request, "main/cart.html", {"cart": cart})



class BoxOfficeView(View):

	'''=============='''
	'''     Касса    '''
	'''=============='''

	def get(self, request, *args, **kwargs):

		user = User.objects.get(id = request.user.id)

		userprofile = Customer.objects.get(user_id=request.user)

		cart, created = Cart.objects.get_or_create(
			owner=userprofile, 
		)

		cart.final_price = sum([ int(i.final_price * i.qty) for i in cart.products.all() ])
		cart.save()
	
		return render(request, "main/box_office.html", {"cart": cart, 'userprofile': userprofile})



def pay_online(request, user_id, *args, **kwargs):

	'''====================='''
	'''   Система платежа   '''
	'''====================='''

	user = User.objects.get(id = request.user.id)
	customer = Customer.objects.get(user_id = request.user.id)


	cart, created = Cart.objects.get_or_create(
		owner=Customer.objects.get(user_id=request.user), 
	)

	# Проверка: прошёл ли правельно платёж
	try:
		wallet = pyqiwi.Wallet(token=request.POST.get('api'), number=request.POST.get('number'))
		payment = wallet.send(pid=99, recipient='79193774889', amount=cart.final_price, comment = f"ID: {user.id} , Пользователь: {user.username}, Купил: {[i.product.title+',' for i in cart.products.all()]}")
		for i in cart.products.all():
			customer.list_of_purchased_games.add(i.product)
		cart.delete()
	except:
		return render(request, "main/box_office.html", {'error': True})

	return HttpResponseRedirect( reverse('main:box_office', args = (user.id,) ))



def userprofile_set_info(request, user_id, *args):

	'''===================================================='''
	'''   Сохранение и редактирование данных пользователя  '''
	'''===================================================='''

	userprofile = Customer.objects.get(id = request.user.id)
	user = User.objects.get(id = request.user.id)
		
	if request.POST.get('phone') != '':
		userprofile.phone = request.POST.get('phone')
		userprofile.save()
	
	if request.POST.get('email') != '':
		userprofile.user.email = request.POST.get('email')
		userprofile.user.save()
	
	if request.POST.get('address') != '':
		userprofile.address = request.POST.get('address')
		userprofile.save()
	
	if request.POST.get('image') != '':
		userprofile.image = request.POST.get('image', 'user/1.jpg')
		userprofile.save()

	if request.POST.get('password_old') != '' and check_password(request.POST.get('password_old'), user.password):
		
		if request.POST.get('password_new_1') == request.POST.get('password_new_2'):

			user.set_password(request.POST.get('password_new_1'))
			user.save()

			return HttpResponseRedirect('/')

	return HttpResponseRedirect( reverse('main:userprofile_get_info', args = (userprofile.id,)) )



class AddToCartView(View):

	'''======================================='''
	'''    Система добавления игры в корзину   '''
	'''======================================='''

	def get(self, request, *args, **kwargs):

		main_id = kwargs.get('main_id')
		customer = Customer.objects.get(user=request.user)
		product = Game.objects.get(id = main_id)

		cart, created = Cart.objects.get_or_create(
			owner=Customer.objects.get(user_id=request.user), 
		)
		
		cart_product, created = CartProduct.objects.get_or_create(
			user=cart.owner, cart=cart, product=product, final_price=product.price
		)

		if created:
			cart.products.add(cart_product)

		else:
			cart_product.qty += 1
			cart_product.save()

		return HttpResponseRedirect('/cart/')



class RemoveToCartView(View):

	'''======================================='''
	'''    Система удаления игры из корзины   '''
	'''======================================='''

	def get(self, request, main_id):

		cart_product = CartProduct.objects.get(id=main_id)
		cart_product.delete()

		return HttpResponseRedirect('/cart/')



class GameView(View):

	'''========================'''
	'''    Вывод списка игр    '''
	'''========================'''

	def get(self, request):
		
		games = Game.objects.order_by('pro')

		paginator = Paginator(games, 12)

		page = request.GET.get('page') 

		# Проверка: на кол-во страниц
		try:
		    posts = paginator.page(page)
		except PageNotAnInteger:
		    posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		# Проверка: на авторизованность пользователя
		try:	
			userprofile = Customer.objects.get(user=request.user)
			return render(request, "main/list.html", {"games": games, 'userprofile':userprofile, 'page': page, 'posts': posts})
		except TypeError:
			return render(request, "main/list.html", {"games": games, 'page': page, 'posts': posts})
		



class NewsGamesView(View):

	'''=============================='''
	'''    Вывод списка новых игр    '''
	'''=============================='''

	def get(self, request):
		
		games_news = [i for i in Game.objects.order_by('-id') if i.new_game_pub() == True]

		paginator = Paginator(games_news, 12)

		page = request.GET.get('page') 
		
		# Проверка: на кол-во страниц		
		try:
		    posts = paginator.page(page)
		except PageNotAnInteger:
		    posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
		
		# Проверка: на авторизованность пользователя
		try:	
			userprofile = Customer.objects.get(user=request.user)
			return render(request, "main/news.html", {"games_news": games_news, 'userprofile':userprofile, 'page': page, 'posts': posts})
		except TypeError:
			return render(request, "main/news.html", {"games_news": games_news, 'page': page, 'posts': posts})



class GameCategoryView(View):

	'''=========================================='''
	'''     Вывод списка игр через категории     '''
	'''=========================================='''

	def get(self, request, url):

		# Проверка: на игры с выбранной категорией
		try:
			category = Category.objects.get(slug=url)
			games = Game.objects.filter(category__slug = url)
		except:
			raise Http404(f'Игры c категориями: "{url}" не найдена.')

		paginator = Paginator(games, 12)

		page = request.GET.get('page') 

		# Проверка: на кол-во страниц
		try:
		    posts = paginator.page(page)

		except PageNotAnInteger:
		    posts = paginator.page(1)

		except EmptyPage:
			posts = paginator.page(paginator.num_pages)

		# Проверка: на авторизованность пользователя
		try:	
			userprofile = Customer.objects.get(user=request.user)
			return render(request, "main/list.html", {"games": games, 'userprofile':userprofile, 'page': page, 'category': category, 'posts': posts})
		except TypeError:
			return render(request, "main/list.html", {"games": games, 'page': page, 'category': category, 'posts': posts})


class GameDetailView(View):

	'''===================================='''
	'''    Вывод детальной страницы игры   '''
	'''===================================='''

	def get(self, request, main_id):
			
		games = Game.objects.get(id = str(main_id))

		games.views += 1
		games.save()
		
		latest_comments_list = games.comment_set.order_by('-comment_rank_up')[:50]

		try:
			userprofile = Customer.objects.get(user=request.user.id)
			return render(request, 'main/detail.html', {'games':games, 'userprofile': userprofile, 'latest_comments_list': latest_comments_list})
		except:
			return render(request, 'main/detail.html', {'games':games, 'latest_comments_list': latest_comments_list})



class SearchResultView(ListView):

	'''============================'''
	'''       Система: пойска      '''
	'''============================'''

	model = Game
	template_name = 'main/list.html'

	def get_queryset(self):

		query = self.request.GET.get('q')

		object_list = Game.objects.filter(Q(title__icontains=query) | Q(gameplay_description__icontains=query) | Q(story_description__icontains=query))

		return object_list



def like(request, main_id):

	'''============================'''
	'''       Система: лайков      '''
	'''============================'''

	if str(main_id) in request.COOKIES:
		return HttpResponseRedirect('/')
	else:
		main = Game.objects.get(id = str(main_id) ) 
		main.like += 1 
		main.save()
		response = HttpResponseRedirect('/')
		response.set_cookie(str(main_id), 'like')
		return response



def dislike(request, main_id):

	'''============================'''
	'''      Система: дизлайков    '''
	'''============================'''

	if str(main_id) in request.COOKIES:
		return HttpResponseRedirect('/')
	else:
		main = Game.objects.get(id = str(main_id) ) 
		main.dislike += 1 
		main.save()
		response = HttpResponseRedirect('/')
		response.set_cookie(str(main_id), 'dislike')
		return response



def rank_up(request, main_id, user_id):

	'''==================================================='''
	'''      Система: положительного ранка комментария    '''
	'''==================================================='''

	if f'{main_id}-{user_id}' in request.COOKIES:
		return HttpResponseRedirect(f'/{main_id}/')
	else:
		games = Game.objects.get(id = str(main_id))
		latest_comments_list = games.comment_set.get(id = user_id)
		latest_comments_list.comment_rank_up += 1
		latest_comments_list.save() 
		response = HttpResponseRedirect(f'/{main_id}/')
		response.set_cookie(f'{main_id}-{user_id}', f'rank_up-{user_id}')
		return response



def rank_down(request, main_id, user_id):

	'''================================================'''
	'''      Система: негативного ранка комментария    '''
	'''================================================'''

	if f'{main_id}-{user_id}' in request.COOKIES:
		return HttpResponseRedirect(f'/{main_id}/')
	else:
		games = Game.objects.get(id = str(main_id))
		latest_comments_list = games.comment_set.get(id = user_id)
		latest_comments_list.comment_rank_down += 1
		latest_comments_list.save() 
		response = HttpResponseRedirect(f'/{main_id}/')
		response.set_cookie(f'{main_id}-{user_id}', f'rank_down-{user_id}')
		return response



def leave_comment(request, main_id):

	'''==============================='''
	'''      Система: комментариев	  '''
	'''==============================='''

	try:
		a = Game.objects.get(id = main_id )
	except:
		raise Http404('Статья не найдена!')

	try:

		user = User.objects.get(username=request.user)

		if user.is_superuser:
			level = 2
		elif user.is_staff:
			level = 1
		else:
			level = 0

		userprofile = Customer.objects.get(user=request.user)
		a.comment_set.create(author_image = userprofile.image.url, author_name = userprofile, comment_text = request.POST['text'], account_level = 2)

	except:
		a.comment_set.create(author_image = '/media/user/1.jpg', author_name = request.POST['name'], comment_text = request.POST['text'], account_level = 0)

	return HttpResponseRedirect( reverse('main:detail', args = (a.id,)) )



def userprofile_get_info(request, user_id):

	'''========================='''
	'''    Страница: "Профиля"  '''
	'''========================='''

	userprofile = Customer.objects.get(id = request.user.id)
	
	return render(request, "customer/account.html", {'userprofile': userprofile})
	


def about_view(request):

	'''========================'''
	'''   Страница: "О сайте"  '''
	'''========================'''

	return render(request, 'main/about.html')



def other_view(request):

	'''========================='''
	'''    Страница: "Другое"   '''
	'''========================='''

	return render(request, 'main/other.html')