from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=1000)
    content = RichTextField(null=True, blank=True)
    
    date_created = models.DateTimeField(default=timezone.now)
    # tags = models.ManyToManyField(Tags, blank=True)
    # detail = RichTextField(blank=True, null=True)
    views_count = models.IntegerField(default=0)
    upvotes = models.ManyToManyField(User, related_name="question_upvotes", blank=True)
    downvotes = models.ManyToManyField(User, related_name="question_downvotes", blank=True)

    slug = AutoSlugField(unique=True, populate_from="title")
    def comment_count(self):
        return self.comment.count()
    def __str__(self):
        return f"{self.title} - {self.user.username} - Question"

    def get_absolute_url(self):
        return reverse("base:question_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.id:  # Check if the object has not been saved (i.e., it's a new question)
            slug = kwargs.get("slug")
            if slug:
                try:
                    question = Question.objects.get(slug=slug)
                    self.question = question
                except Question.DoesNotExist:
                    pass  # Regenerate slug if a question with the same slug doesn't exist

        super().save(*args, **kwargs)



class Comment(models.Model):
    question = models.ForeignKey(Question, related_name="comment", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Use User model for the commenter
    content = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)

    
    
    def __str__(self):
        comment_number = self.question.comment.filter(date_created__lt=self.date_created).count() + 1
        return f"comment[{comment_number}] --- {self.question.title} -- {self.user.username}"
    
    def get_absolute_url(self):
        return reverse("base:question_detail", kwargs={"slug": self.question.slug})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)