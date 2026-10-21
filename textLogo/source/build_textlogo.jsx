#target photoshop
// Chillpass text logo builder.
// Typeface: Montserrat Bold (must be installed in Photoshop).
// License: SIL Open Font License 1.1 (see ../Montserrat-OFL-1.1.txt).
// The finished wordmark is converted to an editable vector shape, so the PSD
// does not depend on the font being installed.
(function () {
    var scriptFile = new File($.fileName);
    var sourceDir = scriptFile.parent;
    var logoDir = sourceDir.parent;
    var OUT = logoDir.fsName + "/";
    var logFile = new File(Folder.temp.fsName + "/chillpass_textlogo_build.log");
    logFile.encoding = "UTF8";
    logFile.open("w");
    function log(msg) { logFile.writeln(msg); }

    var FONT = "Montserrat-Bold";
    var WORD = "chillpass";
    var DOC_W = 2400;
    var DOC_H = 900;
    var FONT_SIZE = 390;
    var TRACKING = -10;
    var TARGET_CENTER_X = 1200;
    var TARGET_CENTER_Y = 439.3;

    function setBlack(ti) {
        var c = new SolidColor();
        c.rgb.hexValue = "000000";
        ti.color = c;
    }

    function addWordmark(doc) {
        var layer = doc.artLayers.add();
        layer.name = "chillpass wordmark";
        layer.kind = LayerKind.TEXT;
        var ti = layer.textItem;
        ti.kind = TextType.POINTTEXT;
        ti.contents = WORD;
        ti.font = FONT;
        ti.size = UnitValue(FONT_SIZE, "px");
        ti.tracking = TRACKING;
        ti.antiAliasMethod = AntiAlias.SMOOTH;
        ti.justification = Justification.LEFT;
        setBlack(ti);
        ti.position = [UnitValue(1200, "px"), UnitValue(500, "px")];

        // Photoshop's own type engine keeps counters and overlapping contours
        // intact; convert the result to a native vector shape.
        ti.convertToShape();
        var shape = doc.activeLayer;
        shape.name = "chillpass wordmark";
        var b = shape.bounds;
        var left = b[0].as("px"), top = b[1].as("px");
        var right = b[2].as("px"), bottom = b[3].as("px");
        log("converted bounds: " + left + "," + top + "," + right + "," + bottom);
        var dx = TARGET_CENTER_X - (left + right) / 2.0;
        var dy = TARGET_CENTER_Y - (top + bottom) / 2.0;
        shape.translate(UnitValue(dx, "px"), UnitValue(dy, "px"));
        b = shape.bounds;
        log("final bounds: " + b[0].as("px") + "," + b[1].as("px") + "," +
            b[2].as("px") + "," + b[3].as("px"));
        return shape;
    }

    function removeEmptyLayers(doc) {
        for (var i = doc.layers.length - 1; i >= 0; i--) {
            var l = doc.layers[i];
            if (l.typename !== "ArtLayer") continue;
            if (l.kind !== LayerKind.NORMAL) continue;
            var b = l.bounds;
            if (b[0].as("px") === 0 && b[1].as("px") === 0 &&
                b[2].as("px") === 0 && b[3].as("px") === 0) {
                l.remove();
            }
        }
    }

    function savePSD(doc, path) {
        var opts = new PhotoshopSaveOptions();
        opts.layers = true;
        opts.embedColorProfile = true;
        opts.maximizeCompatibility = true;
        doc.saveAs(new File(path), opts, true, Extension.LOWERCASE);
    }

    function savePNG(doc, path, transparency) {
        var opts = new ExportOptionsSaveForWeb();
        opts.format = SaveDocumentType.PNG;
        opts.PNG8 = false;
        opts.transparency = transparency;
        opts.interlaced = false;
        opts.quality = 100;
        doc.exportDocument(new File(path), ExportType.SAVEFORWEB, opts);
    }

    function buildWhite() {
        var doc = app.documents.add(DOC_W, DOC_H, 72, "Chillpass textlogo white",
            NewDocumentMode.RGB, DocumentFill.WHITE, 1.0,
            BitsPerChannelType.EIGHT, "sRGB IEC61966-2.1");
        addWordmark(doc);
        savePSD(doc, OUT + "Chillpass_TextLogo_White_2400x900.psd");
        var flat = doc.duplicate("textlogo white export");
        flat.flatten();
        savePNG(flat, OUT + "Chillpass_TextLogo_White_2400x900.png", false);
        flat.close(SaveOptions.DONOTSAVECHANGES);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    }

    function buildTransparent() {
        var doc = app.documents.add(DOC_W, DOC_H, 72, "Chillpass textlogo transparent",
            NewDocumentMode.RGB, DocumentFill.TRANSPARENT, 1.0,
            BitsPerChannelType.EIGHT, "sRGB IEC61966-2.1");
        addWordmark(doc);
        removeEmptyLayers(doc);
        savePSD(doc, OUT + "Chillpass_TextLogo_Transparent_2400x900.psd");
        savePNG(doc, OUT + "Chillpass_TextLogo_Transparent_2400x900.png", true);
        doc.close(SaveOptions.DONOTSAVECHANGES);
    }

    try {
        app.bringToFront();
        app.displayDialogs = DialogModes.NO;
        app.preferences.rulerUnits = Units.PIXELS;
        buildWhite();
        buildTransparent();
        log("DONE");
    } catch (err) {
        log("ERROR line " + err.line + ": " + err.message);
    } finally {
        logFile.close();
    }
})();
