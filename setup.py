'''
    Flask-Shield
    -----------

    Flask-Shield provides user session management for Flask. It handles the
    common tasks of logging in, logging out, and remembering your users'
    sessions over extended periods of time.

    Flask-Shield is not bound to any particular database system or permissions
    model. The only requirement is that your user objects implement a few
    methods, and that you provide a callback to the extension capable of
    loading users from their ID.

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
    url='https://github.com/maxcountryman/flask-shield',
    license='MIT',
    author='fengluo',
    author_email='fengluo17@gmail.com',
    description='User permissions management for Flask',
    long_description=__doc__,
    py_modules=['flask_shield'],
    zip_safe=False,
    platforms='any',
    install_requires=['Flask'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ])
