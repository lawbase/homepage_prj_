#from django.http import HttpResponse

from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Notice, Answer
from .forms import NoticeForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    page = request.GET.get('page', '1')  # 페이지
    notice_list = Notice.objects.order_by('-create_date')
    paginator = Paginator(notice_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'notice_list': page_obj}
    return render(request, 'bbs/notice_list.html', context)

def detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    #notice = Notice.objects.get(id=notice_id)
    context = {'notice': notice}
    return render(request, 'bbs/notice_detail.html', context)

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