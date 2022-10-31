from this import d
from django.db import models
from account.models import Account

from .validators import validate_language
# Create your models here.




class Tag(models.Model):
    title = models.CharField(max_length=100, unique=True, null=True, blank=True)


    def __str__(self):
        return self.title


    @property
    def count_book(self):
        return self.book_set.all().count()




class Book(models.Model):
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True, blank=True)
    language = models.CharField(max_length=5, validators=[validate_language])
    name = models.CharField(max_length=200)
    subtitle = models.TextField()
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to = 'book_image')
    audio = models.FileField(upload_to='book_audio', null=True, blank=True)
    feedback = models.CharField(max_length=200)
    views = models.ManyToManyField(Account, related_name='views', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_saved = models.BooleanField(default=False)












    #views as how many people checked this book
    #like
    #dislike




    #get comment how many
    def get_comment(self):
        return self.parentcomment_set.filter(parent=None).count()


    #get reading count
    def get_reading_count(self):
        reading = self.reading.all().first()
        if reading is not None:
            return reading.count

        return 0


    #get already readed
    def get_readed(self):
        readed = self.readed.all().first()
        if readed is not None:
            return readed.count
        return 0





    #get_wil_read
    def get_willread(self):
        will_read = self.will_read.all().first()
        if will_read is not None:
            return will_read.count
        return 0


    #get discuss about book

    def get_discuss(self):
        discuss = self.discuss.all().first()
        if discuss is not None:
            return discuss.count
        
        return 0




    #define like or not

    def get_like_or_not(self, user):
        like = self.like_book.all().first()
        if user in like.users.all():
            return True
        return False



    def get_like_counter(self):
        like = self.like_book.all().first()
        return like.users.all().count()


    #define dislike or not
    def get_dislike_or_not(self, user):
        dislike = self.dislike_book.all().first()
        if user in dislike.users.all():
            return True
        return False





    def get_star_users_count(self):
        star = self.book_star.all()
        if star.exists():
            users = []
            for i in star:
                for user in i.users.all():
                    if user:
                        users.append(1)
            return sum(users)
        
        return 0





    def get_star_protsent(self):
        if self.get_star_users_count():
            get_how_many = self.get_star_users_count() * 0.1
            if get_how_many < 1:
                return get_how_many + 1
            
            return get_how_many + 1

        
        return 0





    def count_views(self):
        return self.views.all().count()
        


    def __str__(self):
        return f"{self.owner.username}.Book is {self.name} and Tag is {self.tag.title}"



    class Meta:
        ordering = ['-created', '-updated']




    def get_score(self, user):
        if self.book_rating.all().filter(user = user).exists():
            return self.book_rating.all().filter(user = user).first()

        return False


    
    def get_rating(self, user):
        return self.book_rating.all().filter(user = user).first()



    # filter star bul jerde bizler rating filterlep alamiz yagniy 1, 2, 3, 4, 5
    def get_filter_star(self, star):
        star = self.book_star.all().filter(star = star).first()
        if star is not None:
            return star

        return 0



    #this method gives us how many users which is entered one of them a diffirent rating
    def get_filter_users(self, star):
        get_star = self.book_star.all().filter(star = star).first()
        # users = [user for user in get_star.users.all()] or None
        users = get_star.users.all().count() or None
        if users is not None:
            return users
        
        return 0


    #this method gives yagniy bul jerde userdin sanina qarap protsenttin shigarip beredi

    def get_users_protsent_of_rating(self, number):
        if number != 0:
            protsent = number * 0.1
            if protsent < 1:
                return protsent + 1
            
            return protsent + 1
        
        return 0




    # get 5 star how many reviews
    def get_five_star(self):
        star = self.get_filter_star(5)
        if star != 0:
            get_num = self.get_filter_users(star.star)
            return self.get_users_protsent_of_rating(get_num)
        
        return 0


    

    # get 4 star
    def get_four_star(self):
        star = self.get_filter_star(4)
        if star != 0:
            get_num = self.get_filter_users(star.star)
            return self.get_users_protsent_of_rating(get_num)
        
        return 0





    # get 3 star
    def get_three_star(self):
        star = self.get_filter_star(3)
        if star != 0:
            get_num = self.get_filter_users(star.star)
            return self.get_users_protsent_of_rating(get_num)
        
        return 0





    # get 2 star
    def get_two_star(self):
        star = self.get_filter_star(2)
        if star != 0:
            get_num = self.get_filter_users(star.star)
            return self.get_users_protsent_of_rating(get_num)
        
        return 0






    # get 1 star
    def get_one_star(self):
        star = self.get_filter_star(1)
        if star != 0:
            get_num = self.get_filter_users(star.star)
            return self.get_users_protsent_of_rating(get_num)
        
        return 0





class Star(models.Model):
    CHOICE_STAR = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_star')
    star = models.IntegerField(choices=CHOICE_STAR, default=0)
    users = models.ManyToManyField(Account, related_name='star_users', blank=True)


    def __str__(self):
        return f"{self.book.name} -- {self.star}"







class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_rating')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='rating_user')
    score = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user.username} -- {self.score}"









