
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
