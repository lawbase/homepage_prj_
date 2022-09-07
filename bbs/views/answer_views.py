from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Notice, Answer
from ..forms import AnswerForm

@login_required(login_url='common:login')
def answer_create(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.notice = notice
            answer.save()
            return redirect('bbs:detail', notice_id=notice.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'notice': notice, 'form': form}
    return render(request, 'bbs/notice_detail.html', context)

@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbs:detail', notice_id=answer.notice.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('bbs:detail', notice_id=answer.notice.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'bbs/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('bbs:detail', notice_id=answer.notice.id)