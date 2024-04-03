from django.shortcuts import render,redirect
from .forms import ProductAddForm
from django.contrib import messages
from .models import Products
from BillsAndSales.models import Cart
from django.contrib.auth.models import User

# Create your views here.
def AdminHome(request):

    context= {
        "stocktotal": Products.objects.all().count(),
        "salesTotal": Cart.objects.filter(status="Order Placed").count(),
        "usersTotal": User.objects.all().count()-1
    }
    return render(request,"Stock/adminhome.html",context)

def MakeStock(request):
    form = ProductAddForm
    if request.method =="POST":
        form = ProductAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request,"New stock Added")
            return redirect('MakeStock')
    context = {
        "form":form
    }
    return render(request,"Stock/updatestock.html",context)

def TotalStock(request):
    stock = Products.objects.all()
    context = {
        "stock":stock
    }
    return render(request,"Stock/stock.html",context)
def TotalSales(request):
    products = Cart.objects.filter(status="Order Placed")
    total = 0
    tax = 0
    for item in products:
        total += int(item.product.Product_unit_Price)
        tax += int(item.product.GST) 

    context = {
        "stock":products,
        "count":products.count(),
        "total":total,
        "tax":tax
    }
    return render(request,"Stock/sales.html",context)

def DeleteStock(request,pk):
    item = Products.objects.get(id = pk)
    item.delete()
    messages.info(request,"Item Removed from stock")
    return redirect("TotalStock")

def UpdateItem(request,pk):
    item = Products.objects.get(id =pk)
    messages.info(request," {} is not Possible to Update Now. Please delete the item and try to add a new item".format(item))
    return redirect("TotalStock")
    