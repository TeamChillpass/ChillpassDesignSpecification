# Chillpass Design Specification

本仓库收录 Chillpass 品牌视觉资产、设计规范及其参数化生成源文件。

## 仓库结构

```text
ChillpassDesignSpecification/
├── icon/
└── textLogo/
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
