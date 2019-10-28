from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # User를 그냥 쓰는것보다 수정이 좋다 > 혹시 User 클래스명이 바뀔수있기 때문


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        # model = settings.AUTH_USER_MODEL
        # 이렇게 넣을 경우 class가 들어가는게 아니라 settings에 설정한 string이 들어감
        model = get_user_model() # get_user_model()의 User 클래스 자체를 반환함 
        fields = ('email', 'first_name', 'last_name')

