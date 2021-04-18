
# Import for work with admin-panel
from django.contrib import admin

# Import models
from . models import Game, Category, Cart, CartProduct, Comment, Customer, Design

admin.site.register(Game)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Comment)
admin.site.register(Customer)
admin.site.register(Design)
