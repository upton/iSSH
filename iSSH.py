#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rumps import App, MenuItem, rumps
import os, re

class iSSH(App):
    def __init__(self):
        super(iSSH, self).__init__('iSSH')
        self.hm = HostsManager()
        self.ssh = os.path.join(os.path.abspath('.'), 'login.sh')
        self.exp = os.path.join(os.path.abspath('.'), 'auto_login.exp')
        self.hosts_file = os.path.join(os.path.abspath('.'), 'hosts.txt')
        self.ts = os.stat(self.hosts_file).st_mtime
        os.chmod(self.exp, 0755)
        os.chmod(self.ssh, 0755)
        self.menu = self.init_menu()
        
        
    def init_menu(self):
        return self.set_callback(self.hm.read_hosts())
    
                
    def set_callback(self, menus):
        for menu in menus:
            menu.set_callback(self.hello)
            
        return menus
    
    
    def hello(self, sender):
        if sender.key == '__none':
            return
        elif sender.key == '__setting':
            os.system("open " + self.hosts_file)
        else:
            host = self.hm.hosts[sender.key]
            
            lines = ['#!/bin/sh',
                     '\n',
                     self.exp + ' ' + host['ip'] + ' ' + host['user'] + ' ' + host['pass']]
            with open(self.ssh, 'w') as f:
                f.writelines(lines)
                f.flush()

            os.system("open " + self.ssh)
        
    @rumps.timer(2)
    def update(self, _):
        ts = os.stat(self.hosts_file).st_mtime
        if ts != self.ts:
            self.ts = ts
            self.menu.clear()
            menus = self.set_callback(self.hm.read_hosts())
            quit_menu = MenuItem('Quit', key='Quit', callback=rumps.quit_application)
            menus.append(quit_menu)
            
            self.menu = menus

class HostsManager(object):
    def __init__(self):
        self.hosts_file = os.path.join(os.path.abspath('.'), 'hosts.txt')
        self.hosts = {}
        self.default_user = ''
        self.default_pass = ''
    
    def read_hosts(self):
        ms = []
        ms.append(MenuItem('Edit server list', key='__setting'))
        ms.append(MenuItem('-----------------------', key='__none'))
        
        with open(self.hosts_file) as f:
            for line in f.readlines():
                line = line.strip()
                if line and line[0] != '#':
                    hh = line.split('=', 1)
                    if len(hh) == 2:
                        host_name = hh[0].strip()
                        if host_name == 'default-user':
                            self.default_user = hh[1].strip()
                        elif host_name == 'default-pass':
                            self.default_pass = hh[1].strip()
                        else:
                            ip_user_and_pass = re.split(r'\s+', hh[1].strip())
                            if len(ip_user_and_pass) == 3:
                                # 有用户名和密码
                                ip = ip_user_and_pass[0]
                                user = ip_user_and_pass[1]
                                password = ip_user_and_pass[2]
                                ms.append(MenuItem(host_name, key=host_name))
                                self.hosts[host_name] = {'ip':ip, 'user':user, 'pass':password}
                            else:
                                # 没有用户名和密码
                                ip = hh[1].strip()
                                ms.append(MenuItem(host_name, key=host_name))
                                self.hosts[host_name] = {'ip':ip, 'user':self.default_user, 'pass':self.default_pass}
        
        ms.append(MenuItem('-----------------------', key='__none'))
        return ms
    
    
if __name__ == "__main__":
    issh = iSSH()
    issh.run()
