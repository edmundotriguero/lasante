from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


@login_required(login_url='/login/')
def reporte(request):
    print('+++++++++++++++++++')
    template = get_template('email/saludo_mail.html')
    content = template.render()
    email = EmailMultiAlternatives(
        'hola desde djnago',
        'este es el mensaje desde lasante',
        settings.EMAIL_HOST_USER,
        ['etriguero@gaakei.com','edmundotriguero@gmail.com']
    )

    email.attach_alternative(content, 'text/html')
    
    email.send(fail_silently=False)

    return render(request, 'email/saludo_mail.html')