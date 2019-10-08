from django.db import models


class Snippet(models.Model):
	Search = models.CharField(max_length = 100)

	def __str__(self):
		return self.Search