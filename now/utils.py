from now.models import Event, UserJoinEvent


class DataMixin:
    def __init__(self):
        self.kwargs = Event.objects.all()

    def get_event(self, **kwargs):
        """Get event QuerySet"""
        return Event.objects.filter(slug=self.kwargs['event_slug'])

    def check_user_joined_event(self):
        """Check user joined event for delete"""
        event_detail_id = self.get_event()[0].id
        # Get QuerySet all() in model UserJoinEvent for check None or not None database
        user_join_event = UserJoinEvent.objects.all()
        if user_join_event:
            # Get event id from QuerySet for delete database entry
            user_join_event = UserJoinEvent.objects.get(event_id=event_detail_id)
            user_join_event.delete()



