
from django.urls import path
from ratelimit.decorators import ratelimit

from now.views import Index, About, LoginUser, RegisterUser, UpdateUser, \
                      Profile, LogoutUser, Events, ShowEvent, UpdateEvent, \
                      Categories, CategoryEvents, AddEvent, DeleteEvent, \
                      UserGoEvent, UserOutEvent

urlpatterns = [
    path('', Index.as_view(), name='home'),
    path('about/', About.as_view(), name='about'),
    path('login/', ratelimit(key='ip', method='POST', rate='1/m')(LoginUser.as_view()), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:slug>/', UpdateUser.as_view(), name='update_user'),
    path('profile/', Profile.as_view(), name='profile'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('events/', ratelimit(key='ip', method='GET', rate='1/m')(Events.as_view()), name='events'),
    path('event/<slug:event_slug>/', ShowEvent.as_view(), name='event'),
    path('update_event/<slug:slug>/', UpdateEvent.as_view(), name='update_event'),
    path('categories/', Categories.as_view(), name='categories'),
    path('category/<slug:category_slug>/', CategoryEvents.as_view(), name='category'),
    path('add_event/', ratelimit(key='user', method='POST', rate='1/1m')(AddEvent.as_view()), name='add_event'),
    path('delete_event/<slug:event_slug>/', DeleteEvent.as_view(), name='delete_event'),
    path('user_join/<slug:event_slug>/', UserGoEvent.as_view(), name='user_join'),
    path('user_out/<slug:event_slug>/', UserOutEvent.as_view(), name='user_out')
]
