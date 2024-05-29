
from django.db import models

# Create your models here.

class CategoryModel(models.Model):
    categoryName = models.CharField(max_length=100)
    categoryImage = models.ImageField(upload_to='category')

    def __str__(self) -> str:
        return self.categoryName

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    productName = models.CharField(max_length=100)
    productPrice = models.IntegerField(max_length=5,default=0)
    productDescription = models.TextField(default="")
    productImage = models.ImageField(upload_to='product')

    def __str__(self) -> str:
        return self.productName

class Register(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    contact=models.PositiveIntegerField()
    password=models.CharField(max_length=10)

    def __str__(self):
        return self.name

class feedback(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    feedback=models.TextField()

class cartmodel(models.Model):
    order_id=models.CharField(max_length=200)
    product_id=models.CharField(max_length=200)
    user_id=models.CharField(max_length=200)
    quaantity=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    totalprice=models.CharField(max_length=200,default="")
    
    
    def __str__(self):
        return self.order_id

class ordermodel(models.Model):
    userid=models.CharField(max_length=20)
    username=models.CharField(max_length=100)
    useremail=models.CharField(max_length=100)
    usercontact=models.BigIntegerField()
    address=models.TextField()
    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pincode=models.BigIntegerField()
    orederamt=models.CharField(max_length=50)
    paymentvia=models.CharField(max_length=50,default="")
    pymentmethod=models.CharField(default=None,max_length=50)
    transcationid=models.TextField(default=None)
    orderdate=models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self) -> str:
        orderid=self.pk
        return str(orderid)
