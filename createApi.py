#!/usr/bin/env python3
"""
Script tự động tạo dự án Django với Docker setup
Sử dụng: python createApi.py "tên_dự_án"
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def create_directory_structure(api_name):
    """Tạo cấu trúc thư mục cho dự án Django"""
    print(f"Tạo thư mục cho {api_name}...")
    
    # Tạo thư mục chính
    os.makedirs(api_name, exist_ok=True)
    
    # Tạo thư mục con
    project_name = f"{api_name}api"
    app_name = f"{api_name}s"  # Thêm 's' để tạo số nhiều
    
    # Tạo cấu trúc thư mục
    dirs_to_create = [
        f"{api_name}/{project_name}",
        f"{api_name}/{app_name}",
        f"{api_name}/{project_name}/__pycache__",
        f"{api_name}/{app_name}/__pycache__"
    ]
    
    for directory in dirs_to_create:
        os.makedirs(directory, exist_ok=True)
    
    return project_name, app_name

def create_dockerfile(api_name):
    """Tạo file Dockerfile"""
    dockerfile_content = f"""FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "{api_name}api.wsgi:application"]
"""
    
    with open(f"{api_name}/Dockerfile", "w", encoding="utf-8") as f:
        f.write(dockerfile_content)

def create_requirements(api_name):
    """Tạo file requirements.txt"""
    requirements_content = """Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
gunicorn==21.2.0
"""
    
    with open(f"{api_name}/requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)

def create_manage_py(api_name):
    """Tạo file manage.py"""
    project_name = f"{api_name}api"
    manage_content = f"""#!/usr/bin/env python
\"\"\"Django's command-line utility for administrative tasks.\"\"\"
import os
import sys


def main():
    \"\"\"Run administrative tasks.\"\"\"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
"""
    
    with open(f"{api_name}/manage.py", "w", encoding="utf-8") as f:
        f.write(manage_content)

def create_project_files(api_name):
    """Tạo các file cấu hình chính của Django project"""
    project_name = f"{api_name}api"
    
    # __init__.py
    with open(f"{api_name}/{project_name}/__init__.py", "w") as f:
        f.write("")
    
    # wsgi.py
    wsgi_content = f"""\"\"\"
WSGI config for {project_name} project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
\"\"\"

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{project_name}.settings')

application = get_wsgi_application()
"""
    
    with open(f"{api_name}/{project_name}/wsgi.py", "w", encoding="utf-8") as f:
        f.write(wsgi_content)
    
    # settings.py
    settings_content = f"""\"\"\"
Django settings for {project_name} project.
\"\"\"

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-{api_name}-api-key-12345'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    '{api_name}s',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{project_name}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{project_name}.wsgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {{
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}}
"""
    
    with open(f"{api_name}/{project_name}/settings.py", "w", encoding="utf-8") as f:
        f.write(settings_content)
    
    # urls.py
    urls_content = f"""\"\"\"
URL configuration for {project_name} project.
\"\"\"
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/{api_name}s/', include('{api_name}s.urls')),
]
"""
    
    with open(f"{api_name}/{project_name}/urls.py", "w", encoding="utf-8") as f:
        f.write(urls_content)

def create_app_files(api_name):
    """Tạo các file cho Django app"""
    app_name = f"{api_name}s"
    
    # __init__.py
    with open(f"{api_name}/{app_name}/__init__.py", "w") as f:
        f.write("")
    
    # apps.py
    apps_content = f"""from django.apps import AppConfig


class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
"""
    
    with open(f"{api_name}/{app_name}/apps.py", "w", encoding="utf-8") as f:
        f.write(apps_content)
    
    # models.py
    model_name = api_name.capitalize()
    models_content = f"""from django.db import models

class {model_name}(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = '{model_name}'
        verbose_name_plural = '{app_name}'
"""
    
    with open(f"{api_name}/{app_name}/models.py", "w", encoding="utf-8") as f:
        f.write(models_content)
    
    # serializers.py
    serializer_content = f"""from rest_framework import serializers
from .models import {model_name}

class {model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model_name}
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
"""
    
    with open(f"{api_name}/{app_name}/serializers.py", "w", encoding="utf-8") as f:
        f.write(serializer_content)
    
    # views.py
    views_content = f"""from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import {model_name}
from .serializers import {model_name}Serializer

class {model_name}ViewSet(viewsets.ModelViewSet):
    queryset = {model_name}.objects.all()
    serializer_class = {model_name}Serializer
    
    def list(self, request):
        \"\"\"Get all {app_name}\"\"\"
        {api_name}s = {model_name}.objects.all()
        serializer = {model_name}Serializer({api_name}s, many=True)
        return Response({{
            'message': '{app_name.capitalize()} retrieved successfully',
            'data': serializer.data
        }})
    
    def create(self, request):
        \"\"\"Create a new {api_name}\"\"\"
        serializer = {model_name}Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({{
                'message': '{model_name} created successfully',
                'data': serializer.data
            }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        \"\"\"Get a specific {api_name}\"\"\"
        try:
            {api_name} = {model_name}.objects.get(pk=pk)
            serializer = {model_name}Serializer({api_name})
            return Response({{
                'message': '{model_name} retrieved successfully',
                'data': serializer.data
            }})
        except {model_name}.DoesNotExist:
            return Response({{
                'message': '{model_name} not found'
            }}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        \"\"\"Update a {api_name}\"\"\"
        try:
            {api_name} = {model_name}.objects.get(pk=pk)
            serializer = {model_name}Serializer({api_name}, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({{
                    'message': '{model_name} updated successfully',
                    'data': serializer.data
                }})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except {model_name}.DoesNotExist:
            return Response({{
                'message': '{model_name} not found'
            }}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        \"\"\"Delete a {api_name}\"\"\"
        try:
            {api_name} = {model_name}.objects.get(pk=pk)
            {api_name}.delete()
            return Response({{
                'message': '{model_name} deleted successfully'
            }}, status=status.HTTP_204_NO_CONTENT)
        except {model_name}.DoesNotExist:
            return Response({{
                'message': '{model_name} not found'
            }}, status=status.HTTP_404_NOT_FOUND)
"""
    
    with open(f"{api_name}/{app_name}/views.py", "w", encoding="utf-8") as f:
        f.write(views_content)
    
    # urls.py
    urls_content = f"""from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.{model_name}ViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""
    
    with open(f"{api_name}/{app_name}/urls.py", "w", encoding="utf-8") as f:
        f.write(urls_content)

def create_admin_file(api_name):
    """Tạo file admin.py"""
    app_name = f"{api_name}s"
    model_name = api_name.capitalize()
    
    admin_content = f"""from django.contrib import admin
from .models import {model_name}

@admin.register({model_name})
class {model_name}Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
"""
    
    with open(f"{api_name}/{app_name}/admin.py", "w", encoding="utf-8") as f:
        f.write(admin_content)

def create_tests_file(api_name):
    """Tạo file tests.py"""
    app_name = f"{api_name}s"
    model_name = api_name.capitalize()
    
    tests_content = f"""from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import {model_name}

class {model_name}ModelTest(TestCase):
    def setUp(self):
        self.{api_name} = {model_name}.objects.create(
            name='Test {model_name}',
            description='Test Description'
        )
    
    def test_{api_name}_creation(self):
        self.assertEqual(self.{api_name}.name, 'Test {model_name}')
        self.assertEqual(self.{api_name}.description, 'Test Description')
        self.assertTrue(self.{api_name}.created_at)

class {model_name}APITest(APITestCase):
    def setUp(self):
        self.{api_name} = {model_name}.objects.create(
            name='Test {model_name}',
            description='Test Description'
        )
    
    def test_get_{api_name}s(self):
        url = reverse('{app_name}-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)
    
    def test_create_{api_name}(self):
        url = reverse('{app_name}-list')
        data = {{
            'name': 'New {model_name}',
            'description': 'New Description'
        }}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['name'], 'New {model_name}')
"""
    
    with open(f"{api_name}/{app_name}/tests.py", "w", encoding="utf-8") as f:
        f.write(tests_content)

def create_readme(api_name):
    """Tạo file README.md"""
    model_name = api_name.capitalize()
    app_name = f"{api_name}s"
    
    readme_content = f"""# {model_name} API

Django REST API cho {app_name}.

## Cài đặt

1. Tạo và kích hoạt virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\\Scripts\\activate  # Windows
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Tạo superuser:
```bash
python manage.py createsuperuser
```

5. Chạy server:
```bash
python manage.py runserver
```

## Docker

### Build và chạy với Docker:
```bash
docker build -t {api_name}-api .
docker run -p 8000:8000 {api_name}-api
```

## API Endpoints

- `GET /api/{app_name}/` - Lấy danh sách {app_name}
- `POST /api/{app_name}/` - Tạo {api_name} mới
- `GET /api/{app_name}/{{id}}/` - Lấy {api_name} theo ID
- `PUT /api/{app_name}/{{id}}/` - Cập nhật {api_name}
- `DELETE /api/{app_name}/{{id}}/` - Xóa {api_name}

## Model

### {model_name}
- `id`: ID tự động
- `name`: Tên {api_name} (CharField, max_length=100)
- `description`: Mô tả (TextField, optional)
- `created_at`: Thời gian tạo (DateTimeField, auto_now_add=True)
- `updated_at`: Thời gian cập nhật (DateTimeField, auto_now=True)

## Testing

Chạy tests:
```bash
python manage.py test
```
"""
    
    with open(f"{api_name}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

def main():
    if len(sys.argv) != 2:
        print("Sử dụng: python createApi.py 'tên_dự_án'")
        print("Ví dụ: python createApi.py 'product'")
        sys.exit(1)
    
    api_name = sys.argv[1].lower()
    
    # Kiểm tra tên hợp lệ
    if not api_name.replace('_', '').isalnum():
        print("Tên dự án chỉ được chứa chữ cái, số và dấu gạch dưới")
        sys.exit(1)
    
    if os.path.exists(api_name):
        print(f"Thư mục '{api_name}' đã tồn tại!")
        response = input("Bạn có muốn xóa và tạo lại không? (y/N): ")
        if response.lower() in ['y', 'yes']:
            shutil.rmtree(api_name)
        else:
            print("Hủy tạo dự án.")
            sys.exit(1)
    
    print(f"Tạo dự án Django API: {api_name}")
    
    try:
        # Tạo cấu trúc thư mục
        project_name, app_name = create_directory_structure(api_name)
        
        # Tạo các file Docker
        create_dockerfile(api_name)
        create_requirements(api_name)
        
        # Tạo file Django chính
        create_manage_py(api_name)
        
        # Tạo project files
        create_project_files(api_name)
        
        # Tạo app files
        create_app_files(api_name)
        
        # Tạo các file bổ sung
        create_admin_file(api_name)
        create_tests_file(api_name)
        create_readme(api_name)
        
        print(f"✅ Dự án '{api_name}' đã được tạo thành công!")
        print(f"\n📁 Cấu trúc thư mục:")
        print(f"   {api_name}/")
        print(f"   ├── Dockerfile")
        print(f"   ├── manage.py")
        print(f"   ├── requirements.txt")
        print(f"   ├── README.md")
        print(f"   ├── {project_name}/")
        print(f"   │   ├── __init__.py")
        print(f"   │   ├── settings.py")
        print(f"   │   ├── urls.py")
        print(f"   │   └── wsgi.py")
        print(f"   └── {app_name}/")
        print(f"       ├── __init__.py")
        print(f"       ├── admin.py")
        print(f"       ├── apps.py")
        print(f"       ├── models.py")
        print(f"       ├── serializers.py")
        print(f"       ├── urls.py")
        print(f"       ├── views.py")
        print(f"       └── tests.py")
        
        print(f"\n🚀 Để chạy dự án:")
        print(f"   cd {api_name}")
        print(f"   python manage.py makemigrations")
        print(f"   python manage.py migrate")
        print(f"   python manage.py runserver")
        
        print(f"\n🐳 Để chạy với Docker:")
        print(f"   cd {api_name}")
        print(f"   docker build -t {api_name}-api .")
        print(f"   docker run -p 8000:8000 {api_name}-api")
        
    except Exception as e:
        print(f"❌ Lỗi khi tạo dự án: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
