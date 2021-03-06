
from __future__ import absolute_import
from __future__ import print_function

from mnextlib import util
from mnextlib import Router


class Bird(Router):

    """
    Bird router.
    """

    # "bird.pid", "bird.ctl"
    _LOCALSTATEDIR = '/var/run/bird'

    def __init__(self, name, intfIPs=None, confFile=None,
                 **kwargs):
        """
        name: Name of this node.
        intfIPs: Pairs of interface and IP address.
        confFile: Path to bird.conf file.
        **kwargs: Additional parameters to pass super class.
        """
        privateDirs = kwargs.get('privateDirs', [])
        kwargs['privateDirs'] = privateDirs + [self._LOCALSTATEDIR]
        super(Bird, self).__init__(name, intfIPs=intfIPs, **kwargs)
        assert confFile is not None
        self.confFile = util.resolve_path(confFile)

    def start(self, controllers):
        super(Bird, self).start(controllers=controllers)
        self.cmd('chmod 644 %s' % self.confFile)
        self.cmd('bird -c %s -P %s/bird.pid'
                 % (self.confFile, self._LOCALSTATEDIR))

    def stop(self, deleteIntfs=True):
        self.cmd('pkill --pidfile %s/bird.pid' % self._LOCALSTATEDIR)
        super(Bird, self).stop(deleteIntfs=deleteIntfs)
