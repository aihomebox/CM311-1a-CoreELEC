# -*- coding: utf-8 -*-
# check for script and reboot to nand if present
import xbmc
import os
import subprocess

UPD = '/tmp/upda'
if os.path.exists(UPD):
    xbmc.executebuiltin('Notification(更新cd2+alist, 后台正在运行更新)') 
    exit()
else:
    xbmc.executebuiltin('Notification(更新cd2+alist, 开始执行更新)')


nandscript = '/usr/bin/bootgo'
if os.path.exists(nandscript):

    #os.system('chmod +x /storage/.kodi/addons/script.cd2-alist.updates/cd2-alist-updates')
    os.mknod(UPD)    
    subprocess.call('/usr/bin/bootgo')
    os.system('sync')
   
else:
    xbmc.executebuiltin('Notification(cd2+alist_updates, 更新失败)')

Alist = '/tmp/alist'
if os.path.exists(Alist):
    xbmc.executebuiltin('Notification(AList, 更新成功)')
    xbmc.sleep(3000)
    os.remove(Alist)
else:
    xbmc.executebuiltin('Notification(AList, 无可用更新)')

CD2 = '/tmp/cd2'
if os.path.exists(CD2):
    xbmc.executebuiltin('Notification(CD2, 更新成功)')
    xbmc.sleep(3000)
    os.remove(CD2)
    os.remove(UPD)    
else:
    xbmc.executebuiltin('Notification(CD2, 无可用更新)')
    os.remove(UPD)   
exit()