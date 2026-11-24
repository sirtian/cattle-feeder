# -*- coding: utf-8 -*-
"""
远程控制投料车 方案设计图（A3 横版，4 张）
由三维演示 feed-cart-3d.html 的几何反推，单位 mm。
输出：viz/drawings/*.svg + feed-cart-drawings.html
"""
import math
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "drawings")
os.makedirs(OUT, exist_ok=True)

# ---------------- 基本尺寸（mm） ----------------
X_MIN, X_MAX = -1355, 1355
Y_ANT, Y_BEACON, Y_BOX = 1990, 1740, 1560
Y_BOX_BOT, Y_FLOOR = 460, 520
X_BOX0, X_BOX1 = -700, 1300
Z_BOX = 475
GATE_X, GATE_Y0, GATE_Y1 = -370, 600, 800
BELT_X, BELT_W = -370, 500
BELT_Z0, BELT_Z1 = 560, 1330
BELT_Y0, BELT_Y1 = 630, 950
BELT_LEN = math.hypot(BELT_Z1 - BELT_Z0, BELT_Y1 - BELT_Y0)
BELT_ANG = math.degrees(math.atan2(BELT_Y1 - BELT_Y0, BELT_Z1 - BELT_Z0))
CONC_X0, CONC_X1, CONC_Z = -1300, -700, 300
TROUGH_Z0, TROUGH_Z1 = 1170, 1730
TROUGH_RIM, FEED_Y = 700, 540
WHEEL_R, WHEEL_W = 220, 170
AXLE_X, TRACK_Z = 820, 470


def n(v):
    s = f"{v:.2f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


class SVG:
    def __init__(self, w=420, h=297):
        self.w, self.h = w, h
        self.body = []

    def add(self, s):
        self.body.append(s)

    def line(self, x1, y1, x2, y2, cls="vis", extra=""):
        self.add(f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" class="{cls}" {extra}/>')

    @staticmethod
    def _fill(fill):
        if fill and fill != "none":
            return f' style="fill:{fill}"'
        return ' fill="none"'

    def poly(self, pts, cls="vis", fill="none", close=False):
        d = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        self.add(f'<{tag} points="{d}" class="{cls}"{self._fill(fill)}/>')

    def rect(self, x, y, w, h, cls="vis", fill="none", rx=0):
        r = f' rx="{n(rx)}"' if rx else ""
        self.add(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" class="{cls}"{self._fill(fill)}{r}/>')

    def circle(self, cx, cy, r, cls="vis", fill="none"):
        self.add(f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" class="{cls}"{self._fill(fill)}/>')

    def path(self, d, cls="vis", fill="none"):
        self.add(f'<path d="{d}" class="{cls}"{self._fill(fill)}/>')

    def text(self, x, y, s, cls="txt", size=None, anchor="middle", weight=None, rot=None):
        st = f'font-size:{n(size)}px;' if size else ""
        if weight:
            st += f"font-weight:{weight};"
        tr = f' transform="rotate({n(rot)} {n(x)} {n(y)})"' if rot is not None else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{n(x)}" y="{n(y)}" class="{cls}" text-anchor="{anchor}" style="{st}"{tr}>{s}</text>')

    def mtext(self, x, y, lines, cls="notetxt", size=2.2, lh=4.6, anchor="start"):
        for i, line in enumerate(lines):
            self.text(x, y + i * lh, line, cls, size=size, anchor=anchor)

    def render(self, title):
        style = """
        text{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;}
        .vis{stroke:#1f2933;stroke-width:0.5;fill:none;stroke-linecap:round;stroke-linejoin:round;}
        .med{stroke:#33434f;stroke-width:0.32;fill:none;stroke-linecap:round;stroke-linejoin:round;}
        .thin{stroke:#4c5d69;stroke-width:0.22;fill:none;stroke-linecap:round;stroke-linejoin:round;}
        .hid{stroke:#8b99a3;stroke-width:0.2;stroke-dasharray:1.6 0.9;fill:none;}
        .cen{stroke:#b04a3a;stroke-width:0.18;stroke-dasharray:4 1 0.8 1;fill:none;}
        .phantom{stroke:#8b99a3;stroke-width:0.2;stroke-dasharray:3 1 0.8 1;fill:none;}
        .dim{stroke:#2d6b88;stroke-width:0.16;fill:none;}
        .dimext{stroke:#2d6b88;stroke-width:0.13;fill:none;}
        .leader{stroke:#2d6b88;stroke-width:0.16;fill:none;}
        .txt{fill:#1e2933;font-size:2.5px;}
        .dimtxt{fill:#245a75;font-size:2.25px;}
        .notetxt{fill:#33424d;font-size:2.2px;}
        .small{fill:#5b6b76;font-size:1.9px;}
        .viewtitle{fill:#1e2933;font-size:3.2px;font-weight:700;}
        .sheetno{fill:#1e2933;font-size:2.4px;font-weight:700;}
        .titlebig{fill:#15212a;font-size:5.4px;font-weight:700;}
        .red{fill:#a8452f;font-size:2.1px;}
        """
        defs = """
        <defs>
          <pattern id="hatch" width="1.7" height="1.7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="1.7" stroke="#8fa0aa" stroke-width="0.13"/>
          </pattern>
          <pattern id="hatch2" width="1.7" height="1.7" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
            <line x1="0" y1="0" x2="0" y2="1.7" stroke="#9fb0ba" stroke-width="0.12"/>
          </pattern>
          <pattern id="straw" width="2.3" height="2.3" patternUnits="userSpaceOnUse">
            <rect width="2.3" height="2.3" fill="#f5e8d0"/>
            <path d="M0.3 0.6 l0.9 0.2 M1.3 1.7 l0.7 -0.3 M0.5 2.0 l0.5 0.2" stroke="#c49a5e" stroke-width="0.16"/>
          </pattern>
          <pattern id="conc" width="2.0" height="2.0" patternUnits="userSpaceOnUse">
            <rect width="2.0" height="2.0" fill="#f7edc9"/>
            <circle cx="0.6" cy="0.6" r="0.18" fill="#c9a33e"/>
            <circle cx="1.4" cy="1.5" r="0.16" fill="#d4b45a"/>
          </pattern>
          <marker id="arrow" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 z" fill="#2d6b88"/>
          </marker>
        </defs>
        """
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}mm" height="{self.h}mm" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f"<title>{title}</title><style>{style}</style>{defs}"
            + "".join(self.body)
            + "</svg>"
        )


class View:
    def __init__(self, svg, s, ox, oy, xsign=1, ysign=1):
        self.svg, self.s, self.ox, self.oy = svg, s, ox, oy
        self.xsign, self.ysign = xsign, ysign

    def X(self, a):
        return self.ox + self.xsign * a * self.s

    def Y(self, b):
        return self.oy - self.ysign * b * self.s

    def line(self, a1, b1, a2, b2, cls="vis"):
        self.svg.line(self.X(a1), self.Y(b1), self.X(a2), self.Y(b2), cls)

    def rect(self, a1, b1, a2, b2, cls="vis", fill="none", rx=0):
        x1, x2 = sorted((self.X(a1), self.X(a2)))
        y1, y2 = sorted((self.Y(b1), self.Y(b2)))
        self.svg.rect(x1, y1, x2 - x1, y2 - y1, cls, fill, rx)

    def circle(self, a, b, r, cls="vis", fill="none"):
        self.svg.circle(self.X(a), self.Y(b), abs(r * self.s), cls, fill)

    def poly(self, pts, cls="vis", fill="none", close=False):
        self.svg.poly([(self.X(a), self.Y(b)) for a, b in pts], cls, fill, close)

    def text(self, a, b, s, cls="txt", size=None, anchor="middle", weight=None, rot=None):
        self.svg.text(self.X(a), self.Y(b), s, cls, size, anchor, weight, rot)


# ---------------- 标注 ----------------
DIM = "#2d6b88"


def arrow(svg, x, y, direction):
    """direction: 'left','right','up','down' 箭头尖在 (x,y)"""
    L, W = 1.7, 0.48
    if direction == "left":
        p = [(x, y), (x + L, y - W), (x + L, y + W)]
    elif direction == "right":
        p = [(x, y), (x - L, y - W), (x - L, y + W)]
    elif direction == "up":
        p = [(x, y), (x - W, y + L), (x + W, y + L)]
    else:
        p = [(x, y), (x - W, y - L), (x + W, y - L)]
    svg.poly(p, cls="", fill=DIM, close=True)


def dim_h(svg, x1, x2, y, label, ref1=None, ref2=None, text_above=True, tick=False):
    """水平尺寸线，x1..x2 为纸面坐标，ref1/ref2 为引出起点 y"""
    if ref1 is not None:
        svg.line(x1, ref1, x1, y + (1.6 if text_above else -1.6), "dimext")
    if ref2 is not None:
        svg.line(x2, ref2, x2, y + (1.6 if text_above else -1.6), "dimext")
    svg.line(x1, y, x2, y, "dim")
    if abs(x2 - x1) < 5:
        # 小尺寸：斜线
        svg.line(x1 - 0.8, y + 0.8, x1 + 0.8, y - 0.8, "dim")
        svg.line(x2 - 0.8, y + 0.8, x2 + 0.8, y - 0.8, "dim")
        tx = (x1 + x2) / 2
        ty = y - 1.3 if text_above else y + 3.2
        svg.text(tx, ty, label, "dimtxt", size=2.1)
        return
    arrow(svg, x1, y, "left")
    arrow(svg, x2, y, "right")
    tx, ty = (x1 + x2) / 2, y - 1.2 if text_above else y + 3.0
    svg.rect(tx - len(label) * 0.62, ty - 2.1, len(label) * 1.24, 2.9, cls="", fill="#ffffff")
    svg.text(tx, ty, label, "dimtxt", size=2.2)


def dim_v(svg, y1, y2, x, label, ref1=None, ref2=None, text_left=True):
    """竖直尺寸线，y1..y2 纸面坐标，ref 为引出起点 x"""
    if ref1 is not None:
        svg.line(ref1, y1, x + (1.6 if text_left else -1.6), y1, "dimext")
    if ref2 is not None:
        svg.line(ref2, y2, x + (1.6 if text_left else -1.6), y2, "dimext")
    svg.line(x, y1, x, y2, "dim")
    arrow(svg, x, y1, "up")
    arrow(svg, x, y2, "down")
    tx = x - 1.2 if text_left else x + 3.0
    ty = (y1 + y2) / 2
    svg.rect(tx - 1.0, ty - len(label) * 0.62, 2.6, len(label) * 1.24, cls="", fill="#ffffff")
    svg.text(tx, ty, label, "dimtxt", size=2.2, rot=-90)


def leader(svg, x1, y1, x2, y2, text, anchor="start", cls="notetxt", size=2.2, dot=True):
    svg.line(x1, y1, x2, y2, "leader")
    if dot:
        svg.circle(x1, y1, 0.35, cls="", fill=DIM)
    svg.text(x2 + (0.8 if anchor == "start" else -0.8), y2 + 0.7, text, cls, size=size, anchor=anchor)


def balloon(svg, num, x, y, tx, ty):
    svg.line(x, y, tx, ty, "leader")
    svg.circle(tx, ty, 2.7, "med", fill="#ffffff")
    svg.text(tx, ty + 0.9, str(num), "txt", size=2.4, weight="bold")


def center_mark(svg, x, y, r=2.6):
    svg.line(x - r, y, x + r, y, "cen")
    svg.line(x, y - r, x, y + r, "cen")


def frame(svg, sheet_no, total, title, scale, dwg_no, note="方案设计图 · 非施工图", project="智能养牛 · 50 头验证项目"):
    svg.rect(8, 8, 404, 281, "med")
    # 标题栏
    x0, y0, w, h = 282, 251, 122, 38
    svg.rect(x0, y0, w, h, "med")
    svg.line(x0, y0 + 8, x0 + w, y0 + 8, "thin")
    svg.line(x0, y0 + 22, x0 + w, y0 + 22, "thin")
    svg.line(x0, y0 + 30, x0 + w, y0 + 30, "thin")
    svg.line(x0 + 62, y0 + 22, x0 + 62, y0 + h, "thin")
    svg.line(x0 + 92, y0 + 22, x0 + 92, y0 + h, "thin")
    svg.text(x0 + 2, y0 + 5.6, project, "txt", size=2.3, anchor="start")
    svg.text(x0 + w - 2, y0 + 5.6, note, "red", size=1.9, anchor="end")
    svg.text(x0 + w / 2, y0 + 17.5, title, "titlebig", size=4.7)
    svg.text(x0 + 2, y0 + 27, f"图号 {dwg_no}", "txt", size=2.1, anchor="start")
    svg.text(x0 + 64, y0 + 27, f"比例 {scale}", "txt", size=2.1, anchor="start")
    svg.text(x0 + 94, y0 + 27, "日期 2026-11-16", "txt", size=2.1, anchor="start")
    svg.text(x0 + 2, y0 + 35, "设计 项目组", "txt", size=2.1, anchor="start")
    svg.text(x0 + 64, y0 + 35, "审核 —", "txt", size=2.1, anchor="start")
    svg.text(x0 + 94, y0 + 35, "版本 A", "txt", size=2.1, anchor="start")
    svg.text(x0 + w - 2, y0 + 35, f"第 {sheet_no}/{total} 页", "txt", size=2.1, anchor="end")
    # 图幅标记
    svg.text(12, 14.5, "远程控制投料车", "sheetno", anchor="start")
    svg.text(408, 14.5, "单位 mm · 第一角投影", "small", anchor="end")


def ground(svg, x1, x2, y, hatch=True):
    svg.line(x1, y, x2, y, "vis")
    if hatch:
        x = x1
        while x < x2:
            svg.line(x, y, x - 1.6, y + 2.2, "thin")
            x += 4.0


def wheel_side(v, cx):
    v.circle(cx, WHEEL_R, WHEEL_R, "vis")
    v.circle(cx, WHEEL_R, WHEEL_R * 0.70, "thin")
    v.circle(cx, WHEEL_R, 100, "thin")
    v.circle(cx, WHEEL_R, 28, "thin")
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        v.line(cx + 30 * math.cos(a), WHEEL_R + 30 * math.sin(a),
               cx + 95 * math.cos(a), WHEEL_R + 95 * math.sin(a), "thin")


# ============================================================
# FC-01 总图
# ============================================================
def sheet1():
    svg = SVG()
    s = 0.05
    side = View(svg, s, 80, 125)
    top = View(svg, s, 80, 195, ysign=-1)
    front = View(svg, s, 250, 125, xsign=-1)

    # ---- 侧视图（非卸料侧，-Z） ----
    ground(svg, 10, 160, 125)
    wheel_side(side, -AXLE_X)
    wheel_side(side, AXLE_X)

    side.rect(-1250, 300, 1250, 460, "vis", fill="#eef2f4")
    side.rect(-400, 120, 600, 360, "hid")
    side.rect(-700, 460, 1300, 1560, "vis", fill="#f8fafb")
    side.rect(-700, 1490, 1300, 1560, "thin")
    side.line(-680, 520, 1280, 520, "hid")
    side.line(-680, 565, 1280, 565, "hid")
    for lx in (-500, 1000):
        side.rect(lx - 35, 448, lx + 35, 462, "hid")
    # 侧板加强筋
    for xx in (-250, 250, 750, 1150):
        side.line(xx, 470, xx, 1488, "thin")

    # 精料仓
    side.rect(-1300, 500, -700, 1220, "vis", fill="#fbfcfc")
    side.poly([(-1300, 500), (-1220, 290), (-780, 290), (-700, 500)], "vis", fill="#fbfcfc", close=True)
    side.rect(-1290, 1220, -710, 1260, "med", fill="#eef2f4")
    side.rect(-1150, 1260, -850, 1275, "thin")
    for lx in (-1260, -740):
        side.rect(lx, 460, lx + 34, 500, "med", fill="#dfe7eb")

    # 保险杠
    for bx in (-1355, 1265):
        side.rect(bx, 320, bx + 90, 560, "vis", fill="#e8edf0")
        side.line(bx + 45, 340, bx + 45, 540, "thin")

    # 桅杆 / 相机 / 警示灯 / 天线
    side.rect(1167, 970, 1193, 1720, "med")
    side.rect(1135, 1670, 1265, 1770, "med", fill="#eef2f4")
    side.rect(890, 1620, 1010, 1740, "med", fill="#f3e6d8")
    side.line(-720, 1340, -720, 1960, "med")
    side.circle(-720, 1960, 20, "med", fill="#e3f1ef")

    # 远侧侧带/侧门投影
    side.rect(-620, BELT_Y0, -120, BELT_Y1, "hid")
    side.rect(-610, GATE_Y0, -130, GATE_Y1, "hid")

    # 重心
    gx, gy = -70, 900
    side.circle(gx, gy, 55, "cen")
    side.line(gx - 55, gy, gx + 55, gy, "cen")
    side.line(gx, gy - 55, gx, gy + 55, "cen")
    side.text(gx, gy - 3, "G", "txt", size=2.2, weight="bold")

    # 视图名
    svg.text(80, 19, "侧视图（非卸料侧，-Z）", "viewtitle")
    svg.text(80, 23.2, "1:20", "small")

    # 侧视尺寸
    dim_v(svg, 125, side.Y(Y_ANT), 158, "1990", ref1=side.X(1355), ref2=side.X(1355))
    dim_v(svg, 125, side.Y(Y_BOX), 164, "1560", ref1=side.X(1300), ref2=side.X(1300))
    leader(svg, side.X(-700), side.Y(1260), 13, 52, "精料仓顶 1260", anchor="start", size=2.0)
    leader(svg, side.X(600), side.Y(120), 112, 132, "最小离地 120（电池底）", anchor="start", size=2.0)

    dim_h(svg, side.X(-820), side.X(820), 136, "1640", ref1=125, ref2=125)
    dim_h(svg, side.X(-700), side.X(1300), 141, "2000", ref1=125, ref2=125)
    dim_h(svg, side.X(-1355), side.X(1355), 147, "2710", ref1=125, ref2=125)

    # 侧视引出
    leader(svg, side.X(1050), side.Y(1200), 168, 36, "粗料箱 2.0×0.95×1.1", anchor="start", size=2.0)
    leader(svg, side.X(-1000), side.Y(900), 13, 44, "精料仓 0.25 m³", anchor="start", size=2.0)
    leader(svg, side.X(1180), side.Y(1720), 166, 28, "前视相机", anchor="start", size=2.0)

    # 序号
    balloon(svg, 1, side.X(900), side.Y(380), 152, 101)
    balloon(svg, 2, side.X(-200), side.Y(240), 152, 112)
    balloon(svg, 3, side.X(-820), side.Y(240), 20, 112)
    balloon(svg, 4, side.X(300), side.Y(1450), 150, 62)
    balloon(svg, 8, side.X(-1000), side.Y(1100), 18, 88)
    balloon(svg, 10, side.X(900), side.Y(200), 173, 113)
    balloon(svg, 13, side.X(1300), side.Y(440), 168, 103)

    # B-B 剖切线
    svg.line(side.X(GATE_X), 24, side.X(GATE_X), 135, "cen")
    arrow(svg, side.X(GATE_X), 24, "right")
    arrow(svg, side.X(GATE_X), 135, "right")
    svg.text(side.X(GATE_X) + 3, 22, "B", "txt", size=2.6, weight="bold")
    svg.text(side.X(GATE_X) + 3, 139, "B", "txt", size=2.6, weight="bold")

    # ---- 俯视图 ----
    # 轮胎
    for wx in (-AXLE_X, AXLE_X):
        for wz in (-TRACK_Z, TRACK_Z):
            top.rect(wx - WHEEL_R, wz - WHEEL_W / 2, wx + WHEEL_R, wz + WHEEL_W / 2, "thin", fill="#e6ebee", rx=1.5)
    # 底盘/箱体
    top.rect(-1250, -350, 1250, 350, "thin", fill="#eef2f4")
    top.rect(-700, -475, 1300, 475, "vis", fill="#f8fafb")
    top.rect(-660, -435, 1260, 435, "thin", fill="url(#straw)")
    # 链板方向
    for xx in range(-560, 1200, 180):
        top.line(xx, -420, xx, 420, "hid")
    # 侧门与侧带
    top.rect(-610, 475, -130, 535, "hid", fill="#f7e6d2")
    top.rect(-620, BELT_Z0, -120, BELT_Z1, "med", fill="#e3f1ef")
    top.line(-620, BELT_Z0, -620, BELT_Z1, "med")
    top.line(-120, BELT_Z0, -120, BELT_Z1, "med")
    for k in range(8):
        zz = BELT_Z0 + 40 + k * 105
        if zz < BELT_Z1 - 20:
            top.line(-610, zz, -130, zz, "thin")
    top.line(-370, BELT_Z1 - 80, -370, BELT_Z1 - 18, "med")
    arrow(svg, top.X(-370), top.Y(BELT_Z1 - 18), "down")
    # 精料仓
    top.rect(CONC_X0, -CONC_Z, CONC_X1, CONC_Z, "vis", fill="url(#conc)")
    top.rect(-1240, -240, -760, 240, "thin")
    for lx, lz in ((-1260, -260), (-740, -260), (-1000, 260)):
        top.circle(lx, lz, 26, "thin")
    # 绞龙
    top.line(-1000, 0, -820, 420, "med")
    top.line(-820, 420, -820, BELT_Z1, "med")
    top.circle(-820, BELT_Z1, 75, "med", fill="#f7edc9")
    # 电池/电控
    top.rect(-400, -350, 600, 350, "hid")
    top.rect(650, -175, 1150, 175, "hid")
    # 相机
    for cx, cz in ((1200, 0), (-1200, 0), (350, 470), (0, 0)):
        top.rect(cx - 65, cz - 50, cx + 65, cz + 50, "med", fill="#dfe7eb")
    # 保险杠
    for bx in (-1355, 1265):
        top.rect(bx, -500, bx + 90, 500, "thin", fill="#e8edf0")

    svg.text(80, 158, "俯视图", "viewtitle")
    svg.text(80, 162.2, "1:20 · 工作状态（含侧带）", "small")

    dim_v(svg, top.Y(-555), top.Y(1330), 158, "1885", ref1=top.X(1355), ref2=top.X(-370))
    dim_v(svg, top.Y(-555), top.Y(555), 164, "1110", ref1=top.X(1355), ref2=top.X(1355))
    dim_v(svg, top.Y(-475), top.Y(475), 170, "950", ref1=top.X(900), ref2=top.X(900))

    dim_h(svg, top.X(-700), top.X(1300), 271, "2000", ref1=top.Y(475), ref2=top.Y(475))
    dim_h(svg, top.X(-1355), top.X(1355), 276, "2710", ref1=top.Y(500), ref2=top.Y(500))

    # A-A 剖切线
    svg.line(10, top.Y(0), 158, top.Y(0), "cen")
    arrow(svg, 10, top.Y(0), "down")
    arrow(svg, 158, top.Y(0), "down")
    svg.text(14, top.Y(0) - 2, "A", "txt", size=2.6, weight="bold")
    svg.text(150, top.Y(0) - 2, "A", "txt", size=2.6, weight="bold")

    balloon(svg, 7, top.X(-370), top.Y(900), 84, 240)
    balloon(svg, 6, top.X(-370), top.Y(505), 84, 226)
    balloon(svg, 9, top.X(-820), top.Y(BELT_Z1 + 60), 30, 268)
    balloon(svg, 11, top.X(1200), top.Y(0), 166, 186)
    balloon(svg, 12, top.X(1355), top.Y(0), 172, 198)

    # ---- 前视图（+X） ----
    ground(svg, 172, 288, 125)
    for wz in (-TRACK_Z, TRACK_Z):
        front.rect(wz - WHEEL_W / 2, 0, wz + WHEEL_W / 2, 2 * WHEEL_R, "vis", fill="#e6ebee", rx=1.2)
        front.rect(wz - 45, 205, wz + 45, 275, "thin", fill="#dfe7eb")
    front.rect(-350, 300, 350, 460, "med", fill="#eef2f4")
    front.rect(-350, 120, 350, 360, "hid")
    front.rect(-475, 460, 475, 1560, "vis", fill="#f8fafb")
    front.rect(-475, 1490, 475, 1560, "thin")
    # 侧带（斜坡，+Z 在左）
    front.line(475, BELT_Y0, BELT_Z1, BELT_Y1, "med")
    front.line(475, BELT_Y0 + 25, BELT_Z1, BELT_Y1 + 25, "med")
    front.line(475, BELT_Y0 - 25, BELT_Z1, BELT_Y1 - 25, "med")
    front.line(475, BELT_Y0 + 75, BELT_Z1, BELT_Y1 + 75, "thin")
    # 尾端与门
    front.rect(475, GATE_Y0, 535, GATE_Y1, "med", fill="#f7e6d2")
    front.line(535, 600, BELT_Z0, BELT_Y0 + 25, "med")
    # 支腿
    front.line(600, 600, 980, 750, "thin")
    # 料槽内沿（现场）
    front.rect(TROUGH_Z0, 0, 1230, TROUGH_RIM, "phantom")
    front.line(TROUGH_Z0, FEED_Y, 1230, FEED_Y, "phantom")
    # 设备示意
    front.rect(1130, 1650, 1270, 1780, "med", fill="#eef2f4")

    svg.text(250, 19, "前视图（+X，车头方向）", "viewtitle")
    svg.text(250, 23.2, "1:20", "small")

    dim_v(svg, 125, front.Y(Y_ANT), 284, "1990", ref1=front.X(-555), ref2=front.X(-555))
    dim_v(svg, 125, front.Y(950), 180, "950", ref1=front.X(1330), ref2=front.X(1330))
    dim_v(svg, 125, front.Y(630), 174, "630", ref1=front.X(560), ref2=front.X(560))

    dim_h(svg, front.X(475), front.X(1330), 70, "855", ref1=front.Y(630), ref2=front.Y(950), text_above=True)
    dim_h(svg, front.X(-470), front.X(470), 133, "940", ref1=125, ref2=125)
    dim_h(svg, front.X(-555), front.X(555), 140, "1110", ref1=125, ref2=125)
    dim_h(svg, front.X(-555), front.X(1330), 147, "1885", ref1=125, ref2=125)

    leader(svg, front.X(1230), front.Y(700), 200, 109, "槽沿 700", anchor="start", size=2.0)
    leader(svg, front.X(560), front.Y(630), 215, 98, "带尾 630", anchor="start", size=2.0)

    # ---- 参数表 ----
    tx, ty, tw = 292, 27, 118
    rows = [
        ("外形（长×宽×高）", "2710×1110×1990"),
        ("箱体", "2000×950×1100 / 2.09 m³"),
        ("自重 / 满载", "≈650 kg / ≤1200 kg"),
        ("粗料容量", "190–310 kg（容重实测）"),
        ("精料仓", "0.25 m³ / 150–180 kg"),
        ("轴距 / 轮距", "1640 / 940"),
        ("最小离地", "120（电池底）"),
        ("行走", "4×实心胎 440×170"),
        ("车速 / 转弯", "0–0.6 m/s / ≤1.5 m"),
        ("粗料卸料", "链板 0.75 + 侧带 0.37–0.55 kW"),
        ("侧带", "500 宽 × 855 伸出 × 23°"),
        ("精料卸料", "Φ100–150 绞龙 0.37–0.55 kW"),
        ("电池", "48V 5–8 kWh LiFePO4"),
        ("控制 / 防护", "4G+WiFi / IP65"),
    ]
    svg.rect(tx, ty, tw, 6.5 + 5.6 * len(rows), "med", fill="#fbfcfd")
    svg.text(tx + tw / 2, ty + 4.6, "主要技术参数（方案值）", "txt", size=2.5, weight="bold")
    for i, (k, v) in enumerate(rows):
        yy = ty + 10.2 + i * 5.6
        svg.text(tx + 2, yy, k, "txt", size=1.95, anchor="start")
        svg.text(tx + tw - 2, yy, v, "txt", size=1.95, anchor="end")
        if i:
            svg.line(tx, yy - 3.4, tx + tw, yy - 3.4, "thin")

    # ---- 说明 ----
    nx, ny = 292, 126
    svg.text(nx, ny, "技术要求与说明", "txt", size=2.6, weight="bold", anchor="start")
    notes = [
        "1. 本图为方案设计图（非施工图），尺寸单位 mm；未注板厚 3，",
        "   未注焊缝 4 断续焊，焊后校平；结构件 Q235B，饲料接触面",
        "   热镀锌或 304。",
        "2. 外形 2710×1110×1990（含天线）；箱口高 1560；含侧带",
        "   工作总宽 1885。",
        "3. 侧带固定式：仅在料槽连续、槽沿≤700 且沿高一致的通道内",
        "   行驶；转场/过门洞须折叠或快拆侧带（样机建议快拆）。",
        "4. 侧带端越过槽内沿 100，落料高差 250–350；槽沿/槽宽为",
        "   现场条件，实测后冻结。",
        "5. 满载≤1200 kg；轴荷/重心见 FC-03；后轴荷>600 kg 时",
        "   电池后移 150–250 或精料仓前移 100。",
        "6. 安全：急停、前后保险杠、超声/红外、倾角、失联 2 s 停车；",
        "   充电 4 芯触点互锁。",
        "7. 称重：车体 3×500 kg + 精料仓 3×100 kg；每站粗料",
        "   10–15 kg，先粗后精。",
        "8. 5 cm 秸秆松散容重待实测；箱容 2.09 m³，装 190–310 kg。",
        "9. 三维演示见 feed-cart-3d.html；接口尺寸以本图为准。",
        "10. 精料仓锥斗坐入底盘开孔，四周加 40×40 方管补强；三维演示",
        "    未示开孔。",
    ]
    svg.mtext(nx, ny + 5.5, notes, "notetxt", size=1.95, lh=4.35)

    # 卸料路径示意
    fy = 222
    svg.text(292, fy, "卸料路径（每站先粗后精）", "txt", size=2.3, weight="bold", anchor="start")
    boxes = [("链板", 292, 25), ("侧卸门", 324, 25), ("横带", 356, 25), ("料槽", 388, 18)]
    for i, (label, bx, bw) in enumerate(boxes):
        svg.rect(bx, fy + 4, bw, 10, "med", fill="#f4f8f9")
        svg.text(bx + bw / 2, fy + 10.6, label, "txt", size=2.2)
        if i < len(boxes) - 1:
            x1 = bx + bw + 0.8
            x2 = boxes[i + 1][1] - 0.8
            svg.line(x1, fy + 9, x2, fy + 9, "leader")
            arrow(svg, x2, fy + 9, "right")
    svg.text(292, fy + 21, "粗料 10–15 kg → 精料 10–12 kg", "notetxt", size=1.95, anchor="start")
    svg.text(292, fy + 26, "侧带空转 2–3 s 清料；门开度 40–100", "notetxt", size=1.95, anchor="start")

    frame(svg, 1, 4, "远程控制投料车 · 总图", "1:20", "FC-01")
    return svg.render("FC-01 总图")


if __name__ == "__main__":
    files = {"01-general.svg": sheet1()}
    for name, data in files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(data)
        print("wrote", name, len(data))
