from django.conf.urls import url
from dropbox.user.views import UserRegistrationView


urlpatterns = [
    url(r'^signup', UserRegistrationView.as_view()),
    ]