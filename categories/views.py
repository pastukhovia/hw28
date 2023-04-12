import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Category


class CatListView(ListView):
    model = Category
    queryset = Category.objects.order_by('name')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = [{
            'id': category.id,
            'name': category.name
        }
            for category in self.object_list]

        return JsonResponse(response, safe=False)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            'id': self.object.id,
            'name': self.object.name
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CatCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        category = Category.objects.create(name=json_data['name'])

        return JsonResponse({
            'id': category.id,
            'name': category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        json_data = json.loads(request.body)

        self.object.name = json_data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class CatDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'ok'
        })
