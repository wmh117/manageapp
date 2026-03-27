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

# Create your views here.
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

def user_list(request):
    queryset = UserInfo.objects.all()
    return render(request,'user_list.html',{'queryset':queryset})

def user_add(request):
    if request.method == 'GET':
        context = {
        'gender_choices':models.UserInfo.gender_choices,
        "depart_list":models.Department.objects.all()
        }
        return render(request,'user_add.html',context)
    elif request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        age = request.POST.get('age')
        account = request.POST.get('ac')
        ctime = request.POST.get('ctime')
        gender = request.POST.get('gd')
        depart_id = request.POST.get('dp')

        models.UserInfo.objects.create(name=user,password=pwd,age=age,
                                       account=account,create_time=ctime,
                                       gender=gender,depart_id=depart_id)
        return redirect('/user/list/')

from django import forms
class UserModelForm(forms.ModelForm):
    name=forms.CharField(label='员工姓名',min_length=2,max_length=20)
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]
        # widgets = {
        #     'name':forms.TextInput(attrs={'class':'form-control'}),
        #     'password':forms.PasswordInput(attrs={'class':'form-control'}),
        #     'age':forms.NumberInput(attrs={'class':'form-control'}),
        #     'account':forms.NumberInput(attrs={'class':'form-control'}),
        #     'create_time':forms.DateInput(attrs={'class':'form-control'}),
        #     'gender':forms.Select(attrs={'class':'form-control'}),
        #     'depart':forms.Select(attrs={'class':'form-control'}),
        # }
        widgets={
        "password":forms.PasswordInput(render_value=False),
        "create_time":forms.TextInput(attrs={"type":"date"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control',"placeholder":field.label}
def user_model_form_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request,'user_model_form.html',{'form':form})
    elif request.method == 'POST':
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/list/')
        return render(request,'user_model_form.html',{'form':form})
def user_edit(request,nid):
    if request.method == 'GET':
    #从id去数据库获取到编辑的那一行数据（对象）
        row_object=models.UserInfo.objects.filter(id = nid).first()
        form=UserModelForm(instance=row_object)
        return render(request,'user_edit.html',{'form':form})
    row_object=models.UserInfo.objects.filter(id = nid).first()
    form = UserModelForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request,'user_edit.html',{'form':form})
def user_delete(request,nid):
    models.UserInfo.objects.filter(id = nid).delete()
    return redirect('/user/list/')
def prettynum_list(request):
    """ 靓号列表 """
    # 1. 构造搜索条件
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    # 2. 根据搜索条件查询数据库（按等级降序）
    # 注意：此时 queryset 还没被取出来，只是一个查询计划
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 3. 实例化分页组件
    # 传入 request 为了获取页码，传入 queryset 为了计算总数和切片
    page_object = Pagination(request, queryset, page_size=10)

    # 4. 构造上下文
    context = {
        "search_data": search_data,
        "queryset": page_object.page_queryset,  # 重点：传的是切片后的 10 条数据
        "page_string": page_object.html(),      # 生成的页码 HTML 字符串
    }

    return render(request, 'prettynum_list.html', context)
class PrettyNumForm(forms.ModelForm):
    mobile = forms.CharField(label="手机号",
                validators=[RegexValidator(r'^1[3-9]\d{9}$','手机格式错误')])
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        # fields ="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for mobile,field in self.fields.items():
            field.widget.attrs={'class':'form-control',"placeholder":field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('已存在')
        return txt_mobile
def prettynum_add(request):
    """添加靓号"""
    if request.method == 'GET':
        form = PrettyNumForm()
        return render(request,'prettynum_add.html',{'form':form})
    elif request.method == 'POST':
        form = PrettyNumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/prettynum/list/')
        return render(request,'prettynum_add.html',{'form':form})

class PrettyNumEditForm(forms.ModelForm):

    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        # fields ="__all__"
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('hama已存在')
        return txt_mobile

def prettynum_edit(request,nid):
    """编辑靓号"""
    if request.method == 'GET':
    #从id去数据库获取到编辑的那一行数据（对象）
        row_object=models.PrettyNum.objects.filter(id = nid).first()
        form=PrettyNumEditForm(instance=row_object)
        return render(request,'prettynum_edit.html',{'form':form})
    row_object=models.PrettyNum.objects.filter(id = nid).first()
    form = PrettyNumEditForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    return render(request,'user_edit.html',{'form':form})
def prettynum_delete(request,nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/prettynum/list/')
from utils.pagination import Pagination

class AdminModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ["username","password"]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for mobile, field in self.fields.items():
                field.widget.attrs = {'class': 'form-control', "placeholder": field.label}


