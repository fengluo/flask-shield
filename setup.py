'''
    Flask-Shield
    -----------

    Flask-Shield provides user session management for Flask. It handles the
    common tasks of logging in, logging out, and remembering your users'
    sessions over extended periods of time.

    Links
    `````
    * `documentation <http://packages.python.org/Flask-Shield>`_
    * `development version
    <https://github.com/fengluo/flask-shield>`_
'''
from setuptools import setup

setup(
    name='Flask-Shield',
    version=0.1,
    url='https://github.com/fengluo/flask-shield',
    license='MIT',
    author='fengluo',
    author_email='fengluo17@gmail.com',
    description='Flask-Shield is an extension of Flask for permission management based on RBAC.',
    long_description=__doc__,
    py_modules=['flask_shield'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask', ''],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
