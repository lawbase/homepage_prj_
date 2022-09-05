#from django.http import HttpResponse

from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Notice
from .forms import NoticeForm, AnswerForm


def index(request):
    notice_list = Notice.objects.order_by('-create_date')
    context = {'notice_list': notice_list}
    return render(request, 'bbs/notice_list.html', context)

def detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    #notice = Notice.objects.get(id=notice_id)
    context = {'notice': notice}
    return render(request, 'bbs/notice_detail.html', context)

def answer_create(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.notice = notice
            answer.save()
            return redirect('bbs:detail', notice_id=notice.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'notice': notice, 'form': form}
    return render(request, 'bbs/notice_detail.html', context)

def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.create_date = timezone.now()
            notice.save()
            return redirect('bbs:index')
    else:
        form = NoticeForm()
    context = {'form': form}
    return render(request, 'bbs/notice_form.html', context)