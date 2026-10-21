# Chillpass 文字标

## 文件

| 文件 | 说明 |
|---|---|
| `Chillpass_TextLogo_White_2400x900.png` | 白底版，2400×900，黑色文字标，RGB |
| `Chillpass_TextLogo_White_2400x900.psd` | 白底分层源文件，含白色背景和矢量文字标 |
| `Chillpass_TextLogo_Transparent_2400x900.png` | 透明背景版，2400×900，黑色文字标，RGBA |
| `Chillpass_TextLogo_Transparent_2400x900.psd` | 透明分层源文件，仅保留矢量文字标 |

## 设计规格

- 文字：`chillpass`，全小写
- 字体：Montserrat Bold
- 字号：390 px
- 字距：-10（Photoshop / 1000 em）
- 画布：2400 × 900 px
- 字标实际包围盒：x 343–2057，y 250–629 px
- 水平居中，视觉中心略高于画布几何中心
- 文字颜色：`#000000`
- 白底：`#FFFFFF`
- PSD 采用 sRGB、8 位/通道，文字已在 Photoshop 中转换为可编辑矢量形状

## PSD 结构

**White**

- `chillpass wordmark`（矢量形状层）
- `背景`（白色）

**Transparent**

- `chillpass wordmark`（矢量形状层）
- 无背景图层

## 字体授权

**Montserrat** 使用 SIL Open Font License 1.1。

从授权条款看，Montserrat 可以用于商业项目，包括商标、Logo、印刷品和网页中的图形化使用。主要限制是不能把字体软件本身作为独立商品出售；修改后的字体软件如对外分发，仍需保留 OFL 授权。

完整授权文本见 [`Montserrat-OFL-1.1.txt`](Montserrat-OFL-1.1.txt)。字体版权归 The Montserrat Project Authors 所有。

## 参数化源文件

- `source/build_textlogo.jsx`：Photoshop 构建脚本，使用本机 `Montserrat-Bold` 排版并转换为矢量形状
- `source/textlogo_params.json`：字体、字号、字距、画布和颜色参数快照

构建脚本依赖本机已安装 Montserrat Bold；成品 PSD 和 PNG 不依赖字体环境。
