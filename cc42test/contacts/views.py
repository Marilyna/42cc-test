# Create your views here.
from django.shortcuts import render, get_object_or_404
from contacts.models import Contact, Request


def index(request):
    all_contacts = Contact.objects.all()
    return render(request, 'contacts/index.html', {'all_contacts': all_contacts})

    
def detail(request, contact_id):
    cont = get_object_or_404(Contact, pk = contact_id)
    return render(request, 'contacts/detail.html', {'contact': cont})
    
def statistic(request):
    request_list = Request.objects.all().order_by('-timestamp')[:10]
    return render(request, 'contacts/request_statistic.html', {'request_list': request_list})