# Create your views here.
from django.shortcuts import render, get_object_or_404
from contacts.models import Contact


def index(request):
    all_contacts = Contact.objects.all()
    return render(request, 'contacts/index.html', {'all_contacts': all_contacts})

    
def detail(request, contact_id):
    cont = get_object_or_404(Contact, pk = contact_id)
    return render(request, 'contacts/detail.html', {'contact': cont})