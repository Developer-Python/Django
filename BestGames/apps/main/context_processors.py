

# Import models
from . models import Customer, Category, Cart, Design

def categories_and_cart(request):

    '''============================'''
    '''     Вывод на всё сайте     '''
    '''============================'''

    categories = Category.objects.all()
    design = Design.objects.get(id = 1)
    # Для авторизованных пользователей
    try:
        cart = Cart.objects.get(owner = Customer.objects.get(user = request.user))
        count_products_cart = sum([i.qty for i in cart.products.all()])
        return { 'categories': categories, 'count_products_cart': count_products_cart, 'design':design}

    # Для неавторизованных пользователей(для всех)
    except:
        return { 'categories': categories, 'design':design }
