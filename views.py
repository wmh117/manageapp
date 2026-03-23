from tabnanny import verbose

from django.shortcuts import render, redirect

from manageapp import models
from manageapp.models import Department,UserInfo


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