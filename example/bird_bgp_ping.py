#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSBridge
from mininet.log import setLogLevel

import mnextlib


def main():
    # +-----+ .1/8          .2/8 +-----+
    # | r1  |--------(s1)--------| r2  |
    # +-----+     10.0.0.0/8     +-----+
    #    | .1/24                    | .1/24
    #    | 192.168.1.0/24           | 192.168.2.0/24
    #    | .101/24                  | .101/24
    # +------+                   +------+
    # | r1h1 |                   | r2h1 |
    # +------+                   +------+
    net = Mininet(controller=RemoteController, switch=mnextlib.Bird)

    s1 = net.addSwitch('s1', cls=OVSBridge)

    r1 = net.addSwitch(
        'r1',
        intfIPs=[
            ('lo', '1.1.1.1/32'),
            ('r1-eth1', '10.0.0.1/8'),
            ('r1-eth2', '192.168.1.1/24'),
        ],
        confFile='~/mnextlib/example/bird/bgp_ping/r1/bird.conf',
    )
    r2 = net.addSwitch(
        'r2',
        intfIPs=[
            ('lo', '2.2.2.2/32'),
            ('r2-eth1', '10.0.0.2/8'),
            ('r2-eth2', '192.168.2.1/24'),
        ],
        confFile='~/mnextlib/example/bird/bgp_ping/r2/bird.conf',
    )

    net.addLink(s1, r1)
    net.addLink(s1, r2)

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
