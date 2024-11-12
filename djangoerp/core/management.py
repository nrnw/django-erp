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

from djangoerp.core.utils.dependencies  import check_dependency

check_dependency('django.contrib.auth')
check_dependency('django.contrib.contenttypes')
check_dependency('django.contrib.sessions')
check_dependency('django.contrib.sites')
check_dependency('django.contrib.messages')
check_dependency('django.contrib.staticfiles')
check_dependency('django.contrib.admin')
check_dependency('django.contrib.admindocs')
check_dependency('django_comments')
check_dependency('django_markup')
check_dependency('django.contrib.redirects')

from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Installation of application specific stuff.
INSTALLING = False

@receiver(post_migrate)
def install_apps(sender, **kwargs):
    global INSTALLING
    if INSTALLING:
        return
    
    INSTALLING = True
    
    print ("Installing apps ...")
    
    from django.conf import settings
    for app in settings.INSTALLED_APPS:
        if not app.startswith('django.') and (app != "djangoerp.core"):
            try:
                # Dynamically import the management module for each app
                management = __import__("%s.management" % app, {}, {}, ["install"])
                install_func = getattr(management, 'install', None)
                
                if callable(install_func):
                    print(f"Installing app {app}")
                    install_func(sender, **kwargs)
            except (ImportError, AttributeError):
                pass  # Handle missing 'install' function or import errors gracefully
