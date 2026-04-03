from django import forms
from django.shortcuts import render,redirect
from manageapp import models


class LoginForm(forms.Form):
    username = forms.CharField(required='True' ,label='用户名',
                               widget=forms.TextInput(attrs={'class':'form-control'}))

    password = forms.CharField(required='True',label='密码',
                               widget=forms.PasswordInput(render_value=True,attrs={'class':'form-control'}))

def clean_password(self):
    pwd = self.cleaned_data('password')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    form = LoginForm(request.POST)
    if form.is_valid():
        admin_object =  models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("username", '用户名密码错误')
            # form.add_error("password",'用户名密码错误')
            return render(request,'login.html',{'form':form})
        request.session['info']= {'id':admin_object.id ,'name':admin_object.username}
        #创建了info这个字典
        return redirect("/admin/list/")
    return render(request,'login.html',{'form':form})


def logout(request):
    """注销"""
    request.session.clear()
#清除当前session
    return redirect("/admin/list/")

