
from __future__ import absolute_import
from __future__ import print_function

import os
import time

from mininet import node
from mininet.util import errRun


class OVSSwitch(node.OVSSwitch):

    """Open vSwitch switch running in Linux Namespace.
       Depends on ovs-ctl and ovs-vsctl."""

    def __init__(self, name, **params):
        params['inNamespace'] = True
        privateDirs = params.pop('privateDirs', [])
        if os.path.isfile('/usr/local/sbin/ovs-vswitchd'):
            self._isSourceBuild = True
            params['privateDirs'] = privateDirs + [
                '/usr/local/var/run/openvswitch',
                '/usr/local/etc/openvswitch']
        else:
            self._isSourceBuild = False
            params['privateDirs'] = privateDirs + [
                '/var/run/openvswitch',
                '/etc/openvswitch']
        node.OVSSwitch.__init__(self, name, **params)

    def ctl(self, *args, **kwargs):
        "Run ovs-ctl command"
        if self._isSourceBuild:
            cmd = '/usr/local/share/openvswitch/scripts/'
        else:
            cmd = '/usr/share/openvswitch/scripts/'
        return self.cmd(cmd + 'ovs-ctl', *args, **kwargs)

    def start(self, controllers):
        "Start up a new OVS OpenFlow switch using ovs-vsctl"
        if self.inNamespace:
            self.ctl('start', '--system-id=%s' % self.name)
        int(self.dpid, 16)  # DPID must be a hex string
        # Command to add interfaces
        intfs = ''.join(' -- add-port %s %s' % (self, intf) +
                        self.intfOpts(intf)
                        for intf in self.intfList()
                        if self.ports[intf] and not intf.IP())
        # Command to create controller entries
        clist = [(self.name + c.name, '%s:%s:%d' %
                  (c.protocol, c.IP(), c.port))
                 for c in controllers]
        if self.listenPort:
            clist.append((self.name + '-listen',
                          'ptcp:%s' % self.listenPort))
        ccmd = '-- --id=@%s create Controller target=\\"%s\\"'
        if self.reconnectms:
            ccmd += ' max_backoff=%d' % self.reconnectms
        cargs = ' '.join(ccmd % (name, target)
                         for name, target in clist)
        # Controller ID list
        cids = ','.join('@%s' % name for name, _target in clist)
        # Try to delete any existing bridges with the same name
        if not self.isOldOVS():
            cargs += ' -- --if-exists del-br %s' % self
        # One ovs-vsctl command to rule them all!
        self.vsctl(cargs +
                   ' -- add-br %s' % self +
                   ' -- set bridge %s controller=[%s]' % (self, cids) +
                   self.bridgeOpts() +
                   intfs)
        # If necessary, restore TC config overwritten by OVS
        if not self.batch:
            for intf in self.intfList():
                self.TCReapply(intf)

    def stop(self, deleteIntfs=True):
        """Terminate OVS switch.
           deleteIntfs: delete interfaces? (True)"""
        self.cmd('ovs-vsctl del-br', self)
        if self.datapath == 'user':
            self.cmd('ip link del', self)
        if self.inNamespace:
            self.ctl('stop')
        super(OVSSwitch, self).stop(deleteIntfs)

    @classmethod
    def batchShutdown(cls, switches, run=errRun):
        "Shut down a list of OVS switches"
        delcmd = 'del-br %s'
        # Do batch shut down only when switch is not in namespace
        switches = [s for s in switches if not s.inNamespace]
        if switches and not switches[0].isOldOVS():
            delcmd = '--if-exists ' + delcmd
        # First, delete them all from ovsdb
        run('ovs-vsctl ' +
            ' -- '.join(delcmd % s for s in switches))
        # Next, shut down all of the processes
        pids = ' '.join(str(switch.pid) for switch in switches)
        run('kill -HUP ' + pids)
        for switch in switches:
            switch.shell = None
        return switches
