from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify


class Fatmaa(models.Model):
	title = models.CharField(max_length=122)
	slug= models.SlugField(unique=True)
	content = models.TextField()
	updated = models.DateTimeField(auto_now=True)
	timestamp =models.DateTimeField(auto_now_add=True)
	img= models.ImageField(null=True, blank=True , upload_to="post_images")



	def __str__(self):
		return self.title


	class Meta:
		ordering = ['title']

def create_slug(instance, new_slug=None):
	slug_value = slugify(instance.title)
	if new_slug is not None:
		slug_value = new_slug

	query = Fatmaa.objects.filter(slug = slug_value)
	if query.exists():
		slug_value="%s-%s"%(slug_value, query.last().id)
		return create_slug(instance, new_slug=slug_value)
	return slug_value


def pre_save_Fatmaa_function(*args, **kwargs):
	instance = kwargs['instance']
	instance.slug = create_slug(instance)


			
pre_save.connect(pre_save_Fatmaa_function, sender=Fatmaa)
    



