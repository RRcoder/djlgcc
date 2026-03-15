# AGENTS.md - djlgcc Development Guide

## Project Overview

**djlgcc** is a Django 3.1 web application with MySQL 5.7 database. It's a business management system for managing accounts receivable (cuentas corrientes), clients, orders, delivery slips (remitos), and price lists.

## Tech Stack

- **Framework**: Django 3.1
- **Database**: MySQL 5.7
- **Python**: 3.8+
- **Docker**: docker-compose for development

## Build and Run Commands

### Development Server

```bash
# Run Django development server
python manage.py runserver 0.0.0.0:8007

# Using docker-compose
docker-compose up --build
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Testing

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test apps.cuentascorrientes
python manage.py test apps.empresa
python manage.py test apps.members

# Run a single test (specify full path)
python manage.py test apps.cuentascorrientes.tests.YourTestClass.your_test_method

# Run with verbosity
python manage.py test -v 2
```

### Django Management Commands

```bash
# Check for issues
python manage.py check

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

## Code Style Guidelines

### General Principles

- **Language**: All code, comments, and documentation are in Spanish
- **PEP 8**: Follow Python PEP 8 style guide where applicable
- **No comments**: Unless explaining business logic that isn't obvious

### Import Ordering

Order imports as follows (within each group, alphabetically):

1. Standard library imports
2. Third-party Django imports
3. Third-party non-Django imports
4. Local app imports (from other apps)
5. Local module imports (from same app)

```python
# Standard library
from datetime import date
import os
from pathlib import Path

# Django core
from django.db import models
from django.db.models import F, Sum
from django.shortcuts import render, redirect, get_object_or_404

# Django third-party
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, FormView

# Local apps
from apps.empresa.models import DatosUsuarios, Comprobantes

# Same app
from .models import ListaPrecios, Clientes
from .forms import ListaPreciosForm
```

### Models

- Use `related_name` for reverse foreign key relationships
- Use `on_delete=models.PROTECT` for foreign keys (never CASCADE unless intentional)
- Use `null=True, blank=True` for optional fields
- Use `DecimalField` for monetary values
- Use `auto_now` for `updated` timestamp and `auto_now_add` for `created`
- Define `__str__` method using f-strings for all models

```python
class ExampleModel(models.Model):
    name = models.CharField(max_length=100)
    related_model = models.ForeignKey('RelatedModel', on_delete=models.PROTECT, related_name='examples')
    optional_field = models.CharField(max_length=50, null=True, blank=True)
    decimal_field = models.DecimalField(max_digits=12, decimal_places=2)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Example'
        verbose_name_plural = 'Examples'
        ordering = ['name']

    def __str__(self):
        return f"{self.id} - {self.name}"
```

### Views

- Use Class-Based Views (CBVs) for standard CRUD operations
- Use function-based views for complex logic
- Always use `@login_required` decorator or `LoginRequiredMixin` for protected views
- Use `transaction.atomic` for database operations that modify multiple tables
- Use `get_object_or_404` for single object retrieval
- Use `reverse_lazy` for CBVs and `reverse` for function-based views

```python
# Class-Based View example
class MyListView(LoginRequiredMixin, ListView):
    model = MyModel
    template_name = 'app/model_list.html'
    context_object_name = 'objects'
    ordering = ['-created']

# Function-based view with decorator
@login_required
def my_view(request):
    with transaction.atomic():
        # database operations
    return render(request, 'template.html', context)
```

### Forms

- Use `ModelForm` for forms tied to models
- Use `Form` for standalone forms
- Add CSS classes via `widgets` in `Meta` class
- Use Spanish labels

```python
class MyForm(forms.ModelForm):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2']
        widgets = {
            'field1': forms.TextInput(attrs={'class': 'form-control'}),
            'field2': forms.Select(attrs={'class': 'form-select'}),
        }
```

### Templates

- Store in `templates/<app_name>/` directory
- Use HTML5 structure
- Use Bootstrap 5 classes (based on existing templates)

### URL Patterns

- Define app URLs in `<app>/urls.py`
- Include app URLs with namespace in project `urls.py`

```python
# In app/urls.py
app_name = 'app'
urlpatterns = [
    path('list/', views.MyListView.as_view(), name='model_list'),
]

# In project urls.py
path('app/', include('app.urls', namespace='app'))
```

### Error Handling

- Use `try/except` blocks with specific exception types
- Use `messages` framework for user feedback
- Redirect to success/error pages after form submissions

```python
try:
    with transaction.atomic():
        # operations
    messages.success(request, "Operacion exitosa")
except Exception as e:
    messages.error(request, f"Error: {str(e)}")
```

### Naming Conventions

- **Models**: PascalCase (e.g., `Clientes`, `Pedidos`)
- **Functions/variables**: snake_case (e.g., `cliente_id`, `total_importe`)
- **URL names**: snake_case with namespace (e.g., `cuentascorrientes:clientes_list`)
- **Template names**: snake_case with underscores (e.g., `clientes_list.html`)

### Database Operations

- Use Django ORM whenever possible
- Use `bulk_create` for inserting multiple records
- Use `select_related` and `prefetch_related` to reduce queries
- Use raw SQL only when absolutely necessary (see `cuenta_corriente_cliente` example)

## Project Structure

```
djlgcc/
├── manage.py
├── djlgcc/                 # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── empresa/            # Company/sucursal management
│   ├── members/            # User authentication
│   └──cuentascorrientes/  # Main app - accounts, clients, orders
├── templates/              # Shared templates
└── docker/                # Docker files
```

## Database Configuration

Database is configured via environment variables:

- `MYSQL_USER`: Database user
- `MYSQL_PASSWORD`: Database password
- `MYSQL_HOST`: Database host

## Important Notes

- This is an Argentine business application; currency is ARS (Argentine Pesos)
- Timezone is `America/Argentina/Buenos_Aires`
- Uses `pymysql` as MySQL driver
- Static files served from `www/` directory
