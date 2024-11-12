#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the django ERP project.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Emanuele Bertoldi'
__version__ = '0.0.1'

from django.conf.urls import *
from django.conf import settings
from django.urls import path, include
# from django.db.models.loading import cache # Legacy

# Workaround for Django's ticket #10405.
# See http://code.djangoproject.com/ticket/10405#comment:10 for more info.
# if not cache.loaded: # Legacy
#     cache.get_models()

# Basic URL patterns bootstrap.
# urlpatterns = patterns('',) # Legacy
urlpatterns = []
if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns += [path('admin/', admin.site.urls)]  # Updated for Django 2.x+
    
    if 'django.contrib.admindocs' in settings.INSTALLED_APPS:
        urlpatterns += [path('admin/doc/', include('django.contrib.admindocs.urls'))]


if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  urlpatterns += staticfiles_urlpatterns()

# Application specific URL patterns discovering.
LOADING = False

def autodiscover():
    """ Auto discover urls of installed applications. """
    global LOADING
    if LOADING:
        return
    
    LOADING = True

    import importlib

    for app in settings.INSTALLED_APPS:
        if app.startswith('django.'):
            continue

        # Step 1: Find out the app's __path__.
        try:
            app_module = importlib.import_module(app)
            app_path = app_module.__path__
        except ImportError:
            continue

        # Step 2: Check if the app has a 'urls.py'.
        try:
            importlib.import_module(f'{app}.urls')
        except ImportError:
            continue

        # Step 3: Include the app's URL patterns.
        urlpatterns.append(path(f'{app}/', include(f'{app}.urls')))
   
    # Add core.urls explicitly if djangoerp.core is installed
    if 'djangoerp.core' in settings.INSTALLED_APPS:
        from djangoerp.core import urls as core_urls
        urlpatterns.append(path('', include('djangoerp.core.urls')))    
   
    LOADING = False

autodiscover()
