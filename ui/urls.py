"""yay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import views
from django.urls import path
from . import views
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('registration',views.registration,name='registration'),
    path('login',views.login_view,name='login'),
    path('output', views.output,name='output'),
    path('texttospeech',views.texttospeech,name='texttospeech'),
    path('translate-summary', views.translate_summary, name='translate_summary'),
    path('grammar_checker',views.grammar_checker,name="grammar_checker"),
    path('pdf1',views.pdf1,name='pdf1'),
    path('pdf_summary_view',views.pdf1,name="pdf_summary_view"),
    path('grammar',views.grammar,name='grammar'),
    path('profile',views.profile,name='profile'),
    path('history',views.history,name='history'),
    path('home',views.home,name="home"),
    path('summarease',views.summarease,name="summarease"),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),
    path('logout',views.logout,name='logout'),

]
