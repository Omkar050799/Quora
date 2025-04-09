from django.urls import re_path as url

""" User login/ add/ logout profile urls"""
from .views.login import LoginViewSet
from .views.logout import LogoutView
from .views.register_user import RegisterUserView

urlpatterns = [
    url(r'^login/$', LoginViewSet.as_view()),
    url(r'^logout/$', LogoutView.as_view()),
    url(r'^register/$', RegisterUserView.as_view({"post": "post"})),
]

""" User forget_password/ verify_otp/ reset_password/ profile urls"""
from .views.change_password import ChangePasswordView
from .views.forget_password import ForgotPasswordView
from .views.verify_otp import VerifyPasswordView
from .views.reset_password import ResetPasswordView

urlpatterns += [
    url(r'^forget-password/$', ForgotPasswordView.as_view()),
    url(r'^verify-otp/$', VerifyPasswordView.as_view()),
    url(r"^change-password/$", ChangePasswordView.as_view({"post": "change_password"})),
    url(r'^reset-password/$', ResetPasswordView.as_view()),
]

""" login-verify-otp"""
from .views.login_verify_otp import LoginVerifyView
urlpatterns += [
    url(r'^login-verify-otp/$', LoginVerifyView.as_view({'get': 'retrieve'})),
]

from .views.verify_registration_email import VerifyRegistrationView

""" verify registration email"""
urlpatterns += [
    url(r'^verify-email/$', VerifyRegistrationView.as_view({"post": "create"})),
]

''' state, cities '''
from .views.cities import CityView
from .views.states import StateView

urlpatterns += [
    url(r'^cities/$', CityView.as_view({'get': 'list'})),
    url(r'^states/$', StateView.as_view({'get': 'list'})),
]

''' File Upload '''
from .views.file_upload import FileUploadView

urlpatterns += [
    url(r"^upload/$", FileUploadView.as_view({"post": "post"})),
    url(r"^upload/(?P<id>.+)/$",FileUploadView.as_view({"delete": "delete"})),
]

""" Profile """
from .views.profile import ProfileView

urlpatterns += [
    url(r"^profile/$", ProfileView.as_view({"get": "retrieve", "put": "partial_update",})),
]

""" Questions """
from .views.questions import QuestionsView

urlpatterns += [
    url(r"^questions/$", QuestionsView.as_view({"get": "list", "post": "create"})),
    url(
        r"^questions/(?P<id>.+)/$",
            QuestionsView.as_view({"get": "retrieve", "put": "partial_update", "delete": "delete",}
        ),
    ),
]

""" Answers """
from .views.answers import AnswersView

urlpatterns += [
    url(r"^answers/$", AnswersView.as_view({"get": "list", "post": "create"})),
    url(
        r"^answers/(?P<id>.+)/$",
            AnswersView.as_view({"get": "retrieve", "put": "partial_update", "delete": "delete",}
        ),
    ),
]
