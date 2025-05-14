import xbmc
import os
import subprocess

nandscript = '/usr/sbin/rebootfromnand'
if os.path.exists(nandscript):
    xbmc.executebuiltin('Notification(正在重启到安卓系统,  请稍等...)')
    subprocess.call('/usr/sbin/rebootfromnand')    
    #xbmc.sleep(3000)
    os.system('sync')    
    os.system('reboot')     
else:
    xbmc.executebuiltin('Notification(rebootfromnand, not available)')
exit() 
