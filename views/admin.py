from django.shortcuts import render, redirect, HttpResponse
from manageapp import models  # 必须导入你自己的 models
from utils.pagination import Pagination # 导入你的分页组件
from django.core.exceptions import ValidationError
from django import forms

class AdminModelForm(forms.ModelForm):
    # 确认密码字段（不是数据库字段，仅用于校验）
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 这里可以加 md5 加密逻辑，现在先存明文
        return pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd:
            raise ValidationError("两次密码输入不一致")
        return confirm






# 编辑时只改用户名
class AdminEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

# 重置密码专用
class AdminResetModelForm(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {"password": forms.PasswordInput}

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if confirm != pwd: raise ValidationError("密码不一致")
        return confirm




def admin_list(request):


    """ 管理员列表视图 """
    # 1. 处理搜索

    #获取cookie 看session 有没有
    info = request.session.get('info')
    if not info:
        return redirect('/login/')


    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["username__contains"] = search_data

    # 2. 获取数据
    queryset = models.Admin.objects.filter(**data_dict).order_by("-id")

    # 3. 分页
    page_object = Pagination(request, queryset)

    context = {
        "queryset": page_object.page_queryset,
        "page_string": page_object.html(),
        "search_data": search_data
    }
    return render(request, 'admin_list.html', context)


# 1. 添加管理员
def admin_add(request):
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})


# 2. 编辑管理员 (仅改用户名)
def admin_edit(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return HttpResponse("数据不存在")

    title = "编辑管理员"
    if request.method == "GET":
        # 编辑时不显示密码相关的字段
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})


# 3. 删除管理员
def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


# 4. 重置密码
def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    title = f"重置密码 - {row_object.username}"

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, 'change.html', {"form": form, "title": title})