from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard', views.workerDashboard, name="worker-dashboard"),
    path('worker-profile/<str:slug>',
         views.getProfile, name="worker-profile"),
    path('hirings', views.WorkerHiringListView.as_view(),
         name="worker-hiring-list"),
    path('hirings/complete/<int:id>', views.complete_worker_hiring,
         name='complete-worker-hiring'),
    path('change-password', views.change_password, name='change-password'),
    path('edit-profile', views.editWorker, name='edit-profile'),
]

app_name = 'worker'
