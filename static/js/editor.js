  // Declare Variables and Select Elements
  const inputs = document.querySelectorAll('.sliders input');
  const mixBlendModes = document.querySelectorAll('.mix-blend-mode');
  const borderStyles = document.querySelectorAll('.border-styles');
  const textStyles = document.querySelectorAll('.font-select');
  const originalImage = document.getElementById('originalImage');
  const hideImage = document.getElementById('hideImage');
  const text = document.querySelector('#text-1');
  const inputBox = document.getElementById('input-box');
  const image = document.getElementById('image');
  const scaleX = document.getElementById('scaleX');
  const scaleY = document.getElementById('scaleY');
  const dropDownShapes = document.querySelector('.dropdown-shapes');
  const shapes = document.querySelectorAll('.shapes');
  let suffix;
  let mirror = 1;
  let flip = 1;
  let count1 = -1;
  let count2 = -1;


  // Create Event Listeners for Groups
  inputs.forEach(input => input.addEventListener('click', handleUpdate));
  inputs.forEach(input => input.addEventListener('mousemove', handleUpdate));
  mixBlendModes.forEach(mixBlendMode => mixBlendMode.addEventListener('click', changeMixBlendMode));
  borderStyles.forEach(borderStyle => borderStyle.addEventListener('click', changeBorderStyles));
  textStyles.forEach(textStyle => textStyle.addEventListener('click', changeTextStyle));
  shapes.forEach(shape => shape.addEventListener('click', changeClipPathShape));

  //   to download image 

  const file = new File(['blob'], 'new-image.png', {
      type: 'image/*',
  })

  function download() {
      cropper.getCroppedCanvas().toBlob((blob) => {
          var downloadUrl = window.URL.createObjectURL(blob)
          var a = document.createElement('a')
          a.href = downloadUrl
          a.download = 'cropped-image.jpg' // output image name
          a.click()
              //   actionButton[1].innerText = 'Download'
      })
  }



  function downloadImg() {
      let a = document.createElement('a');
      a.href = "https://source.unsplash.com/sqL5xItVgpg";
      a.download = "edited_Image.png";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
  }
  // Set Text & Original & Shapes - display to 'none' 
  text.style.display = 'none';
  originalImage.style.display = 'none';
  dropDownShapes.style.display = 'none';

  // When Sliders Values Change, Update the CSS Variables
  function handleUpdate() {
      suffix = this.dataset.sizing || "";
      document.documentElement.style.setProperty(`--${this.name}`, this.value + suffix);
      this.nextElementSibling.innerHTML = this.value + suffix;
      if (this.nextElementSibling.classList == "noSuffix") {
          this.nextElementSibling.innerHTML = "";
      };
  }

  // Change the Font Style
  function changeTextStyle() {
      document.documentElement.style.setProperty('--font', this.value);
  }
  // Set the Border Style
  function changeBorderStyles() {
      document.documentElement.style.setProperty('--border-styles', this.value);
  }
  // Set Mix Blend Mode Styles to Overlay
  function changeMixBlendMode() {
      document.documentElement.style.setProperty('--mix-blend-mode', this.value);
  }
  // Set Clip Path Shape
  function changeClipPathShape() {
      const shape = this.dataset.shape || "";
      document.documentElement.style.setProperty('--webkit-clip-path', shape);
      document.documentElement.style.setProperty('--clip-path', shape);
      dropDownShapes.style.display = 'none';
  }

  // Show Original image on toggle click for comparison
  function showOriginal() {
      const showOriginalBtn = document.querySelector('#show-original');
      if (originalImage.style.display == 'none') {
          originalImage.style.display = 'block';
          showOriginalBtn.style.color = '#CD343A';

      } else {
          originalImage.style.display = 'none';
          showOriginalBtn.style.color = '#ededed';
      }
  }

  function toggleMirror() {
      if (mirror == 1) {
          document.documentElement.style.setProperty('--scaleX', -1);
          mirror = -1;
          scaleX.value = -1;
      } else {
          document.documentElement.style.setProperty('--scaleX', 1);
          mirror = 1;
          scaleX.value = 1;
      }
  }

  function toggleFlip() {
      if (flip == 1) {
          document.documentElement.style.setProperty('--scaleY', -1);
          scaleY.value = -1;
          flip = -1;
      } else {
          document.documentElement.style.setProperty('--scaleY', 1);
          flip = 1;
          scaleY.value = 1;
      }
  }

  function toggleShapes() {
      if (dropDownShapes.style.display == 'none') {
          dropDownShapes.style.display = 'block';
      } else {
          dropDownShapes.style.display = 'none';
      }
  }

  // Add Text
  function addText() {
      let textContent = document.getElementById('text-content');
      let temp1 = '<span class="text-block-1"> ' + textContent.value + '</span>';
      let temp2 = '<span class="text-block-2"> ' + textContent.value + '</span>';
      text.innerHTML += temp1;
      text.style.display = 'block';
      textContent.value = "";
      count1 += 1;
      count2 += 1;
  }

  // Remove Last Text
  function removeText() {
      let textBlocks1 = document.querySelectorAll('.text-block-1');
      let textBlocks2 = document.querySelectorAll('.text-block-2');
      for (let i = 0; i < textBlocks1.length; i++) {
          if (i == count1) {
              textBlocks1[i].remove();
              count1 -= 1;
          }
      }
      for (let i = 0; i < textBlocks2.length; i++) {
          if (i == count2) {
              textBlocks2[i].remove();
              count2 -= 1;
          }
      }
  }

  // Toggle Text On and Off
  function toggleText() {

      if (text.style.display == 'none') {
          text.style.display = 'block';
      } else {
          text.style.display = 'none';
      }
  }

  // Full Size Image On and Off
  function fullSize() {
      const imageFullSize = document.getElementById('image-full-size');
      imageFullSize.style.display = "block";
      imageFullSize.addEventListener("click", function() {
          imageFullSize.style.display = "none";
      });
  }

  function fullSizeClose() {
      imageFullSize.style.display = "none";
  }

  // Set Image in URL/Source Box
  function source() {
      image.src = inputBox.value;
      originalImage.src = inputBox.value;
      image2.src = inputBox.value;
      inputBox.value = " ";
  }

  // Reset the Overlay Gradients to none;
  function resetOverlay() {
      document.documentElement.style.setProperty('--radial-gradient-overlay-1', "none");
      document.documentElement.style.setProperty('--radial-gradient-overlay-2', "none");
      document.documentElement.style.setProperty('--linear-gradient-overlay-1', "none");
      document.documentElement.style.setProperty('--linear-gradient-overlay-2', "none");
      document.documentElement.style.setProperty('--border-styles', "none");
  }

  function resetBlendMode() {
      document.documentElement.style.setProperty('--mix-blend-mode', 'none');
  }

  // reset All Sliders
  function resetAll() {
      for (let i = 0; i < inputs.length; i++) {
          suffix = inputs[i].dataset.sizing || "";
          inputs[i].value = inputs[i].defaultValue;
          document.documentElement.style.setProperty(`--${inputs[i].name}`, inputs[i].defaultValue + suffix);
          inputs[i].nextElementSibling.innerHTML = inputs[i].defaultValue + suffix;
          toggleText();
          resetOverlay();
      }
      document.documentElement.style.setProperty('--clip-path', "none");
  }

  ! function(e, t) {
      "use strict";
      var r = {
              rgb: {
                  r: [0, 255],
                  g: [0, 255],
                  b: [0, 255]
              },
              hsv: {
                  h: [0, 360],
                  s: [0, 100],
                  v: [0, 100]
              },
              hsl: {
                  h: [0, 360],
                  s: [0, 100],
                  l: [0, 100]
              },
              cmy: {
                  c: [0, 100],
                  m: [0, 100],
                  y: [0, 100]
              },
              cmyk: {
                  c: [0, 100],
                  m: [0, 100],
                  y: [0, 100],
                  k: [0, 100]
              },
              Lab: {
                  L: [0, 100],
                  a: [-128, 127],
                  b: [-128, 127]
              },
              XYZ: {
                  X: [0, 100],
                  Y: [0, 100],
                  Z: [0, 100]
              },
              alpha: {
                  alpha: [0, 1]
              },
              HEX: {
                  HEX: [0, 16777215]
              }
          },
          o = {},
          a = {},
          s = {
              X: [.4124564, .3575761, .1804375],
              Y: [.2126729, .7151522, .072175],
              Z: [.0193339, .119192, .9503041],
              R: [3.2404542, -1.5371385, -.4985314],
              G: [-.969266, 1.8760108, .041556],
              B: [.0556434, -.2040259, 1.0572252]
          },
          l = {
              r: .298954,
              g: .586434,
              b: .114612
          },
          n = {
              r: .2126,
              g: .7152,
              b: .0722
          },
          i = e.Math,
          c = (e.parseInt, e.Colors = function(e) {
              this.colors = {
                  RND: {}
              }, this.options = {
                  color: "rgba(204, 82, 37, 0.8)",
                  XYZMatrix: s,
                  grey: l,
                  luminance: n,
                  valueRanges: r
              }, A(this, e || {})
          }),
          A = function(e, r) {
              var o, s, l = e.options;
              for (var n in g(e), r) r[n] !== t && (l[n] = r[n]);
              o = l.XYZMatrix, r.XYZReference || (l.XYZReference = {
                  X: o.X[0] + o.X[1] + o.X[2],
                  Y: o.Y[0] + o.Y[1] + o.Y[2],
                  Z: o.Z[0] + o.Z[1] + o.Z[2]
              }), s = l.customBG, l.customBG = "string" == typeof s ? b.txt2color(s).rgb : s, a = p(e.colors, l.color, t, !0)
          },
          g = function(e) {
              o !== e && (o = e, a = e.colors)
          };

      function p(e, o, s, l, n) {
          if ("string" == typeof o) s = (o = b.txt2color(o)).type, a[s] = o[s], n = n !== t ? n : o.alpha;
          else if (o)
              for (var i in o) e[s][i] = "Lab" === s ? B(o[i], r[s][i][0], r[s][i][1]) : B(o[i] / r[s][i][1], 0, 1);
          return n !== t && (e.alpha = B(+n, 0, 1)), u(s, l ? e : t)
      }

      function u(e, t) {
          var s, l, n, c = i,
              A = t || a,
              g = b,
              p = o.options,
              u = r,
              B = A.RND,
              y = "",
              v = "",
              x = {
                  hsl: "hsv",
                  cmyk: "cmy",
                  rgb: e
              },
              E = B.rgb;
          if ("alpha" !== e) {
              for (var S in u)
                  if (!u[S][S])
                      for (y in e !== S && "XYZ" !== S && (v = x[S] || "rgb", A[S] = g[v + "2" + S](A[v])), B[S] || (B[S] = {}), s = A[S]) B[S][y] = c.round(s[y] * ("Lab" === S ? 1 : u[S][y][1]));
                  "Lab" !== e && delete A._rgb, E = B.rgb, A.HEX = g.RGB2HEX(E), A.equivalentGrey = p.grey.r * A.rgb.r + p.grey.g * A.rgb.g + p.grey.b * A.rgb.b, A.webSave = l = d(E, 51), A.webSmart = n = d(E, 17), A.saveColor = E.r === l.r && E.g === l.g && E.b === l.b ? "web save" : E.r === n.r && E.g === n.g && E.b === n.b ? "web smart" : "", A.hueRGB = g.hue2RGB(A.hsv.h), t && (A.background = function(e, t, r) {
                  var a = o.options.grey,
                      s = {};
                  return s.RGB = {
                      r: e.r,
                      g: e.g,
                      b: e.b
                  }, s.rgb = {
                      r: t.r,
                      g: t.g,
                      b: t.b
                  }, s.alpha = r, s.equivalentGrey = i.round(a.r * e.r + a.g * e.g + a.b * e.b), s.rgbaMixBlack = f(t, {
                      r: 0,
                      g: 0,
                      b: 0
                  }, r, 1), s.rgbaMixWhite = f(t, {
                      r: 1,
                      g: 1,
                      b: 1
                  }, r, 1), s.rgbaMixBlack.luminance = h(s.rgbaMixBlack, !0), s.rgbaMixWhite.luminance = h(s.rgbaMixWhite, !0), o.options.customBG && (s.rgbaMixCustom = f(t, o.options.customBG, r, 1), s.rgbaMixCustom.luminance = h(s.rgbaMixCustom, !0), o.options.customBG.luminance = h(o.options.customBG, !0)), s
              }(E, A.rgb, A.alpha))
          }
          var w, Q, G, k, R, X, P, I = A.rgb,
              M = A.alpha,
              D = A.background,
              N = f,
              Y = h,
              H = C,
              z = m;
          return (w = N(I, {
              r: 0,
              g: 0,
              b: 0
          }, M, 1)).luminance = Y(w, !0), A.rgbaMixBlack = w, (Q = N(I, {
              r: 1,
              g: 1,
              b: 1
          }, M, 1)).luminance = Y(Q, !0), A.rgbaMixWhite = Q, p.allMixDetails && (w.WCAG2Ratio = H(w.luminance, 0), Q.WCAG2Ratio = H(Q.luminance, 1), p.customBG && ((G = N(I, p.customBG, M, 1)).luminance = Y(G, !0), G.WCAG2Ratio = H(G.luminance, p.customBG.luminance), A.rgbaMixCustom = G), (k = N(I, D.rgb, M, D.alpha)).luminance = Y(k, !0), A.rgbaMixBG = k, (R = N(I, D.rgbaMixBlack, M, 1)).luminance = Y(R, !0), R.WCAG2Ratio = H(R.luminance, D.rgbaMixBlack.luminance), R.luminanceDelta = c.abs(R.luminance - D.rgbaMixBlack.luminance), R.hueDelta = z(D.rgbaMixBlack, R, !0), A.rgbaMixBGMixBlack = R, (X = N(I, D.rgbaMixWhite, M, 1)).luminance = Y(X, !0), X.WCAG2Ratio = H(X.luminance, D.rgbaMixWhite.luminance), X.luminanceDelta = c.abs(X.luminance - D.rgbaMixWhite.luminance), X.hueDelta = z(D.rgbaMixWhite, X, !0), A.rgbaMixBGMixWhite = X), p.customBG && ((P = N(I, D.rgbaMixCustom, M, 1)).luminance = Y(P, !0), P.WCAG2Ratio = H(P.luminance, D.rgbaMixCustom.luminance), A.rgbaMixBGMixCustom = P, P.luminanceDelta = c.abs(P.luminance - D.rgbaMixCustom.luminance), P.hueDelta = z(D.rgbaMixCustom, P, !0)), A.RGBLuminance = Y(E), A.HUELuminance = Y(A.hueRGB), p.convertCallback && p.convertCallback(A, e), A
      }
      c.prototype.setColor = function(e, r, o) {
          return g(this), e ? p(this.colors, e, r, t, o) : (o !== t && (this.colors.alpha = B(o, 0, 1)), u(r))
      }, c.prototype.getColor = function(e) {
          var r = this.colors,
              o = 0;
          if (e) {
              for (e = e.split("."); r[e[o]];) r = r[e[o++]];
              e.length !== o && (r = t)
          }
          return r
      }, c.prototype.setCustomBackground = function(e) {
          return g(this), this.options.customBG = "string" == typeof e ? b.txt2color(e).rgb : e, p(this.colors, t, "rgb")
      }, c.prototype.saveAsBackground = function() {
          return g(this), p(this.colors, t, "rgb", !0)
      }, c.prototype.convertColor = function(e, t) {
          var o = b,
              a = r,
              s = t.split("2"),
              l = s[0],
              n = s[1],
              c = /(?:RG|HS|CM|LA)/,
              A = c.test(l),
              g = c.test(n),
              p = {
                  LAB: "Lab"
              },
              u = function(e, t, r) {
                  var o = {},
                      s = "Lab" === t ? 1 : 0;
                  for (var l in e) o[l] = r ? i.round(e[l] * (s || a[t][l][1])) : e[l] / (s || a[t][l][1]);
                  return o
              };
          return l = a[l] ? l : p[l] || l.toLowerCase(), n = a[n] ? n : p[n] || n.toLowerCase(), A && "RGB2HEX" !== t && (e = u(e, l)), e = l === n ? e : o[l + "2" + n] ? o[l + "2" + n](e, !0) : "HEX" === n ? o.RGB2HEX("RGB2HEX" === t ? e : u("rgb" === l ? e : o[l + "2rgb"](e, !0), "rgb", !0)) : o["rgb2" + n](o[l + "2rgb"](e, !0), !0), g && (e = u(e, n, !0)), e
      }, c.prototype.toString = function(e, t) {
          return b.color2text((e || "rgb").toLowerCase(), this.colors, t)
      };
      var b = {
          txt2color: function(e) {
              var t = {},
                  o = e.replace(/(?:#|\)|%)/g, "").split("("),
                  a = (o[1] || "").split(/,\s*/),
                  s = o[1] ? o[0].substr(0, 3) : "rgb",
                  l = "";
              if (t.type = s, t[s] = {}, o[1])
                  for (var n = 3; n--;) l = s[n] || s.charAt(n), t[s][l] = +a[n] / r[s][l][1];
              else t.rgb = b.HEX2rgb(o[0]);
              return t.alpha = a[3] ? +a[3] : 1, t
          },
          color2text: function(e, t, r) {
              var o = !1 !== r && i.round(100 * t.alpha) / 100,
                  a = "number" == typeof o && !1 !== r && (r || 1 !== o),
                  s = t.RND.rgb,
                  l = t.RND.hsl,
                  n = "hex" === e && a,
                  c = "hex" === e && !n,
                  A = "rgb" === e || n ? s.r + ", " + s.g + ", " + s.b : c ? "#" + t.HEX : l.h + ", " + l.s + "%, " + l.l + "%";
              return c ? A : (n ? "rgb" : e) + (a ? "a" : "") + "(" + A + (a ? ", " + o : "") + ")"
          },
          RGB2HEX: function(e) {
              return ((e.r < 16 ? "0" : "") + e.r.toString(16) + (e.g < 16 ? "0" : "") + e.g.toString(16) + (e.b < 16 ? "0" : "") + e.b.toString(16)).toUpperCase()
          },
          HEX2rgb: function(e) {
              return {
                  r: +("0x" + (e = e.split(""))[0] + e[e[3] ? 1 : 0]) / 255,
                  g: +("0x" + e[e[3] ? 2 : 1] + (e[3] || e[1])) / 255,
                  b: +("0x" + (e[4] || e[2]) + (e[5] || e[2])) / 255
              }
          },
          hue2RGB: function(e) {
              var t = i,
                  r = 6 * e,
                  o = ~~r % 6,
                  a = 6 === r ? 0 : r - o;
              return {
                  r: t.round(255 * [1, 1 - a, 0, 0, a, 1][o]),
                  g: t.round(255 * [a, 1, 1, 1 - a, 0, 0][o]),
                  b: t.round(255 * [0, 0, a, 1, 1, 1 - a][o])
              }
          },
          rgb2hsv: function(e) {
              var t, r, o = i,
                  s = e.r,
                  l = e.g,
                  n = e.b,
                  c = 0;
              return l < n && (l = n + (n = l, 0), c = -1), r = n, s < l && (s = l + (l = s, 0), c = -2 / 6 - c, r = o.min(l, n)), t = s - r, {
                  h: (s ? t / s : 0) < 1e-15 ? a && a.hsl && a.hsl.h || 0 : t ? o.abs(c + (l - n) / (6 * t)) : 0,
                  s: s ? t / s : a && a.hsv && a.hsv.s || 0,
                  v: s
              }
          },
          hsv2rgb: function(e) {
              var t = 6 * e.h,
                  r = e.s,
                  o = e.v,
                  a = ~~t,
                  s = t - a,
                  l = o * (1 - r),
                  n = o * (1 - s * r),
                  i = o * (1 - (1 - s) * r),
                  c = a % 6;
              return {
                  r: [o, n, l, l, i, o][c],
                  g: [i, o, o, n, l, l][c],
                  b: [l, l, i, o, o, n][c]
              }
          },
          hsv2hsl: function(e) {
              var t = (2 - e.s) * e.v,
                  r = e.s * e.v;
              return r = e.s ? t < 1 ? t ? r / t : 0 : r / (2 - t) : 0, {
                  h: e.h,
                  s: e.v || r ? r : a && a.hsl && a.hsl.s || 0,
                  l: t / 2
              }
          },
          rgb2hsl: function(e, t) {
              var r = b.rgb2hsv(e);
              return b.hsv2hsl(t ? r : a.hsv = r)
          },
          hsl2rgb: function(e) {
              var t = 6 * e.h,
                  r = e.s,
                  o = e.l,
                  a = o < .5 ? o * (1 + r) : o + r - r * o,
                  s = o + o - a,
                  l = ~~t,
                  n = a * (a ? (a - s) / a : 0) * (t - l),
                  i = s + n,
                  c = a - n,
                  A = l % 6;
              return {
                  r: [a, c, s, s, i, a][A],
                  g: [i, a, a, c, s, s][A],
                  b: [s, s, i, a, a, c][A]
              }
          },
          rgb2cmy: function(e) {
              return {
                  c: 1 - e.r,
                  m: 1 - e.g,
                  y: 1 - e.b
              }
          },
          cmy2cmyk: function(e) {
              var t = i,
                  r = t.min(t.min(e.c, e.m), e.y),
                  o = 1 - r || 1e-20;
              return {
                  c: (e.c - r) / o,
                  m: (e.m - r) / o,
                  y: (e.y - r) / o,
                  k: r
              }
          },
          cmyk2cmy: function(e) {
              var t = e.k;
              return {
                  c: e.c * (1 - t) + t,
                  m: e.m * (1 - t) + t,
                  y: e.y * (1 - t) + t
              }
          },
          cmy2rgb: function(e) {
              return {
                  r: 1 - e.c,
                  g: 1 - e.m,
                  b: 1 - e.y
              }
          },
          rgb2cmyk: function(e, t) {
              var r = b.rgb2cmy(e);
              return b.cmy2cmyk(t ? r : a.cmy = r)
          },
          cmyk2rgb: function(e, t) {
              var r = b.cmyk2cmy(e);
              return b.cmy2rgb(t ? r : a.cmy = r)
          },
          XYZ2rgb: function(e, t) {
              var r = i,
                  s = o.options.XYZMatrix,
                  l = e.X,
                  n = e.Y,
                  c = e.Z,
                  A = l * s.R[0] + n * s.R[1] + c * s.R[2],
                  g = l * s.G[0] + n * s.G[1] + c * s.G[2],
                  p = l * s.B[0] + n * s.B[1] + c * s.B[2],
                  u = 1 / 2.4;
              return A = A > (s = .0031308) ? 1.055 * r.pow(A, u) - .055 : 12.92 * A, g = g > s ? 1.055 * r.pow(g, u) - .055 : 12.92 * g, p = p > s ? 1.055 * r.pow(p, u) - .055 : 12.92 * p, t || (a._rgb = {
                  r: A,
                  g: g,
                  b: p
              }), {
                  r: B(A, 0, 1),
                  g: B(g, 0, 1),
                  b: B(p, 0, 1)
              }
          },
          rgb2XYZ: function(e) {
              var t = i,
                  r = o.options.XYZMatrix,
                  a = e.r,
                  s = e.g,
                  l = e.b,
                  n = .04045;
              return a = a > n ? t.pow((a + .055) / 1.055, 2.4) : a / 12.92, s = s > n ? t.pow((s + .055) / 1.055, 2.4) : s / 12.92, l = l > n ? t.pow((l + .055) / 1.055, 2.4) : l / 12.92, {
                  X: a * r.X[0] + s * r.X[1] + l * r.X[2],
                  Y: a * r.Y[0] + s * r.Y[1] + l * r.Y[2],
                  Z: a * r.Z[0] + s * r.Z[1] + l * r.Z[2]
              }
          },
          XYZ2Lab: function(e) {
              var t = i,
                  r = o.options.XYZReference,
                  a = e.X / r.X,
                  s = e.Y / r.Y,
                  l = e.Z / r.Z,
                  n = 16 / 116,
                  c = .008856,
                  A = 7.787037;
              return a = a > c ? t.pow(a, 1 / 3) : A * a + n, {
                  L: 116 * (s = s > c ? t.pow(s, 1 / 3) : A * s + n) - 16,
                  a: 500 * (a - s),
                  b: 200 * (s - (l = l > c ? t.pow(l, 1 / 3) : A * l + n))
              }
          },
          Lab2XYZ: function(e) {
              var t = i,
                  r = o.options.XYZReference,
                  a = (e.L + 16) / 116,
                  s = e.a / 500 + a,
                  l = a - e.b / 200,
                  n = t.pow(s, 3),
                  c = t.pow(a, 3),
                  A = t.pow(l, 3),
                  g = 16 / 116,
                  p = .008856,
                  u = 7.787037;
              return {
                  X: (n > p ? n : (s - g) / u) * r.X,
                  Y: (c > p ? c : (a - g) / u) * r.Y,
                  Z: (A > p ? A : (l - g) / u) * r.Z
              }
          },
          rgb2Lab: function(e, t) {
              var r = b.rgb2XYZ(e);
              return b.XYZ2Lab(t ? r : a.XYZ = r)
          },
          Lab2rgb: function(e, t) {
              var r = b.Lab2XYZ(e);
              return b.XYZ2rgb(t ? r : a.XYZ = r, t)
          }
      };

      function d(e, t) {
          var r = {},
              o = 0,
              a = t / 2;
          for (var s in e) o = e[s] % t, r[s] = e[s] + (o > a ? t - o : -o);
          return r
      }

      function m(e, t, r) {
          var o = i;
          return (o.max(e.r - t.r, t.r - e.r) + o.max(e.g - t.g, t.g - e.g) + o.max(e.b - t.b, t.b - e.b)) * (r ? 255 : 1) / 765
      }

      function h(e, t) {
          for (var r = t ? 1 : 255, a = [e.r / r, e.g / r, e.b / r], s = o.options.luminance, l = a.length; l--;) a[l] = a[l] <= .03928 ? a[l] / 12.92 : i.pow((a[l] + .055) / 1.055, 2.4);
          return s.r * a[0] + s.g * a[1] + s.b * a[2]
      }

      function f(e, r, o, a) {
          var s = {},
              l = o !== t ? o : 1,
              n = a !== t ? a : 1,
              i = l + n * (1 - l);
          for (var c in e) s[c] = (e[c] * l + r[c] * n * (1 - l)) / i;
          return s.a = i, s
      }

      function C(e, t) {
          var r = 1;
          return r = e >= t ? (e + .05) / (t + .05) : (t + .05) / (e + .05), i.round(100 * r) / 100
      }

      function B(e, t, r) {
          return e > r ? r : e < t ? t : e
      }
  }(window),
  function(e, t) {
      "use strict";
      var r = '^§app alpha-bg-w">^§slds">^§sldl-1">$^§sldl-2">$^§sldl-3">$^§curm">$^§sldr-1">$^§sldr-2">$^§sldr-4">$^§curl">$^§curr">$$^§opacity">|^§opacity-slider">$$$^§memo">^§raster">$^§raster-bg">$|$|$|$|$|$|$|$|$^§memo-store">$^§memo-cursor">$$^§panel">^§hsv">^hsl-mode §ß">$^hsv-h-ß §ß">H$^hsv-h-~ §~">-^§nsarrow">$$^hsl-h-@ §@">H$^hsv-s-ß §ß">S$^hsv-s-~ §~">-$^hsl-s-@ §@">S$^hsv-v-ß §ß">B$^hsv-v-~ §~">-$^hsl-l-@ §@">L$$^§hsl §hide">^hsv-mode §ß">$^hsl-h-ß §ß">H$^hsl-h-~ §~">-$^hsv-h-@ §@">H$^hsl-s-ß §ß">S$^hsl-s-~ §~">-$^hsv-s-@ §@">S$^hsl-l-ß §ß">L$^hsl-l-~ §~">-$^hsv-v-@ §@">B$$^§rgb">^rgb-r-ß §ß">R$^rgb-r-~ §~">-$^rgb-r-@ §ß">&nbsp;$^rgb-g-ß §ß">G$^rgb-g-~ §~">-$^rgb-g-@ §ß">&nbsp;$^rgb-b-ß §ß">B$^rgb-b-~ §~">-$^rgb-b-@ §ß">&nbsp;$$^§cmyk">^Lab-mode §ß">$^cmyk-c-ß §@">C$^cmyk-c-~ §~">-$^Lab-L-@ §@">L$^cmyk-m-ß §@">M$^cmyk-m-~ §~">-$^Lab-a-@ §@">a$^cmyk-y-ß §@">Y$^cmyk-y-~ §~">-$^Lab-b-@ §@">b$^cmyk-k-ß §@">K$^cmyk-k-~ §~">-$^Lab-x-@ §ß">&nbsp;$$^§Lab §hide">^cmyk-mode §ß">$^Lab-L-ß §@">L$^Lab-L-~ §~">-$^cmyk-c-@ §@">C$^Lab-a-ß §@">a$^Lab-a-~ §~">-$^cmyk-m-@ §@">M$^Lab-b-ß §@">b$^Lab-b-~ §~">-$^cmyk-y-@ §@">Y$^Lab-x-ß §@">&nbsp;$^Lab-x-~ §~">-$^cmyk-k-@ §@">K$$^§alpha">^alpha-ß §ß">A$^alpha-~ §~">-$^alpha-@ §ß">W$$^§HEX">^HEX-ß §ß">#$^HEX-~ §~">-$^HEX-@ §ß">M$$^§ctrl">^§raster">$^§cont">$^§cold">$^§col1">|&nbsp;$$^§col2">|&nbsp;$$^§bres">RESET$^§bsav">SAVE$$$^§exit">$^§resize">$^§resizer">|$$$'.replace(/\^/g, '<div class="').replace(/\$/g, "</div>").replace(/~/g, "disp").replace(/ß/g, "butt").replace(/@/g, "labl").replace(/\|/g, "<div>"),
          o = "är^1,äg^1,äb^1,öh^1,öh?1,öh?2,ös?1,öv?1,üh^1,üh?1,üh?2,üs?1,ül?1,.no-rgb-r är?2,.no-rgb-r är?3,.no-rgb-r är?4,.no-rgb-g äg?2,.no-rgb-g äg?3,.no-rgb-g äg?4,.no-rgb-b äb?2,.no-rgb-b äb?3,.no-rgb-b äb?4{visibility:hidden}är^2,är^3,äg^2,äg^3,äb^2,äb^3{@-image:url(_patches.png)}.§slds div{@-image:url(_vertical.png)}öh^2,ös^1,öv^1,üh^2,üs^1,ül^1{@-image:url(_horizontal.png)}ös?4,öv^3,üs?4,ül^3{@:#000}üs?3,ül^4{@:#fff}är?1{@-color:#f00}äg?1{@-color:#0f0}äb?1{@-color:#00f}är^2{@|-1664px 0}är^3{@|-896px 0}är?1,äg?1,äb?1,öh^3,ös^2,öv?2Ü-2432Öär?2Ü-2944Öär?3Ü-4480Öär?4Ü-3202Öäg^2Äöh^2{@|-640px 0}äg^3{@|-384px 0}äg?2Ü-4736Öäg?3Ü-3968Öäg?4Ü-3712Öäb^2{@|-1152px 0}äb^3{@|-1408px 0}äb?2Ü-3456Öäb?3Ü-4224Öäb?4Ü-2688Ööh^2Äär^3Ääb?4Ü0}öh?4,üh?4Ü-1664Öös^1,öv^1,üs^1,ül^1Ääg^3{@|-256px 0}ös^3,öv?4,üs^3,ül?4Ü-2176Öös?2,öv^2Ü-1920Öüh^2{@|-768px 0}üh^3,üs^2,ül?2Ü-5184Öüs?2,ül^2Ü-5824Ö.S är^2{@|-128px -128Ö.S är?1Ääg?1Ääb?1Äöh^3Äös^2Äöv?2Ü-1408Ö.S är?2Ääb^3Ü-128Ö.S är?3Ü-896Ö.S är?4Ü-256Ö.S äg^2{@|-256px -128Ö.S äg?2Ü-1024Ö.S äg?3Ü-640Ö.S äg?4Ü-512Ö.S äb^2{@|-128px 0}.S äb?2Ü-384Ö.S äb?3Ü-768Ö.S öh?4Äüh?4Ü-1536Ö.S ös^1Äöv^1Äüs^1Äül^1{@|-512px 0}.S ös^3Äöv?4Äüs^3Äül?4Ü-1280Ö.S ös?2Äöv^2Ü-1152Ö.S üh^2{@|-1024px 0}.S üh^3Äüs^2Äül?2Ü-5440Ö.S üs?2Äül^2Ü-5696Ö.XXS ös^2,.XXS öv?2Ü-5120Ö.XXS ös^3,.XXS öv?4,.XXS üs^3,.XXS ül^3,.XXS ül?4Ü-5056Ö.XXS ös?2,.XXS öv^2Ü-4992Ö.XXS üs^2,.XXS ül?2Ü-5568Ö.XXS üs?2,.XXS ül^2Ü-5632Ö".replace(/Ü/g, "{@|0 ").replace(/Ö/g, "px}").replace(/Ä/g, ",.S ").replace(/\|/g, "-position:").replace(/@/g, "background").replace(/ü/g, ".hsl-").replace(/ö/g, ".hsv-").replace(/ä/g, ".rgb-").replace(/~/g, " .no-rgb-}").replace(/\?/g, " .§sldr-").replace(/\^/g, " .§sldl-"),
          a = '∑{@#bbb;font-family:monospace, "Courier New", Courier, mono;font-size:12¥line-ä15¥font-weight:bold;cursor:default;~412¥ä323¥?top-left-radius:7¥?top-Ü-radius:7¥?bottom-Ü-radius:7¥?bottom-left-radius:7¥ö@#444}.S{~266¥ä177px}.XS{~158¥ä173px}.XXS{ä105¥~154px}.no-alpha{ä308px}.no-alpha .§opacity,.no-alpha .§alpha{display:none}.S.no-alpha{ä162px}.XS.no-alpha{ä158px}.XXS.no-alpha{ä90px}∑,∑ div{border:none;padding:0¥float:none;margin:0¥outline:none;box-sizing:content-box}∑ div{|absolute}^s .§curm,«§disp,«§nsarrow,∑ .§exit,∑ ø-cursor,∑ .§resize{öimage:url(_icons.png)}∑ .do-drag div{cursor:none}∑ .§opacity,ø .§raster-bg,∑ .§raster{öimage:url(_bgs.png)}∑ ^s{~287¥ä256¥top:10¥left:10¥overflow:hidden;cursor:crosshair}.S ^s{~143¥ä128¥left:9¥top:9px}.XS ^s{left:7¥top:7px}.XXS ^s{left:5¥top:5px}^s div{~256¥ä256¥left:0px}.S ^l-1,.S ^l-2,.S ^l-3,.S ^l-4{~128¥ä128px}.XXS ^s,.XXS ^s ^l-1,.XXS ^s ^l-2,.XXS ^s ^l-3,.XXS ^s ^l-4{ä64px}^s ^r-1,^s ^r-2,^s ^r-3,^s ^r-4{~31¥left:256¥cursor:default}.S ^r-1,.S ^r-2,.S ^r-3,.S ^r-4{~15¥ä128¥left:128px}^s .§curm{margin:-5¥~11¥ä11¥ö|-36px -30px}.light .§curm{ö|-7px -30px}^s .§curl,^s .§curr{~0¥ä0¥margin:-3px -4¥border:4px solid;cursor:default;left:auto;öimage:none}^s .§curl,∑ ^s .§curl-dark,.hue-dark div.§curl{Ü:27¥?@† † † #fff}.light .§curl,∑ ^s .§curl-light,.hue-light .§curl{?@† † † #000}.S ^s .§curl,.S ^s .§curr{?~3px}.S ^s .§curl-light,.S ^s .§curl{Ü:13px}^s .§curr,∑ ^s .§curr-dark{Ü:4¥?@† #fff † †}.light .§curr,∑ ^s .§curr-light{?@† #000 † †}∑ .§opacity{bottom:44¥left:10¥ä10¥~287¥ö|0 -87px}.S .§opacity{bottom:27¥left:9¥~143¥ö|0 -100px}.XS .§opacity{left:7¥bottom:25px}.XXS .§opacity{left:5¥bottom:23px}.§opacity div{~100%;ä16¥margin-top:-3¥overflow:hidden}.§opacity .§opacity-slider{margin:0 -4¥~0¥ä8¥?~4¥?style:solid;?@#eee †}∑ ø{bottom:10¥left:10¥~288¥ä31¥ö@#fff}.S ø{ä15¥~144¥left:9¥bottom:9px}.XS ø{left:7¥bottom:7px}.XXS ø{left:5¥bottom:5px}ø div{|relative;float:left;~31¥ä31¥margin-Ü:1px}.S ø div{~15¥ä15px}∑ .§raster,ø .§raster-bg,.S ø .§raster,.S ø .§raster-bg{|absolute;top:0¥Ü:0¥bottom:0¥left:0¥~100%}.S ø .§raster-bg{ö|0 -31px}∑ .§raster{opacity:0.2;ö|0 -49px}.alpha-bg-b ø{ö@#333}.alpha-bg-b .§raster{opacity:1}ø ø-cursor{|absolute;Ü:0¥ö|-26px -87px}∑ .light ø-cursor{ö|3px -87px}.S ø-cursor{ö|-34px -95px}.S .light ø-cursor{ö|-5px -95px}∑ .§panel{|absolute;top:10¥Ü:10¥bottom:10¥~94¥?~1¥?style:solid;?@#222 #555 #555 #222;overflow:hidden;ö@#333}.S .§panel{top:9¥Ü:9¥bottom:9px}.XS .§panel{display:none}.§panel div{|relative}«§hsv,«§hsl,«§rgb,«§cmyk,«§Lab,«§alpha,.no-alpha «§HEX,«§HEX{~86¥margin:-1px 0px 1px 4¥padding:1px 0px 3¥?top-~1¥?top-style:solid;?top-@#444;?bottom-~1¥?bottom-style:solid;?bottom-@#222;float:Ö«§hsv,«§hsl{padding-top:2px}.S .§hsv,.S .§hsl{padding-top:1px}«§HEX{?bottom-style:none;?top-~0¥margin-top:-4¥padding-top:0px}.no-alpha «§HEX{?bottom-style:none}«§alpha{?bottom-style:none}.S .rgb-r .§hsv,.S .rgb-g .§hsv,.S .rgb-b .§hsv,.S .rgb-r .§hsl,.S .rgb-g .§hsl,.S .rgb-b .§hsl,.S .hsv-h .§rgb,.S .hsv-s .§rgb,.S .hsv-v .§rgb,.S .hsl-h .§rgb,.S .hsl-s .§rgb,.S .hsl-l .§rgb,.S .§cmyk,.S .§Lab{display:none}«§butt,«§labl{float:left;~14¥ä14¥margin-top:2¥text-align:center;border:1px solid}«§butt{?@#555 #222 #222 #555}«§butt:active{ö@#444}«§labl{?@†}«Lab-mode,«cmyk-mode,«hsv-mode,«hsl-mode{|absolute;Ü:0¥top:1¥ä50px}«hsv-mode,«hsl-mode{top:2px}«cmyk-mode{ä68px}.hsl-h .hsl-h-labl,.hsl-s .hsl-s-labl,.hsl-l .hsl-l-labl,.hsv-h .hsv-h-labl,.hsv-s .hsv-s-labl,.hsv-v .hsv-v-labl{@#f90}«cmyk-mode,«hsv-mode,.rgb-r .rgb-r-butt,.rgb-g .rgb-g-butt,.rgb-b .rgb-b-butt,.hsv-h .hsv-h-butt,.hsv-s .hsv-s-butt,.hsv-v .hsv-v-butt,.hsl-h .hsl-h-butt,.hsl-s .hsl-s-butt,.hsl-l .hsl-l-butt,«rgb-r-labl,«rgb-g-labl,«rgb-b-labl,«alpha-butt,«HEX-butt,«Lab-x-labl{?@#222 #555 #555 #222;ö@#444}.no-rgb-r .rgb-r-labl,.no-rgb-g .rgb-g-labl,.no-rgb-b .rgb-b-labl,.mute-alpha .alpha-butt,.no-HEX .HEX-butt,.cmy-only .Lab-x-labl{?@#555 #222 #222 #555;ö@#333}.Lab-x-disp,.cmy-only .cmyk-k-disp,.cmy-only .cmyk-k-butt{visibility:hidden}«HEX-disp{öimage:none}«§disp{float:left;~48¥ä14¥margin:2px 2px 0¥cursor:text;text-align:left;text-indent:3¥?~1¥?style:solid;?@#222 #555 #555 #222}∑ .§nsarrow{|absolute;top:0¥left:-13¥~8¥ä16¥display:none;ö|-87px -23px}∑ .start-change .§nsarrow{display:block}∑ .do-change .§nsarrow{display:block;ö|-87px -36px}.do-change .§disp{cursor:default}«§hide{display:none}«§cont,«§cold{|absolute;top:-5¥left:0¥ä3¥border:1px solid #333}«§cold{z-index:1;ö@#c00}«§cont{margin-Ü:-1¥z-index:2}«contrast .§cont{z-index:1;ö@#ccc}«orange .§cold{ö@#f90}«green .§cold{ö@#4d0}«§ctrl{|absolute;bottom:0¥left:0¥~100%;ö@#fff}.alpha-bg-b .§ctrl,«§bres,«§bsav{ö@#333}«§col1,«§col2,«§bres,«§bsav{?~1¥?style:solid;?@#555 #222 #222 #555;float:left;~45¥line-ä28¥text-align:center;top:0px}.§panel div div{ä100%}.S .§ctrl div{line-ä25px}.S «§bres,.S «§bsav{line-ä26px}∑ .§exit,∑ .§resize{Ü:3¥top:3¥~15¥ä15¥ö|0 -52px}∑ .§resize{top:auto;bottom:3¥cursor:nwse-resize;ö|-15px -52px}.S .§exit{ö|1px -52px}.XS .§resize,.XS .§exit{~10¥ä10¥Ü:0¥öimage:none}.XS .§exit{top:0px}.XS .§resize{bottom:0px}∑ .§resizer,∑ .§resizer div{|absolute;border:1px solid #888;top:-1¥Ü:-1¥bottom:-1¥left:-1¥z-index:2;display:none;cursor:nwse-resize}∑ .§resizer div{border:1px dashed #333;opacity:0.3;display:block;ö@#bbb}'.replace(/Ü/g, "right").replace(/Ö/g, "left}").replace(/∑/g, ".§app").replace(/«/g, ".§panel .").replace(/¥/g, "px;").replace(/\|/g, "position:").replace(/@/g, "color:").replace(/ö/g, "background-").replace(/ä/g, "height:").replace(/ø/g, ".§memo").replace(/†/g, "transparent").replace(/\~/g, "width:").replace(/\?/g, "border-").replace(/\^/g, ".§sld"),
          s = "iVBORw0KGgo^NSUhEUgAAB4^EACAI#DdoPxz#L0UlEQVR4Xu3cQWrDQBREwR7FF8/BPR3wXktnQL+KvxfypuEhvLJXcp06d/bXd71OPt+trIw95zr33Z1bk1/fudEv79wa++7OfayZ59wrO2PBzklcGQmAZggAAOBYgAYBmpWRAGg^BGgRofAENgAAN#I0CBA6w8AG^ECABgEa/QH§AI0CNDoDwAY^QIAGAVp/AM§AjQI0OgPAAY^QoEGARn8Aw§CNAjQ+gMABg#BCgQYCmGQmABgAAEKBBgEZ/AM§AjQI0PoDAAY^QoEGARn8AM^IAADQI0+gMABg#BCgQYDWHwAw^gAANAjT6A4AB^BGgQoNEfAD^C#0CtP4AgAE^EaBCgaUYCoAE#RoEKDRHwAw^gAANArT+AIAB^BGgQoNEfAAw^gQIMAjf4AgAE^EaBCg9QcAD^CBAgwCN/gBg§EaBGj0BwAM^IECDAK0/AG§ARoEaJqRAGg^BGgRo9AcAD^CBAgwCtPwBg§EaBGj0BwAD^CNAgQKM/AG§ARoEaP0BAAM^I0CBAoz8AG^ECABgEa/QEAAw^jQIEDrDwAY^QIAGAZpmJACaBw^RoEKD1BwAM^IECDAK0/AG§ARoEaPQHAAw^gQIMArT8AY§BGgRo/QEAAw^jQIECjPwBg§EaBGj9AQAD^CNAgQOsPABg#BAgAYBGv0BAANwCwAAGB6gYeckmpEAa^AEaBGj0BwAM^IECDAK0/AG§ARoEaPQHAAM^I0CBAoz8AY§BGgRo/QEAAw^jQIECjPwAY^QIAGARr9AQAD^CNAgQOsPABg#BAgAYBmmYkABoAAECABgEa/QEAAw^jQIEDrDwAY^QIAGARr9Ac§AjQI0OgPABg#BAgAYBWn8Aw§CNAjQ6A8ABg#BCgQYBGfwD§AI0CND6AwAG^EKBBgKYZCYAG#QoEGARn8Aw§CNAjQ+gMABg#BCgQYBGfwAw^gAANAjT6AwAG^EKBBgNYfAD^C#0CNPoDgAE^EaBCg0R8AM^IAADQK0/gCAAQ^RoEKBpRgKgAQAABGgQoNEfAD^C#0CtP4AgAE^EaBCg0R8AD^CBAgwCN/gCAAQ^RoEKD1BwAM^IECDAI3+AG§ARoEaPQHAAw^gQIMArT8AY§BGgRomsMAM^IAADQK0/gCAAQ^RoEKDRHwAw^gAANO7fQHwAw^gAANArT+AIAB^BGgQoNEfAGg^BGgRo9AcAD^CBAgwCtPwBg§EaBGj0BwAD^RIB+Ntg5iea5AD^DAIwI0CND6AwAG^EKBBgEZ/AKAB#EaBCg0R8AM^IAADQK0/gCAAQ^RoEKDRHwAM^IECDAI3+AIAB^BGgQoPUHAAw^gQIMAjf4AY§BGgRo9AcAD^CBAgwCtPwBg§EaBGiakQBo^ARoEaPQHAAw^gQIMArT8AY§BGgRo9AcAAw^jQIECjPwBg§EaBGj9AQAD^CNAgQKM/ABg#BAgAYBGv0BAAM^I0CBA6w8AG^ECABgGaZiQAGgAAQIAGARr9AQAD^CNAgQOsPABg#BAgAYBGv0Bw§CNAjQ6A8AG^ECABgFafwD§AI0CNDoDwAG^EKBBgEZ/AM§AjQI0PoDAAY^QoEGApjkMAAM^I0CBA6w8AG^ECABgEa/QEAAw^jQsIP+AIAB^BGgQoPUHAAw^gQIMAjf4AgAE#Bea/fK+3P5/3PJOvh8t1cO4nflmQAQoAEAAF9Aw/7JHfQHAAw^gQIMArT8AY§BGvwHNPoDAA0AACBAgwCN/gCAAQ^RoEKD1BwAM^IECDAI3+AG§ARoEaPQHAAw^gQIMArT8AY§BGgRo9AcAAw^jQIECjPwBg§EaBGj9AQAD^CNAgQNOMBEAD#I0CBAoz8AY§BGgRo/QEAAw^jQIECjPwAY^QIAGARr9AQAD^CNAgQOsPABg#BAgAYBGv0Bw§CNAjQ6A8AG^ECABgFafwD§AI0CNA0IwHQ^AjQI0OgPABg#BAgAYBWn8Aw§CNAjQ6A8ABg#BCgQYBGfwD§AI0CND6AwAG^EKBBgEZ/AD^C#0CNPoDAAY^QoEGA1h8AM^IAADQI0DQAG^EKBBgEZ/AM§AjQI0PoDAAY^QoEGA1h8AM^IAADQI0+gMABg#BCgQYDWHwAw^gAANArT+AIAB^BGgQoNEfAD^C#0CtP4AgAE^EaBCg9QcAD^CBAgwCN/gCAAQ^RoEKD1BwAM^IECDAK0/AG§ARoEaPQHAAw^gQIMArT8AY§BGgRo/QEAAw^jQIECjPwBgACDhFgC#07t9AfAD^C#0CtP4AgAE^EaBCg0R8Aa^AEaBGj0BwAM^IECDAK0/AG§ARoEaPQHAAM^I0CBAoz8AY§BGgRo/QEAAw^jQIECjPwAY^QIAGARr9AQAD^CNAgQOsPABg#BAgAYBmmYkABoAAECABgEa/QEAAw^jQIEDrDwAY^QIAGARr9Ac§AjQI0OgPABg#BAgAYBWn8Aw§CNAjQ6A8ABg#BCgQYBGfwD§AI0CND6AwAG^EKBBgKYZCYAG#QoEGARn8Aw§CNAjQ+gMABg#BCgQYBGfwAw^gAANAjT6AwAG^EKBBgNYfAD^C#0CNPoDgAE^EaBCg0R8AM^IAADQK0/gCAAQ^RoEKBpRgKgAQAABGgQoNEfAD^C#0CtP4AgAE^EaBCg0R8AD^CBAgwCN/gCAAQ^RoEKD1BwAM^IECDAI3+AG§ARoEaPQHAAw^gQIMArT8AY§BGgRommEAM^CBAgwCN/gCAAQ^RoEKD1BwAM^IECDAI3+AIAB^ARoEaPQHAAw^gQIMArT8AY§BGgRo9AcAGgAAQICGCNBfRfNcABg#BgeICGnVvoDwAY^QIAGAVp/AM§AjQI0OgPADQAAIAADQI0+gMABg#BCgQYDWHwAw^gAANAjT6A4AB^BGgQoNEfAD^C#0CtP4AgAE^EaBCg0R8AD^CBAgwCN/gCAAQ^RoEKD1BwAM^IECDAE0zEgAN#gQIMAjf4AgAE^EaBCg9QcAD^CBAgwCN/gBg§EaBGj0BwAM^IECDAK0/AG§ARoEaPQHAAM^I0CBAoz8AY§BGgRo/QEAAw^jQIEDTjARAAwAACNAgQKM/AG§ARoEaP0BAAM^I0CBAoz8AG^ECABgEa/QEAAw^jQIEDrDwAY^QIAGARr9Ac§AjQI0OgPABg#BAgAYBWn8Aw§CNAjQNIcBY§BGgRo/QEAAw^jQIECjPwBg§EadtAfAD^C#0CtP4AgAE^EaBCgAQABGgAA+AO2TAbHupOgH^ABJRU5ErkJggg==".replace(/§/g, "AAAAAA").replace(/\^/g, "AAAA").replace(/#/g, "AAA");
      e.ColorPicker = {
          _html: r,
          _cssFunc: o,
          _cssMain: a,
          _horizontalPng: "iVBORw0KGgoAAAANSUhEUgAABIAAAAABCAYAAACmC9U0AAABT0lEQVR4Xu2S3Y6CMBCFhyqIsjGBO1/B9/F5DC/pK3DHhVkUgc7Zqus2DVlGU/cnQZKTjznttNPJBABA149HyRf1iN//4mIBCg0jV4In+j9xJiuihly1V/Z9X88v//kNeDXVvyO/lK+IPR76B019+1Riab3H1zkmeqerKnL+Bzwxx6PAgZxaSQU8vB62T28pxcQeRQ2sHw6GxCOWHvP78zwHAARBABOfdYtd30rwxXOEPDF+dj2+91r6vV/id3k+/brrXmaGUkqKhX3i+ffSt16HQ/dorTGZTHrs7ev7Tl7XdZhOpzc651nfsm1bRFF0YRiGaJoGs9nsQuN/xafTCXEco65rzOdzHI9HJEmCqqqwXC6x3++RZRnKssRqtUJRFFiv19jtdthutyAi5Hl+Jo9VZg7+7f3yXuvZf5c3KaXYzByb+WIzO5ymKW82G/0BNcFhO/tOuuMAAAAASUVORK5CYII=",
          _verticalPng: "iVBORw0KGgoAAAANSUhEUgAAAAEAABfACAYAAABn2KvYAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABHtJREFUeNrtnN9SqzAQxpOF1to6zuiVvoI+j6/gva/lA/kKeqUzjtX+QTi7SzSYBg49xdIzfL34+e1usoQQklCnmLwoCjImNwDQA2xRGMqNAYB+gPEH9IdCgIUA6Aem0P1fLoMQAPYNHYDoCKAv8OMHFgKgX2AjDPQDXn4t1l+gt/1fId//yWgE/hUJ+mAn8EyY5wCwXxhrbaHzn8E9iPlv79DdHxXTqciZ4KROnXRVZMF/6U2OPhcEavtAbZH1SM7wRDD7VoHZItCiyEQf4t6+MW9UOxaZybmdCGKqNrB9Eb5SfMg3wTyiagMtigTmWofiSDCOYNTSNz6sLDIoaCU9GWDd0tdhoMMsRm+r8U/EfB0GfjmLXiqzimDd0tdhoLMsI7la45+I+ToM/HIW0kfGVQTrlr7tA91kaUr//fxrKo8jUFB7VAn6AKpHJf+EKwAAAIYD/f7F7/8MVgMo7P+gBqDKr57Lf72V8x8AAMDgYIuvH4EAAAAMDQX6AACAQcI9GGMjDADA4MA/P2KlP8IEAAAYFCz6AACAgaLA8y8AAIN+CMYXoQAADA7u/UPYCAMAMDjI7z9S+SdwDFQX2C9Gh9GMEOWriz8/Pw1lWQZsi/L3R4czzP678Ve+P8f9nCv/C7hwLq99ah8NfKrU15zPB5pVcwtiJt9qGy0IfEE+jQa+Fn0VtI/fkxUPqBlEfRENeF+tqUpbGpi1iu8epwJzvV5XA4GpWC6XGz7F+/u766EgwJ+ckiTJKU3TnI6OjnI6OzvLZf6zMggt3dzckPhIoiTlSGpQ+eEsVegdz0fbCCi4fRs+Po+4yWdeDXiT+6pBSTeHple1pkz3FZ+avpyavoiPxgLN0B7yprY08PlyQTTm0+PWmkH7ynedNKraar4F/lRj1WpTtYh+ozL/cY2sAvZl0gcbZm0gSLBLvkxGoaogiy/HDXemQk2t5pUm8OAhH8/HH6e0mkJ9q9XKKQXfb07xfZnJbZrRxcVFVt6/t7e3Kc1ms5RGo1Eq5VIZuyl9fHw4k/M5xYeoKj64A7eqCt1ZeqWFVSl8NV9OTV3fmvP5qE9VmzSoEcsXpArK1UHen/hZbgL53BZSdyEXalGau/hU8TEW0u3VcoFPy3EDFrTgT+njydeZ0+l0UV7fu7u7iVzziQQmUm4iqRw4n/NxMxw4s/Mp1NSALxf4NEtQ10cjMDwSl+b+/j6hp6enVGb+jUvrn05iKobm6PboOt8vPISY5Pr6OqGXlxe3fOokoGtAbMUJZmqvYmaLQDP+sdrecOjtO/SXeH69P8Imutm5urqy9PDwYOny8tLS4+OjpfPzc0vPz8+WTk9PLb2+vlpZbCzN53NLx8fHVtYZS5PJxMoEZWWqsjKULY3HYytTi1Pex5OMldXKRVXxuLcy/20onmms3BBOxcr5qCrZtsrd45SPel8sGlOxGoGy0neynQ6VL9fsa1YtWlCrtj9G83G7PjdVush5n5q1iJWLZW6u21a1bUvbVnVzlru0pe3RdmlV1/23fZtbZv4Dx+7FBypx77kAAAAASUVORK5CYII=",
          _patchesPng: s,
          _iconsPng: "iVBORw0KGgoAAAANSUhEUgAAAGEAAABDCAMAAAC7vJusAAAAkFBMVEUAAAAvLy9ERERubm7///8AAAD///9EREREREREREREREQAAAD///8AAAD///8AAAD///8AAAD///8AAAD///8AAAD///8AAAD///8AAAD///8AAAD///8cHBwkJCQnJycoKCgpKSkqKiouLi4vLy8/Pz9AQEBCQkJDQ0NdXV1ubm58fHykpKRERERVVVUzMzPx7Ab+AAAAHXRSTlMAAAAAAAQEBQ4QGR4eIyMtLUVFVVVqapKSnJy7u9JKTggAAAFUSURBVHja7dXbUoMwEAbgSICqLYeW88F6KIogqe//dpoYZ0W4AXbv8g9TwkxmvtndZMrEwlw/F8YIRjCCEYxgBCOsFmzqGMEI28J5zzmt0Pc9rdDL0NYgMxIYC5KiKpKAzZphWtZlGm4SjlnkOV6UHeeEUx77rh/npw1dCrI9k9lnwUwF+UG9D3m4ftJJxH4SJdPtaawXcbr+tBaeFrxiur309cIv19+4ytGCU0031a5euPVigLYGqjlAqM4ShOQ+QAYQUO80AMMAAkUGGfMfR9Ul+kmvPq2QGxXKOQBAKdjUgk0t2NiCGEVP+rHT3/iCUMBT90YrPMsKsIWP3x/VolaonJEETchHCS8AYAmaUICQQwaAQnjoXgHAES7jLkEFaHO4bdq/k25HAIpgWY34FwAE5xjCffM+D2DV8B0gRsAZT7hr5gE8wdrJcU+CJqhcqQD7Cx5L7Ph4WnrKAAAAAElFTkSuQmCC",
          _bgsPng: "iVBORw0KGgoAAAANSUhEUgAAASAAAABvCAYAAABM+h2NAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAABORJREFUeNrs3VtTW1UYBuCEcxAI4YydWqTWdqr1V7T/2QsvvPDCCy9qjxZbamsrhZIQUHsCEtfafpmJe8qFjpUxfZ4Zuvt2feydJvAOARZUut1u5bRerl692nV913f99/f6QxWAU6KAAAUEKCAABQQoIAAFBCggAAUEKCAABQQoIAAFBCggAAUEKCAABQQoIEABASggQAEBKCBAAQEoIEABASggQAEBKCBAAQEoIGBQC+jatWvd07zxrv9+Xx8fAQEoIEABASggQAEBKCBAAQEoIEABAQoIQAEBCghAAQEKCEABAQOk2u36kS6AAgLetwJKL29toFRM1be+QrVq3rx58//KvM8BAadGAQEKCFBAAAoIGHwnfhneZ+/Nmzf/LufzrI+AAE/BAAUEoIAABQTwztgLZt68eXvBAE/BABQQoIAAFBAweOwFM2/evL1ggKdgAAoIUEAACggYPPaCmTdv3l4wwFMwAAUEKCAABQQMHnvBzJs3by8Y4CkYgAICFBCAAgIGz4lfBQNQQMDgFlCtVisaaHV1tThubW1VInciD0U+ysdnz54N5+PKysphOnRTHsvHlN9EHo/1l5FrkV9Enoz8W87b29tTOS8vLx9EnoncjlyPvBe5EbkZeT4fU96NvBDr2znv7Ows57y0tLQVeSXy08gf5mNfPhPrjyOfrVarlcXFxZ9yfv78+bl8TPlh5LU8n/KDyOuxfj/y+VjfyHl3d/dCKv28fi/yp/m4sLDwQ+SLke9GvhT5Tinfjnw5f4/F/Pz8rZybzeZn+ZjyzVK+EfnzUr4S+Xopf9/L+fxzc3M5d1qt1hf531Mu5k/IxzGf85VYL+fefHH+RqNRrO/t7RW3L+UbkS9Hvhk5/386Kd/qW8/5duRLMV/OdyJfzNebnZ0t7t92u53v/07K9yJfiLwROT9+ef7HyOux/iDyWuSHkT+K+eLtZX9//2xer9frjyOfyY9/Wn8S86v59qT1p7Ge315zLt4RU16K19+O9YXIu5HnYn435hux3opcj9yOPB3z+5E/iPXf43y1yMX778HBQS3f3pTz+28l5bHIr2N+LN3+zszMzGHkoh/S+mHMF98XlNaP8zHd/0W/pMe943NAwKlSQIACAhQQgAICFBCAAgIUEIACAhQQgAIC/n9GqtXqYbfbHa38+RtSu32llPdqdNL6aOSj+LfxyMVekLTem39Ryr/mPDQ0NBznzXtROikPRW6W8k7k3m9rzXthOsPDw73bUuylGRkZ6cR63nvTSfko8oPIr+Pnz96P/DLW816ezujoaN6DdtyX9+P8eS9QZ2xs7Hxf7qa8Xlr/JO6Ljcjrcf6cj1P+OO+N6V1/fHz8XLz+/Tjfubh+sZcorZ+N9Ycxfybyo8ircf6fc56YmFiJ1/8l8mLk7cjzkfP92U15Ns63G+u9nPcKdWq12lQ8Xu3Ixd6f9Pd8P3UmJycnUszzL2N9LM7/anNzs9V7Q2q32395w/q7ubdH6L/KrVbrpPxlKX9Vyl+X8jel/G0pf5f/aDabvXy9tH6ztH63lDdKebOUH5Xyk1LeKuWd/ry2tlap9P125Onp6Zf9eWpq6lW3b8f6zMzM6/71er3+ppSP+u/XNN/pz41Go+sjIMBTMEABASggQAEBKCBAAQEoIEABASggQAEB/CN/CDAAw78uW9AVDw4AAAAASUVORK5CYII="
      }
  }(window),
  function(e, t) {
      "use strict";
      var r, o, a, s, l, n, i = e.ColorPicker,
          c = !i,
          A = !1,
          g = !1,
          p = {},
          u = {
              w: "White",
              b: "Black",
              c: "Custom"
          },
          b = "",
          d = 1,
          m = {},
          h = {},
          f = !0,
          C = {},
          B = {},
          y = {},
          v = {},
          x = {},
          E = {},
          S = Math,
          w = "requestAnimationFrame",
          Q = "cancelAnimationFrame",
          G = ["ms", "moz", "webkit", "o"],
          k = function(o) {
              this.options = {
                      color: "rgba(204, 82, 37, 0.8)",
                      mode: "rgb-b",
                      fps: 60,
                      delayOffset: 8,
                      CSSPrefix: "cp-",
                      allMixDetails: !0,
                      alphaBG: "w",
                      imagePath: ""
                  },
                  function(o, a) {
                      var s, u = "",
                          b = "";
                      for (var d in a) o.options[d] = a[d];
                      A = document.createStyleSheet !== t && document.getElementById || !!e.MSInputMethodContext, g = void 0 !== document.body.style.opacity, y = new Colors(o.options), delete o.options, (x = y.options).scale = 1, b = x.CSSPrefix, o.color = y, p = x.valueRanges, o.nodes = E = function(e, t) {
                          var r, o, a = e.getElementsByTagName("*"),
                              s = {
                                  colorPicker: e
                              },
                              l = new RegExp(x.CSSPrefix);
                          s.styles = {}, s.textNodes = {}, s.memos = [], s.testNode = document.createElement("div");
                          for (var n = 0, i = a.length; n < i; n++) r = a[n], (o = r.className) && l.test(o) ? (o = o.split(" ")[0].replace(x.CSSPrefix, "").replace(/-/g, "_"), /_disp/.test(o) ? (o = o.replace("_disp", ""), s.styles[o] = r.style, s.textNodes[o] = r.firstChild, r.contentEditable = !0) : (/(?:hs|cmyk|Lab).*?(?:butt|labl)/.test(o) || (s[o] = r), /(?:cur|sld[^s]|opacity|cont|col)/.test(o) && (s.styles[o] = /(?:col\d)/.test(o) ? r.children[0].style : r.style))) : /memo/.test(r.parentNode.className) && s.memos.push(r);
                          return s.panelCover = s.panel.appendChild(document.createElement("div")), s
                      }(function(e) {
                          var t = document.createElement("div"),
                              r = x.CSSPrefix,
                              o = "data:image/png;base64,",
                              a = function(e, t) {
                                  var r = document.createElement("style");
                                  r.setAttribute("type", "text/css"), t && r.setAttribute("id", t), r.styleSheet || r.appendChild(document.createTextNode(e)), document.getElementsByTagName("head")[0].appendChild(r), r.styleSheet && (document.styleSheets[document.styleSheets.length - 1].cssText = e)
                              },
                              s = document.createElement("img");

                          return c ? e.color.options.devPicker : (document.getElementById("colorPickerCSS") ? e.cssIsReady = !0 : (s.onload = s.onerror = function() {
                              var t;
                              i._cssFunc && (t = 1 === this.width && 1 === this.height, i._cssFunc = i._cssFunc.replace(/§/g, r).replace("_patches.png", t ? o + i._patchesPng : x.imagePath + "_patches.png").replace("_vertical.png", t ? o + i._verticalPng : x.imagePath + "_vertical.png").replace("_horizontal.png", t ? o + i._horizontalPng : x.imagePath + "_horizontal.png"), a(i._cssFunc, "colorPickerCSS"), x.customCSS || (i._cssMain = i._cssMain.replace(/§/g, r).replace("_bgs.png", t ? o + i._bgsPng : x.imagePath + "_bgs.png").replace("_icons.png", t ? o + i._iconsPng : x.imagePath + "_icons.png").replace(/opacity:(\d*\.*(\d+))/g, function(e, t) {
                                  return g ? "-moz-opacity: " + t + "; -khtml-opacity: " + t + "; opacity: " + t : '-ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=' + S.round(100 * +t) + ')";filter: alpha(opacity=' + S.round(100 * +t) + ")"
                              }), a(i._cssMain))), e.cssIsReady = !0
                          }, s.src = "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="), (n = l) && T(), t.insertAdjacentHTML("afterbegin", l ? l.nodes.colorPicker.outerHTML || (new XMLSerializer).serializeToString(l.nodes.colorPicker) : i._html.replace(/§/g, r)), (t = t.children[0]).style.cssText = x.initStyle || "", (x.appendTo || document.body).appendChild(t))
                      }(o)), L(x.mode), R(o), K(), u = " " + x.mode.type + "-" + x.mode.z, E.slds.className += u, E.panel.className += u, x.noHexButton && q(E.HEX_butt, b + "butt", b + "labl");
                      x.size !== t && z(t, x.size);
                      for (var m in s = {
                              alphaBG: E.alpha_labl,
                              cmyOnly: E.HEX_labl
                          }) x[m] !== t && H({
                          target: s[m],
                          data: x[m]
                      });
                      x.noAlpha && (E.colorPicker.className += " no-alpha");
                      o.renderMemory(x.memoryColors), X(o), r = !0, P(t, "init"), n && (R(n), $())
                  }(this, o || {})
          };

      function R(e) {
          f = !0, l !== e && (l = e, v = e.color.colors, x = e.color.options, E = e.nodes, y = e.color, B = {}, O(v))
      }

      function X(l, n) {
          var i = n ? re : te;
          i(E.colorPicker, "mousedown", function(n) {
              var i = n || e.event,
                  c = ee(i),
                  g = (i.button || i.which) < 2 ? i.target || i.srcElement : {},
                  p = g.className;
              if (R(l), o = g, P(t, "resetEventListener"), b = "", g === E.sldl_3 || g === E.curm ? (o = E.sldl_3, r = I, b = "changeXYValue", q(E.slds, "do-drag")) : /sldr/.test(p) || g === E.curl || g === E.curr ? (o = E.sldr_4, r = M, b = "changeZValue") : g === E.opacity.children[0] || g === E.opacity_slider ? (o = E.opacity, r = D, b = "changeOpacityValue") : /-disp/.test(p) && !/HEX-/.test(p) ? (r = N, b = "changeInputValue", (3 === g.nextSibling.nodeType ? g.nextSibling.nextSibling : g.nextSibling).appendChild(E.nsarrow), a = {
                      type: (a = p.split("-disp")[0].split("-"))[0],
                      z: a[1] || ""
                  }, q(E.panel, "start-change"), d = 0) : g !== E.resize || x.noResize ? r = t : (x.sizes || function() {
                      var e = ["L", "S", "XS", "XXS"];
                      x.sizes = {}, E.testNode.style.cssText = "position:absolute;left:-1000px;top:-1000px;", document.body.appendChild(E.testNode);
                      for (var t = e.length; t--;) E.testNode.className = x.CSSPrefix + "app " + e[t], x.sizes[e[t]] = [E.testNode.offsetWidth, E.testNode.offsetHeight];
                      E.testNode.removeNode ? E.testNode.removeNode(!0) : document.body.removeChild(E.testNode)
                  }(), o = E.resizer, r = z, b = "resizeApp"), r && (m = {
                      pageX: c.X,
                      pageY: c.Y
                  }, o.style.display = "block", (h = J(o)).width = E.opacity.offsetWidth, h.childWidth = E.opacity_slider.offsetWidth, o.style.display = "", r(i), te(A ? document.body : e, "mousemove", r), s = e[w]($)), !/-disp/.test(p)) return F(i)
          }), i(E.colorPicker, "click", function(e) {
              R(l), H(e)
          }), i(E.colorPicker, "dblclick", H), i(E.colorPicker, "keydown", function(e) {
              R(l), Y(e)
          }), i(E.colorPicker, "keypress", Y), i(E.colorPicker, "paste", function(e) {
              return e.target.firstChild.data = e.clipboardData.getData("Text"), F(e)
          })
      }

      function P(o, l) {
          var n = r;
          r && (e[Q](s), re(A ? document.body : e, "mousemove", r), d && (a = {
              type: "alpha"
          }, $()), "function" != typeof r && "number" != typeof r || delete x.webUnsave, d = 1, r = t, q(E.slds, "do-drag", ""), q(E.panel, "(?:start-change|do-change)", ""), E.resizer.style.cssText = "", E.panelCover.style.cssText = "", E.memo_store.style.cssText = "background-color: " + _(v.RND.rgb) + "; " + W(v.alpha), E.memo.className = E.memo.className.replace(/\s+(?:dark|light)/, "") + (v["rgbaMix" + u[x.alphaBG]].luminance < .22 ? " dark" : " light"), a = t, j(), x.actionCallback && x.actionCallback(o, b || n.name || l || "external"))
      }

      function I(t) {
          var r = t || e.event,
              o = x.scale,
              a = ee(r),
              s = (a.X - h.left) * (4 === o ? 2 : o),
              l = (a.Y - h.top) * o,
              n = x.mode;
          return v[n.type][n.x] = V(s / 255, 0, 1), v[n.type][n.y] = 1 - V(l / 255, 0, 1), Z(), F(r)
      }

      function M(t) {
          var r = t || e.event,
              o = (ee(r).Y - h.top) * x.scale,
              a = x.mode;
          return v[a.type][a.z] = 1 - V(o / 255, 0, 1), Z(), F(r)
      }

      function D(t) {
          var r = t || e.event,
              o = ee(r);
          return f = !0, v.alpha = V(S.round((o.X - h.left) / h.width * 100), 0, 100) / 100, Z("alpha"), F(r)
      }

      function N(t) {
          var r, l = t || e.event,
              n = ee(l),
              i = m.pageY - n.Y,
              c = x.delayOffset,
              A = a.type,
              g = "alpha" === A;
          if (d || S.abs(i) >= c) return d || (d = (i > 0 ? -c : c) + +o.firstChild.data * (g ? 100 : 1), m.pageY += d, i += d, d = 1, q(E.panel, "start-change", "do-change"), E.panelCover.style.cssText = "position:absolute;left:0;top:0;right:0;bottom:0", document.activeElement.blur(), s = e[w]($)), "cmyk" === A && x.cmyOnly && (A = "cmy"), g ? (f = !0, v.alpha = V(i / 100, 0, 1)) : (r = p[A][a.z], v[A][a.z] = "Lab" === A ? V(i, r[0], r[1]) : V(i / r[1], 0, 1)), Z(g ? "alpha" : A), F(l)
      }

      function Y(o) {
          var a, s = o || e.event,
              n = s.which || s.keyCode,
              i = String.fromCharCode(n),
              c = document.activeElement,
              A = c.className.replace(x.CSSPrefix, "").split("-"),
              g = A[0],
              u = A[1],
              b = "alpha" === g,
              d = "HEX" === g,
              m = {
                  k40: -1,
                  k38: 1,
                  k34: -10,
                  k33: 10
              }["k" + n] / (b ? 100 : 1),
              h = {
                  HEX: /[0-9a-fA-F]/,
                  Lab: /[\-0-9]/,
                  alpha: /[\.0-9]/
              }[g] || /[0-9]/,
              f = p[g][g] || p[g][u],
              C = c.firstChild,
              B = oe(c),
              y = C.data,
              E = "0" !== y || d ? y.split("") : [];
          if (/^(?:27|13)$/.test(n) ? (F(s), c.blur()) : "keydown" === s.type ? (m ? a = V(S.round(1e6 * (+y + m)) / 1e6, f[0], f[1]) : /^(?:8|46)$/.test(n) && (B.range || (B.range++, B.start -= 8 === n ? 1 : 0), E.splice(B.start, B.range), a = E.join("") || "0"), a !== t && F(s, !0)) : "keypress" === s.type && (/^(?:37|39|8|46|9)$/.test(n) || F(s, !0), h.test(i) && (E.splice(B.start, B.range, i), a = E.join("")), B.start++), 13 === n && d) return C.data.length % 3 == 0 || "0" === C.data ? l.setColor("0" === C.data ? "000" : C.data, "rgb", v.alpha, !0) : (F(s, !0), c.focus());
          d && a !== t && (a = /^0+/.test(a) ? a : parseInt("" + a, 16) || 0), a !== t && "" !== a && +a >= f[0] && +a <= f[1] && (d && (a = a.toString(16).toUpperCase() || "0"), b ? v[g] = +a : d || (v[g][u] = +a / ("Lab" === g ? 1 : f[1])), Z(b ? "alpha" : g), O(v), r = !0, P(o, s.type), C.data = a, oe(c, S.min(c.firstChild.data.length, B.start < 0 ? 0 : B.start)))
      }

      function H(o) {
          var a, s, n = o || e.event,
              i = n.target || n.srcElement,
              c = i.className,
              A = i.parentNode,
              g = x,
              p = v.RND.rgb,
              u = x.mode,
              b = "",
              d = g.CSSPrefix,
              m = /(?:hs|rgb)/.test(A.className) && /^[HSBLRG]$/.test(i.firstChild ? i.firstChild.data : ""),
              h = /dblc/.test(n.type),
              f = "";
          if (!h || m) {
              if (-1 !== c.indexOf("-labl " + d + "labl")) q(E[c.split("-")[0]], d + "hide", ""), q(E[A.className.split("-")[1]], d + "hide");
              else if (-1 !== c.indexOf(d + "butt"))
                  if (m) h && 2 === x.scale && (b = (b = /hs/.test(u.type) ? "rgb" : /hide/.test(E.hsl.className) ? "hsv" : "hsl") + "-" + b[u.type.indexOf(u.z)]), l.setMode(b || c.replace("-butt", "").split(" ")[0]), f = "modeChange";
                  else if (/^[rgb]/.test(c)) b = c.split("-")[1], q(E.colorPicker, "no-rgb-" + b, (g["noRGB" + b] = !g["noRGB" + b]) ? t : ""), f = "noRGB" + b;
              else if (i === E.alpha_labl) a = g.customBG, s = g.alphaBG, q(E.colorPicker, "alpha-bg-" + s, "alpha-bg-" + (s = g.alphaBG = o.data || ("w" === s ? a ? "c" : "b" : "c" === s ? "b" : "w"))), i.firstChild.data = s.toUpperCase(), E.ctrl.style.backgroundColor = E.memo.style.backgroundColor = "c" !== s ? "" : "rgb(" + S.round(255 * a.r) + ", " + S.round(255 * a.g) + ", " + S.round(255 * a.b) + ")", E.raster.style.cssText = E.raster_bg.previousSibling.style.cssText = "c" !== s ? "" : W(a.luminance < .22 ? .5 : .4), f = "alphaBackground";
              else if (i === E.alpha_butt) q(E.colorPicker, "mute-alpha", (g.muteAlpha = !g.muteAlpha) ? t : ""), f = "alphaState";
              else if (i === E.HEX_butt) q(E.colorPicker, "no-HEX", (g.HEXState = !g.HEXState) ? t : ""), f = "HEXState";
              else if (i === E.HEX_labl) {
                  var C = "web save" === v.saveColor;
                  "web smart" === v.saveColor || C ? C ? l.setColor(g.webUnsave, "rgb") : (g.webUnsave || (g.webUnsave = U(p)), l.setColor(v.webSave, "rgb")) : (g.webUnsave = U(p), l.setColor(v.webSmart, "rgb")), f = "webColorState"
              } else /Lab-x-labl/.test(c) && (q(E.colorPicker, "cmy-only", (g.cmyOnly = !g.cmyOnly) ? t : ""), f = "cmykState");
              else if (i === E.bsav) K(), f = "saveAsBackground";
              else if (i === E.bres) {
                  var B = U(p),
                      y = v.alpha;
                  l.setColor(g.color), K(), l.setColor(B, "rgb", y), f = "resetColor"
              } else if (A === E.col1) v.hsv.h -= v.hsv.h > .5 ? .5 : -.5, Z("hsv"), f = "shiftColor";
              else if (A === E.col2) l.setColor(i.style.backgroundColor, "rgb", v.background.alpha), f = "setSavedColor";
              else if (A === E.memo) {
                  var w = function() {
                          E.memos.blinker && (E.memos.blinker.style.cssText = E.memos.cssText)
                      },
                      Q = function(t) {
                          E.memos.blinker = t, t.style.cssText = "background-color:" + (v.RGBLuminance > .22 ? "#333" : "#DDD"), e.setTimeout(w, 200)
                      };
                  if (i === E.memo_cursor) {
                      w(), E.memos.blinker = t, E.testNode.style.cssText = E.memo_store.style.cssText, E.memos.cssText = E.testNode.style.cssText;
                      for (var G = E.memos.length - 1; G--;)
                          if (E.memos.cssText === E.memos[G].style.cssText) {
                              Q(E.memos[G]);
                              break
                          }
                      if (!E.memos.blinker) {
                          for (G = E.memos.length - 1; G--;) E.memos[G + 1].style.cssText = E.memos[G].style.cssText;
                          E.memos[0].style.cssText = E.memo_store.style.cssText
                      }
                      f = "toMemory"
                  } else w(), l.setColor(i.style.backgroundColor, "rgb", i.style.opacity || 1), E.memos.cssText = i.style.cssText, Q(i), r = 1, f = "fromMemory"
              }
              f && (O(v), r = r || !0, P(o, f))
          }
      }

      function z(r, o) {
          var a, s = r || e.event,
              n = s ? ee(s) : {},
              i = o !== t,
              c = i ? o : n.X - h.left + 8,
              A = i ? o : n.Y - h.top + 8,
              g = x.sizes,
              p = i ? o : A < g.XXS[1] + 25 ? 0 : c < g.XS[0] + 25 ? 1 : c < g.S[0] + 25 || A < g.S[1] + 25 ? 2 : 3,
              u = [" S XS XXS", " S XS", " S", ""][p],
              b = !1,
              d = "";
          B.resizer !== u && (b = /XX/.test(u), a = x.mode, !b || /hs/.test(a.type) && "h" !== a.z ? a.original && l.setMode(a.original) : (d = a.type + "-" + a.z, l.setMode(/hs/.test(a.type) ? a.type + "-s" : "hsv-s"), x.mode.original = d), E.colorPicker.className = E.colorPicker.className.replace(/\s+(?:S|XS|XXS)/g, "") + u, x.scale = b ? 4 : /S/.test(u) ? 2 : 1, x.currentSize = p, B.resizer = u, f = !0, $(), j()), E.resizer.style.cssText = "display: block;width: " + (c > 10 ? c : 10) + "px;height: " + (A > 10 ? A : 10) + "px;"
      }

      function L(e) {
          var t = {
                  rgb_r: {
                      x: "b",
                      y: "g"
                  },
                  rgb_g: {
                      x: "b",
                      y: "r"
                  },
                  rgb_b: {
                      x: "r",
                      y: "g"
                  },
                  hsv_h: {
                      x: "s",
                      y: "v"
                  },
                  hsv_s: {
                      x: "h",
                      y: "v"
                  },
                  hsv_v: {
                      x: "h",
                      y: "s"
                  },
                  hsl_h: {
                      x: "s",
                      y: "l"
                  },
                  hsl_s: {
                      x: "h",
                      y: "l"
                  },
                  hsl_l: {
                      x: "h",
                      y: "s"
                  }
              },
              r = e.replace("-", "_"),
              o = "\\b(?:rg|hs)\\w\\-\\w\\b";
          return q(E.panel, o, e), q(E.slds, o, e), e = e.split("-"), x.mode = {
              type: e[0],
              x: t[r].x,
              y: t[r].y,
              z: e[1]
          }
      }

      function T() {
          var e = /\s+(?:hue-)*(?:dark|light)/g;
          for (var t in E.curl.className = E.curl.className.replace(e, ""), E.curr.className = E.curr.className.replace(e, ""), E.slds.className = E.slds.className.replace(e, ""), E.sldr_2.className = x.CSSPrefix + "sldr-2", E.sldr_4.className = x.CSSPrefix + "sldr-4", E.sldl_3.className = x.CSSPrefix + "sldl-3", E.styles) t.indexOf("sld") || (E.styles[t].cssText = "");
          B = {}
      }

      function j() {
          E.styles.curr.cssText = E.styles.curl.cssText, E.curl.className = x.CSSPrefix + "curl" + (C.noRGBZ ? " " + x.CSSPrefix + "curl-" + C.noRGBZ : ""), E.curr.className = x.CSSPrefix + "curr " + x.CSSPrefix + "curr-" + ("h" === x.mode.z ? C.HUEContrast : C.noRGBZ ? C.noRGBZ : C.RGBLuminance)
      }

      function Z(e) {
          O(y.setColor(t, e || x.mode.type)), f = !0
      }

      function K(e) {
          return y.saveAsBackground(), E.styles.col2.cssText = "background-color: " + _(v.background.RGB) + ";" + W(v.background.alpha), e && O(v), v
      }

      function O(e) {
          var r = S,
              o = C,
              a = u[x.alphaBG];
          o.hueDelta = r.round(100 * e["rgbaMixBGMix" + a].hueDelta), o.luminanceDelta = r.round(100 * e["rgbaMixBGMix" + a].luminanceDelta), o.RGBLuminance = e.RGBLuminance > .22 ? "light" : "dark", o.HUEContrast = e.HUELuminance > .22 ? "light" : "dark", o.contrast = o.luminanceDelta > o.hueDelta ? "contrast" : "", o.readabiltiy = e["rgbaMixBGMix" + a].WCAG2Ratio >= 7 ? "green" : e["rgbaMixBGMix" + a].WCAG2Ratio >= 4.5 ? "orange" : "", o.noRGBZ = x["no" + x.mode.type.toUpperCase() + x.mode.z] ? "g" === x.mode.z && e.rgb.g < .59 || "b" === x.mode.z || "r" === x.mode.z ? "dark" : "light" : t
      }

      function $() {
          if (r) {
              if (!f) return s = e[w]($);
              f = !1
          }
          var l, n, i, c, A = x,
              g = A.mode,
              u = A.scale,
              b = A.CSSPrefix,
              d = v,
              m = E,
              y = m.styles,
              Q = m.textNodes,
              G = p,
              k = a,
              R = C,
              X = B,
              P = S,
              D = W,
              N = _,
              Y = 0,
              H = 0,
              z = d[g.type][g.x],
              L = P.round(255 * z / (4 === u ? 2 : u)),
              T = d[g.type][g.y],
              j = 1 - T,
              Z = P.round(255 * j / u),
              K = 1 - d[g.type][g.z],
              O = P.round(255 * K / u),
              U = [z, T],
              V = "rgb" === g.type,
              F = "h" === g.z,
              q = "hsl" === g.type,
              J = q && "s" === g.z,
              ee = r === I,
              te = r === M;
          for (l in V && (U[0] >= U[1] ? H = 1 : Y = 1, X.sliderSwap !== Y && (m.sldr_2.className = A.CSSPrefix + "sldr-" + (3 - Y), X.sliderSwap = Y)), (V && !te || F && !ee || !F && !te) && (y[F ? "sldl_2" : "sldr_2"][V ? "cssText" : "backgroundColor"] = V ? D((U[Y] - U[H]) / (1 - U[H] || 0)) : N(d.hueRGB)), F || (te || (y.sldr_4.cssText = D(V ? U[H] : J ? P.abs(1 - 2 * j) : j)), ee || (y.sldl_3.cssText = D(q && "l" === g.z ? P.abs(1 - 2 * K) : K)), q && (n = J ? "r-" : "l-", i = J ? j > .5 ? 4 : 3 : K > .5 ? 3 : 4, X[c = J ? "sldr_4" : "sldl_3"] !== i && (m[c].className = A.CSSPrefix + "sld" + n + i, X[c] = i))), te || (y.curm.cssText = "left: " + L + "px; top: " + Z + "px;"), ee || (y.curl.top = O + "px"), k && (y.curr.top = O + "px"), (k && "alpha" === k.type || o === m.opacity) && (y.opacity_slider.left = A.opacityPositionRelative ? d.alpha * ((h.width || m.opacity.offsetWidth) - (h.childWidth || m.opacity_slider.offsetWidth)) + "px" : 100 * d.alpha + "%"), y.col1.cssText = "background-color: " + N(d.RND.rgb) + "; " + (A.muteAlpha ? "" : D(d.alpha)), y.opacity.backgroundColor = N(d.RND.rgb), y.cold.width = R.hueDelta + "%", y.cont.width = R.luminanceDelta + "%", Q) n = l.split("_"), A.cmyOnly && (n[0] = n[0].replace("k", "")), i = n[1] ? d.RND[n[0]][n[1]] : d.RND[n[0]] || d[n[0]], X[l] !== i && (X[l] = i, Q[l].data = i > 359.5 && "HEX" !== l ? 0 : i, "HEX" === l || A.noRangeBackground || (i = d[n[0]][n[1]] !== t ? d[n[0]][n[1]] : d[n[0]], "Lab" === n[0] && (i = (i - G[n[0]][n[1]][0]) / (G[n[0]][n[1]][1] - G[n[0]][n[1]][0])), y[l].backgroundPosition = P.round(100 * (1 - i)) + "% 0%"));
          (n = d._rgb ? [d._rgb.r !== d.rgb.r, d._rgb.g !== d.rgb.g, d._rgb.b !== d.rgb.b] : []).join("") !== X.outOfGammut && (m.rgb_r_labl.firstChild.data = n[0] ? "!" : " ", m.rgb_g_labl.firstChild.data = n[1] ? "!" : " ", m.rgb_b_labl.firstChild.data = n[2] ? "!" : " ", X.outOfGammut = n.join("")), R.noRGBZ && X.noRGBZ !== R.noRGBZ && (m.curl.className = b + "curl " + b + "curl-" + R.noRGBZ, te || (m.curr.className = b + "curr " + b + "curr-" + R.noRGBZ), X.noRGBZ = R.noRGBZ), X.HUEContrast !== R.HUEContrast && "h" === g.z ? (m.slds.className = m.slds.className.replace(/\s+hue-(?:dark|light)/, "") + " hue-" + R.HUEContrast, te || (m.curr.className = b + "curr " + b + "curr-" + R.HUEContrast), X.HUEContrast = R.HUEContrast) : X.RGBLuminance !== R.RGBLuminance && (m.colorPicker.className = m.colorPicker.className.replace(/\s+(?:dark|light)/, "") + " " + R.RGBLuminance, te || "h" === g.z || R.noRGBZ || (m.curr.className = b + "curr " + b + "curr-" + R.RGBLuminance), X.RGBLuminance = R.RGBLuminance), X.contrast === R.contrast && X.readabiltiy === R.readabiltiy || (m.ctrl.className = m.ctrl.className.replace(" contrast", "").replace(/\s*(?:orange|green)/, "") + (R.contrast ? " " + R.contrast : "") + (R.readabiltiy ? " " + R.readabiltiy : ""), X.contrast = R.contrast, X.readabiltiy = R.readabiltiy), X.saveColor !== d.saveColor && (m.HEX_labl.firstChild.data = d.saveColor ? "web save" === d.saveColor ? "W" : "M" : "!", X.saveColor = d.saveColor), A.renderCallback && A.renderCallback(d, g), r && (s = e[w]($))
      }

      function U(e) {
          var t = {};
          for (var r in e) t[r] = e[r];
          return t
      }

      function _(e, t) {
          for (var r = "", o = (t || "rgb").split(""), a = o.length; a--;) r = ", " + e[o[a]] + r;
          return (t || "rgb") + "(" + r.substr(2) + ")"
      }

      function V(e, t, r) {
          return e > r ? r : e < t ? t : e
      }

      function W(e) {
          return e === t && (e = 1), g ? "opacity: " + S.round(1e10 * e) / 1e10 + ";" : "filter: alpha(opacity=" + S.round(100 * e) + ");"
      }

      function F(t, r) {
          return t.preventDefault ? t.preventDefault() : t.returnValue = !1, r || (e.getSelection ? e.getSelection().removeAllRanges() : document.selection.empty()), !1
      }

      function q(e, r, o) {
          return !!e && (e.className = o !== t ? e.className.replace(new RegExp("\\s+?" + r, "g"), o ? " " + o : "") : e.className + " " + r)
      }

      function J(t) {
          var r = t.getBoundingClientRect ? t.getBoundingClientRect() : {
                  top: 0,
                  left: 0
              },
              o = t && t.ownerDocument,
              a = o.body,
              s = o.defaultView || o.parentWindow || e,
              l = o.documentElement || a.parentNode,
              n = l.clientTop || a.clientTop || 0,
              i = l.clientLeft || a.clientLeft || 0;
          return {
              left: r.left + (s.pageXOffset || l.scrollLeft) - i,
              top: r.top + (s.pageYOffset || l.scrollTop) - n
          }
      }

      function ee(t) {
          var r = e.document;
          return {
              X: t.pageX || t.clientX + r.body.scrollLeft + r.documentElement.scrollLeft,
              Y: t.pageY || t.clientY + r.body.scrollTop + r.documentElement.scrollTop
          }
      }

      function te(e, t, r) {
          te.cache = te.cache || {
              _get: function(e, t, r, o) {
                  for (var a = te.cache[t] || [], s = a.length; s--;)
                      if (e === a[s].obj && "" + r == "" + a[s].func) return r = a[s].func, o || (a[s] = a[s].obj = a[s].func = null, a.splice(s, 1)), r
              },
              _set: function(e, t, r) {
                  var o = te.cache[t] = te.cache[t] || [];
                  if (te.cache._get(e, t, r, !0)) return !0;
                  o.push({
                      func: r,
                      obj: e
                  })
              }
          }, !r.name && te.cache._set(e, t, r) || "function" != typeof r || (e.addEventListener ? e.addEventListener(t, r, !1) : e.attachEvent("on" + t, r))
      }

      function re(e, t, r) {
          "function" == typeof r && (r.name || (r = te.cache._get(e, t, r) || r), e.removeEventListener ? e.removeEventListener(t, r, !1) : e.detachEvent("on" + t, r))
      }

      function oe(r, o) {
          var a = {};
          if (o === t) {
              if (e.getSelection) {
                  r.focus(), (s = (l = e.getSelection().getRangeAt(0)).cloneRange()).selectNodeContents(r), s.setEnd(l.endContainer, l.endOffset), a = {
                      end: s.toString().length,
                      range: l.toString().length
                  }
              } else {
                  r.focus();
                  var s, l = document.selection.createRange();
                  (s = document.body.createTextRange()).moveToElementText(r), s.setEndPoint("EndToEnd", l), a = {
                      end: s.text.length,
                      range: l.text.length
                  }
              }
              return a.start = a.end - a.range, a
          }
          if (-1 == o && (o = r.text().length), e.getSelection) r.focus(), e.getSelection().collapse(r.firstChild, o);
          else {
              var n = document.body.createTextRange();
              n.moveToElementText(r), n.moveStart("character", o), n.collapse(!0), n.select()
          }
          return o
      }
      e.ColorPicker = k, k.addEvent = te, k.removeEvent = re, k.getOrigin = J, k.limitValue = V, k.changeClass = q, k.prototype.setColor = function(e, t, r, o) {
          R(this), a = !0, O(y.setColor.apply(y, arguments)), o && this.startRender(!0)
      }, k.prototype.saveAsBackground = function() {
          return R(this), K(!0)
      }, k.prototype.setCustomBackground = function(e) {
          return R(this), y.setCustomBackground(e)
      }, k.prototype.startRender = function(t) {
          R(this), t ? (r = !1, $(), this.stopRender()) : (r = 1, s = e[w]($))
      }, k.prototype.stopRender = function() {
          R(this), e[Q](s), a && (r = 1, P(t, "external"))
      }, k.prototype.setMode = function(e) {
          R(this), L(e), T(), $()
      }, k.prototype.destroyAll = function() {
          var e = this.nodes.colorPicker,
              t = function(e) {
                  for (var r in e)(e[r] && "[object Object]" === e[r].toString() || e[r] instanceof Array) && t(e[r]), e[r] = null, delete e[r]
              };
          this.stopRender(), X(this, !0), t(this), e.parentNode.removeChild(e), e = null
      }, k.prototype.renderMemory = function(e) {
          var r = this.nodes.memos,
              o = [];
          "string" == typeof e && (e = e.replace(/^'|'$/g, "").replace(/\s*/, "").split("','"));
          for (var a = r.length; a--;) e && "string" == typeof e[a] && (o = e[a].replace("rgba(", "").replace(")", "").split(","), e[a] = {
              r: o[0],
              g: o[1],
              b: o[2],
              a: o[3]
          }), r[a].style.cssText = "background-color: " + (e && e[a] !== t ? _(e[a]) + ";" + W(e[a].a || 1) : "rgb(0,0,0);")
      }, te(A ? document.body : e, "mouseup", P);
      for (var ae = G.length; ae-- && !e[w];) e[w] = e[G[ae] + "RequestAnimationFrame"], e[Q] = e[G[ae] + "CancelAnimationFrame"] || e[G[ae] + "CancelRequestAnimationFrame"];
      e[w] = e[w] || function(t) {
          return e.setTimeout(t, 1e3 / x.fps)
      }, e[Q] = e[Q] || function(t) {
          return e.clearTimeout(t), s = null
      }
  }(window),
  function(e) {
      e.jsColorPicker = function(t, r) {
          var o = function(e, t) {
                  var r = this.input,
                      o = this.patch,
                      a = e.RND.rgb,
                      s = e.RND.hsl,
                      l = this.isIE8 ? (e.alpha < .16 ? "0" : "") + Math.round(100 * e.alpha).toString(16).toUpperCase() + e.HEX : "",
                      n = a.r + ", " + a.g + ", " + a.b,
                      i = "rgba(" + n + ", " + e.alpha + ")",
                      c = 1 !== e.alpha && !this.isIE8,
                      A = r.getAttribute("data-colorMode");
                  o.style.cssText = "color:" + (e.rgbaMixCustom.luminance > .22 ? "#222" : "#ddd") + ";background-color:" + i + ";filter:" + (this.isIE8 ? "progid:DXImageTransform.Microsoft.gradient(startColorstr=#" + l + ",endColorstr=#" + l + ")" : ""), r.value = "HEX" !== A || c ? "rgb" === A || "HEX" === A && c ? c ? i : "rgb(" + n + ")" : "hsl" + (c ? "a(" : "(") + s.h + ", " + s.s + "%, " + s.l + "%" + (c ? ", " + e.alpha : "") + ")" : "#" + (this.isIE8 ? l : e.HEX), this.displayCallback && this.displayCallback(e, t, this)
              },
              a = function(e) {
                  return e.value || e.getAttribute("value") || e.style.backgroundColor || "#FFFFFF"
              },
              s = function(e, t) {
                  var r = n.current;
                  if ("toMemory" === t) {
                      for (var o = r.nodes.memos, a = "", s = 0, l = [], i = 0, c = o.length; i < c; i++) a = o[i].style.backgroundColor, s = o[i].style.opacity, s = Math.round(100 * ("" === s ? 1 : s)) / 100, l.push(a.replace(/, /g, ",").replace("rgb(", "rgba(").replace(")", "," + s + ")"));
                      l = "'" + l.join("','") + "'", ColorPicker.docCookies("colorPickerMemos" + (this.noAlpha ? "NoAlpha" : ""), l)
                  } else if ("resizeApp" === t) ColorPicker.docCookies("colorPickerSize", r.color.options.currentSize);
                  else if ("modeChange" === t) {
                      var A = r.color.options.mode;
                      ColorPicker.docCookies("colorPickerMode", A.type + "-" + A.z)
                  }
              },
              l = function(t, l, c) {
                  var A = c ? "removeEventListener" : "addEventListener";
                  t[A]("focus", function(c) {
                      var A = e.ColorPicker.getOrigin(this),
                          g = l ? Array.prototype.indexOf.call(i, this) : 0,
                          p = n[g] || (n[g] = function(t, r) {
                              var l = {
                                  klass: e.ColorPicker,
                                  input: t,
                                  patch: t,
                                  isIE8: !!document.all && !document.addEventListener,
                                  margin: {
                                      left: -1,
                                      top: 2
                                  },
                                  customBG: "#FFFFFF",
                                  color: a(t),
                                  initStyle: "display: none",
                                  mode: ColorPicker.docCookies("colorPickerMode") || "hsv-h",
                                  memoryColors: ColorPicker.docCookies("colorPickerMemos" + ((r || {}).noAlpha ? "NoAlpha" : "")),
                                  size: ColorPicker.docCookies("colorPickerSize") || 1,
                                  renderCallback: o,
                                  actionCallback: s
                              };
                              for (var n in r) l[n] = r[n];
                              return new l.klass(l)
                          }(this, r)),
                          u = p.color.options,
                          b = p.nodes.colorPicker,
                          d = u.appendTo || document.body,
                          m = /static/.test(e.getComputedStyle(d).position) ? {
                              left: 0,
                              top: 0
                          } : d.getBoundingClientRect(),
                          h = 0;
                      u.color = a(t), b.style.cssText = "position: absolute;" + (n[g].cssIsReady ? "" : "display: none;") + "left:" + (A.left + u.margin.left - m.left) + "px;top:" + (A.top + +this.offsetHeight + u.margin.top - m.top) + "px;", l || (u.input = t, u.patch = t, p.setColor(a(t), void 0, void 0, !0), p.saveAsBackground()), n.current = n[g], d.appendChild(b), h = setInterval(function() {
                          n.current.cssIsReady && (h = clearInterval(h), b.style.display = "block")
                      }, 10)
                  }), n.evt && !c || (n.evt = !0, e[A]("mousedown", function(e) {
                      var t = n.current,
                          r = t ? t.nodes.colorPicker : void 0,
                          o = (t && t.color.options.animationSpeed, t && function(e) {
                              for (; e;) {
                                  if (-1 !== (e.className || "").indexOf("cp-app")) return e;
                                  e = e.parentNode
                              }
                              return !1
                          }(e.target)),
                          a = Array.prototype.indexOf.call(i, e.target);
                      o && Array.prototype.indexOf.call(n, o) ? e.target === t.nodes.exit && (r.style.display = "none", document.activeElement.blur()) : -1 !== a || r && (r.style.display = "none")
                  }))
              },
              n = e.jsColorPicker.colorPickers || [],
              i = document.querySelectorAll(t),
              c = new e.Colors({
                  customBG: r.customBG,
                  allMixDetails: !0
              });
          e.jsColorPicker.colorPickers = n;
          for (var A = 0, g = i.length; A < g; A++) {
              var p = i[A];
              if ("destroy" === r) l(p, r && r.multipleInstances, !0), n[A] && n[A].destroyAll();
              else {
                  var u = a(p),
                      b = u.split("(");
                  c.setColor(u), r && r.init && r.init(p, c.colors), p.setAttribute("data-colorMode", b[1] ? b[0].substr(0, 3) : "HEX"), l(p, r && r.multipleInstances, !1), r && r.readOnly && (p.readOnly = !0)
              }
          }
          return e.jsColorPicker.colorPickers
      }, e.ColorPicker.docCookies = function(e, t, r) {
          var o, a, s, l, n = encodeURIComponent,
              i = decodeURIComponent,
              c = {};
          if (void 0 === t) {
              for (a = (o = document.cookie.split(/;\s*/) || []).length; a--;)(s = o[a].split("="))[0] && (c[i(s.shift())] = i(s.join("=")));
              return e ? c[e] : c
          }
          r = r || {}, ("" === t || r.expires < 0) && (r.expires = -1), void 0 !== r.expires && (l = new Date).setDate(l.getDate() + r.expires), document.cookie = n(e) + "=" + n(t) + (l ? "; expires=" + l.toUTCString() : "") + (r.path ? "; path=" + r.path : "") + (r.domain ? "; domain=" + r.domain : "") + (r.secure ? "; secure" : "")
      }
  }(this);

  // JavaScript Color Picker
  const colors = jsColorPicker('input.color', {
      customBG: '#222',
      readOnly: true,
      // patch: false,
      init: function(elm, colors) { // colors is a different instance (not connected to colorPicker)
          elm.style.backgroundColor = elm.value;
          elm.style.color = colors.rgbaMixCustom.luminance > 0.22 ? '#222' : '#ddd';
          color = elm.value;
      }
  });