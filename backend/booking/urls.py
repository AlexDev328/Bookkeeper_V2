from booking import views
from django.urls import path

urlpatterns = [
    path("currency/", views.CurrencyList.as_view()),
    path("currency/<int:pk>", views.CurrencyDetail.as_view()),
    path("account/", views.AccountList.as_view()),
    path("account/<int:pk>", views.AccountDetail.as_view()),
    path("transaction/", views.TransactionList.as_view()),
    path("transaction/<int:pk>", views.TransactionDetail.as_view()),
    path("convertation/", views.ConvertationList.as_view()),
    path("convertation/<int:pk>", views.ConvertationDetail.as_view())
]