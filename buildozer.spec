# ============================================================================
# Buildozer 配置文件 —— 把 Python/Kivy 应用打包成 Android APK
# 文档: https://buildozer.readthedocs.io/
# ============================================================================

[app]

# 应用在手机上显示的名称
title = 今日塔罗

# 包名（只能用小写字母、数字、下划线）
package.name = tarottoday

# 包域名（反写域名，最终应用 ID 为 org.example.photoshow）
package.domain = org.example

# 源码目录（相对本文件所在目录）
source.dir = .

# 打包时包含的文件扩展名
source.include_exts = py,png,jpg,jpeg,kv,atlas

# 应用版本号
version = 0.1

# 依赖库（python3 必选；需要 Material Design 时在后面追加 kivymd）
requirements = python3,kivy

# 屏幕方向：portrait(竖屏) / landscape(横屏) / all
orientation = portrait

# 全屏显示（1=全屏，0=显示系统状态栏）
fullscreen = 0

# ---------------------- Android ----------------------
# 使用 GitHub Actions 预装的 Android SDK（许可证已预先接受，避免 sdkmanager 交互式询问）
# 本地构建请注释掉此行，让 buildozer 自行下载 SDK
android.sdk_path = /usr/local/lib/android/sdk

# 自动接受 Android SDK 许可证（构建时若仍有许可证询问会自动应答 y，避免 CI 卡住）
android.accept_sdk_license = True

# 目标 SDK 版本与最低支持的 Android 系统版本
android.api = 33
android.minapi = 21

# NDK 版本（若构建报 NDK 相关错误，可尝试 25b / 27b）
android.ndk = 25b

# 支持的 CPU 架构（armeabi-v7a 可兼容老设备，但会显著加长构建时间）
android.archs = arm64-v8a

# 是否允许应用数据被备份
android.allow_backup = True

# ---------------------- Release 签名 ----------------------
# 与 .github/workflows/release.yml 中自动生成的密钥保持一致
android.keystore = DomainName.PackageName.keystore
android.keystore.alias = DomainName.PackageName
android.keystore.storepass = android
android.keystore.keypass = android

[buildozer]

# 日志级别（0-2，2 为最详细）
log_level = 2

# 以 root 运行时给出警告
warn_on_root = 1
