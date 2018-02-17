
from __future__ import absolute_import
from __future__ import print_function

from mininet.node import Switch


class Router(Switch):

    """
    Base class for router node.
    """

    def __init__(self, name, intfIPs=None, **kwargs):
        """
        name: Name of this node.
        intfIPs: Pairs of interface and IP address.
        **kwargs: Additional parameters to pass super class.
        """
        # Router node should be created in namespace
        kwargs['inNamespace'] = True
        super(Router, self).__init__(name, **kwargs)
        # e.g.)
        # intfIPs = [
        #     ('lo', '10.0.0.0/32'),
        #     ('r1-eth0', '192.168.1.1/24'),
        # ]
        self.intfIPs = intfIPs or []
        # Router node does not requires "controlIntf"
        self.controlIntf = None

    def setIP(self, *args, **kwargs):
        self.cmd('ip link set dev lo up')
        for intf, ip in self.intfIPs:
            self.cmd('ip address add %s dev %s' % (ip, intf))
            self.cmd('ip link set dev %s up' % intf)
        return None

    def start(self, controllers):
        self.setIP()
