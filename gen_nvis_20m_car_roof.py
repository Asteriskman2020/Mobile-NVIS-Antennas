#!/usr/bin/env python3
"""Generate a 3D poster of a low-profile NVIS 20m magnetic loop on a car roof."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch
import numpy as np

DPI = 200
fig = plt.figure(figsize=(42, 28), dpi=DPI, facecolor='#0d1b2a')

# ── colour palette ─────────────────────────────────────────────────────
BG          = '#0d1b2a'
BG_PANEL    = '#1b2838'
PANEL_BG    = '#e8eef5'
TEXT_LIGHT  = '#e0e0e0'
TEXT_DARK   = '#1a1a2e'
CU_MAIN     = '#b5651d'
CU_HI       = '#e8a54a'
CU_COUPLE   = '#a0522d'
CAR_BODY    = '#37474f'
CAR_ROOF    = '#546e7a'
CAR_GLASS   = '#4fc3f780'
ACCENT_RED  = '#c62828'
ACCENT_BLUE = '#1565c0'
ACCENT_GRN  = '#2e7d32'
GOLD        = '#ffd600'
CAP_BLUE    = '#1565c0'

N_pts = 200

# ═════════════════════════════════════════════════════════════════════════
# MAIN 3D VIEW — Car body + antenna (left 60%)
# ═════════════════════════════════════════════════════════════════════════
ax = fig.add_axes([0.01, 0.06, 0.58, 0.82], projection='3d',
                  computed_zorder=False)
ax.set_facecolor('#162236')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.0, 1.0)
ax.set_zlim(-0.3, 1.4)
ax.view_init(elev=25, azim=-52)
ax.set_box_aspect([1.6, 1.0, 0.85])
ax.axis('off')


# ── helper: thick tube ─────────────────────────────────────────────────
def draw_tube(ax, px, py, pz, color, lw=7, hi_color=None, alpha=1.0, zo=5):
    ax.plot(px, py, pz, color=color, linewidth=lw,
            solid_capstyle='round', alpha=alpha, zorder=zo)
    if hi_color:
        ax.plot(px, py, pz, color=hi_color, linewidth=lw * 0.45,
                solid_capstyle='round', alpha=0.35, zorder=zo + 1)


# ── helper: draw a 3D box ──────────────────────────────────────────────
def draw_box(ax, cx, cy, cz, hw, hd, hh, colors, ec='#333', alpha=0.85, zo=12):
    faces = [
        [[cx-hw, cy-hd, cz-hh], [cx+hw, cy-hd, cz-hh],
         [cx+hw, cy+hd, cz-hh], [cx-hw, cy+hd, cz-hh]],
        [[cx-hw, cy-hd, cz+hh], [cx+hw, cy-hd, cz+hh],
         [cx+hw, cy+hd, cz+hh], [cx-hw, cy+hd, cz+hh]],
        [[cx-hw, cy-hd, cz-hh], [cx+hw, cy-hd, cz-hh],
         [cx+hw, cy-hd, cz+hh], [cx-hw, cy-hd, cz+hh]],
        [[cx-hw, cy+hd, cz-hh], [cx+hw, cy+hd, cz-hh],
         [cx+hw, cy+hd, cz+hh], [cx-hw, cy+hd, cz+hh]],
        [[cx-hw, cy-hd, cz-hh], [cx-hw, cy+hd, cz-hh],
         [cx-hw, cy+hd, cz+hh], [cx-hw, cy-hd, cz+hh]],
        [[cx+hw, cy-hd, cz-hh], [cx+hw, cy+hd, cz-hh],
         [cx+hw, cy+hd, cz+hh], [cx+hw, cy-hd, cz+hh]],
    ]
    for face, fc in zip(faces, colors):
        p = Poly3DCollection([face], alpha=alpha, zorder=zo)
        p.set_facecolor(fc)
        p.set_edgecolor(ec)
        p.set_linewidth(1.2)
        ax.add_collection3d(p)


# ═════════════════════════════════════════════════════════════════════════
# CAR BODY — simplified sedan shape
# ═════════════════════════════════════════════════════════════════════════
# The car sits on the XY plane, front facing +X

# ── lower body (box) ───────────────────────────────────────────────────
car_l = 2.4    # half-length (X)
car_w = 0.70   # half-width (Y)
car_h = 0.35   # height of lower body
z_ground = -0.15
z_body = z_ground + car_h

# bottom
body_bot = [[-car_l, -car_w, z_ground], [car_l, -car_w, z_ground],
            [car_l, car_w, z_ground], [-car_l, car_w, z_ground]]
# top (roof base)
body_top = [[-car_l*0.45, -car_w*0.95, z_body], [car_l*0.30, -car_w*0.95, z_body],
            [car_l*0.30, car_w*0.95, z_body], [-car_l*0.45, car_w*0.95, z_body]]

# sides of lower body
body_faces = [
    # left side
    [[-car_l, -car_w, z_ground], [car_l, -car_w, z_ground],
     [car_l, -car_w, z_body], [-car_l, -car_w, z_body]],
    # right side
    [[-car_l, car_w, z_ground], [car_l, car_w, z_ground],
     [car_l, car_w, z_body], [-car_l, car_w, z_body]],
    # front
    [[car_l, -car_w, z_ground], [car_l, car_w, z_ground],
     [car_l, car_w, z_body], [car_l, -car_w, z_body]],
    # rear
    [[-car_l, -car_w, z_ground], [-car_l, car_w, z_ground],
     [-car_l, car_w, z_body], [-car_l, -car_w, z_body]],
    # top
    body_bot,
]

body_colors = ['#455a64', '#37474f', '#4a6572', '#37474f', '#37474f']
for face, fc in zip(body_faces, body_colors):
    p = Poly3DCollection([face], alpha=0.92, zorder=2)
    p.set_facecolor(fc)
    p.set_edgecolor('#263238')
    p.set_linewidth(1.0)
    ax.add_collection3d(p)

# ── cabin / greenhouse ────────────────────────────────────────────────
# pillars from body top to roof
z_roof = z_body + 0.32
# rear roof corners
rx_r = -car_l * 0.40
rx_f = car_l * 0.25
rw = car_w * 0.90

cabin_faces = [
    # roof top
    [[rx_r, -rw, z_roof], [rx_f, -rw, z_roof],
     [rx_f, rw, z_roof], [rx_r, rw, z_roof]],
    # left glass
    [[rx_r, -rw, z_body], [rx_f, -rw, z_body],
     [rx_f, -rw, z_roof], [rx_r, -rw, z_roof]],
    # right glass
    [[rx_r, rw, z_body], [rx_f, rw, z_body],
     [rx_f, rw, z_roof], [rx_r, rw, z_roof]],
    # windshield (front)
    [[rx_f, -rw, z_body], [rx_f, rw, z_body],
     [rx_f, rw, z_roof], [rx_f, -rw, z_roof]],
    # rear glass
    [[rx_r, -rw, z_body], [rx_r, rw, z_body],
     [rx_r, rw, z_roof], [rx_r, -rw, z_roof]],
]

cabin_colors = [CAR_ROOF, CAR_GLASS, CAR_GLASS, CAR_GLASS, CAR_GLASS]
cabin_alphas = [0.95, 0.35, 0.35, 0.35, 0.35]
for face, fc, al in zip(cabin_faces, cabin_colors, cabin_alphas):
    p = Poly3DCollection([face], alpha=al, zorder=3)
    p.set_facecolor(fc)
    p.set_edgecolor('#263238')
    p.set_linewidth(1.5)
    ax.add_collection3d(p)

# ── hood slope (body top to windshield base) ──────────────────────────
hood_face = [
    [rx_f, -car_w*0.95, z_body], [car_l, -car_w, z_ground + 0.22],
    [car_l, car_w, z_ground + 0.22], [rx_f, car_w*0.95, z_body],
]
p = Poly3DCollection([hood_face], alpha=0.92, zorder=2)
p.set_facecolor('#4a6572')
p.set_edgecolor('#263238')
p.set_linewidth(1.0)
ax.add_collection3d(p)

# ── trunk slope ──────────────────────────────────────────────────────
trunk_face = [
    [rx_r, -car_w*0.95, z_body], [-car_l, -car_w, z_ground + 0.25],
    [-car_l, car_w, z_ground + 0.25], [rx_r, car_w*0.95, z_body],
]
p = Poly3DCollection([trunk_face], alpha=0.92, zorder=2)
p.set_facecolor('#4a6572')
p.set_edgecolor('#263238')
p.set_linewidth(1.0)
ax.add_collection3d(p)

# ── wheels (simple discs) ─────────────────────────────────────────────
wheel_r = 0.15
wheel_theta = np.linspace(0, 2 * np.pi, 24)
wheel_positions = [
    (car_l * 0.6, -car_w - 0.01, z_ground + wheel_r * 0.4),
    (car_l * 0.6, car_w + 0.01, z_ground + wheel_r * 0.4),
    (-car_l * 0.6, -car_w - 0.01, z_ground + wheel_r * 0.4),
    (-car_l * 0.6, car_w + 0.01, z_ground + wheel_r * 0.4),
]
for wx, wy, wz in wheel_positions:
    wpts = [[wx + wheel_r * np.cos(t) * 0.3,
             wy,
             wz + wheel_r * np.sin(t)] for t in wheel_theta]
    p = Poly3DCollection([wpts], alpha=0.85, zorder=2)
    p.set_facecolor('#212121')
    p.set_edgecolor('#111')
    p.set_linewidth(1.5)
    ax.add_collection3d(p)

# ── headlights (two small rectangles at front) ───────────────────────
for side in [-1, 1]:
    hl_face = [
        [car_l + 0.01, side * car_w * 0.6, z_ground + 0.18],
        [car_l + 0.01, side * car_w * 0.85, z_ground + 0.18],
        [car_l + 0.01, side * car_w * 0.85, z_ground + 0.28],
        [car_l + 0.01, side * car_w * 0.6, z_ground + 0.28],
    ]
    p = Poly3DCollection([hl_face], alpha=0.9, zorder=3)
    p.set_facecolor('#fff9c4')
    p.set_edgecolor('#f9a825')
    p.set_linewidth(1.0)
    ax.add_collection3d(p)

# ═════════════════════════════════════════════════════════════════════════
# ANTENNA — 80 cm magnetic loop on car roof
# ═════════════════════════════════════════════════════════════════════════
R_loop = 0.40        # 80 cm diameter / 2
z_ant_base = z_roof  # antenna sits on roof
standoff_h = 0.08    # 8 cm standoff (low profile)
z_loop = z_ant_base + standoff_h
gap_angle = 0.08     # gap at top for capacitor

# ── main loop (horizontal, on roof) ──────────────────────────────────
theta_loop = np.linspace(np.pi / 2 + gap_angle,
                         np.pi / 2 + 2 * np.pi - gap_angle, N_pts)
lx = R_loop * np.cos(theta_loop)
ly = R_loop * np.sin(theta_loop)
lz = np.full_like(theta_loop, z_loop)
draw_tube(ax, lx, ly, lz, CU_MAIN, lw=8, hi_color=CU_HI, zo=10)

# ── capacitor box at top of loop gap ─────────────────────────────────
cap_x = 0.0
cap_y = R_loop
cap_z = z_loop
cap_colors = ['#1565c0', '#1976d2', '#1e88e5', '#1565c0', '#0d47a1', '#1976d2']
draw_box(ax, cap_x, cap_y, cap_z, 0.08, 0.05, 0.04, cap_colors,
         ec='#0d47a1', zo=15)

# leads from loop ends to cap
left_a = np.pi / 2 + gap_angle
right_a = np.pi / 2 + 2 * np.pi - gap_angle
for angle, sign in [(left_a, -0.6), (right_a, 0.6)]:
    ex = R_loop * np.cos(angle)
    ey = R_loop * np.sin(angle)
    ax.plot([ex, cap_x + sign * 0.05], [ey, cap_y], [z_loop, cap_z],
            color=CU_MAIN, linewidth=5, solid_capstyle='round', zorder=11)

# cap label
ax.text(cap_x, cap_y + 0.12, cap_z + 0.06,
        'Vacuum Cap\n15-60 pF\n5 kV rated',
        fontsize=12, fontweight='bold', color='#bbdefb', fontfamily='sans-serif',
        ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d47a1', alpha=0.9,
                  edgecolor='#bbdefb', linewidth=1.5))

# ── stepper motor on cap (small cylinder) ────────────────────────────
mot_theta = np.linspace(0, 2 * np.pi, 20)
mot_r = 0.025
for i in range(len(mot_theta) - 1):
    face = [
        [cap_x + mot_r * np.cos(mot_theta[i]),
         cap_y + mot_r * np.sin(mot_theta[i]), cap_z + 0.04],
        [cap_x + mot_r * np.cos(mot_theta[i + 1]),
         cap_y + mot_r * np.sin(mot_theta[i + 1]), cap_z + 0.04],
        [cap_x + mot_r * np.cos(mot_theta[i + 1]),
         cap_y + mot_r * np.sin(mot_theta[i + 1]), cap_z + 0.07],
        [cap_x + mot_r * np.cos(mot_theta[i]),
         cap_y + mot_r * np.sin(mot_theta[i]), cap_z + 0.07],
    ]
    p = Poly3DCollection([face], alpha=0.8, zorder=16)
    p.set_facecolor('#546e7a')
    p.set_edgecolor('#37474f')
    p.set_linewidth(0.5)
    ax.add_collection3d(p)

ax.text(cap_x + 0.12, cap_y + 0.05, cap_z + 0.09, 'Stepper\nMotor',
        fontsize=11, fontweight='bold', color='#b0bec5', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#37474f', alpha=0.9,
                  edgecolor='#78909c', linewidth=1.2))

# ── coupling loop (small, opposite to cap) ───────────────────────────
R_couple = 0.08     # 16 cm diameter / 2
theta_c = np.linspace(0.15, 2 * np.pi - 0.15, N_pts)
cx_c = R_couple * np.cos(theta_c)
cy_c = R_couple * np.sin(theta_c) - R_loop  # bottom of main loop
cz_c = np.full_like(theta_c, z_loop)
draw_tube(ax, cx_c, cy_c, cz_c, CU_COUPLE, lw=5, hi_color='#d2691e', zo=10)

ax.text(R_couple + 0.06, -R_loop, z_loop + 0.05,
        'Feed Loop\n160 mm dia\nRG-213',
        fontsize=12, fontweight='bold', color='#d7ccc8', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#4e342e', alpha=0.9,
                  edgecolor='#8d6e63', linewidth=1.5))

# ── 4 magnetic mount bases (standoffs) ──────────────────────────────
standoff_pos = [
    (R_loop * 0.7, R_loop * 0.7),
    (R_loop * 0.7, -R_loop * 0.7),
    (-R_loop * 0.7, R_loop * 0.7),
    (-R_loop * 0.7, -R_loop * 0.7),
]
for sx, sy in standoff_pos:
    # dark cylinder for mag-mount base
    for i in range(len(mot_theta) - 1):
        face = [
            [sx + 0.03 * np.cos(mot_theta[i]),
             sy + 0.03 * np.sin(mot_theta[i]), z_ant_base],
            [sx + 0.03 * np.cos(mot_theta[i + 1]),
             sy + 0.03 * np.sin(mot_theta[i + 1]), z_ant_base],
            [sx + 0.03 * np.cos(mot_theta[i + 1]),
             sy + 0.03 * np.sin(mot_theta[i + 1]), z_ant_base + 0.02],
            [sx + 0.03 * np.cos(mot_theta[i]),
             sy + 0.03 * np.sin(mot_theta[i]), z_ant_base + 0.02],
        ]
        p = Poly3DCollection([face], alpha=0.9, zorder=8)
        p.set_facecolor('#212121')
        p.set_edgecolor('#111')
        p.set_linewidth(0.4)
        ax.add_collection3d(p)
    # HDPE standoff rod
    ax.plot([sx, sx], [sy, sy], [z_ant_base + 0.02, z_loop],
            color='#eceff1', linewidth=4, solid_capstyle='round', zorder=7)

# standoff label
ax.text(R_loop * 0.7 + 0.12, -R_loop * 0.7, (z_ant_base + z_loop) / 2,
        'HDPE Standoff\n80 mm\non Mag-Mount',
        fontsize=11, fontweight='bold', color='#cfd8dc', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#263238', alpha=0.9,
                  edgecolor='#78909c', linewidth=1.2))

# ── coax from coupling loop down through window ─────────────────────
coax_pts = np.array([
    [0, -R_loop, z_loop],
    [0, -R_loop - 0.05, z_loop - 0.02],
    [0, -car_w * 0.85, z_body + 0.15],
    [0, -car_w * 0.85, z_body],
    [0, -car_w * 0.85, z_body - 0.08],
])
ax.plot(coax_pts[:, 0], coax_pts[:, 1], coax_pts[:, 2],
        color='#222', linewidth=3, linestyle='--', alpha=0.7, zorder=6)
ax.text(0.05, -car_w * 0.85 - 0.08, z_body + 0.08,
        'RG-58 Coax\n(through\nwindow gap)',
        fontsize=10, fontweight='bold', color='#90a4ae', fontfamily='sans-serif',
        ha='left', zorder=20)

# ── dimension arrows ────────────────────────────────────────────────
# loop diameter
dim_z = z_loop + 0.05
ax.plot([-R_loop, R_loop], [0, 0], [dim_z, dim_z],
        color=ACCENT_RED, linewidth=2.5, linestyle='-', zorder=18)
for s in [-1, 1]:
    ax.plot([s * R_loop, s * (R_loop - 0.04)], [0, 0.025], [dim_z, dim_z],
            color=ACCENT_RED, linewidth=2.5, zorder=18)
    ax.plot([s * R_loop, s * (R_loop - 0.04)], [0, -0.025], [dim_z, dim_z],
            color=ACCENT_RED, linewidth=2.5, zorder=18)
ax.text(0, -0.06, dim_z + 0.03, 'D = 0.80 m (31.5")',
        fontsize=16, fontweight='bold', color='#ef9a9a',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1a2e', alpha=0.9,
                  edgecolor=ACCENT_RED, linewidth=1.5))

# profile height arrow
ph_x = R_loop + 0.15
ax.plot([ph_x, ph_x], [0, 0], [z_ant_base, z_loop + 0.04],
        color=ACCENT_GRN, linewidth=2.5, zorder=18)
for dz in [z_ant_base, z_loop + 0.04]:
    ax.plot([ph_x - 0.02, ph_x + 0.02], [0, 0], [dz, dz],
            color=ACCENT_GRN, linewidth=2.5, zorder=18)
ax.text(ph_x + 0.06, 0, (z_ant_base + z_loop) / 2 + 0.02,
        'Profile\n~10 cm',
        fontsize=14, fontweight='bold', color='#a5d6a7',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a1a2e', alpha=0.9,
                  edgecolor=ACCENT_GRN, linewidth=1.5))

# ── NVIS radiation arrows (going up from loop) ──────────────────────
arrow_style = dict(color='#ff8a65', linewidth=2.5, alpha=0.7, zorder=17)
for arr_x, arr_y in [(0, 0), (0.15, 0.1), (-0.15, 0.1),
                      (0.1, -0.12), (-0.1, -0.12)]:
    z_start = z_loop + 0.08
    z_end = z_loop + 0.55
    ax.plot([arr_x, arr_x * 0.3], [arr_y, arr_y * 0.3],
            [z_start, z_end], **arrow_style)
    # arrowhead
    ax.plot([arr_x * 0.3, arr_x * 0.3 - 0.02],
            [arr_y * 0.3, arr_y * 0.3],
            [z_end, z_end - 0.05], color='#ff8a65', linewidth=2, zorder=17)
    ax.plot([arr_x * 0.3, arr_x * 0.3 + 0.02],
            [arr_y * 0.3, arr_y * 0.3],
            [z_end, z_end - 0.05], color='#ff8a65', linewidth=2, zorder=17)

ax.text(0, 0, z_loop + 0.62, 'NVIS\nRadiation\n(70-90\u00b0)',
        fontsize=16, fontweight='bold', color='#ff8a65',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1a2e', alpha=0.9,
                  edgecolor='#ff8a65', linewidth=2))

# ── ionosphere reflection sketch (arc + return arrows) ──────────────
iono_theta = np.linspace(-0.5, 0.5, 40)
iono_x = 1.2 * np.sin(iono_theta)
iono_y = 1.2 * np.cos(iono_theta) * 0.4
iono_z = np.full_like(iono_theta, z_loop + 1.05)
ax.plot(iono_x, iono_y, iono_z, color='#4dd0e1', linewidth=3,
        linestyle=':', alpha=0.6, zorder=16)
ax.text(0, 0, z_loop + 1.12, 'F2 Layer (~250 km)',
        fontsize=13, fontweight='bold', color='#4dd0e1',
        fontfamily='sans-serif', ha='center', zorder=20)

# ── "FRONT" label on car ────────────────────────────────────────────
ax.text(car_l + 0.15, 0, z_ground + 0.15, 'FRONT \u25B6',
        fontsize=14, fontweight='bold', color='#78909c',
        fontfamily='sans-serif', ha='left', zorder=20)

# ── ground grid ──────────────────────────────────────────────────────
grd = np.linspace(-1.5, 1.5, 10)
for g in grd:
    ax.plot([g, g], [-0.9, 0.9], [z_ground - 0.01, z_ground - 0.01],
            color='#263238', linewidth=0.4, alpha=0.3, zorder=1)
    ax.plot([-1.5, 1.5], [g * 0.6, g * 0.6], [z_ground - 0.01, z_ground - 0.01],
            color='#263238', linewidth=0.4, alpha=0.3, zorder=1)


# ═════════════════════════════════════════════════════════════════════════
# PANEL A — Key Specifications (top-right)
# ═════════════════════════════════════════════════════════════════════════
ax_s = fig.add_axes([0.61, 0.54, 0.37, 0.34])
ax_s.set_facecolor('#e3f2fd')
ax_s.set_xlim(0, 10)
ax_s.set_ylim(0, 10)
ax_s.axis('off')
for sp in ax_s.spines.values():
    sp.set_visible(True)
    sp.set_color(ACCENT_BLUE)
    sp.set_linewidth(2.5)

ax_s.text(5, 9.6, 'NVIS 20 m Car-Roof Loop -- Specifications',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TEXT_DARK, fontfamily='sans-serif')

specs = [
    ('Band',            '20 m  (14.000 - 14.350 MHz)'),
    ('Loop Diameter',   '0.80 m (31.5") -- 0.037\u03bb'),
    ('Loop Material',   '22 mm OD copper tube, 1 mm wall'),
    ('Circumference',   '2.51 m (0.12\u03bb)'),
    ('Tuning Capacitor', 'Vacuum variable 15-60 pF, 5 kV'),
    ('Feed Method',     'Faraday coupling loop 160 mm'),
    ('Profile Height',  '~10 cm above roof surface'),
    ('Radiation Res.',  '~0.15 \u03a9'),
    ('Loss Resistance', '~0.08 \u03a9 (22 mm Cu)'),
    ('Efficiency',      '35-50 % (at 14 MHz)'),
    ('ERP @ 100 W',    '35-50 W radiated'),
    ('Bandwidth',       '25-40 kHz (-2:1 SWR)'),
    ('Q Factor',        '300-500'),
    ('Weight',          '~2.5 kg (5.5 lb) total'),
    ('Max Cap Voltage',  '3-5 kV peak @ 100 W'),
    ('Tuning',          'NEMA17 stepper + worm drive'),
]

row_clrs = ['#bbdefb', '#ffffff']
y0 = 8.95
dy = 0.54
for i, (label, value) in enumerate(specs):
    y = y0 - i * dy
    rc = row_clrs[i % 2]
    ax_s.add_patch(FancyBboxPatch((0.1, y - 0.22), 9.8, 0.48,
                   boxstyle="round,pad=0.04", facecolor=rc, alpha=0.7))
    ax_s.text(0.3, y, label, fontsize=13, fontweight='bold', va='center',
              color=TEXT_DARK, fontfamily='sans-serif')
    ax_s.text(9.7, y, value, fontsize=13, va='center', ha='right',
              color=TEXT_DARK, fontfamily='sans-serif')


# ═════════════════════════════════════════════════════════════════════════
# PANEL B — Installation Guide (bottom-right)
# ═════════════════════════════════════════════════════════════════════════
ax_n = fig.add_axes([0.61, 0.06, 0.37, 0.42])
ax_n.set_facecolor('#fff3e0')
ax_n.set_xlim(0, 10)
ax_n.set_ylim(0, 10)
ax_n.axis('off')
for sp in ax_n.spines.values():
    sp.set_visible(True)
    sp.set_color('#ff9800')
    sp.set_linewidth(2.5)

ax_n.text(5, 9.7, 'Installation & Operation Guide',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TEXT_DARK, fontfamily='sans-serif')

notes = [
    ('1.', 'BUILD LOOP',
     'Cut 2.60 m of 22 mm Cu tube. Fill with sand, bend\n'
     'into 80 cm circle. Leave 15 mm gap at top for cap.'),
    ('2.', 'COUPLING LOOP',
     'Bend 55 cm of RG-213 coax into 160 mm circle.\n'
     'Faraday shield: shield both ends, center one end.'),
    ('3.', 'MOUNT STANDOFFS',
     'Attach 4x HDPE rods (80 mm) to NdFeB mag-mount\n'
     'bases. Place on roof in 40 cm square pattern.'),
    ('4.', 'INSTALL ANTENNA',
     'Set loop horizontal on standoffs. Mount vacuum cap\n'
     'at gap. Attach stepper motor for remote tuning.'),
    ('5.', 'ROUTE COAX',
     'Run RG-58 from coupling loop through door/window\n'
     'seal gap to transceiver. Add choke balun at feed.'),
    ('6.', 'TUNE & OPERATE',
     'NanoVNA sweep 13.8-14.5 MHz. Motor-tune cap for\n'
     'target freq. BW ~30 kHz, retune across band.'),
]

row_clrs_n = ['#ffe0b2', '#ffffff']
y0n = 9.0
dyn = 1.35
for i, (num, title, desc) in enumerate(notes):
    y = y0n - i * dyn
    rc = row_clrs_n[i % 2]
    ax_n.add_patch(FancyBboxPatch((0.2, y - 0.55), 9.6, 1.15,
                   boxstyle="round,pad=0.08", facecolor=rc, alpha=0.6))
    ax_n.add_patch(plt.Circle((0.6, y), 0.35, facecolor='#e65100',
                   edgecolor='white', linewidth=2, zorder=10,
                   transform=ax_n.transData))
    ax_n.text(0.6, y, num, fontsize=15, fontweight='bold', color='white',
              ha='center', va='center', fontfamily='sans-serif', zorder=11)
    ax_n.text(1.2, y + 0.25, title, fontsize=15, fontweight='bold',
              va='center', color='#bf360c', fontfamily='sans-serif')
    ax_n.text(1.2, y - 0.25, desc, fontsize=12, va='center',
              color='#333', fontfamily='sans-serif', linespacing=1.3)

# ── BOM summary ──────────────────────────────────────────────────────
ax_n.text(5, 0.45,
          'BOM: 22mm Cu tube $28 + Vacuum cap $95 + NdFeB mounts $25 + '
          'HDPE rods $8 + RG-213 $6 + RG-58 $10 + Stepper kit $18 + '
          'Hardware $12 = ~$202',
          fontsize=11.5, fontweight='bold', ha='center', va='center',
          color='#bf360c', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff8e1',
                    edgecolor='#e65100', linewidth=2, alpha=0.9))

# ── NVIS note ────────────────────────────────────────────────────────
ax_n.text(5, -0.25,
          '\u26a0 20 m NVIS only works when foF2 > 14 MHz '
          '(high solar activity, SFI > 150, daytime). '
          'For reliable NVIS use 40 m / 80 m.',
          fontsize=11, fontweight='bold', ha='center', va='center',
          color='#b71c1c', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.25', facecolor='#ffcdd2',
                    edgecolor='#b71c1c', linewidth=2, alpha=0.95))

# ═════════════════════════════════════════════════════════════════════════
# TITLE BANNER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.01, 0.93), 0.98, 0.06,
    boxstyle="round,pad=0.008", facecolor=ACCENT_BLUE, alpha=0.95,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.968,
         'NVIS 20 m Car-Roof Antenna  --  Low-Profile Magnetic Loop  --  3D Installation View',
         fontsize=38, fontweight='bold', color='#ffffff',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)
fig.text(0.50, 0.940,
         '0.80 m Loop  |  22 mm Copper  |  Vacuum Cap  |  10 cm Profile  |  '
         '35-50% Eff  |  Mag-Mount  |  Motor Tuned',
         fontsize=22, fontweight='bold', color=GOLD,
         ha='center', va='center', fontfamily='sans-serif', zorder=3)

# ═════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.01, 0.002), 0.98, 0.028,
    boxstyle="round,pad=0.005", facecolor=ACCENT_BLUE, alpha=0.85,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.016,
         'NVIS 20m Car-Roof Loop  |  HS0ZNR  |  Generated 2026-02-23',
         fontsize=18, fontweight='bold', color='#e3f2fd',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)

# ═════════════════════════════════════════════════════════════════════════
# SAVE
# ═════════════════════════════════════════════════════════════════════════
out = r'C:\Users\Jakkrit\.local\bin\NVIS_20m_Car_Roof_3D.jpg'
fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor(),
            pil_kwargs={'quality': 95})
plt.close()
print(f'Saved: {out}')
print(f'Size: {42*DPI} x {28*DPI} px = {42}x{28} inches @ {DPI} DPI')
