# PhotoShow —— Python 打包成 Android APK 示例

一个极简的 Kivy 示例应用：启动后显示一张照片，**5 秒后自动退出**。
配合 GitHub Actions，把本仓库里的 Python 代码自动打包成可安装的 Android APK，全程不需要本地安装 Android 开发环境。

## 项目结构

| 文件 | 作用 |
|------|------|
| `main.py` | Kivy 应用入口，显示照片 5 秒后退出 |
| `buildozer.spec` | Buildozer 打包配置（包名、依赖、签名等） |
| `.github/workflows/debug.yml` | GitHub Actions：构建 **Debug** 版 APK（未签名） |
| `.github/workflows/release.yml` | GitHub Actions：构建 **Release** 版 APK（自动生成密钥并签名） |
| `.gitignore` | 忽略构建产物、APK、签名密钥等 |

## 使用方法（全程在 GitHub 云端构建）

1. 把本文件夹推送到一个 GitHub 仓库（例如 `git push`）。
2. 打开仓库的 **Actions** 页面。
3. 在左侧选择 `Build Kivy Android APK In Debug Mode` 或 `Build Kivy Android APK In Release Mode`。
4. 点击 **Run workflow** → 运行（两个工作流都是手动触发的 `workflow_dispatch`）。
5. 构建完成后（首次约 30~60 分钟），在运行记录页下载 `kivy-app-apk` 构件即可安装到手机。

## 放入你自己的照片

把照片放到项目根目录，命名为以下任意一个，打包后应用会自动显示它：

- `photo.jpg`
- `photo.png`
- `app_image.png`
- `image.jpg`

> 没有照片时，应用会自动生成一张蓝色占位图，保证在任何情况下都能正常显示。

修改 `main.py` 顶部的 `SHOW_SECONDS` 可以调整照片显示时长。

## Debug 与 Release 的区别

- **Debug**：执行 `buildozer -v android debug`，APK 未签名，适合测试安装。
- **Release**：执行 `buildozer -v android release`，自动用 `keytool` 生成签名密钥并签名，适合发布应用商店。生成的密钥会作为构件上传（保留 1 天），**请及时下载保存**，以后用它给应用升级签名。

## 注意事项

- 首次构建会下载 Android SDK / NDK 和 Python 依赖，耗时较长属正常现象。
- 构建环境已安装 `libcairo2-dev`（KivyMD 的 `pycairo` 依赖需要系统 cairo 库，否则 `pip install kivymd` 会报 `Dependency "cairo" not found`）。
- `buildozer.spec` 中的 `android.sdk_path` 指向 GitHub Actions 预装的 Android SDK（许可证已预先接受），可避免 `sdkmanager` 交互式询问许可证导致构建失败；本地构建时请注释掉该行。
- Release 工作流使用的密钥密码是示例值 `android`，如需发布正式应用请自行更换。
- 想使用 KivyMD 组件时，在 `buildozer.spec` 的 `requirements` 中追加 `kivymd` 即可。
