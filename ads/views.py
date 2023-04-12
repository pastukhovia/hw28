import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView

from categories.models import Category
from hw28.settings import TOTAL_ON_PAGE
from users.models import User
from .models import Ad


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by('-price')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        items = [{
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "price": ad.price
        }
            for ad in page_obj
        ]

        response = {
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': items
        }

        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.id,
            "price": self.object.price,
            "desc": self.object.desc,
            "image": self.object.image.name,
            "category": self.object.category.id,
            'is_published': self.object.is_published
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = ['name', 'author', 'price', 'desc', 'category', 'is_published']

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=json_data['name'],
            author=User.objects.get(pk=json_data['author']),
            price=json_data['price'],
            desc=json_data['desc'],
            category=Category.objects.get(pk=json_data['category']),
            is_published=json_data['is_published']
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author.id,
            "price": ad.price,
            "desc": ad.desc,
            "category_id": ad.category.id,
            'is_published': ad.is_published
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = ['name', 'author', 'price', 'desc', 'category']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        json_data = json.loads(request.body)

        self.object.name = json_data['name']
        self.object.author = User.objects.get(pk=json_data['author_id'])
        self.object.price = json_data['price']
        self.object.desc = json_data['desc']
        self.object.category = Category.objects.get(pk=json_data['category_id'])

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'author': self.object.name,
            'price': self.object.price,
            'desc': self.object.desc,
            'is_published': self.object.is_published,
            'category_id': self.object.category.id,
            'image': self.object.image.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['name', 'image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author_id': self.object.author.id,
            'author': self.object.name,
            'price': self.object.price,
            'desc': self.object.desc,
            'is_published': self.object.is_published,
            'category_id': self.object.category.id,
            'image': self.object.image.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({
            'status': 'ok'
        })
