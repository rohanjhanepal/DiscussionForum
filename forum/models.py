from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from django.db.models.signals import pre_save,post_save

from . import utils







class Profile(models.Model):
    GENDER_CHOICES = (
        ('M' , 'Male'),
        ('F', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name='profile')

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    gender = models.CharField(max_length=1,choices=GENDER_CHOICES , blank=True)

    prefered_categories = models.ManyToManyField('forum.Category',related_name='prefered_categories',blank=True)
    prefered_sub_categories = models.ManyToManyField('forum.SubCategory',related_name='prefered_sub_categories',blank=True)

    contribution_score = models.IntegerField(default=0)
    
    questions_answered = models.IntegerField(default=0)

    def get_contribution_score(self):
        return self.contribution_score
    def increase_contribution_score(self):
        self.contribution_score += 1
        self.save()

    def __str__(self):
        return self.user.username

    



class Post(models.Model):
    title = models.CharField(max_length=200,blank=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    tag = models.ManyToManyField('forum.Tag', blank=True,related_name='tag')    

    category = models.ForeignKey('forum.Category', related_name="post_category" ,on_delete=models.CASCADE, null=True, blank=True)
    subcategory = models.ForeignKey('forum.SubCategory', related_name="post_sub_category" ,on_delete=models.CASCADE, null=True, blank=True)

    solved = models.BooleanField(default=False) #has the problem been solved?

    posted_by = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE) #posted by user
    posted_on = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0) #total times the post was viewed

    answerCount = models.IntegerField(default=0) #number of answers
    def increase_answer_count(self):
        self.answerCount += 1
        self.save()
    def decrease_answer_count(self,factor):
        self.answerCount -= factor
        self.save()


    def __str__(self):
        return self.title

class Answer(models.Model):
    answer = models.TextField(max_length=1000, blank=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE) #posted by user
    posted_on = models.DateTimeField(default=timezone.now)

    post = models.ForeignKey(Post, related_name='answer',on_delete=models.CASCADE)

    upvotes = models.IntegerField(default=0)


    def increase_upvotes(self):
        self.upvotes += 1
        self.save()

    def __str__(self):
        return self.answer

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey('forum.Answer', related_name='upvote',on_delete=models.CASCADE)

    def __str__(self):
        return self.answer.post.title

class Tag(models.Model):
    name = models.CharField(max_length=200,blank=False)
    slug = models.SlugField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey('forum.Category',related_name='subcategory',on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'SubCategories'



class Notification(models.Model):

    post = models.ForeignKey(Post, related_name='notification',on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='notification',on_delete=models.CASCADE)
    viewed = models.BooleanField(default=False)
    to_user = models.ForeignKey(User , related_name='notification_to_user',on_delete=models.CASCADE)
    on = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.post.title + " " + self.answer.answer

   




# SIGNALS-----------------

def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = utils.unique_slug_generator_post(str(instance.title))

def update_upvote_count(sender,instance,*args,**kwargs):
    instance.answer.increase_upvotes()
    instance.answer.post.decrease_answer_count(2)
    instance.answer.post.save()
    instance.answer.save()

def update_answer_count(sender,instance,*args,**kwargs):
    instance.post.increase_answer_count()
    instance.post.save()



pre_save.connect(slug_generator, sender=Post)
post_save.connect(update_upvote_count, sender=Upvote)
post_save.connect(update_answer_count, sender=Answer)



#END OF SIGNALS