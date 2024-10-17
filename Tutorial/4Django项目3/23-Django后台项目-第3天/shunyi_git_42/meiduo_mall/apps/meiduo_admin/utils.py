from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageNum(PageNumberPagination):

    # 1.开启分页
    # 2.设置默认每页多少条记录
    page_size = 5

    # 1. 开启 每页多少条记录 可以通过传递的参数传递
    # 2. pagesize=xxx 每页多少条记录的 key
    page_size_query_param = 'pagesize'

    #最大一页多少条记录
    max_page_size = 20

    def get_paginated_response(self, data):
        # self.page.paginator.per_page  动态
        # self.page_size 固定
        return Response(OrderedDict([
            ('count', self.page.paginator.count),           # 总共多少条记录
            ('lists', data),                                # 结果列表
            ('page', self.page.number),                     # 第几页
            ('pages', self.page.paginator.num_pages),       # 总共几页
            ('pagesize', self.page.paginator.per_page)      # 一页多少条记录
        ]))