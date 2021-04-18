

# Import models
from . models import Customer, Category, Cart, Design

def categories_and_cart(request):

    '''============================'''
    '''     Вывод на всё сайте     '''
    '''============================'''

    categories = Category.objects.all()
    people = Customer.objects.count()
    # Попытка поставить дизайн
    try:
        design = Design.objects.get(id = 1)

    # Заглушка пустого дизайна
    except:
        design = ''

    # Попытка авторизовать пользователя
    try:
        cart = Cart.objects.get(owner = Customer.objects.get(user = request.user))
        count_products_cart = sum([i.qty for i in cart.products.all()])
        return { 'categories': categories, 'count_products_cart': count_products_cart, 'design':design, 'people':people}

    # Для неавторизованных пользователей(для всех)
    except:
        return { 'categories': categories, 'design':design, 'people':people}
