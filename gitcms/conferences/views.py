from .models import Conference
import datetime
from django.shortcuts import get_object_or_404, render_to_response

def upcoming(request):
    conferences = Conference.objects.filter(start__gte=datetime.datetime.now()).order_by('start')
    return render_to_response(
                'conferences/list.html',
                {
                    'conferences' : conferences,
                })

def upcoming_submissions(request):
    conferences = Conference.objects.filter(submission_deadline__gte=datetime.datetime.now()).order_by('submission_deadline')
    return render_to_response(
                'conferences/list.html',
                {
                    'conferences' : conferences,
                })

def upcomingical(request):
    '''
    upcomingical(request)

    Returns the calendar of conferences as an ical file.
    '''
    import vobject
    def _add_event(sum, start, end):
        rep = cal.add('vevent')
        rep.add('dtstart').value = start
        rep.add('dtend').value = end
    events = SimpleOccurence.objects.filter(start__gte=datetime.datetime.now()).order_by('start')
    cal = vobject.iCalendar()
    for ev in events:
        _add_event(summary=ev.summary, start=ev.start, end=ev.end)
        if ev.submission_deadline:
            _add_event(summary=('%s deadline' % ev.short_name), start=ev.submission_deadline)
            _add_event(summary('%s deadline in 21 days' % ev.short_name), start=(ev.submission_deadline - datetime.timedelta(days=21)))
    response = HttpResponse(cal.serialize())
    response['Content-Type'] = 'text/calendar'
    return response