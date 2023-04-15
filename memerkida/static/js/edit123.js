/* eslint-disable vars-on-top,no-var,strict,prefer-template,prefer-arrow-callback,prefer-destructuring,object-shorthand,require-jsdoc,complexity,prefer-const,no-unused-vars */
var PIXELATE_FILTER_DEFAULT_VALUE = 20;
var supportingFileAPI = !!(window.File && window.FileList && window.FileReader);
var rImageType = /data:(image\/.+);base64,/;
var shapeOptions = {};
var shapeType;
var activeObjectId;

// Buttons
var $btns = $('.menu-item');
var $btnsActivatable = $btns.filter('.activatable');
var $inputImage = $('#input-image-file');
var $btnDownload = $('#btn-download');
var $btnImgSave = $('#btn-img-save');
var $btnUndo = $('#btn-undo');
var $btnRedo = $('#btn-redo');
var $btnClearObjects = $('#btn-clear-objects');
var $btnRemoveActiveObject = $('#btn-remove-active-object');
var $btnCrop = $('#btn-crop');
var $btnCrop1 = $('#btn-crop1');
var $btnFlip = $('#btn-flip');
var $btnRotation = $('#btn-rotation');
var $btnDrawLine = $('#btn-draw-line');
var $btnDrawShape = $('#btn-draw-shape');
var $btnApplyCrop = $('.btn-apply-crop');
var $btnCancelCrop = $('.btn-cancel-crop');
var $btnFlipX = $('.btn-flip-x');
var $btnFlipY = $('.btn-flip-y');
var $btnResetFlip = $('.btn-reset-flip');
var $btnRotateClockwise = $('.btn-rotate-clockwise');
var $btnRotateCounterClockWise = $('.btn-rotate-counter-clockwise');
var $btnText = $('#btn-text');
var $btnTextStyle = $('.btn-text-style');
var $btnAddIcon = $('#btn-add-icon');
var $btnRegisterIcon = $('.btn-register-icon');
var $btnMaskFilter = $('#btn-mask-filter');
var $btnImageFilter = $('#btn-image-filter');
var $btnLoadMaskImage = $('.input-mask-image-file');
var $btnApplyMask = $('.btn-apply-mask');
var $btnClose = $('.close');

// Input etc.
var $inputRotationRange = $('.input-rotation-range');
var $inputRotationRange1 = $('#input-rotation-range1');
var $inputBrushWidthRange = $('.input-brush-width-range');
var $inputFontSizeRange = $('.input-font-size-range');
var $inputStrokeWidthRange = $('.input-stroke-width-range');
var $inputCheckTransparent = $('.input-check-transparent');
var $inputCheckFilter = $('.input-check-filter');
var $inputCheckGrayscale = $('.input-check-grayscale');
var $inputCheckInvert = $('.input-check-invert');
var $inputCheckSepia = $('#input-check-sepia');
var $inputCheckSepia2 = $('.input-check-sepia2');
var $inputCheckBlur = $('.input-check-blur');
var $inputCheckSharpen = $('.input-check-sharpen');
var $inputCheckEmboss = $('.input-check-emboss');
var $inputCheckRemoveWhite = $('.input-check-remove-white');
var $inputRangeRemoveWhiteThreshold = $('.input-range-remove-white-threshold');
var $inputRangeRemoveWhiteDistance = $('.input-range-remove-white-distance');
var $inputCheckBrightness = $('.input-check-brightness');
var $inputRangeBrightnessValue = $('.input-range-brightness-value');
var $inputCheckNoise = $('.input-check-noise');
var $inputRangeNoiseValue = $('.input-range-noise-value');
var $inputCheckPixelate = $('.input-check-pixelate');
var $inputRangePixelateValue = $('.input-range-pixelate-value');
var $inputCheckTint = $('.input-check-tint');
var $inputRangeTintOpacityValue = $('.input-range-tint-opacity-value');
var $inputCheckMultiply = $('.input-check-multiply');
var $inputCheckBlend = $('.input-check-blend');
var $inputCheckColorFilter = $('.input-check-color-filter');
var $inputRangeColorFilterValue = $('.input-range-color-filter-value');

// Sub menus
var $displayingSubMenu = $();
var $cropSubMenu = $('#crop-sub-menu');
var $flipSubMenu = $('#flip-sub-menu');
var $rotationSubMenu = $('#rotation-sub-menu');
var $freeDrawingSubMenu = $('#free-drawing-sub-menu');
var $drawLineSubMenu = $('#draw-line-sub-menu');
var $drawShapeSubMenu = $('#draw-shape-sub-menu');
var $textSubMenu = $('#text-sub-menu');
var $iconSubMenu = $('#icon-sub-menu');
var $filterSubMenu = $('#filter-sub-menu');
var $imageFilterSubMenu = $('#image-filter-sub-menu');

// Select line type
var $selectLine = $('[name="select-line-type"]');

// Select shape type
var $selectShapeType = $('[name="select-shape-type"]');

// Select color of shape type
var $selectColorType = $('[name="select-color-type"]');

// Select blend type
var $selectBlendType = $('[name="select-blend-type"]');



// Image editor
if (screen.width <= 600) {
    var imageEditor = new tui.ImageEditor('.tui-image-editor', {
        cssMaxWidth: screen.width - 50,
        cssMaxHeight: 500,

        // cssMaxWidth: 170,
        // cssMaxHeight: 200,
        selectionStyle: {
            cornerSize: 20,
            rotatingPointOffset: 70,
        },
    });
} else {
    var imageEditor = new tui.ImageEditor('.tui-image-editor', {
        cssMaxWidth: 500,
        cssMaxHeight: 500,

        selectionStyle: {
            cornerSize: 20,
            rotatingPointOffset: 70,
        },

    });
}

// Color picker for free drawing
var brushColorpicker = tui.colorPicker.create({
    container: $('#tui-brush-color-picker')[0],
    color: '#000000',
});
var brushColorpicker = tui.colorPicker.create({
    container: $('#tui-brush-color-picker1')[0],
    color: '#000000',
});

// Color picker for text palette
var textColorpicker = tui.colorPicker.create({

    container: $('#tui-text-color-picker')[0],
    color: '#000000',
});

var textColorpicker = tui.colorPicker.create({

    container: $('#tui-text-color-picker1')[0],
    color: '#000000',
});
// Color picker for shape
var shapeColorpicker = tui.colorPicker.create({
    container: $('#tui-shape-color-picker')[0],
    color: '#000000',
});
var shapeColorpicker = tui.colorPicker.create({
    container: $('#tui-shape-color-picker1')[0],
    color: '#000000',
});
// Color picker for icon
var iconColorpicker = tui.colorPicker.create({
    container: $('#tui-icon-color-picker')[0],
    color: '#000000',
});

var tintColorpicker = tui.colorPicker.create({
    container: $('#tui-tint-color-picker')[0],
    color: '#000000',
});

var multiplyColorpicker = tui.colorPicker.create({
    container: $('#tui-multiply-color-picker')[0],
    color: '#000000',
});

var blendColorpicker = tui.colorPicker.create({
    container: $('#tui-blend-color-picker')[0],
    color: '#00FF00',
});
var iconColorpicker = tui.colorPicker.create({
    container: $('#tui-icon-color-picker1')[0],
    color: '#000000',
});

var tintColorpicker = tui.colorPicker.create({
    container: $('#tui-tint-color-picker1')[0],
    color: '#000000',
});

var multiplyColorpicker = tui.colorPicker.create({
    container: $('#tui-multiply-color-picker1')[0],
    color: '#000000',
});

var blendColorpicker = tui.colorPicker.create({
    container: $('#tui-blend-color-picker1')[0],
    color: '#00FF00',
});

// Common global functions
// HEX to RGBA
function hexToRGBa(hex, alpha) {
    var r = parseInt(hex.slice(1, 3), 16);
    var g = parseInt(hex.slice(3, 5), 16);
    var b = parseInt(hex.slice(5, 7), 16);
    var a = alpha || 1;

    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
}

function base64ToBlob(data) {
    var mimeString = '';
    var raw, uInt8Array, i, rawLength;

    raw = data.replace(rImageType, function(header, imageType) {
        mimeString = imageType;

        return '';
    });

    raw = atob(raw);
    rawLength = raw.length;
    uInt8Array = new Uint8Array(rawLength); // eslint-disable-line

    for (i = 0; i < rawLength; i += 1) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], { type: mimeString });
}

function resizeEditor() {
    var $editor = $('.tui-image-editor');
    var $container = $('.tui-image-editor-canvas-container');
    var height = parseFloat($container.css('max-height'));

    $editor.height(height);
}

function getBrushSettings() {
    var brushWidth = parseInt($inputBrushWidthRange.val(), 10);
    var brushColor = brushColorpicker.getColor();

    return {
        width: brushWidth,
        color: hexToRGBa(brushColor, 0.5),
    };
}

function activateShapeMode() {
    if (imageEditor.getDrawingMode() !== 'SHAPE') {
        imageEditor.stopDrawingMode();
        imageEditor.startDrawingMode('SHAPE');
    }
}

function activateIconMode() {
    imageEditor.stopDrawingMode();
}

function activateTextMode() {
    if (imageEditor.getDrawingMode() !== 'TEXT') {
        imageEditor.stopDrawingMode();
        imageEditor.startDrawingMode('TEXT');
    }
}

function setTextToolbar(obj) {
    var fontSize = obj.fontSize;
    var fontColor = obj.fill;

    $inputFontSizeRange.val(fontSize);
    textColorpicker.setColor(fontColor);
}

function setIconToolbar(obj) {
    var iconColor = obj.fill;

    iconColorpicker.setColor(iconColor);
}

function setShapeToolbar(obj) {
    var fillColor, isTransparent, isFilter;
    var colorType = $selectColorType.val();
    var changeValue = colorType === 'stroke' ? obj.stroke : obj.fill.type;
    isTransparent = changeValue === 'transparent';
    isFilter = changeValue === 'filter';

    if (colorType === 'stroke') {
        if (!isTransparent && !isFilter) {
            shapeColorpicker.setColor(changeValue);
        }
    } else if (colorType === 'fill') {
        if (!isTransparent && !isFilter) {
            fillColor = obj.fill.color;
            shapeColorpicker.setColor(fillColor);
        }
    }

    $inputCheckTransparent.prop('checked', isTransparent);
    $inputCheckFilter.prop('checked', isFilter);
    $inputStrokeWidthRange.val(obj.strokeWidth);
}

function showSubMenu(type) {
    var $submenu;

    switch (type) {
        case 'shape':
            $submenu = $drawShapeSubMenu;
            break;
        case 'icon':
            $submenu = $iconSubMenu;
            break;
        case 'text':
            $submenu = $textSubMenu;
            break;
        default:
            $submenu = 0;
    }

    $displayingSubMenu.hide();
    $displayingSubMenu = $submenu.show();
}

function applyOrRemoveFilter(applying, type, options) {
    if (applying) {
        imageEditor.applyFilter(type, options).then(function(result) {
            // console.log(result);
        });
    } else {
        imageEditor.removeFilter(type);
    }
}

// Attach image editor custom events
imageEditor.on({
    objectAdded: function(objectProps) {
        console.info(objectProps);
    },
    undoStackChanged: function(length) {
        if (length) {
            $btnUndo.removeClass('disabled');
        } else {
            $btnUndo.addClass('disabled');
        }
        resizeEditor();
    },
    redoStackChanged: function(length) {
        if (length) {
            $btnRedo.removeClass('disabled');
        } else {
            $btnRedo.addClass('disabled');
        }
        resizeEditor();
    },
    objectScaled: function(obj) {
        if (obj.type === 'text') {
            $inputFontSizeRange.val(obj.fontSize);
        }
    },
    addText: function(pos) {
        imageEditor
            .addText('Double Click', {
                position: pos.originPosition,
            })
            .then(function(objectProps) {
                //console.log(objectProps);
            });
    },
    objectActivated: function(obj) {
        activeObjectId = obj.id;
        if (obj.type === 'rect' || obj.type === 'circle' || obj.type === 'triangle') {
            showSubMenu('shape');
            setShapeToolbar(obj);
            activateShapeMode();
        } else if (obj.type === 'icon') {
            showSubMenu('icon');
            setIconToolbar(obj);
            activateIconMode();
        } else if (obj.type === 'text') {
            showSubMenu('text');
            setTextToolbar(obj);
            activateTextMode();
        }
    },
    mousedown: function(event, originPointer) {
        if ($imageFilterSubMenu.is(':visible') && imageEditor.hasFilter('colorFilter')) {
            imageEditor.applyFilter('colorFilter', {
                x: parseInt(originPointer.x, 10),
                y: parseInt(originPointer.y, 10),
            });
        }
    },
});

// Attach button click event listeners
$btns.on('click', function() {
    $btnsActivatable.removeClass('active');
});

$btnsActivatable.on('click', function() {
    $(this).addClass('active');
});

$btnUndo.on('click', function() {
    $displayingSubMenu.hide();

    if (!$(this).hasClass('disabled')) {
        imageEditor.discardSelection();
        imageEditor.undo();
    }
});

$btnRedo.on('click', function() {
    $displayingSubMenu.hide();

    if (!$(this).hasClass('disabled')) {
        imageEditor.discardSelection();
        imageEditor.redo();
    }
});

$btnClearObjects.on('click', function() {
    $displayingSubMenu.hide();
    imageEditor.clearObjects();
});

$btnRemoveActiveObject.on('click', function() {
    $displayingSubMenu.hide();
    imageEditor.removeObject(activeObjectId);

});

$btnCrop.on('click', function() {
    imageEditor.startDrawingMode('CROPPER');
    $displayingSubMenu.hide();
    $displayingSubMenu = $cropSubMenu.show();
});
$btnCrop1.on('click', function() {
    imageEditor.startDrawingMode('CROPPER');
    // $displayingSubMenu.hide();
    // $displayingSubMenu = $cropSubMenu.show();
});

$btnFlip.on('click', function() {
    imageEditor.stopDrawingMode();
    $displayingSubMenu.hide();
    $displayingSubMenu = $flipSubMenu.show();
});

$btnRotation.on('click', function() {
    imageEditor.stopDrawingMode();
    $displayingSubMenu.hide();
    $displayingSubMenu = $rotationSubMenu.show();
});

$btnClose.on('click', function() {
    imageEditor.stopDrawingMode();
    $displayingSubMenu.hide();
});

$btnApplyCrop.on('click', function() {
    imageEditor.crop(imageEditor.getCropzoneRect()).then(function() {
        imageEditor.stopDrawingMode();
        resizeEditor();
    });
});

$btnCancelCrop.on('click', function() {
    imageEditor.stopDrawingMode();
});


$btnFlipX.on('click', function() {
    imageEditor.flipX().then(function(status) {
        //console.log'flipX: ', status.flipX);
        //console.log'flipY: ', status.flipY);
        //console.log'angle: ', status.angle);
    });
});

$btnFlipY.on('click', function() {
    imageEditor.flipY().then(function(status) {
        //console.log'flipX: ', status.flipX);
        //console.log'flipY: ', status.flipY);
        //console.log'angle: ', status.angle);
    });
});

$btnResetFlip.on('click', function() {
    imageEditor.resetFlip().then(function(status) {
        //console.log'flipX: ', status.flipX);
        //console.log'flipY: ', status.flipY);
        //console.log'angle: ', status.angle);
    });
});

$btnRotateClockwise.on('click', function() {
    imageEditor.rotate(30);
});

$btnRotateCounterClockWise.on('click', function() {
    imageEditor.rotate(-30);
});

$inputRotationRange.on('mousedown', function() {
    var changeAngle = function() {
        imageEditor.setAngle(parseInt($inputRotationRange.val(), 10))['catch'](function() {});
    };
    $(document).on('mousemove', changeAngle);
    $(document).on('mouseup', function stopChangingAngle() {
        $(document).off('mousemove', changeAngle);
        $(document).off('mouseup', stopChangingAngle);
    });
});

$inputRotationRange.on('change', function() {
    imageEditor.setAngle(parseInt($inputRotationRange.val(), 10))['catch'](function() {});
});


$inputRotationRange1.on('mousedown', function() {
    var changeAngle = function() {
        imageEditor.setAngle(parseInt($inputRotationRange1.val(), 10))['catch'](function() {});
    };
    $(document).on('mousemove', changeAngle);
    $(document).on('mouseup', function stopChangingAngle() {
        $(document).off('mousemove', changeAngle);
        $(document).off('mouseup', stopChangingAngle);
    });
});

$inputRotationRange1.on('change', function() {
    imageEditor.setAngle(parseInt($inputRotationRange1.val(), 10))['catch'](function() {});
});
$inputBrushWidthRange.on('change', function() {
    imageEditor.setBrush({ width: parseInt(this.value, 10) });
});

$inputImage.on('change', function(event) {
    var file;

    if (!supportingFileAPI) {
        alert('This browser does not support file-api');
    }

    file = event.target.files[0];
    imageEditor.loadImageFromFile(file).then(function(result) {
        //console.log(result);
        imageEditor.clearUndoStack();
    });
});

$btnImgSave.on('click', () => {
    var imageName = imageEditor.getImageName();
    var dataURL = imageEditor.toDataURL();
    var blob, type, w;

    if (supportingFileAPI) {
        blob = base64ToBlob(dataURL);
        type = blob.type.split('/')[1];
        if (imageName.split('.').pop() !== type) {
            imageName += '.' + type;
        }
        // upload(blob, "img")
        var x = 150;
        var y = 150;
        var width = 200;
        var height = 200;
        displayTshirt(x, y, width, height);

    } else {
        alert('This browser needs a file-server');
        w = window.open();
        w.document.body.innerHTML = '<img src="' + dataURL + '">';
    }
});

$btnDownload.on('click', function() {
    var imageName = imageEditor.getImageName();
    var dataURL = imageEditor.toDataURL();
    var blob, type, w;

    if (supportingFileAPI) {
        blob = base64ToBlob(dataURL);
        type = blob.type.split('/')[1];
        if (imageName.split('.').pop() !== type) {
            imageName += '.' + type;
        }

        // Library: FileSaver - saveAs
        saveAs(blob, imageName); // eslint-disable-line
    } else {
        alert('This browser needs a file-server');
        w = window.open();
        w.document.body.innerHTML = '<img src="' + dataURL + '">';
    }
});

// control draw line mode
$btnDrawLine.on('click', function() {
    imageEditor.stopDrawingMode();
    $displayingSubMenu.hide();
    $displayingSubMenu = $drawLineSubMenu.show();
    $selectLine.eq(0).change();
});

$selectLine.on('change', function() {
    var mode = $(this).val();
    var settings = getBrushSettings();

    imageEditor.stopDrawingMode();
    if (mode === 'freeDrawing') {
        imageEditor.startDrawingMode('FREE_DRAWING', settings);
    } else {
        imageEditor.startDrawingMode('LINE_DRAWING', settings);
    }
});

brushColorpicker.on('selectColor', function(event) {
    imageEditor.setBrush({
        color: hexToRGBa(event.color, 0.5),
    });
});

// control draw shape mode
$btnDrawShape.on('click', function() {
    showSubMenu('shape');

    // step 1. get options to draw shape from toolbar
    shapeType = $('[name="select-shape-type"]:checked').val();

    shapeOptions.stroke = '#000000';
    shapeOptions.fill = '#ffffff';

    shapeOptions.strokeWidth = Number($inputStrokeWidthRange.val());

    // step 2. set options to draw shape
    imageEditor.setDrawingShape(shapeType, shapeOptions);

    // step 3. start drawing shape mode
    activateShapeMode();
});

$selectShapeType.on('change', function() {
    shapeType = $(this).val();

    imageEditor.setDrawingShape(shapeType);
});
$selectColorType.on('change', function() {
    var colorType = $(this).val();
    if (colorType === 'stroke') {
        $inputCheckFilter.prop('disabled', true);
        $inputCheckFilter.prop('checked', false);
    } else {
        $inputCheckTransparent.prop('disabled', false);
        $inputCheckFilter.prop('disabled', false);
    }
});

$inputCheckTransparent.on('change', onChangeShapeFill);
$inputCheckFilter.on('change', onChangeShapeFill);
shapeColorpicker.on('selectColor', function(event) {
    $inputCheckTransparent.prop('checked', false);
    $inputCheckFilter.prop('checked', false);
    onChangeShapeFill(event);
});

function onChangeShapeFill(event) {
    var colorType = $selectColorType.val();
    var isTransparent = $inputCheckTransparent.prop('checked');
    var isFilter = $inputCheckFilter.prop('checked');
    var shapeOption;

    if (event.color) {
        shapeOption = event.color;
    } else if (isTransparent) {
        shapeOption = 'transparent';
    } else if (isFilter) {
        shapeOption = {
            type: 'filter',
            filter: [{ pixelate: PIXELATE_FILTER_DEFAULT_VALUE }],
        };
    }

    if (colorType === 'stroke') {
        imageEditor.changeShape(activeObjectId, {
            stroke: shapeOption,
        });
    } else if (colorType === 'fill') {
        imageEditor.changeShape(activeObjectId, {
            fill: shapeOption,
        });
    }

    imageEditor.setDrawingShape(shapeType, shapeOptions);
}

$inputStrokeWidthRange.on('change', function() {
    var strokeWidth = Number($(this).val());

    imageEditor.changeShape(activeObjectId, {
        strokeWidth: strokeWidth,
    });

    imageEditor.setDrawingShape(shapeType, shapeOptions);
});

// control text mode
$btnText.on('click', function() {
    showSubMenu('text');
    activateTextMode();
});

$inputFontSizeRange.on('change', function() {
    imageEditor.changeTextStyle(activeObjectId, {
        fontSize: parseInt(this.value, 10),
    });
});

$btnTextStyle.on('click', function(e) {
    // eslint-disable-line
    var styleType = $(this).attr('data-style-type');
    var styleObj;

    e.stopPropagation();

    switch (styleType) {
        case 'b':
            styleObj = { fontWeight: 'bold' };
            break;
        case 'i':
            styleObj = { fontStyle: 'italic' };
            break;
        case 'u':
            styleObj = { underline: true };
            break;
        case 'l':
            styleObj = { textAlign: 'left' };
            break;
        case 'c':
            styleObj = { textAlign: 'center' };
            break;
        case 'r':
            styleObj = { textAlign: 'right' };
            break;
        default:
            styleObj = {};
    }

    imageEditor.changeTextStyle(activeObjectId, styleObj);
});

textColorpicker.on('selectColor', function(event) {
    imageEditor.changeTextStyle(activeObjectId, {
        fill: event.color,
    });
});

// control icon
$btnAddIcon.on('click', function() {
    showSubMenu('icon');
    activateIconMode();
});

function onClickIconSubMenu(event) {
    var element = event.target || event.srcElement;
    var iconType = $(element).attr('data-icon-type');

    imageEditor.once('mousedown', function(e, originPointer) {
        imageEditor
            .addIcon(iconType, {
                left: originPointer.x,
                top: originPointer.y,
            })
            .then(function(objectProps) {
                // console.log(objectProps);
            });
    });
}

$btnRegisterIcon.on('click', function() {
    $iconSubMenu
        .find('.menu-item')
        .eq(3)
        .after('<li id="customArrow" class="menu-item icon-text" data-icon-type="customArrow">↑</li>');

    imageEditor.registerIcons({
        customArrow: 'M 60 0 L 120 60 H 90 L 75 45 V 180 H 45 V 45 L 30 60 H 0 Z',
    });

    $btnRegisterIcon.off('click');

    $iconSubMenu.on('click', '#customArrow', onClickIconSubMenu);
});

$iconSubMenu.on('click', '.icon-text', onClickIconSubMenu);

iconColorpicker.on('selectColor', function(event) {
    imageEditor.changeIconColor(activeObjectId, event.color);
});

// control mask filter
$btnMaskFilter.on('click', function() {
    imageEditor.stopDrawingMode();
    $displayingSubMenu.hide();

    $displayingSubMenu = $filterSubMenu.show();
});

$btnImageFilter.on('click', function() {
    var filters = {
        grayscale: $inputCheckGrayscale,
        invert: $inputCheckInvert,
        sepia: $inputCheckSepia,
        sepia2: $inputCheckSepia2,
        blur: $inputCheckBlur,
        shapren: $inputCheckSharpen,
        emboss: $inputCheckEmboss,
        removeWhite: $inputCheckRemoveWhite,
        brightness: $inputCheckBrightness,
        noise: $inputCheckNoise,
        pixelate: $inputCheckPixelate,
        tint: $inputCheckTint,
        multiply: $inputCheckMultiply,
        blend: $inputCheckBlend,
        colorFilter: $inputCheckColorFilter,
    };

    tui.util.forEach(filters, function($value, key) {
        $value.prop('checked', imageEditor.hasFilter(key));
    });
    $displayingSubMenu.hide();

    $displayingSubMenu = $imageFilterSubMenu.show();
});

$btnLoadMaskImage.on('change', function() {
    var file;
    var imgUrl;

    if (!supportingFileAPI) {
        alert('This browser does not support file-api');
    }

    file = event.target.files[0];

    if (file) {
        imgUrl = URL.createObjectURL(file);

        imageEditor.loadImageFromURL(imageEditor.toDataURL(), 'FilterImage').then(function() {
            imageEditor.addImageObject(imgUrl).then(function(objectProps) {
                URL.revokeObjectURL(file);
                //console.log(objectProps);
            });
        });
    }
});

$btnApplyMask.on('click', function() {
    imageEditor
        .applyFilter('mask', {
            maskObjId: activeObjectId,
        })
        .then(function(result) {
            //console.log(result);
        });
});

$inputCheckGrayscale.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Grayscale', null);
});

$inputCheckInvert.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Invert', null);
});

$inputCheckSepia.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Sepia', null);
});

$inputCheckSepia2.on('change', function() {
    applyOrRemoveFilter(this.checked, 'vintage', null);
});

$inputCheckBlur.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Blur', { blur: 0.1 });
});

$inputCheckSharpen.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Sharpen', null);
});

$inputCheckEmboss.on('change', function() {
    applyOrRemoveFilter(this.checked, 'Emboss', null);
});

$inputCheckRemoveWhite.on('change', function() {
    applyOrRemoveFilter(this.checked, 'removeColor', {
        color: '#FFFFFF',
        useAlpha: false,
        distance: parseInt($inputRangeRemoveWhiteDistance.val(), 10) / 255,
    });
});

$inputRangeRemoveWhiteDistance.on('change', function() {
    applyOrRemoveFilter($inputCheckRemoveWhite.is(':checked'), 'removeColor', {
        distance: parseInt(this.value, 10) / 255,
    });
});

$inputCheckBrightness.on('change', function() {
    applyOrRemoveFilter(this.checked, 'brightness', {
        brightness: parseInt($inputRangeBrightnessValue.val(), 10) / 255,
    });
});

$inputRangeBrightnessValue.on('change', function() {
    applyOrRemoveFilter($inputCheckBrightness.is(':checked'), 'brightness', {
        brightness: parseInt(this.value, 10) / 255,
    });
});

$inputCheckNoise.on('change', function() {
    applyOrRemoveFilter(this.checked, 'noise', {
        noise: parseInt($inputRangeNoiseValue.val(), 10),
    });
});

$inputRangeNoiseValue.on('change', function() {
    applyOrRemoveFilter($inputCheckNoise.is(':checked'), 'noise', {
        noise: parseInt(this.value, 10),
    });
});

$inputCheckPixelate.on('change', function() {
    applyOrRemoveFilter(this.checked, 'pixelate', {
        blocksize: parseInt($inputRangePixelateValue.val(), 10),
    });
});

$inputRangePixelateValue.on('change', function() {
    applyOrRemoveFilter($inputCheckPixelate.is(':checked'), 'pixelate', {
        blocksize: parseInt(this.value, 10),
    });
});

$inputCheckTint.on('change', function() {
    applyOrRemoveFilter(this.checked, 'blendColor', {
        mode: 'tint',
        color: tintColorpicker.getColor(),
        alpha: parseFloat($inputRangeTintOpacityValue.val()),
    });
});

tintColorpicker.on('selectColor', function(e) {
    applyOrRemoveFilter($inputCheckTint.is(':checked'), 'blendColor', {
        color: e.color,
    });
});

$inputRangeTintOpacityValue.on('change', function() {
    applyOrRemoveFilter($inputCheckTint.is(':checked'), 'blendColor', {
        alpha: parseFloat($inputRangeTintOpacityValue.val()),
    });
});

$inputCheckMultiply.on('change', function() {
    applyOrRemoveFilter(this.checked, 'blendColor', {
        color: multiplyColorpicker.getColor(),
    });
});

multiplyColorpicker.on('selectColor', function(e) {
    applyOrRemoveFilter($inputCheckMultiply.is(':checked'), 'blendColor', {
        color: e.color,
    });
});

$inputCheckBlend.on('change', function() {
    applyOrRemoveFilter(this.checked, 'blendColor', {
        mode: $selectBlendType.val(),
        color: blendColorpicker.getColor(),
    });
});

blendColorpicker.on('selectColor', function(e) {
    applyOrRemoveFilter($inputCheckBlend.is(':checked'), 'blendColor', {
        color: e.color,
    });
});

$selectBlendType.on('change', function() {
    applyOrRemoveFilter($inputCheckBlend.is(':checked'), 'blendColor', {
        mode: this.value,
    });
});

$inputCheckColorFilter.on('change', function() {
    applyOrRemoveFilter(this.checked, 'removeColor', {
        color: '#FFFFFF',
        distance: $inputRangeColorFilterValue.val() / 255,
    });
});

$inputRangeColorFilterValue.on('change', function() {
    applyOrRemoveFilter($inputCheckColorFilter.is(':checked'), 'removeColor', {
        distance: this.value / 255,
    });
});

// Etc..

// Load sample image
imageEditor.loadImageFromURL('/static/editor/sampleImage.jpg', 'SampleImage').then(function(sizeValue) {
    //console.log(sizeValue);
    imageEditor.clearUndoStack();
});

// IE9 Unselectable
$('.menu').on('selectstart', function() {
    return false;
});


/***************************Imge Save, Alignments*******************************************/


var x = 150;
var y = 150;
var width = 200;
var height = 200;
var selectValX = 150,
    selectValY = 150,
    selectValWidth = 200,
    selectValHeight = 200,
    imgDisplay;
let selectX = document.getElementById("selectX");
let selectY = document.getElementById("selectY");
let selectWidth = document.getElementById("selectWidth");
let selectHeight = document.getElementById("selectHeight");



var $editor = $('.tui-image-editor');
var c = document.getElementById("myCanvas");
var ctx = c.getContext("2d");
const displayTshirt = (x, y, width, height) => {

    imgDisplay = document.getElementById("myCanvas");
    $editor[0].classList.add("hidden");
    funcContainer.classList.add("hidden");
    mainFuncContainer.classList.add("hidden");
    opsContainer.classList.add("hidden");
    selectPos.classList.remove("hidden");
    imgDisplay.classList.remove("hidden");
    ctx.clearRect(0, 0, c.width, c.height);
    var dataURL = imageEditor.toDataURL();

    var img = document.getElementById("frame");
    var imageObj = new Image();
    imageObj.src = dataURL;
    // imageObj.onload = function() {
    imageObj.onload = function() {

        ctx.drawImage(imageObj, x, y, width, height);

    };


    ctx.drawImage(img, 0, 0, 500, 500);
    // const du = c.toDataURL();
    // console.log(du);
};

selectX.addEventListener("change", () => {
    selectValX = selectX.value;
    displayTshirt(selectValX, selectValY, selectValWidth, selectValHeight)

});
selectY.addEventListener("change", () => {
    selectValY = selectY.value;
    displayTshirt(selectValX, selectValY, selectValWidth, selectValHeight)

});
selectWidth.addEventListener("change", () => {
    selectValWidth = selectWidth.value;
    displayTshirt(selectValX, selectValY, selectValWidth, selectValHeight)

});
selectHeight.addEventListener("change", () => {
    selectValHeight = selectHeight.value;
    displayTshirt(selectValX, selectValY, selectValWidth, selectValHeight)

})
var $btnImgSave = $('#btn-img-save');
const saveEditImg = () => {
    var imageName1 = imageEditor.getImageName();
    var dataURL1 = imageEditor.toDataURL();
    var imageName2 = imageEditor.getImageName();
    var dataURL2 = c.toDataURL();
    var blob1, blob2, type, w;



    if (supportingFileAPI) {
        blob2 = base64ToBlob(dataURL2);
        type = blob2.type.split('/')[1];
        if (imageName2.split('.').pop() !== type) {
            imageName2 += '.' + type;
        }
    }

    if (supportingFileAPI) {
        blob1 = base64ToBlob(dataURL1);
        type = blob1.type.split('/')[1];
        if (imageName1.split('.').pop() !== type) {
            imageName1 += '.' + type;
        }

    }

    upload(blob1, blob2);
};

const saveEditTshirt = () => {

    var imageName = imageEditor.getImageName();
    var dataURL = c.toDataURL();
    var blob, type, w;

    if (supportingFileAPI) {
        blob = base64ToBlob(dataURL);
        type = blob.type.split('/')[1];
        if (imageName.split('.').pop() !== type) {
            imageName += '.' + type;
        }
        // saveEditImg();
        upload(blob, "tshirt");

    }
}

function downT() {
    var imageName = imageEditor.getImageName();
    var dataURL = c.toDataURL();
    var blob, type, w;

    if (supportingFileAPI) {
        blob = base64ToBlob(dataURL);
        type = blob.type.split('/')[1];
        if (imageName.split('.').pop() !== type) {
            imageName += '.' + type;
        }
        // Library: FileSaver - saveAs
        saveAs(blob, imageName); // eslint-disable-line
    } else {
        alert('This browser needs a file-server');
        w = window.open();
        w.document.body.innerHTML = '<img src="' + dataURL + '">';
    }
}



function upload(file1, file2) {



    document.getElementById("loader2").classList.remove("hidden");
    // console.log(document.getElementById("loader2"))

    // Create a form using FormData. This holds key value pairs.
    var formdata = new FormData();

    // Add a key value pair ("snap", file) to the FormData object. file is the original file passed sent to the upload function.
    formdata.append("printImg", file1);
    formdata.append("tshirtImg", file2);
    formdata.append("tshirtId", document.getElementById("tshirtId").innerText);
    fetch(`/saveImg/img=type`, {
            method: 'POST',
            body: formdata,
        }).then((response) => response.json())
        .then((data) => {
            //console.log('Success:', data);
            if (data.status == "ok") {
                update();
                document.getElementById("buyBtn").setAttribute("href", `/${data.tshirtId}=t/${data.printId}=p/customize/noCart/order`)
                document.getElementById("loader2").classList.add("hidden");
                document.getElementById("posManipulator").classList.add("hidden");
            } else {
                setTimeout(() => {
                    document.getElementById("loader2").classList.add("hidden");
                }, 100000);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}
const update = () => {

    setTimeout(() => {

        document.getElementById("saveBtn").style.display = "none";
        document.getElementById("buyBtn").style.display = "block";
    }, 1000);
    // console.log("ok");
}