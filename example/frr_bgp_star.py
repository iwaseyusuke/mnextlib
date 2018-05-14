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
    net = Mininet(controller=RemoteController, switch=mnextlib.FRRouting)

    s1 = net.addSwitch('s1', cls=OVSBridge)

    r1 = net.addSwitch(
        'r1',
        confDir='~/mnextlib/example/frr/bgp_star/r1',
    )
    r2 = net.addSwitch(
        'r2',
        confDir='~/mnextlib/example/frr/bgp_star/r2',
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
