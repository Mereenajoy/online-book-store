from django.db import models

class User_reg(models.Model):
    uid = models.IntegerField("Id Of User", primary_key=True)
    fname = models.CharField("First Name", max_length=30)
    email = models.EmailField("email", max_length=30)
    password = models.CharField("password", max_length=10)
    usertype = models.CharField(max_length=5, default="U")
    def __str__(self):
        return self.fname



class Book(models.Model):
    bid = models.IntegerField("Id Of Book", primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # publidate = models.DateField()
    quantity = models.IntegerField()
    # language = models.CharField(max_length=20, default='English')
    # publisher = models.CharField(max_length=100)
    image = models.ImageField(upload_to='book_cover',default='1.png')
    isdelete = models.BooleanField(default = True )

    def __str__(self):
        return self.title
    
    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()





class cart(models.Model):
    customer = models.ForeignKey(User_reg, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)



class CartProduct(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "cart:" + str(self.cart.id) + "cartproduct:" + str(self.id)


ORDER_STATUS = (
    ("order recived", "order recived"),
    ("order processing", "order processing"),
    ("order on the way", "order on the way"),
    ("order completed", "order completed"),
    ("order cancelled", "order cancelled")
)


class Orders(models.Model):
    cart = models.ForeignKey(cart, on_delete=models.CASCADE)
    customer = models.ForeignKey(User_reg, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=100,default="ssss")
    mobile  =models.CharField(max_length=50, default="45678")

    def __str__(self):
        return "order:" + str(self.id)
    





    
    
