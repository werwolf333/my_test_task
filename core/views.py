from django.shortcuts import render
from django.views import View
from core.models import Application
from core.set_selenium_range import set_selenium_range
from django.core.paginator import Paginator
from pyvirtualdisplay import Display


class TestList(View):
    def get(self, request):
        args = {}
        apps = Application.objects.all().filter()
        year_order_by = request.GET.get("year_order_by")
        if year_order_by == "ASC":
            apps = apps.order_by("released")
        if year_order_by == "DESC":
            apps = apps.order_by("released").reverse()
        set = request.GET.get('set')
        if request.GET.get("f")!='' and request.GET.get("f")!=None:
            apps = apps.filter(company__contains=request.GET.get('f'))
        if set == None:
            set = 10
        apps = Paginator(apps, set)
        page_number = request.GET.get('page')
        args['set'] = set
        if request.GET.get("f")!=None:
            args['f'] = request.GET.get('f')
        args['year_order_by'] = year_order_by
        args['applications'] = apps.get_page(page_number)
        return render(request, 'core/list.html', args)


class Parsing(View):
    def get(self, request):
        args = {}
        return render(request, 'core/parsing.html', args)

    def post(self, request):
        args = {}
        args['start'] = request.POST['start']
        args['end'] = request.POST['end']
        if args['start']=='' or args['end']=='':
            args['errors'] = 'задайте диапазон'
        else:
            start = int(request.POST['start'])
            end = int(request.POST['end'])
            selenium_range(start, end)
            args['message'] = 'обновлено'
        return render(request, 'core/parsing.html', args)


def selenium_range(start, end):
    disp = Display(visible=False, size=(600, 600))
    disp.start()
    generator = set_selenium_range(start, end)
    for id in range(start, end):
        args = next(generator)
        app = Application(
            id=id,
            name=args['name_app'],
            company=args['name_company'],
            released=args['release_year'],
            mail=args['mail']
        )
        app.save()
    disp.stop()
