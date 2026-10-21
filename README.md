# Chillpass Design Specification

本仓库收录 Chillpass 品牌视觉资产、设计规范及其参数化生成源文件。

## 仓库结构

```text
ChillpassDesignSpecification/
├── README.md
├── .gitignore
└── icon/
    ├── README.md
    ├── app-icon/
    │   ├── Chillpass_Icon_Clean_1024.png
    │   ├── Chillpass_Icon_Clean_1024.psd
    │   ├── Chillpass_Icon_NoWhite_1024.png
    │   └── Chillpass_Icon_NoWhite_1024.psd
    └── source/
        ├── generate_icon.py
        ├── build_chillpass.jsx
        └── icon_params.json
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
