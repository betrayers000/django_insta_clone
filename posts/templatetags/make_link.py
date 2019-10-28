from django import template
import re

register = template.Library()

@register.filter
def hashtag_link(post):
    content = post.content # #아침 #점심 #저녁 => <a>#고양이</a>
    hashtags = post.hashtags.all() # QuerySer [HashTag Object(1)....]
    for hashtag in hashtags:
        # content = content.replace(
        #     f"{hashtag.content}",
        #     f'<a href="/posts/hashtags/{hashtag.id}/">{hashtag.content}</a>')

        # 정규식을 이용해서 #보노 #보노보노 둘다 태그 걸리게 하기
        content = re.sub(
            fr'{hashtag.content}\b', 
            f'<a href="/posts/hashtags/{hashtag.id}/">{hashtag.content}</a>',
            content
        )
    return content