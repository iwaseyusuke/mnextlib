
from __future__ import absolute_import
from __future__ import print_function

from mnextlib import util
from mnextlib import Router


class VPP(Router):

    """
    FD.io VPP router.
    """

    _PRIVATE_DIRS = [
        '/var/run'
        '/dev/shm'
    ]

    def __init__(self, name, confFile, intfIPs=None,
                 **kwargs):
        """
        name: Name of this node.
        confFile: Path to bird.conf file.
        intfIPs: Pairs of interface and IP address.
        **kwargs: Additional parameters to pass super class.
        """
        privateDirs = kwargs.get('privateDirs', [])
        kwargs['privateDirs'] = privateDirs + self._PRIVATE_DIRS
        super(VPP, self).__init__(name, intfIPs=intfIPs, **kwargs)
        assert confFile is not None
        self.confFile = util.resolve_path(confFile)

    def start(self, controllers):
        super(VPP, self).start(controllers=controllers)
        for intf in self.intfList():
            self.cmd('ip link set %s down' % intf.name)
        # self.cmd('systemctl start vpp')
        self.cmd('rm -f /dev/shm/db /dev/shm/global_vm /dev/shm/vpe-api')
        self.cmd('/sbin/modprobe uio_pci_generic')
        self.cmd('/usr/bin/vpp -c %s &' % self.confFile)
        self.cmd('echo $! > /var/run/vpp/vpp.pid')
        while True:
            ret = self.cmd('test -S /run/vpp/cli.sock; echo $?').strip()
            time.sleep(1)
            if ret == '0':
                break
        for intf, ip in self.intfIPs:
            self.cmd('vppctl create host-interface name %s' % intf)
            self.cmd('vppctl set interface ip address host-%s %s' % (intf, ip))
            self.cmd('vppctl set interface state host-%s up' % intf)

    def stop(self, deleteIntfs=True):
        # self.cmd('systemctl stop vpp')
        self.cmd('pkill --pidfile /var/run/vpp/vpp.pid')
        self.cmd('rm -f /dev/shm/db /dev/shm/global_vm /dev/shm/vpe-api')
        self.cmd('rm /var/run/.vpp_*')
        super(VPP, self).stop(deleteIntfs=deleteIntfs)
