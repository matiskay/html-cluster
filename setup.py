from setuptools import setup


setup(
    name='html_cluster',
    version='0.1',
    url='https://github.com/matiskay/html-cluster',
    description='A command line tool to cluster html files',
    long_description='',
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
        'html-similarity',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Environment :: Console',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Internet :: WWW/HTTP',
    ],
)