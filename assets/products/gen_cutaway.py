# -*- coding: utf-8 -*-
"""Half-section schematic of a tungsten carbide seat ring.
Standard engineering drawing: left half = exterior (filled dark grey with highlight),
right half = section (hatched). Centerline divides. All outlines are exact closed polygons.
"""
import math

# viewBox
VBW, VBH = 980, 500
CX = 360   # center axis x

# seat ring longitudinal section params
TOP_Y = 150
BOT_Y = 370
H     = BOT_Y - TOP_Y
RTOP  = 130
RBOT  = 105
RI    = 50

# outer outline (trapezoid): top edge at y=TOP_Y, bottom edge at y=BOT_Y
# right side: (CX+RTOP, TOP_Y) -> (CX+RBOT, BOT_Y)
# left side:  (CX-RTOP, TOP_Y) -> (CX-RBOT, BOT_Y)
outer = [(CX-RTOP, TOP_Y), (CX+RTOP, TOP_Y), (CX+RBOT, BOT_Y), (CX-RBOT, BOT_Y)]
# inner bore (rectangle)
bore  = [(CX-RI, TOP_Y), (CX+RI, TOP_Y), (CX+RI, BOT_Y), (CX-RI, BOT_Y)]

def path_d(*polys):
    parts = []
    for poly in polys:
        parts.append("M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in poly) + " Z")
    return " ".join(parts)

full_path = path_d(outer, bore)

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VBW} {VBH}" '
       f'width="100%" font-family="Helvetica, Arial, sans-serif">',
       '<title>Carbide Seat Ring - Half Section</title>',
       '<desc>Half-section schematic. Left half = exterior view, right half = section view. Dark grey = cemented carbide. Generic, not to scale.</desc>',
'''<defs>
  <linearGradient id="body" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%"  stop-color="#5A626B"/>
    <stop offset="48%" stop-color="#454C54"/>
    <stop offset="52%" stop-color="#2E343B"/>
    <stop offset="100%" stop-color="#22272D"/>
  </linearGradient>
  <pattern id="cut" x="0" y="0" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="7" height="7" fill="#3A4148"/>
    <line x1="0" y1="0" x2="0" y2="7" stroke="#FFFFFF" stroke-width="1" opacity="0.85"/>
  </pattern>
  <linearGradient id="hilite" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.15"/>
    <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0"/>
    <stop offset="100%" stop-color="#000000" stop-opacity="0.15"/>
  </linearGradient>
  <clipPath id="leftHalf"><rect x="0" y="0" width="''' + str(CX) + f'''" height="{VBH}"/></clipPath>
  <clipPath id="rightHalf"><rect x="''' + str(CX) + f'''" y="0" width="{VBW-CX}" height="{VBH}"/></clipPath>
  <marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#1E293B"/>
  </marker>
</defs>''',
f'<rect x="0" y="0" width="{VBW}" height="{VBH}" rx="14" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>',
f'<text x="40" y="36" font-size="15" font-weight="bold" fill="#1E293B">Tungsten Carbide Seat Ring - Half Section</text>',
f'<text x="40" y="54" font-size="10.5" fill="#64748B">Generic schematic - left = exterior, right = section. Dark grey = cemented carbide (WC).</text>']

# Whole cross-section filled with body gradient (dark grey body)
svg.append(f'<path d="{full_path}" fill-rule="evenodd" fill="url(#body)" stroke="#1E293B" stroke-width="1.6" stroke-linejoin="round"/>')

# Section hatching on right half
svg.append(f'<path d="{full_path}" fill-rule="evenodd" fill="url(#cut)" clip-path="url(#rightHalf)"/>')

# Subtle highlight overlay across whole figure
svg.append(f'<path d="{full_path}" fill-rule="evenodd" fill="url(#hilite)" stroke="none"/>')

# Centerline (axis of rotation) - dash-dot
svg.append(f'<g stroke="#1E293B" stroke-width="0.9" stroke-dasharray="10,3,1.5,3" fill="none">'
           f'<line x1="{CX}" y1="{TOP_Y-15}" x2="{CX}" y2="{BOT_Y+15}"/>'
           '</g>')
svg.append(f'<text x="{CX}" y="{TOP_Y-22}" font-size="9.5" fill="#64748B" text-anchor="middle">Axis</text>')

# Subtle inner-bore shadow line (depth cue)
svg.append(f'<line x1="{CX-RI}" y1="{TOP_Y+4}" x2="{CX-RI}" y2="{BOT_Y-4}" stroke="#000000" stroke-width="2" opacity="0.25"/>')
svg.append(f'<line x1="{CX+RI}" y1="{TOP_Y+4}" x2="{CX+RI}" y2="{BOT_Y-4}" stroke="#000000" stroke-width="2" opacity="0.25"/>')

# Annotations
# Sealing face (top edge, left half)
svg.append(f'<line x1="{CX-RTOP*0.6:.0f}" y1="{TOP_Y}" x2="140" y2="105" stroke="#1E293B" stroke-width="0.9" marker-end="url(#ar)"/>')
svg.append('<line x1="140" y1="105" x2="50" y2="105" stroke="#1E293B" stroke-width="0.9"/>')
svg.append('<text x="42" y="92" font-size="11" font-weight="bold" fill="#1E293B">Sealing face</text>')
svg.append('<text x="42" y="105" font-size="9.5" fill="#64748B">Top face - narrow contact</text>')
svg.append('<text x="42" y="118" font-size="9.5" fill="#64748B">against mating part</text>')

# Tapered outer band (right side, on the slant)
svg.append(f'<line x1="{CX+RBOT+10:.0f}" y1="{BOT_Y-30}" x2="680" y2="190" stroke="#1E293B" stroke-width="0.9" marker-end="url(#ar)"/>')
svg.append('<line x1="680" y1="190" x2="760" y2="190" stroke="#1E293B" stroke-width="0.9"/>')
svg.append('<text x="768" y="182" font-size="11" font-weight="bold" fill="#1E293B">Tapered outer band</text>')
svg.append('<text x="768" y="194" font-size="9.5" fill="#64748B">Larger at top, narrower at bottom</text>')

# Through bore (inner cylinder)
svg.append(f'<line x1="{CX+RI}" y1="{(TOP_Y+BOT_Y)//2}" x2="680" y2="290" stroke="#1E293B" stroke-width="0.9" marker-end="url(#ar)"/>')
svg.append('<line x1="680" y1="290" x2="760" y2="290" stroke="#1E293B" stroke-width="0.9"/>')
svg.append('<text x="768" y="282" font-size="11" font-weight="bold" fill="#1E293B">Through bore</text>')
svg.append('<text x="768" y="294" font-size="9.5" fill="#64748B">Honed media passage</text>')

# Cut face (right half section)
svg.append(f'<line x1="{CX+RBOT-15}" y1="{BOT_Y-20}" x2="170" y2="380" stroke="#1E293B" stroke-width="0.9" marker-end="url(#ar)"/>')
svg.append('<line x1="170" y1="380" x2="80" y2="380" stroke="#1E293B" stroke-width="0.9"/>')
svg.append('<text x="72" y="372" font-size="11" font-weight="bold" fill="#1E293B">Cut face</text>')
svg.append('<text x="72" y="384" font-size="9.5" fill="#64748B">Section view - solid WC</text>')
svg.append('<text x="72" y="396" font-size="9.5" fill="#64748B">dense, homogeneous</text>')

# legend
svg.append('''<g transform="translate(40, 420)">
  <rect x="0" y="0" width="280" height="42" rx="8" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>
  <text x="12" y="16" font-size="10" font-weight="bold" fill="#1E293B">Material key</text>
  <rect x="12" y="22" width="18" height="12" fill="#454C54" stroke="#1E293B" stroke-width="0.8"/>
  <text x="36" y="32" font-size="9.5" fill="#475569">Exterior view - solid WC</text>
  <rect x="160" y="22" width="18" height="12" fill="url(#cut)" stroke="#1E293B" stroke-width="0.8"/>
  <text x="184" y="32" font-size="9.5" fill="#475569">Section - WC material</text>
</g>''')

svg.append(f'<text x="380" y="{VBH-12}" font-size="9" fill="#94A3B8" text-anchor="middle">Generic schematic - not to scale. Form is typical of hard-seat rings; final profile per customer drawing.</text>')

# ============================================================
# Top-right isometric 3D ring preview (ELLIPSE-based, all outlines closed)
# A horizontal ring viewed in isometric: top ellipse ring, bottom ellipse,
# front outer wall band, front bore wall band, one cut quad.
# ============================================================
# -- frame --
svg.append('<rect x="560" y="22" width="180" height="200" rx="10" fill="#FFFFFF" stroke="#E2E8F0" stroke-width="1"/>')
svg.append('<text x="574" y="42" font-size="10" font-weight="bold" fill="#1E293B">3D preview</text>')

# -- geometry --
CX3, CY3 = 650, 120      # top ellipse center
RXI, RYI = 16.0, 9.5      # inner ellipse radii
RXO, RYO = 34.0, 20.0     # outer ellipse radii
DH      = 34.0            # vertical offset to bottom ellipse (height)

# Top face ring band = outer ellipse minus inner ellipse (evenodd)
svg.append(f'<path d="M {CX3-RXO:.0f},{CY3} A {RXO:.1f} {RYO:.1f} 0 1 1 {CX3+RXO:.0f},{CY3} '
           f'A {RXO:.1f} {RYO:.1f} 0 1 1 {CX3-RXO:.0f},{CY3} Z '
           f'M {CX3-RXI:.0f},{CY3} A {RXI:.1f} {RYI:.1f} 0 1 0 {CX3+RXI:.0f},{CY3} '
           f'A {RXI:.1f} {RYI:.1f} 0 1 0 {CX3-RXI:.0f},{CY3} Z" '
           f'fill-rule="evenodd" fill="#4A525A" stroke="#1E293B" stroke-width="1.3"/>')

# Front outer wall band: top outer lower arc -> right edge -> bottom lower arc -> left edge (closed)
svg.append(f'<path d="M {CX3-RXO:.0f},{CY3} A {RXO:.1f} {RYO:.1f} 0 0 0 {CX3+RXO:.0f},{CY3} '
           f'L {CX3+RXO:.0f},{CY3+DH:.0f} '
           f'A {RXO:.1f} {RYO:.1f} 0 0 1 {CX3-RXO:.0f},{CY3+DH:.0f} Z" '
           f'fill="#3F464D" stroke="#1E293B" stroke-width="1.3"/>')

# Front bore wall band: top inner lower arc -> right -> bottom inner lower arc -> left (closed)
svg.append(f'<path d="M {CX3-RXI:.0f},{CY3} A {RXI:.1f} {RYI:.1f} 0 0 0 {CX3+RXI:.0f},{CY3} '
           f'L {CX3+RXI:.0f},{CY3+DH:.0f} '
           f'A {RXI:.1f} {RYI:.1f} 0 0 1 {CX3-RXI:.0f},{CY3+DH:.0f} Z" '
           f'fill="#2A3037" stroke="#1E293B" stroke-width="1.2"/>')

# Bottom outer ellipse silhouette (depth cue, partial arc)
svg.append(f'<path d="M {CX3-RXO:.0f},{CY3+DH:.0f} A {RXO:.1f} {RYO:.1f} 0 0 0 {CX3+RXO:.0f},{CY3+DH:.0f}" '
           f'fill="none" stroke="#1E293B" stroke-width="1"/>')

# Cut quad: a radial plane at front-left, from inner bore to outer wall,
# showing solid material section (hatching)
svg.append(f'<path d="M {CX3-26:.0f},{CY3+15:.0f} L {CX3-11:.0f},{CY3+7:.0f} '
           f'L {CX3-11:.0f},{CY3+DH+7:.0f} L {CX3-26:.0f},{CY3+DH+15:.0f} Z" '
           f'fill="url(#cut)" stroke="#1E293B" stroke-width="1.4" stroke-linejoin="round"/>')

svg.append('</svg>')

with open(r"D:/AI/AI test/全链路AI外贸/独立站/assets/products/cutaway-seat-ring-isometric.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))
print("SVG written,", len(svg), "lines")