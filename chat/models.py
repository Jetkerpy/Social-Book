from django.db import models
from account.models import Account


# Create your models here.





class ChatOnetoOne(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='from_user')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.body




