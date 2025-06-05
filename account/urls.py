from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.signupview,name='signup'),
    path('login/',views.login_view,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutview,name='logout'),
    path('email/',views.send_email_view,name='email'),
    path('send_mail/',views.send_email_view2,name='send_mail'),
    path('update_password/',views.update_pasword,name='update_password'),
    path('identifyuser/',views.identifyuserview,name='identifyuser'),
    path('resetpassword/<en_uname>/',views.resetpasswordview,name='resetpassword')
]   