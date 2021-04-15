

# Import models
from . models import Customer, Category, Cart

def categories_and_cart(request):

    '''============================'''
    '''     Вывод на всё сайте     '''
    '''============================'''

    categories = Category.objects.all()

    try:
        cart = Cart.objects.get(owner = Customer.objects.get(user = request.user))
        count_products_cart = sum([i.qty for i in cart.products.all()])
        return { 'categories': categories, 'count_products_cart': count_products_cart, }

    except:
        return { 'categories': categories }