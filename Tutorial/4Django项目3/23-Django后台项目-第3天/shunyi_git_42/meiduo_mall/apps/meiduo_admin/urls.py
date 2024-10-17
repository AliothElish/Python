# from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from apps.meiduo_admin.user import meiduo_token
from apps.meiduo_admin.views import home,user,images,sku
from apps.meiduo_admin.views import permissions

urlpatterns = [
    # path('authorizations/',obtain_jwt_token),
    path('authorizations/',meiduo_token),

    # 日活统计
    path('statistical/day_active/',home.DailyActiveAPIView.as_view()),
    # 日下单用户
    path('statistical/day_orders/',home.DailyOrderCountAPIView.as_view()),
    # 月增用户趋势图
    path('statistical/month_increment/',home.MonthCountAPIView.as_view()),


    # user
    path('users/',user.UserAPIView.as_view()),
    # 获取图片新增中的 sku展示
    path('skus/simple/',images.ImageSKUAPIView.as_view()),


    #
    path('skus/categories/',sku.GoodsCategoryAPIView.as_view()),

    #sku 中获取 spu的数据
    path('goods/simple/', sku.SPUListAPIView.as_view()),

    #sku 中获取 spu的规格和规格选项
    path('goods/<spu_id>/specs/', sku.SPUSpecAPIView.as_view()),

    #权限中 获取 ContentType 的数据
    path('permission/content_types/', permissions.ConentTypeListAPIView.as_view()),

    #组中 获取 权限列表数据
    path('permission/simple/', permissions.GroupPermissionListAPIView.as_view()),

    #组中 获取 权限列表数据
    path('permission/groups/simple/', permissions.SimpleGroupListAPIView.as_view()),
]

from rest_framework.routers import DefaultRouter
#  1.创建router实例
rouer=DefaultRouter()
# 2. 设置路由
rouer.register('skus/images',images.ImageModelViewSet,basename='images')



################sku#############################
rouer.register('skus',sku.SKUModelViewSet,basename='skus')



###############权限##################################
rouer.register('permission/perms',permissions.PermissionModelViewSet,basename='perms')

###############组##################################
rouer.register('permission/groups',permissions.GroupModelViewSet,basename='groups')

###############普通管理员##################################
rouer.register('permission/admins',permissions.AdminUserModelViewSet,basename='admins')

# 3.追加到 urlpatterns
urlpatterns+=rouer.urls