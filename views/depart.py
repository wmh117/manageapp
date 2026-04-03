from logging import disable
from tabnanny import verbose

from django.contrib.admin.helpers import AdminForm
from django.db.models import CharField
from django.shortcuts import render, redirect,HttpResponse,reverse
from django.template.defaultfilters import title

from utils.pagination import Pagination
from manageapp import models
from manageapp.models import Department, UserInfo, PrettyNum
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django import forms




def depart_list(request):
    """部门列表"""
    queryset = Department.objects.all()
    return render(request,'depart_list.html',{'queryset':queryset})#可以传递参数了

def depart_add(request):
    """添加部门"""
    if request.method == 'GET':
        return render(request,'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')

def depart_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id = nid).delete()
    return redirect('/depart/list/')

def depart_edit(request,nid):
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id = nid).first()
        return render(request,'depart_edit.html',{'row_object':row_object})
    models.Department.objects.filter(id = nid).update(title=request.POST.get('title'))
    return redirect('/depart/list/')