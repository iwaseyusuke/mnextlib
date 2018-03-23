
from __future__ import absolute_import
from __future__ import print_function

from mnextlib import Quagga


class FRRouting(Quagga):

    """
    FRRouting router.
    """

    _LOCALSTATEDIR = '/var/run/frr'
    _PRIVATE_DIRS = [
        _LOCALSTATEDIR,  # "zserv.api", "*.pid", "*.vty"
        '/var/log/frr',  # logs
    ]
    _SBINDIR = '/usr/lib/frr'
