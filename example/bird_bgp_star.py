#!/usr/bin/env python

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.node import OVSBridge
from mininet.log import setLogLevel

import mnextlib


def main():
    # --+--------+------------------+-- 10.0.0.0/24, fc00::/64
    #   |        |         |        |
    #   |.1/24   |.2/24    |.3/24   |.254/24
    # +----+   +----+   +----+   +------+
    # | r1 |   | r2 |   | r3 |   | r254 |
    # +----+   +----+   +----+   +------+
    net = Mininet(controller=RemoteController, switch=mnextlib.Bird)

    s1 = net.addSwitch('s1', cls=OVSBridge)

    r1 = net.addSwitch(
        'r1',
        intfIPs=[
            ('lo', '1.1.1.1/32'),
            ('r1-eth1', '10.0.0.1/8'),
            ('r2-eth1', 'fc00::1/64'),
        ],
        confFile='~/mnextlib/example/bird/bgp_star/r1/bird.conf',
    )
    r2 = net.addSwitch(
        'r2',
        intfIPs=[
            ('lo', '2.2.2.2/32'),
            ('r2-eth1', '10.0.0.2/8'),
            ('r2-eth1', 'fc00::2/64'),
        ],
        confFile='~/mnextlib/example/bird/bgp_star/r2/bird.conf',
    )
    # r2 = net.addSwitch(
    #     'r2',
    #     intfIPs=[
    #         ('r2-eth1', '10.0.0.2/24'),
    #         ('r2-eth1', 'fc00::2/64'),
    #     ],
    #     cls=mnextlib.Router,
    # )
    r3 = net.addSwitch(
        'r3',
        intfIPs=[
            ('r3-eth1', '10.0.0.3/24'),
            ('r3-eth1', 'fc00::3/64'),
        ],
        cls=mnextlib.Router,
    )
    r254 = net.addSwitch(
        'r254',
        intfIPs=[
            ('r254-eth1', '10.0.0.254/24'),
            ('r254-eth1', 'fc00::254/64'),
        ],
        cls=mnextlib.Router,
    )

    net.addLink(s1, r1)
    net.addLink(s1, r2)
    net.addLink(s1, r3)
    net.addLink(s1, r254)

    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
