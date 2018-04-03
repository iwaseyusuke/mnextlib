#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSBridge
from mininet.log import setLogLevel

import mnextlib


def main():
    # r1: Route Reflector Client
    # r2: Route Reflector Client
    # r254: Route Reflector
    #
    #            +------+
    #      +-----| r254 |-----+
    # iBGP |     +------+     | iBGP
    #      |        |         |
    #    +----+     |      +----+
    #    | r1 |----(s1)----| r2 |
    #    +----+            +----+
    #      |                  |
    #   +------+          +------+
    #   | r1h1 |          | r2h1 |
    #   +------+          +------+
    net = Mininet(controller=RemoteController, switch=mnextlib.FRRouting)

    s1 = net.addSwitch('s1', cls=OVSBridge)

    r1 = net.addSwitch(
        'r1',
        confDir='~/mnextlib/example/frr/route_reflector/r1',
    )
    r2 = net.addSwitch(
        'r2',
        confDir='~/mnextlib/example/frr/route_reflector/r2',
    )
    r254 = net.addSwitch(
        'r254',
        confDir='~/mnextlib/example/frr/route_reflector/r254',
    )

    net.addLink(s1, r1)
    net.addLink(s1, r2)
    net.addLink(s1, r254)

    r1h1 = net.addHost(
        'r1h1',
        ip='192.168.1.101/24',
        defaultRoute='via 192.168.1.1 dev r1h1-eth0')
    r2h1 = net.addHost(
        'r2h1',
        ip='192.168.2.101/24',
        defaultRoute='via 192.168.2.1 dev r2h1-eth0')

    net.addLink(r1, r1h1)
    net.addLink(r2, r2h1)

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
