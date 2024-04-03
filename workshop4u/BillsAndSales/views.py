from django.shortcuts import render,redirect
from products.models import Products
from .models import BillCalculations
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart,BillFinal

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# Create your views here.

@login_required(login_url="SignIn")
def Billing(request):
    product = Products.objects.all().exclude(Product_Stock=0)
    bill = BillCalculations.objects.filter(completed=False)
    total = 0
    for item in bill:
        total += int(item.product.Product_unit_Price)
    context = {
        "product":product,
        "bill":bill,
        "total":total,
    }
    return render(request,"Stock/billing.html",context)


@login_required(login_url="SignIn")
def delete_bill_product(request,id):
    BillCalculations.objects.get(id = id).delete()
    return redirect("Billing")

def AddBill(request):
    item = request.POST["pname"]
    bach = request.POST['pbatch']
    if Products.objects.filter(Product_Name = item).exists():
        product = Products.objects.get(Product_Name = item)
        bill = BillCalculations.objects.create(product = product,quantity = '1')
        bill.save()
        return redirect("Billing")
    elif Products.objects.filter(Batch_Code = bach).exists():
        product = Products.objects.get(Batch_Code = bach)
        bill = BillCalculations.objects.create(product = product,quantity = '1')
        bill.save()
        return redirect("Billing")
    else:
        messages.info(request,"no item to add")
    
    return redirect(Billing)



@login_required(login_url="SignIn")
def MakeSale(request):
    u_bill = BillCalculations.objects.filter(completed=False)
    total = 0
    tax = 0
    for item in u_bill:
        p = Products.objects.get(id =item.product.id)
        new_stock =int(p.Product_Stock)-1
        if new_stock != 0:
            p.Product_Stock = new_stock
        else:
            p.Product_Stock = 0
        p.save()
        total += int(item.product.Product_unit_Price)
        tax += int(item.product.GST) /100 * int(item.product.Product_unit_Price)
    Bill = BillFinal.objects.create(quantity=u_bill.count(),toatalprice=total,tax = tax)
    u_bill.update(completed=True,BillId=Bill.id)
    
    return redirect('TotalBills')

@login_required(login_url="SignIn")
def TotalBills(request):
    bills = BillFinal.objects.all()
    total = 0
    tax = 0
    for item in bills:
        total += int(item.toatalprice)
        tax += int(item.tax) 
    context = {
        "bills":bills,
        "count":bills.count(),
        "total":total,
        "tax":tax
    }
    return render(request,"Stock/bills.html",context)


@login_required(login_url="SignIn")
def CartView(request):
    cart = Cart.objects.filter(customer  = request.user,status="cart")
    total = 0
    tax = 0
    for item in cart:
        total += int(item.product.Product_unit_Price)
        tax += int(item.product.GST) 
    
    context = {
        "cart":cart,
        "itemcount" : len(cart),
        "totalbeforetax":(total-tax),
        "total":total,
        "tax":tax
    }
    return render(request,"cart.html",context)

@login_required(login_url="SignIn")
def userOrders(request):
    cart = Cart.objects.filter(customer  = request.user,status="Order Placed")
    total = 0
    tax = 0
    for item in cart:
        total += int(item.product.Product_unit_Price)
        tax += int(item.product.GST) 
    context = {
        "cart":cart,
        "itemcount" : len(cart),
        "totalbeforetax":(total-tax),
        "total":total,
        "tax":tax
    }
    return render(request,"orders.html",context)
    
@login_required(login_url="SignIn")
def CartAdd(request,pk):
    item = Products.objects.get(id = pk)
    cart = Cart.objects.create(product = item,customer = request.user,itemcount = "1")
    cart.save()
    return redirect('CartView')


@login_required(login_url="SignIn")
def DeleteCart(request,pk):
    cartitem = Cart.objects.get(id = pk)
    cartitem.delete()
    return redirect('CartView')



@login_required(login_url="SignIn")
def PlaceOrder(request):
    cart = Cart.objects.filter(customer = request.user,status="cart")
    currency = 'INR'
    amount = int(request.POST["total"])*100
    print("AMOUNT = ",amount)
  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))
  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'http://127.0.0.1:8000/BillsAndSales/paymenthandler/{}/{}'.format(razorpay_order_id,amount)
    
    cart.update(house = request.POST["House"],area=request.POST["Area"],landmark = request.POST["landmark"],phone = request.POST["phone"],orderId=razorpay_order_id,status = 'Payment Pending') 
  # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    return render(request,"makepayment.html",context)
    

    
@csrf_exempt
def paymenthandler(request,razorpay_order_id,amount):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            print(payment_id,"---",razorpay_order_id,"--",signature)
            params_dict = {'razorpay_order_id': razorpay_order_id,'razorpay_payment_id': payment_id,'razorpay_signature': signature}
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = amount # Rs. 200
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    cart=Cart.objects.filter(orderId=razorpay_order_id)
                    for c in cart:
                        p = Products.objects.get(id=c.product_id)
                        print(p)
                        new_stock=int(p.Product_Stock)-1
                        if new_stock != 0:
                            p.Product_Stock = new_stock
                        else:
                            p.Product_Stock = 8
                        p.save()
                    print("working 17")
                    Cart.objects.filter(orderId=razorpay_order_id).update(status="Order Placed",paymentMethod="Online Payment")
                    return redirect('userOrders')
                    # render success page on successful caputre of payment
                except:
                    print("Amount may be wrong ",amount,type(amount))
                    return redirect('userOrders')
                    # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
                # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
            # if we don't find the required parameters in POST data
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()
        