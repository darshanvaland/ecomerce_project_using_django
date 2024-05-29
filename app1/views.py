
from django.shortcuts import render,redirect
from .models import CategoryModel,ProductModel,Register,feedback,cartmodel,ordermodel
from .forms import UserRegisterForm,UserfeedbackForm
from django.db.models import Q
import razorpay
from  django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
# Create your views here.
def productNavView():
    productData = ProductModel.objects.all()
    return productData

def sessiondataview(request):
    email_1=request.session['user']
    dictData={'email':email_1}
    return dictData

def CategoryView(request):
    if 'user' in request.session:
        categoryData = CategoryModel.objects.all()
        sessiondataview1=sessiondataview(request)
        productNavData = productNavView()
        return render(request,'index.html',{'categoryKey':categoryData,'productAllKey':productNavData,'sessiondataview1':sessiondataview1})
    else:
        categoryData=CategoryModel.objects.all()
        productNavData=productNavView()
        return render(request,'index.html',{'categoryKey':categoryData, 'productAllkey':productNavData})

# def register(request):
#     if request.method=='POST':
#         model=Register()
#         model.name=request.POST['name']
#         model.email=request.POST['username']
#         model.contact=request.POST['contact']
#         model.password=request.POST['password']
#         model.save()
#         return redirect('Category')
#     return render(request,'register.html')

def register(request):
    obj=UserRegisterForm(request.POST) 
    if obj.is_valid():
        data=Register.objects.all().filter(email=request.POST['email'])
        if len(data)<=0:
            obj.save()
            return redirect('Category')
        else:
            return render(request,'register.html',{'message':'alredy exist'})
    return render(request,'register.html')

def login(request):
    if request.POST:
        email_1=request.POST['email']
        password_1=request.POST['password']
        try:
            data=Register.objects.get(email=email_1,password=password_1) 
            if data:
                request.session['user'] = email_1
                request.session['userid']=data.pk
                print(request.session['user'])
                return redirect('Category')
        except:
            return redirect ('login')
        # print(email,password)
    return render(request,'login.html')
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return redirect('Category')
    return redirect('login')

def productall(request):
    if 'user' in request.session:
        a=ProductModel.objects.all()
        sessiondataview1=sessiondataview(request)
        return render(request,'productall.html',{'a':a,'sessiondataview1':sessiondataview1} )
    else:
        return redirect('login')

def productcatwise(request,id):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)       
        a=ProductModel.objects.filter(category=id)
        return render(request,'productall.html',{'a':a,'sessiondataview1':sessiondataview1})
    else:
        return redirect('login')

def profile(request):
    if 'user' in request.session:
        data=Register.objects.get(email=request.session['user'])
        print(data)
        if request.method=='POST':
            data.name=request.POST['name']
            data.password=request.POST['password']
            data.save()
        return render(request,'profile.html',{'abc':data})
    else:
        return redirect('login')

def feedback(request):
    # data=UserfeedbackForm(request.POST)
    # if data.is_valid():
    if 'user' in request.session:
        data=Register.objects.get(email=request.session['user'])
        data_1=UserfeedbackForm(request.POST)
        if data_1.is_valid():
            data_1.save()
            redirect('Category')
        return render(request,'feedback.html',{'pqr':data})
    else:
        redirect(login)

def productdetaiils(request,id):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        a=ProductModel.objects.get(pk=id)
        if request.POST:
            model=cartmodel()
            model.order_id='0'
            model.user_id=request.session['userid']
            model.product_id=id
            model.quaantity='1'
            model.price=a.productPrice
            model.totalprice=str(int(model.quaantity)*a.productPrice)
            model.save()
        return render(request,'cartshow.html',{'abc':a ,'sessiondataview1':sessiondataview1})
    else:
     return redirect('login')

def cart(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        print(sessiondataview1)
        cartdata=cartmodel.objects.filter(user_id=request.session['userid']) & cartmodel.objects.filter(order_id="0")
        totalamt=0
        cartlist=[]
        for i in cartdata:
            pk_id=i.pk
            totalamt+=int(i.totalprice)
            producttotalprice=i.totalprice
            productdata=ProductModel.objects.get(pk=i.product_id)
            productImage=productdata.productImage
            productName=productdata.productName
            productquentity=i.quaantity
            productPrice=productdata.productPrice
            cartdict={'id':pk_id,'productImage':productImage,'productName':productName,'productPrice':productPrice,'producttotalprice':producttotalprice,"productquentity":productquentity}
            cartlist.append(cartdict)
        # print(cartdata,len(cartdata))
        return render(request,'usercart.html',{'sessiondataview1':sessiondataview1,'cart':cartdata,'noitem':len(cartlist),'cartlist':cartlist,"totalamt":totalamt})
    else:
        return redirect('login')    

def delete_cartitem(request,id):
        if 'user' in request.session:
            # sessiondataview1=sessiondataview(request)
            a=cartmodel.objects.get(pk=id)
            a.delete()
            return redirect('cart')
        else:
            return redirect('login')
def delete_cartall(request):
        if 'user' in request.session:
            
            a=cartmodel.objects.all()
            a.delete()
            return redirect('cart')

        else:
            return redirect('login')
def ordersucces(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        return render(request,'ordersuccess.html', {'sessiondataview1':sessiondataview1})
    else:
        return redirect('login')
def myorder(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        if request.method== 'POST':
            request.session['orderid']= request.POST['orderid']
            print("orderid : ",request.POST['orderid'])
            return redirect('orderdetialsview')
        else:
            orderdata=ordermodel.objects.filter(userid=request.session['userid']).order_by('-id')
            return render(request,'myorder.html', {'sessiondataview1': sessiondataview1,'orderdata':orderdata})
    else:
        return redirect('login')

def orderdetialsview(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        orderidvalue=request.session['orderid']
        orderdata=ordermodel.objects.get(id=orderidvalue)
        addressdata=orderdata.address+","+orderdata.city+","+orderdata.state+","+str(orderdata.pincode)
        orderdict={ 
            'name' :orderdata.username,
            "contact":orderdata.usercontact,
            "address":orderdata.address,
            "orderAmount":orderdata.orederamt,
            "paymentVia":orderdata.paymentvia,
            "paymentMethod":orderdata.pymentmethod,
            "transactionId":orderdata.transcationid,
            }
        cartquery=cartmodel.objects.filter(order_id=orderidvalue)
        cartdatarray=[]
        for i in cartquery:
            productnamequery=ProductModel.objects.get(id=i.product_id)
            cartdict={
                'productId':i.product_id,
                'productName':productnamequery.productName,
                'productImage':productnamequery.productImage.url,
                'qty':i.quaantity,
                'price':i.price,
                'totalPrice':i.totalprice
                }
            cartdatarray.append(cartdict)
            return render(request,'orderdetails.html',{'sessiondataview1':sessiondataview1,'OrderDetailData':orderdict,'cartdata':cartdatarray})
    else:
        return redirect("login")
def search(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        query= request.GET.get('search')
        qset=query.split(' ')
        print(qset)
        for q in qset:
            b=ProductModel.objects.filter(Q(category__categoryname__iconstains=q) |Q(
                productName__iconstains=q) | Q(productPrice__iconstains=q)).distinct()     
        return render(request,'productall.html',{'a':b,'sessiondataview1':sessiondataview1})  
    else:
        return redirect('login')     

def shiping(request):
    if 'user' in request.session:
        sessiondataview1=sessiondataview(request)
        data=Register.objects.get(email=request.session['user'])
        cartdata=cartmodel.objects.filter(user_id=request.session['userid']) & cartmodel.objects.filter(order_id="0")
        totalamt=0
        sessionId=request.session['userid']

        for i in cartdata:
            totalamt+=int(i.totalprice)
            if request.POST:
                model=ordermodel()
                model.userid=request.session['userid']
                model.username=request.POST['username']
                model.useremail=request.POST['useremail']
                model.usercontact=request.POST['usercontact']
                model.address=request.POST['address']
                model.city=request.POST['city']
                model.state=request.POST['state']
                model.pincode=request.POST['pincode']
                model.orederamt=request.POST['orederamt']
                model.paymentvia=request.POST['paymentvia']
                if model.paymentvia=="cash":
                   model.pymentmethod=""
                   model.transcationid=""
                   model.save()
                   orderid=ordermodel.objects.latest('id')
                   for i in cartdata:
                    cartData=cartmodel.objects.get(id=i.pk)
                    cartData.order_id=str(orderid)
                    cartData.save()
                    return redirect('ordersucces')
                else:
                    request.session['shippingUserId'] = sessionId
                    request.session['shippingName'] = request.POST['username']
                    request.session['shippingEmail'] = request.POST['useremail']
                    request.session['shippingContact'] = request.POST['usercontact']
                    request.session['shippingAddress'] = request.POST['address']
                    request.session['shippingCity'] = request.POST['city']
                    request.session['shippingState'] = request.POST['state']
                    request.session['shippingPincode'] = request.POST['pincode']
                    request.session['shippingOrderAmount'] = str(totalamt)
                    request.session['shippingPaymentVia'] = "Online"
                    request.session['shippingPaymentMethod'] = "Razorpay"
                    request.session['shippingTransactionId'] = ""
                    return redirect('razorpayView') 
            return render(request,'shiping.html',{'abc':data,'totalamt':totalamt,'sessiondataview1':sessiondataview1})
        return render(request,'shiping.html',{'abc':data,'totalamt':totalamt})
    else:
        return redirect('login')
RAZOR_KEY_ID = 'rzp_test_E4U9eSxDvTLGyY'
RAZOR_KEY_SECRET = 'b1VJ6lT0GPXMHE7WWrZV7iWt'
client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))
def razorpayView(request):
    currency = 'INR'
    amount = int(request.session['shippingOrderAmount'])*100
    # Create a Razorpay Order
    razorpay_order = client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'http://127.0.0.1:8000/paymenthandler/'    
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url    
    return render(request,'razorpayDemo.html',context=context)
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')

            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = client.utility.verify_payment_signature(
                params_dict)
            
            amount = int(request.session['shippingOrderAmount'])*100  # Rs. 200
            # capture the payemt
            client.payment.capture(payment_id, amount)

            #Order Save Code
            orderModel = ordermodel()
            orderModel.userid = request.session['shippingUserId']
            orderModel.username = request.session['shippingName']
            orderModel.useremail = request.session['shippingEmail']
            orderModel.usercontact = request.session['shippingContact']
            orderModel.address = request.session['shippingAddress']
            orderModel.city = request.session['shippingCity']
            orderModel.state = request.session['shippingState']
            orderModel.pincode = request.session['shippingPincode']
            orderModel.orederamt = request.session['shippingOrderAmount']
            orderModel.paymentvia = request.session['shippingPaymentVia']
            orderModel.pymentmethod = request.session['shippingPaymentMethod']
            orderModel.transcationid = payment_id
            orderModel.save()
            orderid = ordermodel.objects.latest('id')
        
            cartdata=cartmodel.objects.filter(user_id=request.session['userid']) & cartmodel.objects.filter(order_id="0")
            for i in cartdata:
                cartData = cartmodel.objects.get(id=i.pk)
                cartData.order_id = str(orderid)
                cartData.save()
            # render success page on successful caputre of payment
            return redirect('ordersucces')
        except:
            print("Hello")
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        print("Hello1")
       # if other than POST request is made.
        return HttpResponseBadRequest()

