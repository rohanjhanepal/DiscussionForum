import random
import string
from django.utils.text import slugify
from . import models

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for k in range(size))

def unique_slug_generator_post(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance)
        #slug = slugify('reverse array in c')
    #print("this is a title-------------->>>>>>> " + str(instance.title))

    #Klass = instance.__class__
    qs_exists = models.Post.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    print("this is a slug-------------->>>>>>> " + slug)
    return slug