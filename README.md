# Chillpass 设计规范

本仓库收录 Chillpass 品牌视觉资产与参数化设计源文件。

## 应用图标

提供两种 1024×1024 版本：

| 版本 | 说明 | 文件 |
|---|---|---|
| Clean | 白色连续曲率超椭圆底板 + 黑色 CP 钥匙标志，四角外侧透明 | `app-icon/Chillpass_Icon_Clean_1024.png` / `.psd` |
| NoWhite | 仅黑色 CP 钥匙标志，透明背景 | `app-icon/Chillpass_Icon_NoWhite_1024.png` / `.psd` |

## 规格

- 尺寸：1024 × 1024 px
- 色彩：sRGB，8 位/通道
- 标志颜色：`#000000`
- Clean 底板：`#FFFFFF`
- Clean 外轮廓：超椭圆连续曲线，指数约 5.9；不存在直边与圆弧相接造成的硬拐点
- PNG 均带 Alpha 通道；Clean 的透明区域位于四角外侧，NoWhite 全部背景透明
- 标志由参数化矢量路径重建，原图没有作为位图图层嵌入 PSD

## PSD 结构

**Clean**

- `White squircle base`
- `CP Key Mark`
  - `C - ring`
  - `P - key bow`
  - `Key - stem`
  - `Key - web`
  - `Key - upper tooth`
  - `Key - lower tooth`

**NoWhite**

- `CP Key Mark`
  - `C - ring`
  - `P - key bow`
  - `Key - stem`
  - `Key - web`
  - `Key - upper tooth`
  - `Key - lower tooth`

## 目录结构

```text
Chillpass设计规范/
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

## 参数化源文件

- `source/generate_icon.py`：参数表、几何路径、预览和 Photoshop 构建脚本生成器
- `source/build_chillpass.jsx`：Photoshop 矢量形状层构建与导出脚本
- `source/icon_params.json`：图标几何与颜色参数快照

白色底板使用连续曲率超椭圆路径，四边与四角之间由平滑贝塞尔曲线过渡；标志的 C、P、钥匙杆和齿部由圆弧、直线与贝塞尔曲线参数定义。PSD 中的成品标志和底板均为可编辑形状层。
