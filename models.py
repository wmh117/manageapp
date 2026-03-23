from django.db import models


class Department(models.Model):
    """Department model部门表"""
    title = models.CharField(max_length=32,verbose_name='部门标题')
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(max_length=20,verbose_name='员工姓名')
    password = models.CharField(max_length=64,verbose_name='员工密码')
    age = models.IntegerField(verbose_name='员工年龄')
    account = models.DecimalField(max_digits=10,decimal_places=2,default=0,verbose_name='账户余额')
    create_time = models.DateTimeField(verbose_name='入职时间')
    depart = models.ForeignKey(verbose_name='部门',to = "Department",to_field='id',on_delete=models.CASCADE)
    gender_choices = (
    (1,'男'),
    (2,'女'),
    )
    gender = models.SmallIntegerField(verbose_name='性别',choices=gender_choices)