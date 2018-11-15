from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from base.models import Locale, User

def index(request):
    locale_list = Locale.objects.order_by('city')
    context = {'locale_list': locale_list}
    return render(request, 'subscription/index.html', context)

def submit(request):
    email = request.POST.get('email')
    locale_id = request.POST.get('locale_id')
    user = User(
        email=email,
        locale_id_id=locale_id,
        active=True
    )
    user.save()
    return HttpResponseRedirect(reverse('subscription:submitted'))

def submitted(request):
    return render(request, 'subscription/submitted.html')
