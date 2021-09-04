"""Django_Hotel_Manage_System URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView
from django.urls import path, include, reverse_lazy, re_path
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog
from rest_framework import routers

from booking.api import ServiceViewSet, BookingTypeViewSet, BookingViewSet, CheckInViewSet, CheckOutViewSet
from customer.api import CustomerViewSet
from reservation.api import ReservationViewSet
from room.api import RoomViewSet, RoomTypeViewSet, FacilityViewSet
from blog.api import CategoryViewSet, ArticleList, CategoryArticleList, ArticleViewSet, ArticleCommentList, \
    CommentRetrieveUpdateDestroy, CommentList
from dashboard.forms import PasswordChangeForm, ResetPasswordForm, SetPasswordForm
from dashboard.views import loginrequest, registeruser, UserProfileView
from staff.api import StaffRoleViewSet, StaffViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", loginrequest, name="loginrequest"),
    path("register/", registeruser, name="register"),

    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('changepassword/',
         PasswordChangeView.as_view(template_name='registration/changepassword.html', form_class=PasswordChangeForm,
                                    success_url=reverse_lazy('dashboard')), name='changepassword'),
    path('passwordreset/',
         PasswordResetView.as_view(template_name='registration/resetpassword.html', form_class=ResetPasswordForm,
                                   success_url=reverse_lazy('passwordresetsendmail')), name='resetpassword'),
    path('passwordresetmail/', PasswordResetDoneView.as_view(template_name='registration/sendmailnoti.html'),
         name='passwordresetsendmail'),
    path('setnewpassword/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='registration/setnewpassword.html', form_class=SetPasswordForm,
                                          success_url=reverse_lazy('password_reset_complete')), name='setnewpassword'),
]

urlpatterns += [
    path('booking/', include('booking.urls')),
    path('customers/', include('customer.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reservation/', include('reservation.urls')),
    path('rooms/', include('room.urls')),
    path('staffs/', include('staff.urls')),
    path('blog/', include('blog.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('', RedirectView.as_view(url='dashboard/', permanent=True)),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='js-catalog')
]

router = routers.DefaultRouter()
router.register(r'rooms', RoomViewSet, 'room')
router.register(r'room-types', RoomTypeViewSet, 'room-type')
router.register(r'facilities', FacilityViewSet, 'facility')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r'articles', ArticleViewSet, 'article')
router.register(r'services', ServiceViewSet, 'service')
router.register(r'booking-types', BookingTypeViewSet, 'booking-type')
router.register(r'bookings', BookingViewSet, 'booking')
router.register(r'checkins', CheckInViewSet, 'checkin')
router.register(r'checkouts', CheckOutViewSet, 'checkout')
router.register(r'customers', CustomerViewSet, 'customer')
router.register(r'reservations', ReservationViewSet, 'reservation')
router.register(r'staff-roles', StaffRoleViewSet, 'staff-role')
router.register(r'staffs', StaffViewSet, 'staff')


urlpatterns += [
    path('api/articlelist/', ArticleList.as_view()),
    path('api/category-articles/<slug:slug>/', CategoryArticleList.as_view()),
    path('api/article-comments/<slug:slug>/', ArticleCommentList.as_view()),
    path('api/comments/', CommentList.as_view()),
    path('api/comments/<int:pk>/', CommentRetrieveUpdateDestroy.as_view()),
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
