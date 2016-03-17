from django import forms
from django.forms import ValidationError

from .models import Post

class PostForm(forms.Form):
    title = forms.CharField(
        required = False, label = '글제목', help_text = '기왕이면 짧게..'
    ) # 글제목은 여기보단 템플릿에서 바꾸는게 효율적일듯
    content = forms.CharField(widget = forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if '카지노' in title:
            self.add_error('카지노는 사용할 수 없습니다.')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category', 'title', 'content', 'tags', )
        # exclude = ('title', 'category', ) # 사용하지 않을 필드만을 명시하는 기능
        # fields = '__all__' # 전체를 포함하고 싶은 경우

    def clean_title(self):
        title = self.cleaned_data.get('title', '', )
        if '바보' in title:
            raise ValidationError('바보스러운 기운이 난다.')
        return title.strip()

    def clean(self):
        super(PostEditForm, self).clean()
        title = self.cleaned_data.get('title', '')
        content = self.cleaned_data.get('content', '')

        if '안녕' in title:
            self.add_error('title', '안녕은 이제 그만 안녕')
        if '안녕' in content:
            self.add_error('content', '안녕은 이제 그만 안녕')
