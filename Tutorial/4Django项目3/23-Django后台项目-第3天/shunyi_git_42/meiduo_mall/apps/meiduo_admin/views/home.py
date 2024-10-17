

"""
日活用户

当天登录的用户的总量
2020-10-30  10:10:10
2020-10-30  15:10:10

2020-10-30  00:00:00
"""
from apps.users.models import User
from datetime import date
from rest_framework.response import Response


from rest_framework.views import APIView
# 基类
from rest_framework.generics import GenericAPIView
# 一般和Mixin配合使用      mixin(增删改查)
from rest_framework.generics import ListAPIView,RetrieveAPIView
# 三级视图 已经继承了Mixin http方法都不用写了


class DailyActiveAPIView(APIView):

    def get(self,request):

        today = date.today()
        count = User.objects.filter(last_login__gte=today).count()

        return Response({'count':count})


"""
日下单用户量统计


"""
class DailyOrderCountAPIView(APIView):

    def get(self,request):
        today=date.today()
        count=User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({'count':count})


"""

1. 获取今天的日期
2. 往前回退30天
3. 遍历查询数据
    
    例如: 10-01  到 10-2 数据
    3.1 获取区间开始的日期
    3.2 获取区间结束的日期
    3.3 查询
    3.4 把查询的数据放入列表中

"""
from datetime import timedelta
class MonthCountAPIView(APIView):

    def get(self,request):
        # 1. 获取今天的日期
        today=date.today()
        # 2. 往前回退30天
        before_date=today-timedelta(days=30)
        data=[]
        # 3. 遍历查询数据
        for i in range(30):
            #i=0
            #
            #     例如: 10-01  到 10-2 数据
            #     3.1 获取区间开始的日期
            start_date=before_date + timedelta(days=i)
            #     3.2 获取区间结束的日期
            end_date=before_date + timedelta(days=(i+1))
            #     3.3 查询
            count=User.objects.filter(date_joined__gte=start_date,
                                      date_joined__lt=end_date).count()
            #     3.4 把查询的数据放入列表中
            data.append({
                'count':count,
                'date':start_date
            })

        return Response(data)