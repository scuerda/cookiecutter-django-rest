from setuptools import setup

setup(
    name='{{ cookiecutter.app_name }}',
    version='0.1',
    packages=['{{ cookiecutter.app_name }}', 'users', 'djangoproject'],
)
