from setuptools import setup, find_packages


setup(
    name='feincms-articles',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'FeinCMS>=1.7',
        'django-mptt',
        'django-pagination',
    ],
    version='1.1.3',
    description='Provides Articles using (FeinCMS content) with categories and tags.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/feincms-articles/',
)
