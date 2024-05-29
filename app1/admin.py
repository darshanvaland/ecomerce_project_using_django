from django.contrib import admin
from .models import CategoryModel,ProductModel,Register,feedback,cartmodel,ordermodel
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryName','categoryImage']
admin.site.register(CategoryModel,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['category','productName','productPrice','productImage']
admin.site.register(ProductModel,ProductAdmin)

admin.site.register(Register)

class feedbackdata(admin.ModelAdmin):
    list_display=['name']
    list_filter=['name']
    

admin.site.register(feedback,feedbackdata)

class cartadmin(admin.ModelAdmin):
    list_display=['order_id','product_id','user_id','price']
admin.site.register(cartmodel,cartadmin)
admin.site.register(ordermodel)

