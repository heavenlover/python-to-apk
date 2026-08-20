# 今日塔罗 —— Python 打包成 Android APK 示例

一个适合手机竖屏使用的 Kivy 塔罗占卜应用：选择牌阵后抽牌，牌面会按位置摊开，并提供正位、逆位和组合解读。
配合 GitHub Actions，把本仓库里的 Python 代码自动打包成可安装的 Android APK，全程不需要本地安装 Android 开发环境。

## 项目结构

| 文件 | 作用 |
|------|------|
| `main.py` | Kivy 应用入口，提供随机单牌占卜 |
| `720px/` | 韦特塔罗牌图资源，包含牌背和完整 78 张牌 |
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

牌面和牌义都定义在 `main.py` 的 `CARDS` 列表中，可以按需要继续添加牌。应用使用本地图片，翻牌时不需要网络。

## 牌阵功能

- **单张牌**：当日简短提示与行动指引。
- **圣三角**：过去、现在、未来，共 3 张。
- **二选一**：共同主题、选择 A、选择 B、行动建议，共 4 张。
- **凯尔特十字**：现状、阻碍、根源、过去影响、可能目标、近期走向、内心状态、外部环境、希望与担忧、最终走向，共 10 张。

每张牌会随机决定正位或逆位。解读会综合大阿尔卡那数量、权杖/圣杯/宝剑/星币花色重点，以及各位置的牌义，作为代入现实处境的参考建议。

## 图片版权说明

`720px/` 中使用的是经典 Rider-Waite-Smith（韦特）塔罗牌图，包含 22 张大阿尔卡那和 56 张小阿尔卡那。该套原始牌图已进入美国公共领域；发布 APK 前仍建议保留图片来源信息，并根据目标国家/地区的版权规则进行确认。

## Debug 与 Release 的区别

- **Debug**：执行 `buildozer -v android debug`，APK 未签名，适合测试安装。
- **Release**：执行 `buildozer -v android release`，自动用 `keytool` 生成签名密钥并签名，适合发布应用商店。生成的密钥会作为构件上传（保留 1 天），**请及时下载保存**，以后用它给应用升级签名。

## 注意事项

- 首次构建会下载 Android SDK / NDK 和 Python 依赖，耗时较长属正常现象。
- 构建环境已安装 `libcairo2-dev`（KivyMD 的 `pycairo` 依赖需要系统 cairo 库，否则 `pip install kivymd` 会报 `Dependency "cairo" not found`）。
- `buildozer.spec` 中的 `android.sdk_path` 指向 GitHub Actions 预装的 Android SDK（许可证已预先接受），可避免 `sdkmanager` 交互式询问许可证导致构建失败；本地构建时请注释掉该行。
- GitHub Actions 预装 SDK 的 `sdkmanager` 位于 `cmdline-tools/latest/bin/`，而 buildozer 只在 `tools/bin/` 下找它——workflow 里已用符号链接解决（对应步骤名 `Prepare Android SDK for buildozer`）。
- Release 工作流使用的密钥密码是示例值 `android`，如需发布正式应用请自行更换。
- 想使用 KivyMD 组件时，在 `buildozer.spec` 的 `requirements` 中追加 `kivymd` 即可。
