from __future__ import unicode_literals

import hashlib

from django.utils.encoding import force_bytes
from django.utils.http import urlquote

TEMPLATE_FRAGMENT_KEY_TEMPLATE = 'template.cache.%s.%s'


def make_template_fragment_key(fragment_name, vary_on=None):
    if vary_on is None:
        vary_on = ()
    key = ':'.join(urlquote(var) for var in vary_on)

    # Current stable version of python does not have FIPS support for hashlib. Passing
    # usedforsecurity=False only works in RHEL versions of python, and is needed to
    # run this code on hardened RHEL machines. The try-except block will not be needed once
    # the following issue is resolved:
    #
    # https://bugs.python.org/issue9216
    try:
	    args = hashlib.md5(force_bytes(key), usedforsecurity=False)
	except TypeError:
	    args = hashlib.md5(force_bytes(key))

    return TEMPLATE_FRAGMENT_KEY_TEMPLATE % (fragment_name, args.hexdigest())
