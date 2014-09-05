==============
django-domains
==============


.. image:: https://badge.fury.io/py/django-domains.png
    :target: http://badge.fury.io/py/django-domains

.. image:: https://travis-ci.org/marazmiki/django-domains.png?branch=master
    :target: https://travis-ci.org/marazmiki/django-domains

.. image:: https://coveralls.io/repos/marazmiki/django-domains/badge.png?branch=master
    :target: https://coveralls.io/r/marazmiki/django-domains?branch=master

.. image:: https://pypip.in/d/django-domains/badge.png
    :target: https://pypi.python.org/pypi/django-domains


Installation
------------

1. Install the package

.. code:: bash

    pip install django-domains

2. Open settings.py and add middlewares into end of MIDDLEWARE_CLASSES tuple:

.. code:: python

    MIDDLEWARE_CLASSES += (
        'domains.middleware.RequestMiddleware',
        'domains.middleware.DynamicSiteMiddleware',
    )

First middleware ``domains.middleware.RequestMiddleware`` is required, because
it sets the `request` object into local thread.

Second middleware ``domains.middleware.DynamicSiteMiddleware`` is optional. You
can use it for dynamical changing `SITE_ID` parameter corresponding site's PK
with requested domains (see Django sites framework).

If you also want to use different templates for domains, add template loaders
in begin of TEMPLATE_LOADERS tuple:

.. code:: python

    TEMPLATE_LOADERS = (
        'domains.loaders.filesystem.Loader',
        'domains.loaders.app_directories.Loader',
        # another loaders
    )

3. Run tests:

.. code:: bash

    ./manage.py test domains

Usage
-----

If you want to use different template sets for each domains, just create
directories with name `domainname.tld` (don't forget add TEMPLATE_LOADERS
as figured in Installation) and put templates here.

Also you can use custom function that builds domain name. You must add
`DOMAINS_TEMPLATE_NAME_FUNCTION` attribute into your settings.py and
specify path to naming function.

Function must return tuple with path fragments. This fragments will be
joined into full template path with django-domains.

Expect you call this function `my_custom_template_name` and placed it in
`my/project/utils.py`:

Btw, you can access to `request` :)

.. code:: python

    def my_custom_template_name(template_dir, template_name):
        """
        This function generates template path in format:

            {template_dir}/custom/domains/{host}/{template_name}
        """
        from domains.utils import get_request

        request = get_request()

        return (template_dir, 'custom', 'domains', request.get_host,
                template_name)


Add into your `settings.py` this line:

.. code:: python

    DOMAINS_TEMPLATE_NAME_FUNCTION = 'my.project.utils.my_custom_template_name'

