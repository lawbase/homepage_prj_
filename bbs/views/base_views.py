from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from ..models import Notice

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