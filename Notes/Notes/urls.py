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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from core import views

router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/create-note/', views.CreateNote.as_view()),
    path('api/get-notes/', views.GetNotes.as_view()),
    path('api/get-notes/<uuid:pk>/', views.GetNote.as_view()),
    path('api/create-label/', views.CreateLabel.as_view()),
    path('api/get-labels/', views.GetLabels.as_view()),
    path('api/get-users/', views.GetUsers.as_view()),
    path('api/update-note/<uuid:pk>/', views.UpdateNote.as_view()),
    path('api/delete-note/<uuid:pk>/', views.DeleteNote.as_view()),
    path('api/delete-label/<uuid:pk>/', views.DeleteLabel.as_view()),
    path('api/update-label/<uuid:pk>/', views.UpdateLabel.as_view()),
    path('api/login/', views.Login.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/render-note/<uuid:id>/', views.RenderNote.as_view()),
    # path('api/save-note-test/<uuid:pk>/', views.SaveNoteTest.as_view()), 
    path('api/get-shared-notes/', views.GetSharedNotes.as_view()), 
    path('api/read-note/', views.ReadNote.as_view()), 
    path('api/status/', views.Status.as_view()),
    path('api/signup/', views.SignUp.as_view()),
    path('api/test/', views.Test.as_view()),
    path('api/validate-signup/', views.ValidateData.as_view()),
    path('api/check-token/', views.CheckToken.as_view()),
    path('api/check-username/', views.CheckUsername.as_view()),
]

# add at the last
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
