# Chillpass Design Specification

本仓库收录 Chillpass 品牌视觉资产、设计规范、团队头像与活动物料。

## 仓库结构

```text
ChillpassDesignSpecification/
├── icon/
├── textLogo/
├── 头像/
└── 首次公测海报/
```

## 资产导航

### 应用图标

完整规格与图层说明见 [icon/README.md](icon/README.md)。

- `icon/app-icon/Chillpass_Icon_Clean_1024.png`：白色连续曲率底板配黑色标志，透明四角
- `icon/app-icon/Chillpass_Icon_Clean_1024.psd`：分层可编辑源文件
- `icon/app-icon/Chillpass_Icon_NoWhite_1024.png`：透明背景，仅黑色标志
- `icon/app-icon/Chillpass_Icon_NoWhite_1024.psd`：分层可编辑源文件
- `icon/source/`：图标几何参数、Python 生成器与 Photoshop 构建脚本

所有图标均为 1024×1024 px、sRGB、8 位/通道；成品由参数化矢量路径在 Adobe Photoshop 中重建，源图片未作为位图嵌入 PSD。

### 文字标

完整规格与字体授权说明见 [textLogo/README.md](textLogo/README.md)。

- `textLogo/Chillpass_TextLogo_White_2400x900.png`：白底版，RGB
- `textLogo/Chillpass_TextLogo_White_2400x900.psd`：白底分层源文件
- `textLogo/Chillpass_TextLogo_Transparent_2400x900.png`：透明背景版，RGBA
- `textLogo/Chillpass_TextLogo_Transparent_2400x900.psd`：透明分层源文件
- `textLogo/source/`：Photoshop 构建脚本与排版参数

文字标使用 **Montserrat Bold**，画布 2400×900 px，字号 390 px，字距 -10。文字已转换为可编辑矢量形状。Montserrat 采用 SIL Open Font License 1.1，可用于商业项目；完整授权文本见 `textLogo/Montserrat-OFL-1.1.txt`。

### 团队头像

- `头像/CAI.jpg` / `头像/CAI.psd`：1280×1280
- `头像/CHEN.jpg` / `头像/CHEN.psd`：1296×1296
- `头像/YANG.jpg` / `头像/YANG.psd`：1280×1280

三位团队成员的手绘头像，提供正方形 JPG 预览图和 Photoshop 分层源文件。

### 首次公测海报

- `首次公测海报/首次公测海报.png` / `.psd`：5166×6917，首轮公测招募主海报
- `首次公测海报/二维码.jpg` / `二维码-1.psd`：916×916，配套二维码素材
- `首次公测海报/配图.jpg` / `配图-1.psd`：1279×1706，配套插画素材

首轮公测宣传物料，包含主海报、二维码和配图的发布图与分层源文件。
