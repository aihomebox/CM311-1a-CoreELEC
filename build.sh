#!/bin/sh
version="20.5-Nexus"
source_img_name="CoreELEC-Amlogic-ng.arm-${version}-Generic"
source_img_file="${source_img_name}.img.gz"
source_img_url="https://github.com/aihomebox/AIHOMEBOX/releases/download/AIHOME/CoreELEC-Amlogic-ng.arm-21.2-Omega-Generic.img.gz"
target_img_prefix="CoreELEC-Amlogic-ng.arm-${version}"
target_img_name="${target_img_prefix}-E900V22C-$(date +%Y.%m.%d)"
mount_point="target"
common_files="common-files"
system_root="SYSTEM-root"
kodi="kodi"
bin="bin"

etc_path="${system_root}/etc"
autostart_path="${system_root}/usr/bin"
modules_load_path="${system_root}/usr/lib/modules-load.d"
systemd_path="${system_root}/usr/lib/systemd/system"
libreelec_path="${system_root}/usr/lib/libreelec"
config_path="${system_root}/usr/config"
kodi_userdata="${mount_point}/.kodi/userdata"

echo "Welcome to build CoreELEC for Skyworth E900V22C!"
echo "Downloading CoreELEC-${version} generic image"
wget ${source_img_url} -O ${source_img_file} || exit 1
echo "Decompressing CoreELEC image"
gzip -d ${source_img_file} || exit 1

echo "Creating mount point"
mkdir ${mount_point}
echo "Mounting CoreELEC boot partition"
sudo mount -o loop,offset=4194304 ${source_img_name}.img ${mount_point}

echo "Copying E900V22C DTB file"
sudo cp ${common_files}/e900v22c.dtb ${mount_point}/dtb.img

echo "Decompressing SYSTEM image"
sudo unsquashfs -d ${system_root} ${mount_point}/SYSTEM



echo "Copying fs-resize script"
sudo cp ${common_files}/fs-resize ${libreelec_path}/fs-resize
sudo chown root:root ${libreelec_path}/fs-resize
sudo chmod 0775 ${libreelec_path}/fs-resize

echo "Copying autostart script"
sudo cp ${common_files}/autostart.sh ${autostart_path}/autostart.sh
sudo chmod 0775 ${autostart_path}/autostart.sh

echo "Copying os-release file"
sudo cp ${common_files}/os-release ${etc_path}/os-release
sudo chmod 0664 ${etc_path}/os-release

echo "Removing coreelec settings (service.coreelec.settings)"
target_setting_dir="${system_root}/usr/share/kodi/addons/service.coreelec.settings"
if [ -d "${target_setting_dir}" ]; then
   sudo rm -rf "${target_setting_dir}"
    if [ $? -ne 0 ]; then
        echo "删除 ${target_setting_dir} 失败"
        exit 1
    fi
    echo "已删除自带设置: ${target_setting_dir}"
else
    echo "${target_setting_dir} 不存在，跳过删除"
fi


echo "Copying kodi file path"
sudo cp -r ${kodi} ${system_root}/usr/share

echo "Copying bin file path"
sudo cp -r ${bin} ${system_root}/usr/

# 赋予 /usr/bin/startgo, /usr/bin/bootgo 和 /usr/bin/chat 执行权限
sudo chmod +x ${system_root}/usr/bin/startgo
sudo chmod +x ${system_root}/usr/bin/bootgo
sudo chmod +x ${system_root}/usr/bin/chat

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/startgo ] && [ -x ${system_root}/usr/bin/bootgo ] && [ -x ${system_root}/usr/bin/chat ]; then
    echo "/usr/bin/startgo, /usr/bin/bootgo 和 /usr/bin/chat 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/startgo, /usr/bin/bootgo 和 /usr/bin/chat 执行权限失败。"
    exit 1
fi

# 赋予 /usr/bin/ 下的 fin 和 /usr/bin/ 下的 vs 执行权限
sudo chmod +x ${system_root}/usr/bin/fin
sudo chmod +x ${system_root}/usr/bin/vs

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/fin ] && [ -x ${system_root}/usr/bin/vs ]; then
    echo "/usr/bin/fin 和 /usr/bin/vs 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/fin 和 /usr/bin/vs 执行权限失败。"
    exit 1
fi

# 赋予 /usr/bin/setboot 文件执行权限
sudo chmod +x ${system_root}/usr/bin/setboot

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/setboot ]; then
    echo "/usr/bin/setboot 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/setboot 执行权限失败。"
    exit 1
fi

# 赋予 /usr/bin/pro 文件执行权限
sudo chmod +x ${system_root}/usr/bin/pro

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/pro ]; then
    echo "/usr/bin/pro 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/pro 执行权限失败。"
    exit 1
fi


# 赋予 /usr/bin/initial 文件执行权限
sudo chmod +x ${system_root}/usr/bin/initial

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/initial ]; then
    echo "/usr/bin/initial 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/initial 执行权限失败。"
    exit 1
fi

# 赋予 /usr/bin/updatecheck 文件执行权限
sudo chmod +x ${system_root}/usr/bin/updatecheck

# 检查权限是否设置成功
if [ -x ${system_root}/usr/bin/updatecheck ]; then
    echo "/usr/bin/updatecheck 已成功赋予执行权限。"
else
    echo "赋予 /usr/bin/updatecheck 执行权限失败。"
    exit 1
fi

# 删除文件前检查文件是否存在
if [ -f ${system_root}/usr/share/kodi/.kodi.zip ]; then
    sudo rm ${system_root}/usr/share/kodi/.kodi.zip
    if [ $? -ne 0 ]; then
        echo "删除 /usr/share/kodi/.kodi.zip 文件失败"
        exit 1
    fi
fi

echo "Downloading.kodi.zip file"
wget -O.kodi.zip "https://media-gdgz-fy-person01.gd5oss.ctyunxs.cn/PERSONCLOUD/dc75b479-08a5-4e0b-aa99-c1b0ea91c815.zip?response-content-disposition=attachment%3Bfilename%3D%22.kodi.zip%22%3Bfilename*%3DUTF-8%27%27.kodi.zip&x-amz-CLIENTNETWORK=UNKNOWN&x-amz-CLOUDTYPEIN=PERSON&x-amz-CLIENTTYPEIN=WEB&Signature=2Lc828xReWqs%2B0KGRbbb9%2BNYczc%3D&AWSAccessKeyId=g6jU1T3TkAbPKf5ouH5d&x-amz-userLevel=7&Expires=1747216964&x-amz-limitrate=51200&x-amz-FSIZE=184584211&x-amz-UID=354906919&x-amz-UFID=324931194017670457"
if [ $? -ne 0 ]; then
    echo "下载.kodi.zip 文件失败"
    exit 1
fi

# 移动文件前检查文件是否存在
if [ -f.kodi.zip ]; then
    sudo mv .kodi.zip ${system_root}/usr/share/kodi/
    if [ $? -ne 0 ]; then
        echo "移动.kodi.zip 文件失败"
        exit 1
    fi
else
    echo ".kodi.zip 文件未成功下载，无法移动"
    exit 1
fi

echo "Copying rc_keymap files"
sudo cp ${common_files}/rc_maps.cfg ${config_path}/rc_maps.cfg
sudo chown root:root ${config_path}/rc_maps.cfg
sudo chmod 0664 ${config_path}/rc_maps.cfg
sudo cp ${common_files}/e900v22c.rc_keymap ${config_path}/rc_keymaps/e900v22c
sudo chown root:root ${config_path}/rc_keymaps/e900v22c
sudo chmod 0664 ${config_path}/rc_keymaps/e900v22c
sudo cp ${common_files}/keymap.hwdb ${config_path}/hwdb.d/keymap.hwdb
sudo chown root:root ${config_path}/hwdb.d/keymap.hwdb
sudo chmod 0664 ${config_path}/hwdb.d/keymap.hwdb

echo "Copying autostart files"
sudo cp ${common_files}/autostart.sh ${config_path}/autostart.sh
sudo chown root:root ${config_path}/autostart.sh
sudo chmod 0755 ${config_path}/autostart.sh

echo "Compressing SYSTEM image"
sudo mksquashfs ${system_root} SYSTEM -comp lzo -Xalgorithm lzo1x_999 -Xcompression-level 9 -b 524288 -no-xattrs
echo "Replacing SYSTEM image"
sudo rm ${mount_point}/SYSTEM.md5
sudo dd if=/dev/zero of=${mount_point}/SYSTEM
sudo sync
sudo rm ${mount_point}/SYSTEM
sudo mv SYSTEM ${mount_point}/SYSTEM
sudo md5sum ${mount_point}/SYSTEM > SYSTEM.md5
sudo mv SYSTEM.md5 target/SYSTEM.md5
sudo rm -rf ${system_root}

echo "Unmounting CoreELEC boot partition"
sudo umount -d ${mount_point}
echo "Mounting CoreELEC data partition"
sudo mount -o loop,offset=541065216 ${source_img_name}.img ${mount_point}

echo "Creating keymaps directory for kodi"
sudo mkdir -p -m 0755 ${kodi_userdata}/keymaps
echo "Copying kodi config files"
sudo cp ${common_files}/advancedsettings.xml ${kodi_userdata}/advancedsettings.xml
sudo chown root:root ${kodi_userdata}/advancedsettings.xml
sudo chmod 0644 ${kodi_userdata}/advancedsettings.xml
sudo cp ${common_files}/backspace.xml ${kodi_userdata}/keymaps/backspace.xml
sudo chown root:root ${kodi_userdata}/keymaps/backspace.xml
sudo chmod 0644 ${kodi_userdata}/keymaps/backspace.xml

echo "Unmounting CoreELEC data partition"
sudo umount -d ${mount_point}
echo "Deleting mount point"
rm -rf ${mount_point}

echo "Rename image file"
mv ${source_img_name}.img ${target_img_name}.img
echo "Compressing CoreELEC image"
gzip ${target_img_name}.img
sha256sum ${target_img_name}.img.gz > ${target_img_name}.img.gz.sha256
