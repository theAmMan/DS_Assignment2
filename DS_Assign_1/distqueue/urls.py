from django.urls import path
from . import views 

urlpatterns = [
    path('topics',views.Topics),
    path('consumer/register',views.registerConsumer),
    path('producer/register',views.registerProducer),
    path('producer/produce',views.enqueue),
    path('consumer/consume',views.dequeue),
    path('size',views.size),
]