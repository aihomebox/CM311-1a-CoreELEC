# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os
import subprocess

# 定义核心路径
NAND_SCRIPT = '/usr/bin/doviset'
HDR_FLAG_FILE = '/tmp/hdr'

def show_notification(title, message, time=3000):
    """封装通知函数，简化调用"""
    xbmc.executebuiltin(f'Notification({title}, {message}, {time})')

def execute_script(script_path):
    """执行外部脚本，带权限检查和结果反馈"""
    try:
        # 确保脚本有执行权限
        os.chmod(script_path, 0o755)
        # 执行脚本并捕获输出
        result = subprocess.run(
            script_path,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            show_notification('脚本执行结果', '核心脚本已成功生效')
            xbmc.sleep(2000)  # 暂停2秒等待脚本生效
            return True
        else:
            error_msg = f'脚本执行失败：{result.stderr[:50]}'  # 截取前50字符避免通知过长
            show_notification('错误', error_msg)
            return False
    except Exception as e:
        show_notification('错误', f'执行脚本异常：{str(e)[:50]}')
        return False

def check_current_mode():
    """查看当前杜比视界模式状态（关闭后返回主菜单，不退出）"""
    dialog = xbmcgui.Dialog()
    if os.path.exists(HDR_FLAG_FILE):
        status = '当前模式：显示设备不支持杜比视界模式'
    else:
        status = '当前模式：显示设备支持杜比视界模式'
    # 用ok对话框显示状态，关闭后自动回到主菜单（无退出逻辑）
    dialog.ok('模式状态', status)
    # 不添加任何退出代码，关闭对话框后自然返回上级菜单

def show_second_menu():
    """二级菜单：杜比视界模式切换选项"""
    dialog = xbmcgui.Dialog()
    # 根据HDR文件是否存在，显示不同的二级选项
    if os.path.exists(HDR_FLAG_FILE):
        second_options = [
            '切换为【显示设备支持杜比视界模式】',
            '返回上一级菜单'
        ]
    else:
        second_options = [
            '切换为【显示设备不支持杜比视界模式】',
            '返回上一级菜单'
        ]
    
    # 显示二级菜单
    second_choice = dialog.select('杜比视界切换设置', second_options)
    
    # 处理二级菜单选择
    if second_choice == 0:
        if os.path.exists(HDR_FLAG_FILE):
            # 切换为无杜比视界模式（删除HDR文件）
            try:
                os.remove(HDR_FLAG_FILE)
                # 第一步：先执行提示（优先显示切换成功的通知）
                show_notification('切换成功', '已成功切换为显示设备支持杜比视界模式')
                xbmc.sleep(1000)  # 短暂等待，确保提示被用户看到
                # 第二步：执行核心脚本生效
                execute_script(NAND_SCRIPT)
            except Exception as e:
                show_notification('错误', f'切换失败：{str(e)[:50]}')
        else:
            # 切换为支持杜比视界模式（创建HDR文件）
            try:
                with open(HDR_FLAG_FILE, 'w') as f:
                    f.write('')  # 创建空文件作为标志
                # 第一步：先执行提示（优先显示切换成功的通知）
                show_notification('切换成功', '已成功切换为显示设备不支持杜比视界模式')
                xbmc.sleep(1000)  # 短暂等待，确保提示被用户看到
                # 第二步：执行核心脚本生效
                execute_script(NAND_SCRIPT)
            except Exception as e:
                show_notification('错误', f'切换失败：{str(e)[:50]}')
    # second_choice == 1 或 -1 时，直接返回，不做任何操作（回到一级主菜单）

def main_menu():
    """一级主菜单（循环显示，直到选择退出）"""
    dialog = xbmcgui.Dialog()
    # 循环显示主菜单，直到用户选择“退出”
    while True:
        # 构建一级菜单选项
        main_options = [
            '杜比视界模式切换',
            '查看当前模式状态',
            '退出'
        ]
        # 显示一级菜单（返回选中项的索引，取消返回-1）
        main_choice = dialog.select('杜比视界切换设置', main_options)
        
        # 处理一级菜单选择
        if main_choice == 0:  # 选择：模式切换 → 进入二级菜单
            show_second_menu()
        elif main_choice == 1:  # 选择：查看状态 → 显示状态后回到主菜单
            check_current_mode()
        elif main_choice == 2 or main_choice == -1:  # 选择：退出/取消 → 终止循环
            show_notification('提示', '已退出杜比视界设置')
            break

# 程序入口
if __name__ == '__main__':
    # 先弹出一级确认，再进入主菜单
    dialog = xbmcgui.Dialog()
    if dialog.yesno('杜比视界切换设置', '是否要进入支持杜比视界的和不支持的杜比视界的显示设备切换设置？'):
        # 检查核心脚本是否存在
        if not os.path.exists(NAND_SCRIPT):
            dialog.ok('提示', '网络校验失败，请稍后重试！')
        else:
            # 进入循环主菜单（查看状态后不退出）
            main_menu()
    else:
        show_notification('提示', '已取消进入设置')