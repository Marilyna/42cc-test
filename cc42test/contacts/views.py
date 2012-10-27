from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from contacts.models import Contact, Request
from contacts.forms import LoginForm, ContactForm


def index(request):
    all_contacts = Contact.objects.all()
    return render(request, 'contacts/index.html',
                  {'all_contacts': all_contacts})


def detail(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    return render(request, 'contacts/detail.html', {'contact': contact})


def edit(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        is_valid = form.is_valid()
        if request.is_ajax():
            if is_valid:
                form.save()
                # we need new form for ImageField to be displayed correctly
                form = ContactForm(instance=contact)
            return render(request, 'contacts/edit_form.html',
                          {'form': form, 'contact': contact})
        if is_valid:
            form.save()
            return redirect(detail, contact_id=contact_id)
    else:
        form = ContactForm(instance=contact)
    return render(request, 'contacts/edit.html',
                  {'form': form, 'contact': contact})


def statistics(request):
    request_list = Request.objects.all().order_by('-timestamp')[:10]
    return render(request, 'contacts/request_statistics.html',
                  {'request_list': request_list})


def sign_in(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login(request, login_form.user)
            return redirect(index)
    else:
        login_form = LoginForm()
    return render(request, 'contacts/sign_in.html',
                  {'login_form': login_form})


def sign_out(request):
    logout(request)
    return redirect(index)
