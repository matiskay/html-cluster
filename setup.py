from setuptools import setup, find_packages


setup(
    name='html_cluster',
    version='0.1',
    # packages=find_packages(exclude=('tests', 'tests.*')),
    url='http://matiskay.com/code/html-cluster.html',
    description='html-cluster tool',
    # long_description=open('README.rst').read(),
    author='Edgar Marca',
    author_email='matiskay@gmail.com',
    maintainer='Edgar Marca',
    maintainer_email='matiskay@gmail.com',
    license='BSD',
    entry_points={
        'console_scripts': ['html-cluster = html_cluster.tool:cli']
    },
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'requests',
        'click',
    ],
    classifiers=[
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
    ],
)