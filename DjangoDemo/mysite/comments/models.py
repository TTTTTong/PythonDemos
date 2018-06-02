from django.db import models


# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=100)
    # email = models.EmailField(max_length=255)
    # url = models.URLField(blank=True)
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.post', on_delete=models.CASCADE)  # Django2.0版本创建外键时需要在后面加上on_delete

    def __str__(self):
        return self.text[:20]
