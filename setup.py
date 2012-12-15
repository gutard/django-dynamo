from setuptools import setup, find_packages
import os
from distutils.util import convert_path

def read(*args):
    return open(os.path.join(os.path.dirname(__file__), *args)).read()



CLASSIFIERS =[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Framework :: Django',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules'
    ]

VERSION = __import__('dynamo').version

setup(
    name = 'django-dynamo',
    version = VERSION,
    url='https://bitbucket.org/schacki/django-dynamo/overview',
    download_url ='https://bitbucket.org/schacki/django-dynamo/downloads',
    author='Juergen Schackmann',
    author_email='juergen.schackmann@googlemail.com',
    description='Dynamo let users and admins create and mantain their Django DYNAmic MOdels dynamically at runtime.',
    long_description=read( 'readme.rst'),
    license='BSD',
    platforms=['any'],
    classifiers=CLASSIFIERS,
    install_requires=[],
    packages=find_packages(exclude=['tests\*','dynamo_project.*']),
    zip_safe = False
)



