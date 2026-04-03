from django.utils.safestring import mark_safe
import copy


class Pagination:
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        # 1. 拷贝并保留搜索条件 (如 q=188)
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        self.page_param = page_param

        # 2. 获取当前页并计算切片位置
        page = request.GET.get(page_param, "1")
        self.page = int(page) if page.isdecimal() else 1
        self.page_size = page_size
        self.start = (self.page - 1) * page_size
        self.end = self.page * page_size

        # 3. 切片后的数据（传给页面显示）
        self.page_queryset = queryset[self.start:self.end]

        # 4. 计算总页数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        self.total_page_count = total_page_count + 1 if div else total_page_count
        self.plus = plus

    def html(self):
        # 计算页码范围（防止页码太多溢出）
        if self.total_page_count <= 2 * self.plus + 1:
            start_page, end_page = 1, self.total_page_count
        else:
            if self.page <= self.plus:
                start_page, end_page = 1, 2 * self.plus + 1
            elif (self.page + self.plus) > self.total_page_count:
                start_page, end_page = self.total_page_count - 2 * self.plus, self.total_page_count
            else:
                start_page, end_page = self.page - self.plus, self.page + self.plus

        page_str_list = []

        # 生成页码按钮
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])  # 动态修改页码参数
            if i == self.page:
                page_str_list.append(f'<li class="active"><a href="?{self.query_dict.urlencode()}">{i}</a></li>')
            else:
                page_str_list.append(f'<li><a href="?{self.query_dict.urlencode()}">{i}</a></li>')

        return mark_safe("".join(page_str_list))