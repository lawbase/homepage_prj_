from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Notice
from ..forms import NoticeForm

@login_required(login_url='common:login')
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user  # author 속성에 로그인 계정 저장
            notice.create_date = timezone.now()
            notice.save()
            return redirect('bbs:index')
    else:
        form = NoticeForm()
    context = {'form': form}
    return render(request, 'bbs/notice_form.html', context)

@login_required(login_url='common:login')
def notice_modify(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbs:detail', notice_id=notice.id)
    if request.method == "POST":
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.modify_date = timezone.now()  # 수정일시 저장
            notice.save()
            return redirect('bbs:detail', notice_id=notice.id)
    else:
        form = NoticeForm(instance=notice)
    context = {'form': form}
    return render(request, 'bbs/notice_form.html', context)

@login_required(login_url='common:login')
def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.user != notice.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('bbs:detail', notice_id=notice.id)
    notice.delete()
    return redirect('bbs:index')