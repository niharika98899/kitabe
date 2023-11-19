from django.contrib import admin
from . models import Cart,Customer,Product,Category,SubCategory
from django import forms
# Register your models here.

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subcategory":
            if "category" in request.GET:
                category_id = request.GET["category"]
                kwargs["queryset"] = kwargs["queryset"].filter(category_id=category_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ['id','title','discounted_Price','category','subcategory','product_image']

admin.site.register(Product, ProductAdmin)

'''    
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_Price','category','subcategory','product_image']
'''

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
	list_display = ['id','user','product','quantity']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id','name']

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
	list_display = ['id','category','name']