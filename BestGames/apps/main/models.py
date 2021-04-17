
# Import for work with createing of user
from django.dispatch import receiver
from django.db.models.signals import post_save

# Import for work with time
from django.utils import timezone
import datetime

# Import models
from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):

	'''============================'''
	'''      Модель: Категорий     '''
	'''============================'''

	name = models.CharField(verbose_name='Категория', max_length=200)
	slug = models.SlugField(unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Категорий'
		verbose_name_plural = '2) Категорий'



class Game(models.Model):

	'''========================'''
	'''       Модель: Игры     '''
	'''========================'''

	title = models.CharField('Название', max_length=60)
	title_description = models.TextField('Описание на обложке', max_length=180)
	gameplay_description = models.TextField('Геймплей')
	story_description = models.TextField('Сюжет')
	game_features_description = models.TextField('Игровые особенности')
	language_text = models.CharField('Язык текста', max_length=25)
	language_voise = models.CharField('Язык озвучки', max_length=25)
	os = models.CharField('Операцеонная система', max_length=50)
	cpu = models.CharField('Процессор', max_length=50)
	ram = models.CharField('Оперативка', max_length=50)
	gpu = models.CharField('Видеокарта', max_length=50)
	hard_disk = models.CharField('Жёсткий диск', max_length=50)
	data = models.IntegerField('Дата выхода игры', default=0)
	category = models.ManyToManyField(Category, verbose_name='Категорий')
	image_1 = models.ImageField('1) Изображение из игры', upload_to='game/')
	image_2 = models.ImageField('2) Изображение из игры', upload_to='game/')
	image_3 = models.ImageField('3) Изображение из игры', upload_to='game/')
	image_4 = models.ImageField('4) Изображение из игры', upload_to='game/')
	image_wrapper = models.ImageField('Обложка', upload_to='game/')
	torrent = models.FileField('Torrent файл', upload_to='torrents/')
	like = models.IntegerField('Нравиться', default='0')
	dislike = models.IntegerField('Не нравиться', default='0')
	views = models.IntegerField('Просмотры', default='0')
	pro = models.CharField('PRO', max_length=1)
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Стоймость игры')
	pub_date = models.DateTimeField('Дата публикаций игры на сайте')


	def __str__(self):
		return self.title


	class Meta:
		verbose_name = 'Игра'
		verbose_name_plural = '1) Игры'



class Customer(models.Model):

	'''============================='''
	'''     Модель: Пользователя    '''
	'''============================='''

	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, related_name='related_user')
	phone = models.CharField(verbose_name='Номер телефона', null=True, max_length=11)
	address = models.CharField(verbose_name='Адрес', null=True, max_length=80)
	image = models.ImageField(verbose_name='Аватарка', upload_to='user/')
	list_of_purchased_games = models.ManyToManyField(Game, verbose_name='Список приобретённых игр', blank=True, related_name='related_list_of_purchased_games')

	def __str__(self):
		return self.user.username

	class Meta:
		verbose_name = 'Пользователь'
		verbose_name_plural = '6) Пользователи (Дополнительно)'



class CartProduct(models.Model):

	'''================================='''
	'''      Модель: Игры в корзине     '''
	'''================================='''

	user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
	cart = models.ForeignKey('Cart', verbose_name='Корзина', related_name='related_products', on_delete=models.CASCADE)
	product = models.ForeignKey(Game, verbose_name='Игра', on_delete=models.CASCADE)
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена')

	def __str__(self):
		return 'Игра: {}'.format(self.product.title)

	class Meta:
		verbose_name = 'Продукт в корзине'
		verbose_name_plural = '5) Продукты в корзине'



class Cart(models.Model):

	'''=========================='''
	'''      Модель: Корзины     '''
	'''=========================='''

	owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
	products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_product = models.PositiveIntegerField(default=0)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0,verbose_name='Общая цена')

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name = 'Корзина'
		verbose_name_plural = '4) Корзина'



class Comment(models.Model):

	'''============================'''
	'''     Модель: Комментария    '''
	'''============================'''

	games = models.ForeignKey(Game, on_delete=models.CASCADE)
	author_name = models.CharField('Имя автора', max_length=25)
	author_image = models.ImageField(verbose_name='Аватарка', blank=True, upload_to='user/')
	account_level = models.IntegerField('Уровень аккаунта', default='0')
	comment_text = models.CharField('Коментарий', max_length=100)
	comment_time = models.DateTimeField('дата коментария', auto_now=True)
	comment_rank_up = models.IntegerField('Нравиться', default='0')
	comment_rank_down = models.IntegerField('Не нравиться', default='0')

	def __str__(self):
		return self.author_name

	class Meta:
		verbose_name = 'Коментарий'
		verbose_name_plural = '3) Коментарии'



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

	'''========================================='''
	'''      Система: Создание пользователя     '''
	'''========================================='''

	if created:
		Customer.objects.create(user=instance, image='/media/user/1.jpg')
