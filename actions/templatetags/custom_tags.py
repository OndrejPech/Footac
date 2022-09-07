from django import template

register = template.Library()


@register.simple_tag
def start_end_video(link, video_time, type):
    """return videolink with start and end parameters base on type of action"""
    # TODO can I use Integer as key for faster search or different way how to speed lookups?
    action_types = {'shot': (5, 10),
                    'pass': (2, 5),
                    'foul': (5, 10),
                    'throw in': (3, 6),
                    'corner kick:': (3, 10),
                    'goal kick': (3, 10),
                    'free kick': (3, 10),
                    'substitution': (5, 20),
                    'offside': (10, 10),
                    'goal': (30, 10),
                    'penalty': (5, 10),
                    'yellow card': (30, 10),
                    'red card': (30, 10)
                    }

    try:
        start_end = action_types[type]
        start = video_time - start_end[0]
        end = video_time + start_end[1]
    except KeyError:
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
        encoded_querystring = '&'.join(filtered_querystring)  #'id=5&type=4...'
        url = f'{url}&{encoded_querystring}'

    return url
