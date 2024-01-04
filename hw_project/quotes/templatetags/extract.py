from bson.objectid import ObjectId

from django import template

from ..utils import get_mongodb
from bson.errors import InvalidId

register = template.Library()

@register.filter(name='author')
def get_author(id_):
    db = get_mongodb()
    try:
        author = db.authors.find_one({'_id': ObjectId(id_)})
        return author['fullname'] if author else 'Unknown Author'
    except (TypeError, InvalidId):
        return 'Unknown Author'


# register.filter('author', get_author)
