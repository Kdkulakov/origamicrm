from django.urls import path
from materials.views import MaterialCreate, MaterialList, MaterialUpdate, MaterialUpdateCount, MaterialInstanceAdd, \
    MaterialInstanceDel

app_name = 'materials'


urlpatterns = [
    path('create/', MaterialCreate.as_view(), name='create'),
    path('instance_add/', MaterialInstanceAdd.as_view(), name='instance_add'),
    path('update/<int:pk>/', MaterialUpdate.as_view(), name='update'),
    path('updatecount/<int:pk>/', MaterialUpdateCount.as_view(), name='updatecount'),
    path('instance_del/', MaterialInstanceDel.as_view(), name='instance_del'),
    # path('<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('', MaterialList.as_view(), name='index'),
]
