#!/usr/bin/env python3
"""Generate the Chillpass app icon from parametric vector geometry.

Deliverables are built inside Photoshop from native vector shape layers:
  - Clean icon: 1024 px, full-bleed white, RGB PNG + layered PSD
  - No-white:   1024 px, transparent background, RGBA PNG + layered PSD

Run this script to regenerate previews and the Photoshop build script.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
ANALYSIS = ROOT / "_analysis"
TEMP = Path(r"C:\Users\chenyuchong\AppData\Local\Temp\chillpass_icon")
TEMP_OUT = TEMP / "out"
for folder in (OUT, ANALYSIS, TEMP, TEMP_OUT):
    folder.mkdir(parents=True, exist_ok=True)

FINAL_SIZE = 1024
TILE_CX = 640.0
TILE_CY = 639.5
TILE_W = 1050.0
FINAL_SCALE = FINAL_SIZE / TILE_W

PARAMS = {
    "version": 1,
    "reference": {"width": 1280, "height": 1280},
    "final": {"width": FINAL_SIZE, "height": FINAL_SIZE, "dpi": 72},
    "mapping": {
        "scale": FINAL_SCALE,
        "source_center": [TILE_CX, TILE_CY],
        "destination_center": [FINAL_SIZE / 2.0, FINAL_SIZE / 2.0],
    },
    "mark_color": "#000000",
    "clean_background": "#FFFFFF",
    "white_base": {
        "size": FINAL_SIZE,
        "exponent": 5.9,
        "segments": 160,
    },
    "C": {
        "cx": 587.0,
        "cy": 519.5,
        "r_outer": 205.9,
        "r_inner": 143.4,
        "outer_top_deg": -54.0,
        "inner_top_deg": -55.5,
        "bottom_deg": 60.0,
    },
    "P": {
        "cx": 740.75,
        "cy": 578.0,
        "r_outer": 135.25,
        "r_inner": 73.0,
        "terminal_x": 723.0,
        "topbar_left": 650.0,
    },
    "stem": {
        "left": 632.5,
        "right": 690.0,
        "top": 443.0,
        "bottom_center": 977.5,
        "bottom_radius": 28.75,
        "top_left_radius": 8.0,
    },
    "teeth": {
        "upper": {"left": 632.5, "right": 781.0, "top": 845.5, "bottom": 886.5,
                  "tl": 0.0, "tr": 4.0, "br": 20.0, "bl": 0.0},
        "web": {"left": 632.5, "right": 711.5, "top": 885.5, "bottom": 915.5,
                "tl": 0.0, "tr": 4.0, "br": 4.0, "bl": 0.0},
        "lower": {"left": 632.5, "right": 780.0, "top": 914.5, "bottom": 956.5,
                  "tl": 0.0, "tr": 4.0, "br": 18.0, "bl": 0.0},
    },
}

Point = tuple[float, float]
Cubic = tuple[Point, Point, Point, Point]


def p(x: float, y: float) -> Point:
    return (float(x), float(y))


def distance(a: Point, b: Point) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def arc_cubics(cx: float, cy: float, r: float,
               start_deg: float, end_deg: float) -> list[Cubic]:
    """Cubic Bezier approximation of a circular arc, split to <=90 deg."""
    delta = end_deg - start_deg
    count = max(1, int(math.ceil(abs(delta) / 90.0 - 1e-9)))
    step = delta / count
    result: list[Cubic] = []
    for i in range(count):
        a0 = math.radians(start_deg + step * i)
        a1 = math.radians(start_deg + step * (i + 1))
        k = (4.0 / 3.0) * math.tan((a1 - a0) / 4.0)
        p0 = p(cx + r * math.cos(a0), cy + r * math.sin(a0))
        p3 = p(cx + r * math.cos(a1), cy + r * math.sin(a1))
        d0 = (-r * math.sin(a0), r * math.cos(a0))
        d1 = (-r * math.sin(a1), r * math.cos(a1))
        p1 = p(p0[0] + k * d0[0], p0[1] + k * d0[1])
        p2 = p(p3[0] - k * d1[0], p3[1] - k * d1[1])
        result.append((p0, p1, p2, p3))
    return result


class PathBuilder:
    """Collect contiguous cubic segments for one closed contour."""

    def __init__(self, start: Point):
        self.start = p(*start)
        self.current = p(*start)
        self.segments: list[Cubic] = []

    def line(self, end: Point) -> None:
        end = p(*end)
        if distance(end, self.current) < 1e-9:
            return
        self.segments.append((self.current, self.current, end, end))
        self.current = end

    def arc(self, cx: float, cy: float, r: float,
            start_deg: float, end_deg: float) -> None:
        allowed = p(cx + r * math.cos(math.radians(start_deg)),
                    cy + r * math.sin(math.radians(start_deg)))
        if distance(allowed, self.current) > 1e-5:
            raise ValueError(f"Arc start mismatch: {allowed} vs {self.current}")
        segs = arc_cubics(cx, cy, r, start_deg, end_deg)
        self.segments.extend(segs)
        self.current = segs[-1][3]

    def close(self) -> None:
        self.line(self.start)


def c_shape() -> list[Cubic]:
    q = PARAMS["C"]
    cx, cy, ro, ri = q["cx"], q["cy"], q["r_outer"], q["r_inner"]
    top_outer = q["outer_top_deg"]
    top_inner = q["inner_top_deg"] + 360.0
    bottom = q["bottom_deg"]
    b = PathBuilder(p(cx + ro * math.cos(math.radians(top_outer)),
                      cy + ro * math.sin(math.radians(top_outer))))
    b.arc(cx, cy, ro, top_outer, bottom - 360.0)
    b.line(p(cx + ri * math.cos(math.radians(bottom)),
             cy + ri * math.sin(math.radians(bottom))))
    b.arc(cx, cy, ri, bottom, top_inner)
    b.close()
    return b.segments


def p_shape() -> list[Cubic]:
    q = PARAMS["P"]
    cx, cy, ro, ri = q["cx"], q["cy"], q["r_outer"], q["r_inner"]
    tx = q["terminal_x"]
    theta_out = math.degrees(math.acos((tx - cx) / ro))
    theta_in = math.degrees(math.acos((tx - cx) / ri))
    y_in_cut = cy + ri * math.sin(math.radians(theta_in))
    top_left = p(q["topbar_left"], cy - ro)
    b = PathBuilder(top_left)
    b.line(p(cx, cy - ro))
    b.arc(cx, cy, ro, -90.0, theta_out)
    b.line(p(tx, y_in_cut))
    b.arc(cx, cy, ri, theta_in, -90.0)
    b.line(p(q["topbar_left"], cy - ri))
    b.close()
    return b.segments


def stem_shape() -> list[Cubic]:
    q = PARAMS["stem"]
    l, r, t = q["left"], q["right"], q["top"]
    bc, br, tlr = q["bottom_center"], q["bottom_radius"], q["top_left_radius"]
    midx = (l + r) / 2.0
    b = PathBuilder(p(l + tlr, t))
    b.line(p(r, t))
    b.line(p(r, bc))
    b.arc(midx, bc, br, 0.0, 180.0)
    b.line(p(l, t + tlr))
    b.arc(l + tlr, t + tlr, tlr, 180.0, 270.0)
    b.close()
    return b.segments


def rounded_rect_shape(q: dict) -> list[Cubic]:
    l, r, t, btm = q["left"], q["right"], q["top"], q["bottom"]
    tl, tr, br, bl = q["tl"], q["tr"], q["br"], q["bl"]
    b = PathBuilder(p(l + tl, t))
    b.line(p(r - tr, t))
    if tr:
        b.arc(r - tr, t + tr, tr, -90.0, 0.0)
    b.line(p(r, btm - br))
    if br:
        b.arc(r - br, btm - br, br, 0.0, 90.0)
    b.line(p(l + bl, btm))
    if bl:
        b.arc(l + bl, btm - bl, bl, 90.0, 180.0)
    b.line(p(l, t + tl))
    if tl:
        b.arc(l + tl, t + tl, tl, 180.0, 270.0)
    b.close()
    return b.segments


def all_shapes() -> dict[str, list[Cubic]]:
    return {
        "C - ring": c_shape(),
        "P - key bow": p_shape(),
        "Key - stem": stem_shape(),
        "Key - web": rounded_rect_shape(PARAMS["teeth"]["web"]),
        "Key - upper tooth": rounded_rect_shape(PARAMS["teeth"]["upper"]),
        "Key - lower tooth": rounded_rect_shape(PARAMS["teeth"]["lower"]),
    }


def to_icon(pt: Point) -> Point:
    m = PARAMS["mapping"]
    sx, sy = m["source_center"]
    dx, dy = m["destination_center"]
    s = m["scale"]
    return (dx + (pt[0] - sx) * s, dy + (pt[1] - sy) * s)


def flatten(segments: list[Cubic], per_curve: int = 36) -> list[Point]:
    pts: list[Point] = []
    for p0, p1, p2, p3 in segments:
        for i in range(per_curve):
            t = i / float(per_curve)
            mt = 1.0 - t
            x = (mt ** 3) * p0[0] + 3 * (mt ** 2) * t * p1[0] + \
                3 * mt * (t ** 2) * p2[0] + (t ** 3) * p3[0]
            y = (mt ** 3) * p0[1] + 3 * (mt ** 2) * t * p1[1] + \
                3 * mt * (t ** 2) * p2[1] + (t ** 3) * p3[1]
            pts.append((x, y))
    return pts


def segments_to_nodes(segments: list[Cubic], transform=None) -> list[dict]:
    if transform is None:
        transform = to_icon
    if distance(segments[0][0], segments[-1][3]) > 1e-5:
        raise ValueError("Contour is not closed")
    nodes: list[dict] = []
    for i, (p0, p1, p2, p3) in enumerate(segments):
        if i == 0:
            nodes.append({"a": transform(p0), "i": transform(p0), "o": transform(p1)})
        else:
            if distance(p0, segments[i - 1][3]) > 1e-5:
                raise ValueError("Contour is not contiguous")
            nodes[-1]["o"] = transform(p1)
        if i < len(segments) - 1:
            nodes.append({"a": transform(p3), "i": transform(p2), "o": transform(p3)})
        else:
            nodes[0]["i"] = transform(p2)

    # Round and classify smoothness for a tidy Photoshop path.
    result = []
    for node in nodes:
        a = tuple(round(v, 4) for v in node["a"])
        inh = tuple(round(v, 4) for v in node["i"])
        outh = tuple(round(v, 4) for v in node["o"])
        vin = (a[0] - inh[0], a[1] - inh[1])
        vout = (outh[0] - a[0], outh[1] - a[1])
        lv_in = math.hypot(*vin)
        lv_out = math.hypot(*vout)
        smooth = False
        if lv_in > 0.2 and lv_out > 0.2:
            cross = abs(vin[0] * vout[1] - vin[1] * vout[0])
            dot = vin[0] * vout[0] + vin[1] * vout[1]
            smooth = cross < 1e-3 * lv_in * lv_out and dot > 0
        result.append({
            "a": [a[0], a[1]],
            # Photoshop's left handle is the outgoing control point in this
            # path construction; right is the incoming control point.
            "l": [outh[0], outh[1]],
            "r": [inh[0], inh[1]],
            "smooth": smooth,
        })
    return result


def make_layer_payload() -> list[dict]:
    return [
        {"name": name, "nodes": segments_to_nodes(segments)}
        for name, segments in all_shapes().items()
    ]


def squircle_cubics() -> list[Cubic]:
    """Continuous-curvature superellipse sampled by arc length.

    The resulting Catmull-Rom cubics pass through uniformly spaced boundary
    points and have a continuous tangent at every anchor. The source tile's
    measured exponent is 5.9, so the corner transition has no straight-to-arc
    curvature break.
    """
    q = PARAMS["white_base"]
    size, exponent, count = q["size"], q["exponent"], q["segments"]
    c0 = size / 2.0
    radius = size / 2.0
    t = np.linspace(0.0, 2.0 * math.pi, 8192, endpoint=False)
    cosine = np.cos(t)
    sine = np.sin(t)
    xs = c0 + radius * np.sign(cosine) * np.abs(cosine) ** (2.0 / exponent)
    ys = c0 + radius * np.sign(sine) * np.abs(sine) ** (2.0 / exponent)
    raw = np.column_stack([xs, ys])
    closed = np.vstack([raw, raw[0]])
    lengths = np.sqrt((np.diff(closed, axis=0) ** 2).sum(axis=1))
    cumulative = np.concatenate([[0.0], np.cumsum(lengths)])
    targets = np.linspace(0.0, cumulative[-1], count, endpoint=False)
    sampled = np.column_stack([
        np.interp(targets, cumulative, closed[:, 0]),
        np.interp(targets, cumulative, closed[:, 1]),
    ])
    prev = sampled[(np.arange(count) - 1) % count]
    nxt = sampled[(np.arange(count) + 1) % count]
    tangents = (nxt - prev) * 0.5
    result: list[Cubic] = []
    for i in range(count):
        p0 = sampled[i]
        p3 = sampled[(i + 1) % count]
        p1 = p0 + tangents[i] / 3.0
        p2 = p3 - tangents[(i + 1) % count] / 3.0
        result.append((p(*p0), p(*p1), p(*p2), p(*p3)))
    return result


def white_base_nodes() -> list[dict]:
    return segments_to_nodes(squircle_cubics(), transform=lambda pt: pt)


def mask_from_cubics(size: int, segments: list[Cubic], ss: int = 4,
                     transform=None) -> Image.Image:
    W = size * ss
    mask = Image.new("L", (W, W), 0)
    draw = ImageDraw.Draw(mask)
    if transform is None:
        transform = lambda pt: pt
    pts = [transform(pt) for pt in flatten(segments, per_curve=10)]
    draw.polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def mark_mask(size: int, ss: int = 4) -> Image.Image:
    W = size * ss
    mask = Image.new("L", (W, W), 0)
    draw = ImageDraw.Draw(mask)
    for segments in all_shapes().values():
        pts = [to_icon(pt) for pt in flatten(segments)]
        draw.polygon([(x * ss, y * ss) for x, y in pts], fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def build_previews() -> None:
    mark = mark_mask(FINAL_SIZE, ss=4)
    base = mask_from_cubics(FINAL_SIZE, squircle_cubics(), ss=4)

    # Clean icon: continuous-corner white squircle over a transparent canvas.
    clean = Image.new("RGBA", (FINAL_SIZE, FINAL_SIZE), (0, 0, 0, 0))
    white = Image.new("RGBA", clean.size, (255, 255, 255, 255))
    black = Image.new("RGBA", clean.size, (0, 0, 0, 255))
    clean = Image.composite(white, clean, base)
    clean = Image.composite(black, clean, mark)
    clean.save(ANALYSIS / "preview_clean_1024.png")

    # Transparent mark only.
    no_white = Image.new("RGBA", (FINAL_SIZE, FINAL_SIZE), (0, 0, 0, 0))
    no_white = Image.composite(black, no_white, mark)
    no_white.save(ANALYSIS / "preview_no_white_1024.png")

    # Previews over a neutral background show the actual alpha silhouette.
    grey = Image.new("RGBA", (FINAL_SIZE, FINAL_SIZE), (218, 218, 218, 255))
    clean_grey = grey.copy()
    clean_grey.alpha_composite(clean)
    no_white_grey = grey.copy()
    no_white_grey.alpha_composite(no_white)
    clean_grey.convert("RGB").save(ANALYSIS / "preview_clean_on_grey.png")
    no_white_grey.convert("RGB").save(ANALYSIS / "preview_no_white_on_grey.png")

    side = Image.new("RGB", (FINAL_SIZE * 2 + 32, FINAL_SIZE), (25, 25, 25))
    side.paste(clean_grey.convert("RGB"), (0, 0))
    side.paste(no_white_grey.convert("RGB"), (FINAL_SIZE + 32, 0))
    side.save(ANALYSIS / "clean_vs_no_white.png")
    print("preview: mark coverage", float((np.asarray(mark) > 127).mean()))
    print("preview: white base coverage", float((np.asarray(base) > 127).mean()))
    print("previews written")


def jsx_number(x: float) -> str:
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s if s else "0"


def node_js(node: dict) -> str:
    a = ",".join(jsx_number(v) for v in node["a"])
    l = ",".join(jsx_number(v) for v in node["l"])
    r = ",".join(jsx_number(v) for v in node["r"])
    smooth = "true" if node["smooth"] else "false"
    return f'{{a:[{a}],l:[{l}],r:[{r}],smooth:{smooth}}}'


def generate_jsx(payload: list[dict], white_nodes: list[dict]) -> Path:
    layer_js = ",\n".join(
        '  {name:"%s",nodes:[%s]}' % (
            layer["name"].replace('"', '\\"'),
            ",".join(node_js(n) for n in layer["nodes"]),
        )
        for layer in payload
    )
    white_js = ",".join(node_js(n) for n in white_nodes)
    psd_clean = (TEMP_OUT / "Chillpass_Icon_Clean_1024.psd").as_posix()
    png_clean = (TEMP_OUT / "Chillpass_Icon_Clean_1024.png").as_posix()
    psd_no_white = (TEMP_OUT / "Chillpass_Icon_NoWhite_1024.psd").as_posix()
    png_no_white = (TEMP_OUT / "Chillpass_Icon_NoWhite_1024.png").as_posix()
    log_path = (TEMP / "build.log").as_posix()
    jsx_path = TEMP / "build_chillpass.jsx"

    jsx = f"""#target photoshop
(function () {{
    var logFile = new File("{log_path}");
    logFile.encoding = "UTF8";
    logFile.open("w");
    function log(msg) {{ logFile.writeln(msg); }}
    var LAYERS = [
{layer_js}
    ];
    var WHITE_BASE = [{white_js}];
    var MARK_HEX = "000000";
    var BASE_HEX = "FFFFFF";
    var DOC_SIZE = {FINAL_SIZE};

    function selectPathByName(name) {{
        var d = new ActionDescriptor();
        var ref = new ActionReference();
        ref.putName(charIDToTypeID("Path"), name);
        d.putReference(charIDToTypeID("null"), ref);
        executeAction(charIDToTypeID("slct"), d, DialogModes.NO);
    }}

    function makeShapeLayer(doc, data, group, hexColor) {{
        var points = [];
        for (var i = 0; i < data.nodes.length; i++) {{
            var n = data.nodes[i];
            var pt = new PathPointInfo();
            pt.kind = n.smooth ? PointKind.SMOOTHPOINT : PointKind.CORNERPOINT;
            pt.anchor = n.a;
            pt.leftDirection = n.l;
            pt.rightDirection = n.r;
            points.push(pt);
        }}
        var sub = new SubPathInfo();
        sub.closed = true;
        sub.operation = ShapeOperation.SHAPEADD;
        sub.entireSubPath = points;
        var pathName = "__tmp_" + data.name.replace(/ /g, "_");
        var pathItem = doc.pathItems.add(pathName, [sub]);
        selectPathByName(pathName);

        var color = new SolidColor();
        color.rgb.hexValue = hexColor;
        var desc = new ActionDescriptor();
        var ref = new ActionReference();
        ref.putClass(stringIDToTypeID("contentLayer"));
        desc.putReference(charIDToTypeID("null"), ref);
        var usingDesc = new ActionDescriptor();
        var typeDesc = new ActionDescriptor();
        var colorDesc = new ActionDescriptor();
        colorDesc.putDouble(charIDToTypeID("Rd  "), color.rgb.red);
        colorDesc.putDouble(charIDToTypeID("Grn "), color.rgb.green);
        colorDesc.putDouble(charIDToTypeID("Bl  "), color.rgb.blue);
        typeDesc.putObject(charIDToTypeID("Clr "), charIDToTypeID("RGBC"), colorDesc);
        usingDesc.putObject(charIDToTypeID("Type"), stringIDToTypeID("solidColorLayer"), typeDesc);
        desc.putObject(charIDToTypeID("Usng"), stringIDToTypeID("contentLayer"), usingDesc);
        executeAction(charIDToTypeID("Mk  "), desc, DialogModes.NO);

        var layer = doc.activeLayer;
        layer.name = data.name;
        if (group) {{
            layer.move(group, ElementPlacement.INSIDE);
        }}
        try {{
            pathItem.remove();
        }} catch (pathErr) {{
            log("path cleanup warning: " + pathErr.message);
        }}
        return layer;
    }}

    function savePSD(doc, path) {{
        var opts = new PhotoshopSaveOptions();
        opts.layers = true;
        opts.embedColorProfile = true;
        opts.maximizeCompatibility = true;
        doc.saveAs(new File(path), opts, true, Extension.LOWERCASE);
    }}

    function exportPNG(doc, path, transparent) {{
        var opts = new ExportOptionsSaveForWeb();
        opts.format = SaveDocumentType.PNG;
        opts.PNG8 = false;
        opts.transparency = transparent;
        opts.interlaced = false;
        opts.quality = 100;
        doc.exportDocument(new File(path), ExportType.SAVEFORWEB, opts);
    }}

    function buildVersion(clean, psdPath, pngPath) {{
        var name = clean ? "Chillpass icon clean" : "Chillpass icon no white";
        var doc = app.documents.add(DOC_SIZE, DOC_SIZE, 72, name,
            NewDocumentMode.RGB, DocumentFill.TRANSPARENT,
            1.0, BitsPerChannelType.EIGHT, "sRGB IEC61966-2.1");
        if (clean) {{
            makeShapeLayer(doc, {{name: "White squircle base", nodes: WHITE_BASE}}, null, BASE_HEX);
        }}
        var group = doc.layerSets.add();
        group.name = "CP Key Mark";
        for (var i = 0; i < LAYERS.length; i++) {{
            makeShapeLayer(doc, LAYERS[i], group, MARK_HEX);
        }}
        log(name + ": layers=" + doc.layers.length +
            ", artLayers=" + doc.artLayers.length +
            ", groups=" + doc.layerSets.length);

        savePSD(doc, psdPath);
        log("saved PSD " + psdPath);
        exportPNG(doc, pngPath, true);
        log("saved PNG " + pngPath);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    }}

    try {{
        app.bringToFront();
        app.displayDialogs = DialogModes.NO;
        app.preferences.rulerUnits = Units.PIXELS;
        buildVersion(true, "{psd_clean}", "{png_clean}");
        buildVersion(false, "{psd_no_white}", "{png_no_white}");
        log("DONE");
    }} catch (err) {{
        log("ERROR line " + err.line + ": " + err.message);
    }} finally {{
        logFile.close();
    }}
}})();
"""
    jsx_path.write_text(jsx, encoding="utf-8")
    (ROOT / "build_chillpass.jsx").write_text(jsx, encoding="utf-8")
    (TEMP_OUT / "icon_params.json").write_text(
        json.dumps(PARAMS, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", jsx_path)
    return jsx_path


if __name__ == "__main__":
    shapes = all_shapes()
    payload = make_layer_payload()
    for name, segs in shapes.items():
        print(f"{name}: {len(segs)} cubic segments -> "
              f"{len(payload[[x['name'] for x in payload].index(name)]['nodes'])} anchors")
    build_previews()
    white_nodes = white_base_nodes()
    print(f"white base: {len(white_nodes)} anchors")
    generate_jsx(payload, white_nodes)
