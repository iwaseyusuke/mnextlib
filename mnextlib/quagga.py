
from __future__ import absolute_import
from __future__ import print_function

import os

from mnextlib import util
from mnextlib import Router


class Quagga(Router):

    """
    Quagga router.
    """

    _LOCALSTATEDIR = '/var/run/quagga'
    _PRIVATE_DIRS = [
        _LOCALSTATEDIR,     # "zserv.api", "*.pid", "*.vty"
        '/var/log/quagga',  # logs
    ]
    _SBINDIR = '/usr/lib/quagga'

    def __init__(self, name, intfIPs=None, confDir=None,
                 **kwargs):
        """
        name: Name of this node.
        intfIPs: Pairs of interface and IP address.
        confDir: Path to config files directory.
        **kwargs: Additional parameters to pass super class.
        """
        privateDirs = kwargs.get('privateDirs', [])
        kwargs['privateDirs'] = privateDirs + self._PRIVATE_DIRS
        super(Quagga, self).__init__(name, intfIPs=intfIPs, **kwargs)
        assert confDir is not None
        self.confDir = util.resolve_path(confDir)
        self.sbinDir = self._SBINDIR
        if os.path.isfile("/usr/sbin/zebra"):
            # Case for APT package
            self.sbinDir = "/usr/sbin"

        self.zebraConf = None
        _conf = '%s/zebra.conf' % self.confDir
        if os.path.isfile(_conf):
            self.zebraConf = _conf

        self.bgpdConf = None
        _conf = '%s/bgpd.conf' % self.confDir
        if os.path.isfile(_conf):
            self.bgpdConf = _conf

        self.ospfdConf = None
        _conf = '%s/ospfd.conf' % self.confDir
        if os.path.isfile(_conf):
            self.ospfdConf = _conf

    def start(self, controllers):
        super(Quagga, self).start(controllers=controllers)
        if self.zebraConf:
            self.cmd('chmod 644 %s' % self.zebraConf)
            self.cmd('%s/zebra --daemon --config_file %s'
                     % (self.sbinDir, self.zebraConf))
        if self.bgpdConf:
            self.cmd('chmod 644 %s' % self.bgpdConf)
            self.cmd('%s/bgpd --daemon --config_file %s'
                     % (self.sbinDir, self.bgpdConf))
        if self.ospfdConf:
            self.cmd('chmod 644 %s' % self.ospfdConf)
            self.cmd('%s/ospfd --daemon --config_file %s'
                     % (self.sbinDir, self.ospfdConf))

    def stop(self, deleteIntfs=True):
        if self.zebraConf:
            self.cmd('pkill --pidfile %s/zebra.pid' % self._LOCALSTATEDIR)
        if self.bgpdConf:
            self.cmd('pkill --pidfile %s/bgpd.pid' % self._LOCALSTATEDIR)
        if self.ospfdConf:
            self.cmd('pkill --pidfile %s/ospfd.pid' % self._LOCALSTATEDIR)
        super(Quagga, self).stop(deleteIntfs=deleteIntfs)
