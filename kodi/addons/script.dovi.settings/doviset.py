# -*- coding: utf-8 -*-
import xbmc
import xbmcgui
import os
import subprocess

# 定义核心路径
NAND_SCRIPT = '/storage/.kodi/addons/script.dovi.settings/doviset'
HDR_FLAG_FILE = '/tmp/hdr'
# 新增：bootcmd_counter文件路径（仅读取，不修改）
BOOTCMD_COUNTER = '/storage/bootcmd_counter'

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

# 核心：仅读取bootcmd_counter数值（不修改）
def get_bootcmd_counter():
    """
    读取bootcmd_counter文件数值（仅读取，不修改）
    - 文件不存在 → 返回奇数1（默认支持杜比视界）
    - 内容非数字 → 返回奇数1
    - 正常读取 → 返回对应整数值
    """
    try:
        if not os.path.exists(BOOTCMD_COUNTER):
            return 1
        with open(BOOTCMD_COUNTER, 'r') as f:
            content = f.read().strip()
            counter = int(content)
            return counter
    except Exception as e:
        # 记录日志便于调试，不影响用户使用
        xbmc.log(f"读取bootcmd_counter失败: {str(e)}", level=xbmc.LOGWARNING)
        return 1

def check_current_mode():
    """查看当前杜比视界模式状态（基于bootcmd_counter校正显示）"""
    dialog = xbmcgui.Dialog()
    # 核心修改：仅基于bootcmd_counter判断显示状态（不依赖tmp/hdr）
    counter = get_bootcmd_counter()
    if counter % 2 == 0:  # 偶数 → 显示“不支持杜比视界”
        status = '当前模式：显示设备不支持杜比视界模式'
    else:  # 奇数/文件不存在 → 显示“支持杜比视界”
        status = '当前模式：显示设备支持杜比视界模式'
    # 用ok对话框显示状态，关闭后自动回到主菜单
    dialog.ok('模式状态', status)

def show_second_menu():
    """二级菜单：杜比视界模式切换选项（基于bootcmd_counter校正）"""
    dialog = xbmcgui.Dialog()
    # 核心：基于bootcmd_counter生成菜单（不修改计数器，仅校正显示）
    counter = get_bootcmd_counter()
    if counter % 2 == 0:  # 偶数 → 菜单显示“切换为支持”
        second_options = [
            '切换为【显示设备支持杜比视界模式】',
            '返回上一级菜单'
        ]
    else:  # 奇数 → 菜单显示“切换为不支持”
        second_options = [
            '切换为【显示设备不支持杜比视界模式】',
            '返回上一级菜单'
        ]
    
    # 显示二级菜单
    second_choice = dialog.select('杜比视界切换设置', second_options)
    
    # 处理二级菜单选择（仅操作tmp/hdr文件，不修改计数器）
    if second_choice == 0:
        try:
            if counter % 2 == 0:
                # 偶数（显示不支持）→ 切换为支持：删除HDR临时文件
                if os.path.exists(HDR_FLAG_FILE):
                    os.remove(HDR_FLAG_FILE)
                show_notification('切换成功', '已成功切换为显示设备支持杜比视界模式')
            else:
                # 奇数（显示支持）→ 切换为不支持：创建HDR临时文件
                with open(HDR_FLAG_FILE, 'w') as f:
                    f.write('')  # 创建空文件作为标志
                show_notification('切换成功', '已成功切换为显示设备不支持杜比视界模式')
            
            xbmc.sleep(1000)  # 短暂等待，确保提示被用户看到
            # 执行核心脚本生效
            execute_script(NAND_SCRIPT)
        except Exception as e:
            show_notification('错误', f'切换失败：{str(e)[:50]}')
    # 选择返回/取消 → 回到一级主菜单

def main_menu():
    """一级主菜单（循环显示，直到选择退出）"""
    dialog = xbmcgui.Dialog()
    # 循环显示主菜单，直到用户选择“退出”
    while True:
        main_options = [
            '杜比视界模式切换',
            '查看当前模式状态',
            '退出'
        ]
        main_choice = dialog.select('杜比视界切换设置', main_options)
        
        if main_choice == 0:  # 模式切换 → 二级菜单
            show_second_menu()
        elif main_choice == 1:  # 查看状态
            check_current_mode()
        elif main_choice == 2 or main_choice == -1:  # 退出/取消
            show_notification('提示', '已退出杜比视界设置')
            break

# 程序入口
if __name__ == '__main__':
    dialog = xbmcgui.Dialog()
    if dialog.yesno('杜比视界切换设置', '是否要进入杜比视界显示切换设置？'):
        # 检查核心脚本是否存在
        if not os.path.exists(NAND_SCRIPT):
            dialog.ok('提示', '校验失败！请稍后再试！！！')
        else:
            main_menu()
    else:
        show_notification('提示', '已取消进入设置')