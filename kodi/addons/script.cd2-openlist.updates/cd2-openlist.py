# -*- coding: utf-8 -*-
# check for script and reboot to nand if present
import xbmc
import os
import subprocess

UPD = '/tmp/upda'
if os.path.exists(UPD):
    xbmc.executebuiltin('Notification(更新cd2+openlist, 后台正在运行更新)') 
    exit()
else:
    xbmc.executebuiltin('Notification(更新cd2+openlist, 开始执行更新)')


nandscript = '/usr/bin/bootgo'
if os.path.exists(nandscript):

    #os.system('chmod +x /storage/.kodi/addons/script.cd2-openlist.updates/cd2-openlist-updates')
    os.mknod(UPD)    
    subprocess.call('/usr/bin/bootgo')
    os.system('sync')
   
else:
    xbmc.executebuiltin('Notification(cd2+openlist_updates, 更新失败)')

Openlist = '/tmp/openlist'
if os.path.exists(Openlist):
    xbmc.executebuiltin('Notification(OpenList, 更新成功)')
    # 执行 vs 程序
    subprocess.call('/usr/bin/vs')
    xbmc.sleep(3000)
    os.remove(Openlist)
else:
    xbmc.executebuiltin('Notification(OpenList, 无可用更新)')

CD2 = '/tmp/cd2'
if os.path.exists(CD2):
    xbmc.executebuiltin('Notification(CD2, 更新成功)')
    # 执行 vs 程序
    subprocess.call('/usr/bin/vs')
    xbmc.sleep(3000)
    os.remove(CD2)
    os.remove(UPD)    
else:
    xbmc.executebuiltin('Notification(CD2, 无可用更新)')
    os.remove(UPD)   
exit()