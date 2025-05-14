# -*- coding: utf-8 -*-
# check for script and reboot to nand if present
import xbmc
import os
import subprocess

# 定义标记文件路径
bootup_file = '/storage/bootup'
nandscript = '/usr/bin/chat'

# 检查标记文件是否存在
if not os.path.exists(bootup_file):
    # 第一次运行，生成标记文件
    with open(bootup_file, 'w') as f:
        f.write('')
    xbmc.executebuiltin('Notification(开机默认智能更新CD2和Alist)')
else:
    # 第二次运行，删除标记文件
    os.remove(bootup_file)
    xbmc.executebuiltin('Notification(开机默认手动更新CD2和Alist)')

if os.path.exists(nandscript):
    xbmc.executebuiltin('Notification(设置, 开机智能/手动更新挂载插件)')
    # os.system('chmod +x /usr/bin/chat')
    subprocess.call(nandscript)
    os.system('sleep 2')
    # xbmc.sleep(300)
    # xbmc.executebuiltin('Powerdown')

CE = '/storage/bootup'
if os.path.exists(CE):
   if os.path.exists(CE):
    xbmc.executebuiltin('Notification(开机默认智能更新CD2和Alist, 设置成功)')

else:
    xbmc.executebuiltin('Notification(开机默认手动更新CD2和Alist, 设置成功)')
exit()
    