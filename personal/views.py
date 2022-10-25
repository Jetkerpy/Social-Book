
from django.shortcuts import render,redirect
from account.models import Account
from notification.models import Notification
from myaccount.models import MyAccount
from django.contrib import messages
from django.http import HttpResponse, FileResponse

from book.models import (
    Tag,
    Book
)
from question.models import Question

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.paginator import Paginator, EmptyPage



# Create your views here.



def home(request):
    user = request.user
    #Notifications 
    notification = Notification.objects.filter(receiver__username = user).first()
    counting_how_many = Notification.objects.filter(receiver__username = user, is_seen = False).count()

    # book's tags
    tags = Tag.objects.all()
    # / book's tags

    # filter book
    q = request.GET.get('q')
    if q == 'all' or q == None:
         books = Book.objects.all()
         
    else:
        books = Book.objects.filter(tag__title = q)

    # active users
    active_users = [user for user in Account.objects.all() if user.book_set.all().count() >=3]

    # Paginations
    p = Paginator(books, 5)
    
    page_number = request.GET.get('page', 1)

    try:
        pages = p.page(page_number)
    except EmptyPage:
        pages = p.page(1)




    # Robot process
  
    count = 0 #how many message sent it
    robot = request.session.get('me')
    questions = None
    messages = {}
    if request.user.is_authenticated:
        book = Book.objects.filter(owner = request.user).count()
        if book == 0:
            request.session['me'] = True
        
           
           
        request.session['me'] = False

        questions = Question.objects.filter(is_answered = False).exclude(user = request.user)
        count += questions.count()
        if questions.count() == 1:
            messages['question'] = 'we have question to which there are no answer'

        else:
            messages['question'] = 'we have questions to which there are no answers'



    

    
    
    elif robot is None:
        messages['welcome'] = 'Welcome to our My Social Book'
        messages['robot'] = 'Hi I am Robot'
        messages['help'] = 'I am glad to help you!'
        messages['ask'] = 'Do you have an account or not?'
        
        count = 2

      
        
        

   


    context = {
        'noti': notification,
        'how_may': counting_how_many,
        'tags': tags,
        'books': pages,
        'active_users': active_users,
        'message': messages,
        'robot': robot,
        'count': count,
        'questions': questions
        
    }

    return render(request, 'home.html', context)






def accept_to_friends_list_view(request, *args, **kwargs):
    
    if request.method == 'GET':
        receiver = request.GET.get('receiver')
        sender = request.GET.get('sender')
        account = Account.objects.get(username = sender)
        
        my_account = MyAccount.objects.filter(account__username = receiver).first()
        my_account.friends.add(account)
        is_seen = Notification.objects.filter(receiver__username = receiver, sender__username = sender).first()
        if is_seen.how_many == 1:
            is_seen.is_seen = True
            is_seen.how_many -= 1
            is_seen.save()

        
    return HttpResponse('Succesgo')





def cancel_follower_to_accept(request):
    if request.method == 'GET':
        receiver = request.GET.get('receiver')
        sender = request.GET.get('sender')
        account_sender = Account.objects.get(username = sender)
        account_receiver = Account.objects.get(username = receiver)

        obj = Notification.objects.get(sender = account_sender, receiver = account_receiver)
        obj.delete()
        return redirect('notification:notification-view', account_receiver.pk)
    
    return HttpResponse('Successgooo!')










#download as pdf file

def download_as_pdf(request, book_name):
    book = Book.objects.get(name = book_name)
    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    obj = [
        book.name,
        book.subtitle
    ]
    for line in obj:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='book.pdf')
