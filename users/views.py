import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import Ad
from hw28.settings import TOTAL_ON_PAGE
from locations.models import Location
from .models import User


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)

        items = [{
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': user.location_id.name,
            'total_ads': Ad.objects.all().filter(author_id=user.id).count()
        }
            for user in page_obj
        ]

        response = {
            'total': paginator.count,
            'num_pages': paginator.num_pages,
            'items': items
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        response = {
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'role': self.object.role,
            'age': self.object.age,
            'locations': self.object.location_id.name
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'role', 'age', 'locations', 'password']

    def post(self, request, *args, **kwargs):
        json_data = json.loads(request.body)

        location, created = Location.objects.get_or_create(name=json_data['locations'],
                                                           defaults={'lat': 0, 'lng': 0})

        user = User.objects.create(
            username=json_data['username'],
            first_name=json_data['first_name'],
            last_name=json_data['last_name'],
            role=json_data['role'],
            password=json_data['password'],
            age=json_data['age'],
            location_id=location,
        )

        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'age': user.age,
            'locations': user.location_id.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'password', 'first_name', 'last_name', 'age', 'locations']

    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()

        json_data = json.loads(request.body)

        location, created = Location.objects.update_or_create(name=json_data['locations'],
                                                              defaults={'lat': 0, 'lng': 0})

        self.object.username = json_data['username']
        self.object.first_name = json_data['first_name']
        self.object.last_name = json_data['last_name']
        self.object.password = json_data['password']
        self.object.age = json_data['age']
        self.object.location_id = location

        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'username': self.object.username,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'age': self.object.age,
            'locations': self.object.location_id.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({
            'status': 'ok'
        })
