import xbmc
import xbmcgui
import os
import socket
import xbmcvfs
import urllib.request
from http_server import get_cloud_tips, check_md5, run_http_server, stop_http_server
import threading


# 检查网络连接
def check_internet():
    response = os.system("ping -c 1 www.baidu.com")
    return response == 0


# 获取机器的内网IP地址
def get_local_ip(port=19798):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception as e:
        print(f"Error getting local IP address: {e}")
        local_ip = "127.0.0.1"

    if local_ip:
        return f"{local_ip}"
    return None


# 从配置文件中读取vkey
def read_vkey_from_config():
    config_path = xbmcvfs.translatePath('special://userdata/userconfig/npc.conf')
    try:
        with open(config_path, 'r') as f:
            for line in f.readlines():
                if line.startswith('vkey='):
                    return line.split('=')[1].strip()
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None


# 从配置文件中读取CD2+OpenList版本号
def read_cd2_from_config():
    config_path = xbmcvfs.translatePath('special://userdata/Version')
    try:
        with open(config_path, 'r') as f:
            for line in f.readlines():
                if line.startswith('cd2='):
                    return line.split('=')[1].strip()
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None


# 从配置文件中读取OpenList版本号
def read_openlist_from_config():
    config_path = xbmcvfs.translatePath('special://userdata/Version')
    try:
        with open(config_path, 'r') as f:
            for line in f.readlines():
                if line.startswith('openlist='):
                    return line.split('=')[1].strip()
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None


def read_path_from_config():
    config_path = xbmcvfs.translatePath('special://userdata/cdisklist.txt')
    try:
        with open(config_path, 'r') as f:
            for line in f.readlines():
                return line.split()
    except Exception as e:
        print(f"Error reading config file: {e}")
    return None


class CustomQRDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.qr_code_url = kwargs["qr_code_url"]
        self.cd2 = kwargs.get("cd2")
        self.openlist = kwargs.get("openlist")
        self.catalogue = kwargs.get("catalogue")
        self.local_ip = get_local_ip()

    def onInit(self):
        self.getControl(100).setImage(self.qr_code_url)
        self.getControl(101).setLabel("扫描二维码登陆CD2（挂载云盘）")
        self.getControl(102).setLabel(f"IP地址: {self.local_ip}")
        self.getControl(103).setLabel(f"或者浏览器输入IP地址（登录设备需在同一网段）")
        self.getControl(104).setLabel(f"CD2版本号：{self.cd2}\n")
        self.getControl(105).setLabel(f"OpenList版本号：{self.openlist}")
        self.getControl(106).setLabel(f"OpenList地址：{self.local_ip}:5244\n    用户名：admin 密码：1234")
        self.getControl(108).setLabel(f"已挂载的云盘：{self.catalogue}")


# 按顺序尝试获取二维码的函数
def get_qr_code_url():
    local_ip = get_local_ip()
    if not local_ip:
        return None
    base_url = f"http://{local_ip}"
    # 接口一
    qr_code_url = f"https://qun.qq.com/qrcode/index?data={base_url}"
    try:
        with urllib.request.urlopen(qr_code_url) as response:
            if response.getcode() == 200:
                return qr_code_url
    except:
        pass

    # 接口二
    qr_code_url = f"https://api.pwmqr.com/qrcode/create/?url={base_url}"
    try:
        with urllib.request.urlopen(qr_code_url) as response:
            if response.getcode() == 200:
                return qr_code_url
    except:
        pass

    # 接口三
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={base_url}"
    try:
        with urllib.request.urlopen(qr_code_url) as response:
            if response.getcode() == 200:
                return qr_code_url
    except:
        pass

    return None


def main():
    # 使用一个线程启动HTTP服务器
    server_thread = threading.Thread(target=run_http_server)
    server_thread.start()

    if not check_internet():
        local_ip = get_local_ip()
        dialog = xbmcgui.Dialog()
        dialog.ok("网络问题", f"您的设备未联网，设备IP：{local_ip}")
    else:
        qr_code_url = get_qr_code_url()
        if qr_code_url is None:
            dialog = xbmcgui.Dialog()
            dialog.ok("二维码获取失败", "无法获取二维码，请检查网络和接口设置。")
            return
        vkey = read_vkey_from_config()
        cd2 = read_cd2_from_config()
        openlist = read_openlist_from_config()
        catalogue = read_path_from_config()

        if check_md5():
            get_cloud_tips()
        else:
            print("文件的MD5值不匹配，停止执行网盘状态检测。")

        # 显示自定义对话框
        scriptPath = xbmcvfs.translatePath("special://home/addons/plugin.clouddrive/")
        xmlFilename = "dialog_layout.xml"
        defaultSkin = "Default"
        defaultRes = "1080i"
        dialog = CustomQRDialog(xmlFilename, scriptPath, defaultSkin, defaultRes, qr_code_url=qr_code_url, vkey=vkey,
                                cd2=cd2, openlist=openlist, catalogue=catalogue)
        dialog.doModal()
        del dialog

    # 当对话框关闭时，停止HTTP服务器
    stop_http_server()
    # 确保线程已完全关闭
    server_thread.join()


if __name__ == "__main__":
    main()