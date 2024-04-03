from django.urls import path
from .import views

urlpatterns = [
    path("Billing",views.Billing,name="Billing"),
    path("AddBill",views.AddBill,name="AddBill"),
    path("delete_bill_product/<int:id>",views.delete_bill_product,name="delete_bill_product"),
    path("MakeSale",views.MakeSale,name="MakeSale"),
    path("TotalBills",views.TotalBills,name="TotalBills"),
    path("CartView",views.CartView,name="CartView"),
    path("CartAdd/<int:pk>",views.CartAdd,name="CartAdd"),
    path("DeleteCart/<int:pk>",views.DeleteCart,name="DeleteCart"),
    path("PlaceOrder/",views.PlaceOrder,name="PlaceOrder"),
    path('paymenthandler/<str:razorpay_order_id>/<int:amount>', views.paymenthandler, name='paymenthandler'),
    path("userOrders/",views.userOrders,name="userOrders"),
]
