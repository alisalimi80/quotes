from celery import shared_task
from .models import Quote , Tag
import requests

@shared_task
def get_random_quote():
    response = requests.get(url='https://api.quotable.io/quotes/random')
    data = response.json()[0]
    tag_list = []
    for tag in data['tags']:
        tag_obj , _ = Tag.objects.get_or_create(name=tag)
        tag_list.append(tag_obj)
    try:
        quote = Quote.objects.get(quote_id=data['_id'])
    except Quote.DoesNotExist:
        quote = Quote.objects.create(
            quote_id = data["_id"],
            author = data["author"],
            content = data["content"],
            author_slug = data["authorSlug"],
            dateadded = data["dateAdded"],
            datemodified = data["dateModified"],
            length = data["length"],
        )
    quote.tags.add(*tag_list)