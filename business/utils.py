from django.utils.text import slugify
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)
        if slug == instance.slug:
            return slug

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    qs_null = Klass.objects.filter(slug=slug)

    if qs_exists or qs_null == None:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
