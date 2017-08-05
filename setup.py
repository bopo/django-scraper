from setuptools import setup

import os

setup(
    name='django-scraper',
    version='0.13.0',
    description='Creating Scrapy scrapers via the Django admin interface',
    author='bopo',
    author_email='Holger.Drewes@gmail.com',
    url='https://github.com/bopo/django-scraper/',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='BSD License',
    platforms=['OS Independent'],
    packages=[
        'django_scraper',
        'django_scraper.management',
        'django_scraper.management.commands',
        'django_scraper.migrations',
        'django_scraper.spiders',
        'django_scraper.utils',
    ],
    package_data = {
        'dynamic_scraper': [
            'static/js/*',
        ],
    },
    install_requires=[
        'future>=0.15,<0.16',
        'jsonpath-rw>=1.4',
        'pillow>=3.0,<4.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
)
