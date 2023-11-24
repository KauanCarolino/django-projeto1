from django.http import Http404
from django.shortcuts import redirect, render
from authors.form import RegisterForm
from django.contrib import messages

def register_view(request):
    # Contador de vezes que entou nesta tela
    # request.session['number'] = request.session.get('number') or 1
    # request.session['number'] += 1

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    
    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        form.save()
        messages.success(request,'Your user is created, please log in.')
        
        del(request.session['register_form_data'])

    return redirect('authors:register')
