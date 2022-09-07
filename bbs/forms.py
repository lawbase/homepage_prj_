from django import forms
from bbs.models import Notice, Answer


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice  # 사용할 모델
        fields = ['subject', 'content']  # NoticeForm에서 사용할 Notice 모델의 속성
        #widgets = {
        #    'subject': forms.TextInput(attrs={'class': 'form-control'}),
        #    'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 20}),
        #}
        labels = {
            'subject': '제목',
            'content': '내용',
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }