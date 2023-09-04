from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Event, Attendee
from .forms import EventForm


# Create your views here.
def event_list(request):
    events = Event.objects.all()

    return render(request, 'event_list.html', {'events': events})


def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    attendees = Attendee.objects.filter(event=event)

    context = {
        'event': event,
        'attendees': attendees
    }

    return render(request, 'event_details.html', context)


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            return redirect('event_detail', event_id=event.id)

    else:
        form = EventForm()

    return render(request, 'event_form.html', {'form': form})


@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    Attendee.objects.get_or_create(user=request.user, event=event)

    return redirect('event_detail', event_id=event.id)
