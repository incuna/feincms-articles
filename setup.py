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
    version='1.2.2',
    description='Provides Articles using (FeinCMS content) with categories and tags.',
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/feincms-articles/',
    license='BSD',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
