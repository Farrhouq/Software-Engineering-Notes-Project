"""
URL configuration for Notes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/create-note/', views.CreateNote.as_view()),
    path('api/get-notes/', views.GetNotes.as_view()),
    path('api/get-notes/<uuid:id>/', views.GetNote.as_view()),
    path('api/create-label/', views.CreateLabel.as_view()),
    path('api/update-note/<uuid:pk>/', views.UpdateNote.as_view()),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/render-note/<uuid:id>/', views.RenderNote.as_view()),
    # path('api/save-note-test/<uuid:pk>/', views.SaveNoteTest.as_view()), 
    path('api/get-shared-notes/', views.GetSharedNotes.as_view()), 
]
