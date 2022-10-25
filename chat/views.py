from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import ChatOnetoOne
from account.models import Account
from django.http import JsonResponse
# Create your views here.









@csrf_exempt
def get_message_from_js(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('name')
        text = request.POST.get('text')
        receiver = Account.objects.get(username = username)
        ChatOnetoOne.objects.create(
            user = request.user,
            sender = request.user,
            receiver = receiver,
            body = text
        )
        
        return JsonResponse({'data': 'Data saved'})

    else:
        return JsonResponse({'data': 'data Not saved'})





def send_message_view(request):
    user = request.user

    if request.method == 'POST':
        receiver_pk = request.POST.get('receiver')
        text = request.POST.get('text') or None
        account = Account.objects.get(pk = receiver_pk)
     
        if text is not None:
            ChatOnetoOne.objects.create(
                user = user,
                sender = user,
                receiver = account,
                body = text
            )

     

        else:
            messages.error(request, "You can't send an empty message!!")
            return redirect('myaccount:my-account', receiver_pk)



        return redirect('myaccount:my-account', receiver_pk)
