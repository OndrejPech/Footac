from django import template
from django.db.models import ImageField

register = template.Library()


@register.simple_tag
def start_end_video(link, video_time, ttype):
    """return video-link with start and end parameters base on type of action"""
    # TODO can I use Integer as key for faster search or different way how to speed lookups?
    action_types = {'shot': (5, 20),
                    'pass': (2, 10),
                    'foul': (5, 20),
                    'throw in': (3, 16),
                    'corner kick': (3, 25),
                    'goal kick': (3, 20),
                    'free kick': (3, 20),
                    'substitution': (5, 20),
                    'offside': (10, 20),
                    'goal': (20, 20),
                    'penalty kick': (5, 10),
                    'yellow card': (20, 20),
                    'red card': (20, 20),
                    'lob/cross': (10, 10)
                    }

    try:
        start_end = action_types[ttype]
        start = video_time - start_end[0]
        end = video_time + start_end[1]
    except KeyError:
        print(f'{ttype} not found by start_end_video tag')
        start = video_time - 5
        end = video_time + 10

    add = f'?start={start}&end={end}'
    return link + add


@register.simple_tag
def update_url(value, key, urlencode=None):
    """returns url with updated/replaced key-value pair"""
    field_name = key
    page_num = value
    url = f'?{field_name}={page_num}'

    if urlencode:
        querystring = urlencode.split('&')   # ['page=2','id=5',...]
        # remove the item with mentioned key
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)  # 'id=5&type=4...'
        url = f'{url}&{encoded_querystring}'

    return url


@register.simple_tag
def get_image_path(dirname: str, file: ImageField) -> str:
    return dirname + str(file)
