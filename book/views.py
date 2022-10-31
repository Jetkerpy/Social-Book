from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Book, Star, Rating, Tag
from django.contrib import messages
from likeordislike.models import Like, Dislike
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from comment.forms import ParentCommentForm, ChildCommentForm
from comment.models import ParentComment, ChildComment

# Create your views here.




#delete book

def delete_book_view(request, book):
    book = Book.objects.get(name = book)
    form = BookForm(request.POST or None, instance=book)
    if request.method == 'POST':
        book.delete()

        messages.success(request, 'Your book successfuly deleted!')
        return redirect('/')

    context = {
        'book': book
    }
    return render(request, 'book/delete_book.html', context)
    







#book update view function
@login_required
def update_book_function(request, book):
    user = request.user
    book = Book.objects.get(name = book)
    
    form = BookForm(request.POST or None, request.FILES or None, instance=book)

    if form.is_valid():
        form.save()
        messages.success(request, f"\"{book.name}\" book succesfully updated!")
        return redirect('book:detail', book.pk)


    context = {
        'form': form,
        'book': book
    }
    return render(request, 'book/update_book.html', context)








#book detail view function
def book_detail_view(request, *args, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    book = Book.objects.get(pk = pk)

    #get comments
    comments = ParentComment.objects.filter(book = book)
    
    #aldinnan created etip qoyamiz
    liked_book, created = Like.objects.get_or_create(book = book)
    disliked_book, created = Dislike.objects.get_or_create(book = book)
    
    recommend_books = Book.objects.filter(tag = book.tag).exclude(name  = book.name)
    first_book = Book.objects.filter(tag = book.tag).exclude(name  = book.name).first()
    
    is_liked = False
    is_disliked = False
    score = None
    is_rating = True
    

    if user.is_authenticated:
        
        get_rating = book.get_rating(user)
        
        if book.get_score(user) != False:
            score = book.get_score(user).score
        
        if get_rating is not None:
            is_rating = True
        else:
            is_rating = False
        
        #views 
        if user not in book.views.all():
            book.views.add(user)

        #define user's like
        if book.get_like_or_not(user):
            is_liked = True

        else:
            is_liked = False

        #define dislike
        if book.get_dislike_or_not(user):
            is_disliked = True

        else:
            is_disliked = False


     


    #Comment
    form = ParentCommentForm()
    
    if request.method == 'POST':
        form = ParentCommentForm(request.POST or None)
        user = request.POST.get('user')

        if user != 'AnonymousUser':
            if form.is_valid():
                obj = form.save(commit=False)
                obj.book = book
                obj.user = request.user
                obj.save()
                return redirect('book:detail', book.pk)

        else:
            messages.error(request, 'Comment qaldiriw ushin siz dizimnen yamasa loginnen otiwin\'izge tuwri keledi!')
            return redirect('book:detail', book.pk)

    


    


    context = {
        'book': book,
        'is_rating': is_rating,
        'score': score,
        'is_liked': is_liked,
        'is_disliked': is_disliked,
        'recommend_books': recommend_books,
        'first_book': first_book,
        'form': form,
        'comments': comments,
    }
    
    return render(request, 'book/book_detail.html', context)







# Rating for star

def star_rating_view(request):
    user = request.user
    if request.method == 'POST':
        book_name = request.POST.get('book')
        score = int(request.POST.get('score'))
        book = Book.objects.filter(name = book_name).first()
        rating, created = Rating.objects.get_or_create(book = book, user = user)
        star, created = Star.objects.get_or_create(book = book, star = score)

        if rating.score != score:
            rating.score = score
            rating.save()

            define_users = Star.objects.filter(book = book).exclude(star = score)
        
            if define_users.exists():
                for obj in define_users:
                    if user in obj.users.all():
                        obj.users.remove(user)
                

            if user not in star.users.all() and star.star != score:
                star.users.add(user)

            else:
                star.users.add(user)

    return JsonResponse({'data': 'Saved'})







#Add book
@login_required
def add_book(request):
    context = { }
    tags = Tag.objects.all()
    


    if request.method == 'POST':
        form = BookForm(request.POST or None, request.FILES or None)

        tag = request.POST.get('tag') or None
        
        if tag is not None:
            get_tag, created = Tag.objects.get_or_create(title = tag)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.owner = request.user
                obj.tag = get_tag
                obj.save()

                messages.success(request, 'Kitap awmetli saqlandi!')
                return redirect('myaccount:my-account', request.user.pk)

        else:
            messages.error(request, 'Siz qaysi turine tiyisli ekenin kiritiwiniz shart')
            return redirect('book:add-book')

    else:
        form = BookForm(request.POST or None, request.FILES or None)


    context['tags'] = tags        
    context['form'] = form        

    
    return render(request, 'book/add_book.html', context)




