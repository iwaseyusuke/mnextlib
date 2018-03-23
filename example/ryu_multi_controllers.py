#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel


def main():
    """
       c1             c2
       |              |
       +---+------+---+
           |      |
    h1 --- s1 --- s2 --- h2
    """
    net = Mininet(controller=RemoteController)

    # ryu-manager --ofp-listen-host '127.0.0.2' ryu.app.simple_switch_13
    net.addController('c1', ip='127.0.0.2')

    # ryu-manager --ofp-listen-host '127.0.0.3' ryu.app.simple_switch_13
    net.addController('c2', ip='127.0.0.3')

    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')

    h1 = net.addHost('h1')
    h2 = net.addHost('h2')

    net.addLink(s1, h1)
    net.addLink(s2, h2)

    net.addLink(s1, s2)

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
