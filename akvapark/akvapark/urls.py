"""
URL configuration for akvapark project.
"""
from django.urls import path
from coral import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('regis/', views.regis, name='regis'),
    path('home/', views.home, name='home'),
    path('attractions/', views.attractions, name='attractions'),
    path('tariffs/', views.tariffs, name='tariffs'),
    path('account/', views.account, name='account'),
    path('tickets/', views.tickets, name='tickets'),
      path('add-review/', views.add_review, name='add_review'),
    path("admin/", views.manage, name="manage"),
    path('admin/statistics/', views.statistics, name='statistics'),
    path('admin/checks/', views.checks, name='checks'),
    path('admin/users/', views.users, name='users'),
    path('admin/logs/', views.logs, name='logs'),
    # path('export-receipts/', views.ExportReceiptsView.as_view(), name='export_receipts'),
    # path('import-receipts/', views.ImportReceiptsView.as_view(), name='import_receipts'),
    path('admin/backup-db/', views.backup_db_view, name='backup_db'),
    path('process-payment/', views.process_payment, name='process_payment'),
]