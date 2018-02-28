#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel

import mnextlib


def main():
    net = Mininet(controller=RemoteController)

    net.addController('c0')

    s1 = net.addSwitch(
        name='s1',
        # Example of Options:
        # cls=mnextlib.OVSSwitch,  # OVS in namespace
        # failMode='standalone',  # default 'secure'
        # datapath='user',  # default 'kernel'
        # protocols='OpenFlow15',  # default 'OpenFlow13'
        # dpid='11:22:33:44:55:66:77:88',  # default auto signed
    )
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h3 = net.addHost('h3')

    net.addLink(s1, h1)
    net.addLink(s2, h2)
    net.addLink(s3, h3)

    net.addLink(s1, s2)
    net.addLink(s2, s3)
    net.addLink(s3, s1)

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
