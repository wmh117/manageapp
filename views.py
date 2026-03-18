from django.shortcuts import render
from manageapp import models
from manageapp.models import Department


# Create your views here.
def depart_list(request):
    """部门列表"""
    queryset = Department.objects.all()
    return render(request,'depart_list.html',{'queryset':queryset})#可以传递参数了

def depart_add(request):
    """添加部门"""
    return render(request,'depart_add.html')