from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.cache import cache
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from now.forms import AddEventForm, LoginUserForm, RegisterUserForm, UpdateEventForm, UpdateUserForm
from now.models import Category, CustomUser, Event, UserJoinEvent
from now.utils import DataMixin


class Index(View):
    """class Index using for index page view."""

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'now/index.html')


class About(View):
    """class About using for about app information page view."""

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'now/about.html')


class RegisterUser(CreateView):
    """class RegisterUser using for registration users."""

    form_class = RegisterUserForm
    template_name = 'now/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Form validation user information for save in database"""
        user = form.save()
        login(self.request, user)
        return redirect('events')


class LoginUser(LoginView):
    """class LoginUser using for login users."""

    form_class = LoginUserForm
    template_name = 'now/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class UpdateUser(UpdateView):
    """class UpdateUser using for update user`s information."""

    model = CustomUser
    form_class = UpdateUserForm
    template_name = 'now/update_user.html'

    def form_valid(self, form):
        """Form validation user information for save in database"""
        user = form.save()
        login(self.request, user)
        return redirect('profile')


class Profile(ListView):
    """class Profile using for view user account 'profile'."""

    model = CustomUser
    template_name = 'now/profile.html'
    context_object_name = 'profile'


class LogoutUser(View):
    """class LogoutUser using for logout event."""

    def get(self, request, *args, **kwargs):
        """Method get using for user exit of account"""
        logout(request)
        return redirect('login')


class AddEvent(CreateView):
    """class AddEvent using for create event."""

    form_class = AddEventForm
    template_name = 'now/add_event.html'
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        """Form validation event information for save in database"""
        # return object that has not saved in database
        fields = form.save(commit=False)
        fields.user = CustomUser.objects.get(id=self.request.user.id)
        # create user for event
        fields.save()
        return redirect('events')


class UpdateEvent(UpdateView):
    """class UpdateEvent using for update event`s info."""

    model = Event
    form_class = UpdateEventForm
    template_name = 'now/update_event.html'
    login_url = reverse_lazy('home')

    def get_queryset(self):
        """QuerySet get event for update form UpdateEventForm"""
        return Event.objects.filter(slug=self.kwargs['slug'])

    def form_valid(self, form):
        """Form validation event information for save in database"""
        # return object that has not saved in database
        fields = form.save(commit=False)
        # create user for event
        fields.user = CustomUser.objects.get(id=self.request.user.id)
        fields.save()
        return redirect('event_detail')


class Events(ListView):
    """class Events using for view events."""

    # Parameter paginate_by using for control count events on events page
    paginate_by = 3
    model = Event
    template_name = 'now/events.html'
    context_object_name = 'events'

    def get_queryset(self):
        """QuerySet filtered events of related category in Event model"""
        return Event.objects.filter(is_published=True).select_related('category')


class ShowEvent(DataMixin, DetailView):
    """class ShowEvent using for view detail event`s info."""

    model = Event
    template_name = 'now/event_detail.html'
    slug_url_kwarg = 'event_slug'

    def get_context_data(self, **kwargs):
        """Method get_context_data create context information for check parameters view template"""
        # Call the base implementation first to get a context
        context = super(ShowEvent, self).get_context_data(**kwargs)
        event = self.get_event()
        event_detail_id = event[0].id
        # Get QuerySet in model UserJoinEvent for check None or not None database
        user_join_event = UserJoinEvent.objects.filter(event_id=event_detail_id)
        if user_join_event:
            # Create context['event_id'] from QuerySet all() for check event_detail_id and event_id in template
            context['event_id'] = UserJoinEvent.objects.get(event_id=event_detail_id)
        return context


class Categories(ListView):
    """class Categories using for view event`s categories."""

    model = Category
    template_name = 'now/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """QuerySet get or create cache and view categories of related events"""
        cats = cache.get('cats')
        if not cats:
            # If not cache get QuerySet and create cache
            cats = Category.objects.annotate(Count('event'))
            cache.set('cats', cats, 60)
        return cats


class CategoryEvents(ListView):
    """class CategoryEvents using for view category`s events."""

    # Parameter paginate_by using for control count events on category page
    paginate_by = 3
    model = Event
    template_name = 'now/category_events.html'
    context_object_name = 'category_events'
    # Parameter allow_empty = False using for generation 404page if category`s events list is empty
    allow_empty = False

    def get_queryset(self):
        """QuerySet filtered events of related category in Event model"""
        return Event.objects.filter(category__slug=self.kwargs['category_slug'],
                                    is_published=True).select_related('category')


class DeleteEvent(DataMixin, DeleteView):
    """class EventDelete using for delete user`s event."""

    model = Event
    # Get create page confirm delete if initialization delete event process
    template_name = 'now/event_confirm_delete.html'
    slug_url_kwarg = 'event_slug'

    def delete(self, request, *args, **kwargs):
        """Method delete using for delete event"""
        # Get event get_event() from DataMixin QuerySet
        event = self.get_event()
        # Check user joined event for delete
        self.check_user_joined_event()

        event.delete()

    def get_success_url(self):
        return reverse_lazy('home')


class UserOutEvent(DataMixin, View):
    """class UserOutEvent using for user exit of event."""

    def get(self, request, *args, **kwargs):
        """Method get_out_users using for user exit of event"""
        self.check_user_joined_event()

        return redirect('home')


class UserGoEvent(DataMixin, View):
    """class UserGoEvent using for user join of event."""

    def get(self, request, *args, **kwargs):
        """Method get_join_users using for user join of event"""
        # Get event id (event_detail_id) from QuerySet
        event = self.get_event()
        event_detail_id = event[0].id
        # Method get_or_create from QuerySet model UserJoinEvent using for check repeat database entry
        user_join_event, created = UserJoinEvent.objects.get_or_create(event_id=event_detail_id,
                                                                       user_id=request.user.id)
        user_join_event.pk
        if created:
            # Delete user_join_event from model UserJoinEvent if repeat database entry
            user_join_event.delete()
        # Save user_join_event from model UserJoinEvent if not repeat database entry
        user_join_event.save()

        return redirect('home')


def page_not_found(request, exception):
    return HttpResponseNotFound(f'<h1> Страница не найдена </h1>')


def page_server_error(request, exception):
    return HttpResponseServerError(f'<h1> Ошибка сервера </h1>')
