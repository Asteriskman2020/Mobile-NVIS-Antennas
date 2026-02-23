#!/usr/bin/env python3
"""
Generate a detailed 3D poster: low-profile NVIS 40 m magnetic loop on car roof.
Realistic sedan with curved body, detailed antenna, radiation pattern inset.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

DPI = 200
fig = plt.figure(figsize=(44, 30), dpi=DPI, facecolor='#0a1628')

# ── colour palette ─────────────────────────────────────────────────────
CU_MAIN     = '#b5651d'
CU_HI       = '#e8a54a'
CU_COUPLE   = '#a0522d'
ACCENT_BLUE = '#1565c0'
ACCENT_RED  = '#c62828'
ACCENT_GRN  = '#2e7d32'
GOLD        = '#ffd600'
TEXT_DARK   = '#1a1a2e'

N = 200  # curve resolution

# ═════════════════════════════════════════════════════════════════════════
# MAIN 3D VIEW  (left 58%)
# ═════════════════════════════════════════════════════════════════════════
ax = fig.add_axes([0.01, 0.06, 0.57, 0.82], projection='3d',
                  computed_zorder=False)
ax.set_facecolor('#111d30')
ax.set_xlim(-2.0, 2.0)
ax.set_ylim(-1.2, 1.2)
ax.set_zlim(-0.35, 1.6)
ax.view_init(elev=22, azim=-48)
ax.set_box_aspect([2.0, 1.2, 0.95])
ax.axis('off')


# ── helpers ─────────────────────────────────────────────────────────────
def tube(ax, px, py, pz, c, lw=7, hc=None, a=1.0, zo=5):
    ax.plot(px, py, pz, color=c, linewidth=lw, solid_capstyle='round',
            alpha=a, zorder=zo)
    if hc:
        ax.plot(px, py, pz, color=hc, linewidth=lw * 0.4,
                solid_capstyle='round', alpha=0.35, zorder=zo + 1)


def poly(ax, verts, fc, ec='#222', a=0.92, lw=1.0, zo=2):
    p = Poly3DCollection([verts], alpha=a, zorder=zo)
    p.set_facecolor(fc)
    p.set_edgecolor(ec)
    p.set_linewidth(lw)
    ax.add_collection3d(p)


def box3d(ax, cx, cy, cz, hw, hd, hh, cols, ec='#333', a=0.85, zo=12):
    f = [
        [[cx-hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx-hw,cy+hd,cz-hh]],
        [[cx-hw,cy-hd,cz+hh],[cx+hw,cy-hd,cz+hh],[cx+hw,cy+hd,cz+hh],[cx-hw,cy+hd,cz+hh]],
        [[cx-hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz+hh],[cx-hw,cy-hd,cz+hh]],
        [[cx-hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz+hh],[cx-hw,cy+hd,cz+hh]],
        [[cx-hw,cy-hd,cz-hh],[cx-hw,cy+hd,cz-hh],[cx-hw,cy+hd,cz+hh],[cx-hw,cy-hd,cz+hh]],
        [[cx+hw,cy-hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz+hh],[cx+hw,cy-hd,cz+hh]],
    ]
    for face, fc_ in zip(f, cols):
        poly(ax, face, fc_, ec=ec, a=a, zo=zo)


# ═════════════════════════════════════════════════════════════════════════
# CAR — realistic sedan built from profiled cross-sections
# ═════════════════════════════════════════════════════════════════════════
# Car: front = +X,  length ~4.6m scale → ±2.3 on X
z_g = -0.18  # ground level

# --- body profile: list of (x, half_width, z_bottom, z_beltline) ---
# Creates a smooth sedan shape via lofted cross-sections
body_xs = np.array([-2.2, -2.0, -1.6, -1.0, -0.4, 0.0, 0.4, 0.8,
                     1.2, 1.6, 2.0, 2.2, 2.35])
body_ws = np.array([0.40, 0.72, 0.78, 0.80, 0.80, 0.80, 0.80, 0.80,
                     0.78, 0.74, 0.66, 0.50, 0.30])
body_zbot = np.full_like(body_xs, z_g)
body_ztop = np.array([z_g+0.20, z_g+0.38, z_g+0.44, z_g+0.46, z_g+0.46,
                       z_g+0.46, z_g+0.46, z_g+0.46, z_g+0.44,
                       z_g+0.42, z_g+0.36, z_g+0.28, z_g+0.20])

# glass / cabin profile  (narrower, starts at B-pillar region)
cab_xs = np.array([-1.4, -1.0, -0.5, 0.0, 0.5, 0.9, 1.2])
cab_ws = np.array([0.68, 0.74, 0.76, 0.76, 0.76, 0.72, 0.65])
cab_ztop = np.array([z_g+0.44, z_g+0.72, z_g+0.78, z_g+0.80,
                      z_g+0.78, z_g+0.72, z_g+0.60])

# ── lower body panels (left side, right side, top, bottom) ───────────
car_dark   = '#2d3a45'
car_mid    = '#3a4d5c'
car_light  = '#4a6272'
car_accent = '#546e7a'

# -- left body side (outer, facing viewer typically) --
for i in range(len(body_xs) - 1):
    x0, x1 = body_xs[i], body_xs[i + 1]
    w0, w1 = body_ws[i], body_ws[i + 1]
    zb0, zb1 = body_zbot[i], body_zbot[i + 1]
    zt0, zt1 = body_ztop[i], body_ztop[i + 1]
    # left side face
    poly(ax, [[x0, -w0, zb0], [x1, -w1, zb1], [x1, -w1, zt1], [x0, -w0, zt0]],
         car_mid, ec='#1e2d38', zo=2)
    # right side face
    poly(ax, [[x0, w0, zb0], [x1, w1, zb1], [x1, w1, zt1], [x0, w0, zt0]],
         car_dark, ec='#1e2d38', zo=2)
    # top panel (hood/roof/trunk base)
    poly(ax, [[x0, -w0, zt0], [x1, -w1, zt1], [x1, w1, zt1], [x0, w0, zt0]],
         car_light, ec='#1e2d38', zo=2)
    # bottom panel
    poly(ax, [[x0, -w0, zb0], [x1, -w1, zb1], [x1, w1, zb1], [x0, w0, zb0]],
         '#1a2530', ec='#111', zo=1)

# front face
x_f = body_xs[-1]
w_f = body_ws[-1]
zt_f = body_ztop[-1]
poly(ax, [[x_f, -w_f, z_g], [x_f, w_f, z_g],
          [x_f, w_f, zt_f], [x_f, -w_f, zt_f]],
     '#3d5060', ec='#1e2d38', zo=2)

# rear face
x_r = body_xs[0]
w_r = body_ws[0]
zt_r = body_ztop[0]
poly(ax, [[x_r, -w_r, z_g], [x_r, w_r, z_g],
          [x_r, w_r, zt_r], [x_r, -w_r, zt_r]],
     '#2a3842', ec='#1e2d38', zo=2)

# ── cabin / greenhouse ────────────────────────────────────────────────
glass_c   = '#5bc0de'
glass_a   = 0.30
pillar_c  = '#1e2d38'
roof_c    = '#4a6272'

# cabin side panels (glass + pillars)
for i in range(len(cab_xs) - 1):
    x0, x1 = cab_xs[i], cab_xs[i + 1]
    w0, w1 = cab_ws[i], cab_ws[i + 1]
    # find body beltline z at these x positions
    zb0 = np.interp(x0, body_xs, body_ztop)
    zb1 = np.interp(x1, body_xs, body_ztop)
    zt0, zt1 = cab_ztop[i], cab_ztop[i + 1]
    # left glass
    poly(ax, [[x0, -w0, zb0], [x1, -w1, zb1], [x1, -w1, zt1], [x0, -w0, zt0]],
         glass_c, ec='#1e2d38', a=glass_a, lw=1.5, zo=3)
    # right glass
    poly(ax, [[x0, w0, zb0], [x1, w1, zb1], [x1, w1, zt1], [x0, w0, zt0]],
         glass_c, ec='#1e2d38', a=glass_a, lw=1.5, zo=3)
    # roof panel
    poly(ax, [[x0, -w0, zt0], [x1, -w1, zt1], [x1, w1, zt1], [x0, w0, zt0]],
         roof_c, ec='#1e2d38', a=0.95, lw=1.0, zo=4)

# windshield (front glass)
x_wf = cab_xs[-1]
w_wf = cab_ws[-1]
zb_wf = np.interp(x_wf, body_xs, body_ztop)
zt_wf = cab_ztop[-1]
# windshield slopes forward: top edge is further back than bottom
poly(ax, [[x_wf, -w_wf, zb_wf], [x_wf, w_wf, zb_wf],
          [x_wf - 0.15, w_wf * 0.95, zt_wf],
          [x_wf - 0.15, -w_wf * 0.95, zt_wf]],
     glass_c, ec='#1e2d38', a=0.35, lw=2, zo=3)

# rear glass
x_rg = cab_xs[0]
w_rg = cab_ws[0]
zb_rg = np.interp(x_rg, body_xs, body_ztop)
zt_rg = cab_ztop[0]
poly(ax, [[x_rg, -w_rg, zb_rg], [x_rg, w_rg, zb_rg],
          [x_rg + 0.1, w_rg * 0.95, zt_rg],
          [x_rg + 0.1, -w_rg * 0.95, zt_rg]],
     glass_c, ec='#1e2d38', a=0.35, lw=2, zo=3)

# ── A-pillars, B-pillars, C-pillars (dark bars) ─────────────────────
pillar_w = 0.06
pillar_positions = [
    (cab_xs[-1], cab_ws[-1]),     # A-pillar (front)
    (cab_xs[2], cab_ws[2]),       # B-pillar (mid)
    (cab_xs[0], cab_ws[0]),       # C-pillar (rear)
]
for px_p, pw_p in pillar_positions:
    zb_p = np.interp(px_p, body_xs, body_ztop)
    zt_p = np.interp(px_p, cab_xs, cab_ztop)
    for side in [-1, 1]:
        poly(ax,
             [[px_p - pillar_w, side * pw_p, zb_p],
              [px_p + pillar_w, side * pw_p, zb_p],
              [px_p + pillar_w, side * pw_p, zt_p],
              [px_p - pillar_w, side * pw_p, zt_p]],
             pillar_c, ec='#111', a=0.9, lw=1.5, zo=4)

# ── door panel lines (subtle grooves on body sides) ──────────────────
door_x_positions = [-0.2, 0.8]  # two doors (front door gap, rear door gap)
for dx in door_x_positions:
    zb_d = z_g + 0.02
    zt_d = np.interp(dx, body_xs, body_ztop) - 0.02
    w_d = np.interp(dx, body_xs, body_ws)
    # left side door line
    ax.plot([dx, dx], [-w_d - 0.005, -w_d - 0.005], [zb_d, zt_d],
            color='#1a2530', linewidth=2, zorder=3)
    # right side door line
    ax.plot([dx, dx], [w_d + 0.005, w_d + 0.005], [zb_d, zt_d],
            color='#1a2530', linewidth=2, zorder=3)

# ── door handles ─────────────────────────────────────────────────────
handle_positions = [(-0.55, 'left'), (0.45, 'left'),
                    (-0.55, 'right'), (0.45, 'right')]
for hx, hside in handle_positions:
    hw = np.interp(hx, body_xs, body_ws)
    hz = np.interp(hx, body_xs, body_ztop) - 0.08
    hy = -hw - 0.008 if hside == 'left' else hw + 0.008
    ax.plot([hx - 0.06, hx + 0.06], [hy, hy], [hz, hz],
            color='#90a4ae', linewidth=3, solid_capstyle='round', zorder=4)

# ── side mirrors ─────────────────────────────────────────────────────
for side in [-1, 1]:
    mx = cab_xs[-1] - 0.05
    mw = np.interp(mx, body_xs, body_ws)
    my = side * (mw + 0.12)
    mz = np.interp(mx, body_xs, body_ztop) + 0.04
    # mirror arm
    ax.plot([mx, mx], [side * mw, my], [mz, mz],
            color='#2d3a45', linewidth=3, solid_capstyle='round', zorder=4)
    # mirror housing (small box)
    mirror_face = [
        [mx - 0.04, my, mz - 0.03],
        [mx + 0.04, my, mz - 0.03],
        [mx + 0.04, my, mz + 0.03],
        [mx - 0.04, my, mz + 0.03],
    ]
    poly(ax, mirror_face, '#2d3a45', ec='#1a2530', a=0.9, zo=4)

# ── headlights ───────────────────────────────────────────────────────
for side in [-1, 1]:
    hl_x = body_xs[-1] + 0.01
    hl_w = body_ws[-1]
    hl_w2 = np.interp(body_xs[-2], body_xs, body_ws)
    hl_y_inner = side * hl_w * 0.3
    hl_y_outer = side * hl_w2 * 0.95
    hl_zb = z_g + 0.16
    hl_zt = z_g + 0.28
    poly(ax,
         [[hl_x, hl_y_inner, hl_zb], [hl_x, hl_y_outer, hl_zb],
          [hl_x, hl_y_outer, hl_zt], [hl_x, hl_y_inner, hl_zt]],
         '#fff9c4', ec='#fdd835', a=0.85, lw=1.5, zo=3)

# ── taillights ───────────────────────────────────────────────────────
for side in [-1, 1]:
    tl_x = body_xs[0] - 0.01
    tl_w = body_ws[0]
    tl_w2 = np.interp(body_xs[1], body_xs, body_ws)
    poly(ax,
         [[tl_x, side * tl_w * 0.3, z_g + 0.08],
          [tl_x, side * tl_w2 * 0.9, z_g + 0.08],
          [tl_x, side * tl_w2 * 0.9, z_g + 0.20],
          [tl_x, side * tl_w * 0.3, z_g + 0.20]],
         '#d32f2f', ec='#b71c1c', a=0.85, lw=1.5, zo=3)

# ── front grille ─────────────────────────────────────────────────────
gx = body_xs[-1] + 0.015
gw = body_ws[-1] * 0.7
gzb = z_g + 0.03
gzt = z_g + 0.16
poly(ax, [[gx, -gw, gzb], [gx, gw, gzb],
          [gx, gw, gzt], [gx, -gw, gzt]],
     '#1a2530', ec='#263238', a=0.9, zo=3)
# grille bars
for gz_bar in np.linspace(gzb + 0.02, gzt - 0.02, 4):
    ax.plot([gx + 0.005, gx + 0.005], [-gw * 0.9, gw * 0.9],
            [gz_bar, gz_bar], color='#78909c', linewidth=1.5, zorder=4)

# ── license plate (rear) ────────────────────────────────────────────
lp_x = body_xs[0] - 0.015
poly(ax, [[lp_x, -0.12, z_g + 0.06], [lp_x, 0.12, z_g + 0.06],
          [lp_x, 0.12, z_g + 0.14], [lp_x, -0.12, z_g + 0.14]],
     '#f5f5f5', ec='#333', a=0.9, zo=3)

# ── wheels with rims ────────────────────────────────────────────────
wt = np.linspace(0, 2 * np.pi, 32)
wheel_r = 0.17
rim_r = 0.10
wheel_locs = [
    (1.55, -0.80, z_g + 0.01),
    (1.55,  0.80, z_g + 0.01),
    (-1.45, -0.80, z_g + 0.01),
    (-1.45,  0.80, z_g + 0.01),
]
for wx, wy, wz in wheel_locs:
    # tyre
    tyre_pts = [[wx + wheel_r * np.cos(t) * 0.35, wy, wz + wheel_r * np.sin(t)]
                for t in wt]
    poly(ax, tyre_pts, '#1a1a1a', ec='#111', a=0.9, zo=3)
    # rim
    rim_pts = [[wx + rim_r * np.cos(t) * 0.35, wy, wz + rim_r * np.sin(t)]
               for t in wt]
    poly(ax, rim_pts, '#b0bec5', ec='#78909c', a=0.85, zo=4)
    # wheel arch shadow (subtle arc above wheel)
    arch_t = np.linspace(-0.3, np.pi + 0.3, 30)
    arch_x = wx + (wheel_r + 0.03) * np.cos(arch_t) * 0.35
    arch_y = np.full(30, wy)
    arch_z = wz + (wheel_r + 0.03) * np.sin(arch_t)
    ax.plot(arch_x, arch_y, arch_z, color='#1a2530', linewidth=3, zorder=3)

# ── bumpers ──────────────────────────────────────────────────────────
# front bumper
fb_x = body_xs[-1] + 0.02
fb_w = body_ws[-2] * 0.92
poly(ax, [[fb_x, -fb_w, z_g], [fb_x, fb_w, z_g],
          [fb_x, fb_w, z_g + 0.08], [fb_x, -fb_w, z_g + 0.08]],
     '#263238', ec='#1a2530', a=0.9, zo=3)
# rear bumper
rb_x = body_xs[0] - 0.02
rb_w = body_ws[1] * 0.85
poly(ax, [[rb_x, -rb_w, z_g], [rb_x, rb_w, z_g],
          [rb_x, rb_w, z_g + 0.08], [rb_x, -rb_w, z_g + 0.08]],
     '#263238', ec='#1a2530', a=0.9, zo=3)

# ── roof rails (subtle lines on roof edges) ──────────────────────────
for side in [-1, 1]:
    rail_xs = np.linspace(cab_xs[0] + 0.1, cab_xs[-1] - 0.1, 30)
    rail_ys = np.array([side * np.interp(x, cab_xs, cab_ws) for x in rail_xs])
    rail_zs = np.array([np.interp(x, cab_xs, cab_ztop) + 0.005 for x in rail_xs])
    ax.plot(rail_xs, rail_ys, rail_zs, color='#78909c', linewidth=2.5,
            solid_capstyle='round', zorder=5)

# ═════════════════════════════════════════════════════════════════════════
# ANTENNA — 1.0 m magnetic loop for 40 m, horizontal on roof
# ═════════════════════════════════════════════════════════════════════════
R_loop = 0.50       # 1.0 m diameter / 2
z_roof_mid = np.interp(0, cab_xs, cab_ztop) + 0.005   # middle of roof
standoff_h = 0.10   # 10 cm standoff
z_loop = z_roof_mid + standoff_h
gap_angle = 0.07

# ── main loop ────────────────────────────────────────────────────────
theta_l = np.linspace(np.pi / 2 + gap_angle,
                      np.pi / 2 + 2 * np.pi - gap_angle, N)
lx = R_loop * np.cos(theta_l)
ly = R_loop * np.sin(theta_l)
lz = np.full(N, z_loop)
tube(ax, lx, ly, lz, CU_MAIN, lw=9, hc=CU_HI, zo=10)

# ── capacitor enclosure at loop gap ──────────────────────────────────
cap_x, cap_y, cap_z = 0.0, R_loop, z_loop
cap_cols = ['#1565c0','#1976d2','#1e88e5','#1565c0','#0d47a1','#1976d2']
box3d(ax, cap_x, cap_y, cap_z, 0.10, 0.06, 0.05, cap_cols, ec='#0d47a1', zo=15)

# leads from loop ends to cap
for angle, sx in [(np.pi/2 + gap_angle, -0.7), (np.pi/2 + 2*np.pi - gap_angle, 0.7)]:
    ex, ey = R_loop * np.cos(angle), R_loop * np.sin(angle)
    ax.plot([ex, cap_x + sx * 0.06], [ey, cap_y], [z_loop, cap_z],
            color=CU_MAIN, linewidth=6, solid_capstyle='round', zorder=11)

# cap label + arrow line
ax.plot([cap_x, cap_x + 0.25], [cap_y + 0.06, cap_y + 0.25],
        [cap_z + 0.05, cap_z + 0.20],
        color='#90caf9', linewidth=1.5, linestyle='-', zorder=19)
ax.text(cap_x + 0.27, cap_y + 0.27, cap_z + 0.22,
        'Vacuum Variable Cap\n30-220 pF  |  7.5 kV\n+ Stepper Motor Tuning',
        fontsize=11, fontweight='bold', color='#bbdefb', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d47a1', alpha=0.92,
                  edgecolor='#64b5f6', linewidth=1.5))

# stepper motor cylinder on cap
mot_t = np.linspace(0, 2 * np.pi, 20)
mot_r = 0.028
for i in range(len(mot_t) - 1):
    face = [
        [cap_x + mot_r*np.cos(mot_t[i]),   cap_y + mot_r*np.sin(mot_t[i]),   cap_z + 0.05],
        [cap_x + mot_r*np.cos(mot_t[i+1]), cap_y + mot_r*np.sin(mot_t[i+1]), cap_z + 0.05],
        [cap_x + mot_r*np.cos(mot_t[i+1]), cap_y + mot_r*np.sin(mot_t[i+1]), cap_z + 0.09],
        [cap_x + mot_r*np.cos(mot_t[i]),   cap_y + mot_r*np.sin(mot_t[i]),   cap_z + 0.09],
    ]
    poly(ax, face, '#455a64', ec='#37474f', a=0.85, lw=0.5, zo=16)

# ── weatherproof cap cover (polycarbonate dome outline) ──────────────
dome_t = np.linspace(0, 2 * np.pi, 40)
dome_r = 0.12
dome_x = cap_x + dome_r * np.cos(dome_t)
dome_y = cap_y + dome_r * np.sin(dome_t) * 0.7
dome_z = np.full(40, cap_z + 0.06)
ax.plot(dome_x, dome_y, dome_z, color='#80cbc4', linewidth=1.5,
        linestyle='--', alpha=0.5, zorder=14)

# ── coupling loop (bottom of main loop) ──────────────────────────────
R_couple = 0.10     # 200 mm diameter / 2 (larger for 40m matching)
theta_c = np.linspace(0.12, 2 * np.pi - 0.12, N)
cx_c = R_couple * np.cos(theta_c)
cy_c = R_couple * np.sin(theta_c) - R_loop
cz_c = np.full(N, z_loop)
tube(ax, cx_c, cy_c, cz_c, CU_COUPLE, lw=5, hc='#d2691e', zo=10)

# feed loop label
ax.plot([R_couple * 0.7, R_couple + 0.20], [-R_loop, -R_loop - 0.15],
        [z_loop, z_loop + 0.12], color='#bcaaa4', linewidth=1.5, zorder=19)
ax.text(R_couple + 0.22, -R_loop - 0.17, z_loop + 0.14,
        'Faraday Feed Loop\n200 mm dia | RG-213\nShield both ends',
        fontsize=11, fontweight='bold', color='#d7ccc8', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#3e2723', alpha=0.92,
                  edgecolor='#8d6e63', linewidth=1.5))

# ── SO-239 connector at feed loop gap ────────────────────────────────
so_x, so_y, so_z = 0, -R_loop - R_couple, z_loop
# small silver hex
hex_t = np.linspace(0, 2 * np.pi, 7)
hex_pts = [[so_x + 0.018 * np.cos(t), so_y + 0.018 * np.sin(t), so_z]
           for t in hex_t]
poly(ax, hex_pts, '#b0bec5', ec='#78909c', a=0.9, zo=12)
ax.text(so_x - 0.08, so_y - 0.04, so_z - 0.03, 'SO-239',
        fontsize=9, fontweight='bold', color='#90a4ae', fontfamily='sans-serif',
        ha='center', zorder=20)

# ── 4 standoff posts on mag-mount bases ──────────────────────────────
standoff_pos = [
    ( R_loop * 0.65,  R_loop * 0.65),
    ( R_loop * 0.65, -R_loop * 0.65),
    (-R_loop * 0.65,  R_loop * 0.65),
    (-R_loop * 0.65, -R_loop * 0.65),
]
for sx, sy in standoff_pos:
    z_roof_at = np.interp(sx, cab_xs, cab_ztop) + 0.005
    # mag mount base (dark disc)
    base_pts = [[sx + 0.04 * np.cos(t), sy + 0.04 * np.sin(t), z_roof_at]
                for t in np.linspace(0, 2 * np.pi, 20)]
    poly(ax, base_pts, '#212121', ec='#111', a=0.9, zo=8)
    # rubber pad ring
    ring_pts = [[sx + 0.035 * np.cos(t), sy + 0.035 * np.sin(t), z_roof_at + 0.005]
                for t in np.linspace(0, 2 * np.pi, 20)]
    poly(ax, ring_pts, '#37474f', ec='#263238', a=0.8, zo=9)
    # HDPE standoff rod (white)
    ax.plot([sx, sx], [sy, sy], [z_roof_at + 0.01, z_loop],
            color='#eceff1', linewidth=5, solid_capstyle='round', zorder=8)
    # top clip (small disc)
    clip_pts = [[sx + 0.025 * np.cos(t), sy + 0.025 * np.sin(t), z_loop]
                for t in np.linspace(0, 2 * np.pi, 16)]
    poly(ax, clip_pts, '#e0e0e0', ec='#bdbdbd', a=0.9, zo=11)

# standoff label
ax.plot([R_loop*0.65 + 0.04, R_loop*0.65 + 0.28],
        [-R_loop*0.65, -R_loop*0.65 - 0.18],
        [z_loop * 0.5 + z_roof_mid * 0.5, z_loop * 0.5 + z_roof_mid * 0.5 - 0.06],
        color='#b0bec5', linewidth=1.5, zorder=19)
ax.text(R_loop*0.65 + 0.30, -R_loop*0.65 - 0.20,
        z_loop * 0.5 + z_roof_mid * 0.5 - 0.08,
        'HDPE Post 100 mm\nNdFeB Mag-Mount\nNo drill install',
        fontsize=10.5, fontweight='bold', color='#cfd8dc', fontfamily='sans-serif',
        ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.22', facecolor='#1a2530', alpha=0.92,
                  edgecolor='#78909c', linewidth=1.2))

# ── coax routing down to transceiver ─────────────────────────────────
coax_path = np.array([
    [0, -R_loop - R_couple, z_loop],
    [0.05, -R_loop - R_couple - 0.05, z_loop - 0.02],
    [0.10, -(np.interp(0.1, cab_xs, cab_ws) + 0.02), z_roof_mid - 0.05],
    [0.15, -(np.interp(0.1, body_xs, body_ws) + 0.01), z_g + 0.40],
    [0.15, -(np.interp(0.1, body_xs, body_ws) + 0.01), z_g + 0.25],
])
ax.plot(coax_path[:, 0], coax_path[:, 1], coax_path[:, 2],
        color='#222', linewidth=3.5, linestyle='--', alpha=0.7, zorder=6)
ax.text(0.22, coax_path[3, 1] - 0.06, z_g + 0.32,
        'RG-58 Coax\nthrough\nwindow seal',
        fontsize=10, fontweight='bold', color='#78909c', fontfamily='sans-serif',
        ha='left', zorder=20)

# ── choke balun (small toroid near window entry) ─────────────────────
balun_t = np.linspace(0, 2 * np.pi, 30)
bx = 0.12
by = coax_path[2, 1]
bz = z_roof_mid - 0.02
br = 0.025
balun_x = bx + br * np.cos(balun_t) * 0.3
balun_y = by + br * np.cos(balun_t) * 0.3
balun_z = bz + br * np.sin(balun_t)
ax.plot(balun_x, balun_y, balun_z, color='#5d4037', linewidth=4, zorder=7)
ax.text(bx + 0.06, by, bz, 'Choke\nBalun', fontsize=9, color='#8d6e63',
        fontweight='bold', fontfamily='sans-serif', zorder=20)

# ═════════════════════════════════════════════════════════════════════════
# NVIS RADIATION PATTERN  —  arrows + ionosphere
# ═════════════════════════════════════════════════════════════════════════
arrow_c = '#ff8a65'
# multiple upward arrows from loop
for arr_x, arr_y, spread in [
    (0, 0, 0.0), (0.18, 0.12, 0.06), (-0.18, 0.12, 0.06),
    (0.12, -0.15, 0.05), (-0.12, -0.15, 0.05),
    (0.25, 0, 0.08), (-0.25, 0, 0.08),
]:
    z0 = z_loop + 0.10
    z1 = z_loop + 0.65
    ax.plot([arr_x, arr_x * 0.15 + spread * 0.1],
            [arr_y, arr_y * 0.15],
            [z0, z1], color=arrow_c, linewidth=2.2, alpha=0.65, zorder=17)
    # arrowhead
    ax.plot([arr_x * 0.15 + spread * 0.1, arr_x * 0.15 + spread * 0.1 - 0.015],
            [arr_y * 0.15, arr_y * 0.15],
            [z1, z1 - 0.04], color=arrow_c, linewidth=2, alpha=0.65, zorder=17)
    ax.plot([arr_x * 0.15 + spread * 0.1, arr_x * 0.15 + spread * 0.1 + 0.015],
            [arr_y * 0.15, arr_y * 0.15],
            [z1, z1 - 0.04], color=arrow_c, linewidth=2, alpha=0.65, zorder=17)

# NVIS label
ax.text(0, 0, z_loop + 0.73,
        'NVIS Radiation\n70\u00b0 \u2013 90\u00b0 Elevation',
        fontsize=15, fontweight='bold', color='#ff8a65',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a1628', alpha=0.92,
                  edgecolor='#ff8a65', linewidth=2))

# ionosphere arc
iono_t = np.linspace(-0.6, 0.6, 60)
iono_x = 1.4 * np.sin(iono_t)
iono_y = 0.8 * np.cos(iono_t) * 0.3
iono_z = np.full(60, z_loop + 1.20)
ax.plot(iono_x, iono_y, iono_z, color='#4dd0e1', linewidth=3.5,
        linestyle=':', alpha=0.55, zorder=16)
# secondary ionosphere layer
ax.plot(iono_x * 0.85, iono_y * 0.85, iono_z + 0.08, color='#80deea',
        linewidth=2, linestyle=':', alpha=0.35, zorder=16)

ax.text(0, 0, z_loop + 1.32,
        'F2 Layer  ~250 km  |  foF2 > 7 MHz (reliable)',
        fontsize=12, fontweight='bold', color='#4dd0e1',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a1628', alpha=0.85,
                  edgecolor='#4dd0e1', linewidth=1.2))

# reflected return arrows (coming back down at edges)
for rx, ry in [(0.8, 0.3), (-0.8, 0.3), (0.6, -0.4), (-0.6, -0.4)]:
    ax.plot([rx * 0.3, rx], [ry * 0.3, ry],
            [z_loop + 1.15, z_loop + 0.35],
            color='#26c6da', linewidth=1.8, linestyle='--', alpha=0.4, zorder=16)
    # small arrowhead at bottom
    ax.plot([rx, rx - 0.02 * np.sign(rx)], [ry, ry],
            [z_loop + 0.35, z_loop + 0.42],
            color='#26c6da', linewidth=1.8, alpha=0.4, zorder=16)

# ── dimension arrows ────────────────────────────────────────────────
# loop diameter
dz = z_loop + 0.06
ax.plot([-R_loop, R_loop], [0, 0], [dz, dz],
        color=ACCENT_RED, linewidth=2.5, zorder=18)
for s in [-1, 1]:
    ax.plot([s*R_loop, s*(R_loop-0.04)], [0, 0.03], [dz, dz],
            color=ACCENT_RED, linewidth=2.5, zorder=18)
    ax.plot([s*R_loop, s*(R_loop-0.04)], [0, -0.03], [dz, dz],
            color=ACCENT_RED, linewidth=2.5, zorder=18)
ax.text(0, -0.08, dz + 0.03, 'D = 1.00 m (39.4")',
        fontsize=15, fontweight='bold', color='#ef9a9a',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a1628', alpha=0.9,
                  edgecolor=ACCENT_RED, linewidth=1.5))

# profile height
ph_x = R_loop + 0.18
z_roof_at_0 = np.interp(0, cab_xs, cab_ztop) + 0.005
ax.plot([ph_x, ph_x], [0, 0], [z_roof_at_0, z_loop + 0.05],
        color=ACCENT_GRN, linewidth=2.5, zorder=18)
for dz_ in [z_roof_at_0, z_loop + 0.05]:
    ax.plot([ph_x - 0.025, ph_x + 0.025], [0, 0], [dz_, dz_],
            color=ACCENT_GRN, linewidth=2.5, zorder=18)
ax.text(ph_x + 0.06, 0, (z_roof_at_0 + z_loop) / 2 + 0.02,
        'Profile\n~10 cm',
        fontsize=13, fontweight='bold', color='#a5d6a7',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a1628', alpha=0.9,
                  edgecolor=ACCENT_GRN, linewidth=1.5))

# FRONT label
ax.text(2.55, 0, z_g + 0.18, 'FRONT \u25B6',
        fontsize=14, fontweight='bold', color='#607d8b',
        fontfamily='sans-serif', ha='left', zorder=20)

# ── ground / road surface ───────────────────────────────────────────
for g in np.linspace(-1.8, 1.8, 12):
    ax.plot([g, g], [-1.1, 1.1], [z_g - 0.01, z_g - 0.01],
            color='#192133', linewidth=0.4, alpha=0.3, zorder=1)
    ax.plot([-1.8, 1.8], [g * 0.6, g * 0.6], [z_g - 0.01, z_g - 0.01],
            color='#192133', linewidth=0.4, alpha=0.3, zorder=1)

# road center line
ax.plot([-1.8, 1.8], [0, 0], [z_g - 0.008, z_g - 0.008],
        color='#ffd600', linewidth=1.5, linestyle='--', alpha=0.2, zorder=1)


# ═════════════════════════════════════════════════════════════════════════
# PANEL A — Specifications (top-right)
# ═════════════════════════════════════════════════════════════════════════
ax_s = fig.add_axes([0.60, 0.52, 0.38, 0.36])
ax_s.set_facecolor('#e3f2fd')
ax_s.set_xlim(0, 10)
ax_s.set_ylim(0, 10)
ax_s.axis('off')
for sp in ax_s.spines.values():
    sp.set_visible(True)
    sp.set_color(ACCENT_BLUE)
    sp.set_linewidth(2.5)

ax_s.text(5, 9.6, 'NVIS 40 m Car-Roof Loop  --  Specifications',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TEXT_DARK, fontfamily='sans-serif')

specs = [
    ('Band',             '40 m  (7.000 \u2013 7.300 MHz)'),
    ('NVIS Reliability', 'Excellent (foF2 > 7 MHz typical)'),
    ('Loop Diameter',    '1.00 m (39.4")  =  0.074\u03bb'),
    ('Circumference',    '3.14 m (0.074\u03bb)'),
    ('Loop Material',    '22 mm OD copper tube, 1 mm wall'),
    ('Inductance',       '~2.45 \u03bcH'),
    ('Reactance (XL)',   '~109 \u03a9 at 7.15 MHz'),
    ('Tuning Capacitor', 'Vacuum variable 30\u2013220 pF, 7.5 kV'),
    ('Cap at Resonance', '~210 pF at 7.0 MHz'),
    ('Feed Method',      'Faraday coupling loop 200 mm dia'),
    ('Profile Height',   '~10 cm above roof (low drag)'),
    ('Radiation Res.',   '~6 m\u03a9'),
    ('Loss Res. (Cu)',   '~32 m\u03a9'),
    ('Cap ESR',          '~11 m\u03a9 (vacuum Q \u2248 10 000)'),
    ('Efficiency',       '~12\u201315 %'),
    ('ERP @ 50 W',      '~6\u20137.5 W radiated'),
    ('Bandwidth',        '~5\u20138 kHz  (Q \u2248 900\u20131200)'),
    ('Max Cap Voltage',  '~3.6 kV @ 50 W'),
    ('Weight',           '~3.0 kg (6.6 lb) complete'),
    ('Tuning',           'NEMA17 stepper + worm gear'),
]

row_clrs = ['#bbdefb', '#ffffff']
y0 = 9.0
dy = 0.44
for i, (label, value) in enumerate(specs):
    y = y0 - i * dy
    rc = row_clrs[i % 2]
    ax_s.add_patch(FancyBboxPatch((0.1, y - 0.18), 9.8, 0.40,
                   boxstyle="round,pad=0.04", facecolor=rc, alpha=0.7))
    ax_s.text(0.3, y, label, fontsize=12.5, fontweight='bold', va='center',
              color=TEXT_DARK, fontfamily='sans-serif')
    ax_s.text(9.7, y, value, fontsize=12.5, va='center', ha='right',
              color=TEXT_DARK, fontfamily='sans-serif')


# ═════════════════════════════════════════════════════════════════════════
# PANEL B — Installation Guide (bottom-right, taller)
# ═════════════════════════════════════════════════════════════════════════
ax_n = fig.add_axes([0.60, 0.06, 0.38, 0.40])
ax_n.set_facecolor('#fff3e0')
ax_n.set_xlim(0, 10)
ax_n.set_ylim(0, 10)
ax_n.axis('off')
for sp in ax_n.spines.values():
    sp.set_visible(True)
    sp.set_color('#ff9800')
    sp.set_linewidth(2.5)

ax_n.text(5, 9.75, 'Installation & Operation Guide',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TEXT_DARK, fontfamily='sans-serif')

notes = [
    ('1.', 'BUILD MAIN LOOP',
     'Cut 3.20 m of 22 mm Cu tube. Fill with sand, cap ends,\n'
     'bend into 1.00 m circle. Leave 20 mm gap for capacitor.'),
    ('2.', 'COUPLING LOOP',
     'Bend 65 cm of RG-213 into 200 mm circle (Faraday shield).\n'
     'Connect shield both ends, center conductor one end only.'),
    ('3.', 'CAPACITOR ASSEMBLY',
     'Mount vacuum variable (30-220 pF, 7.5 kV) in IP65 box.\n'
     'Attach NEMA17 stepper + worm gear. Short Cu leads to loop.'),
    ('4.', 'MAGNETIC MOUNTS',
     'Place 4x heavy NdFeB mounts on clean roof in square pattern.\n'
     'Screw HDPE rods (100 mm) into mounts. Add loop clips on top.'),
    ('5.', 'INSTALL & ROUTE',
     'Set loop horizontal on standoffs. Route RG-58 + motor cable\n'
     'through window seal. Add ferrite choke balun at feedpoint.'),
    ('6.', 'TUNE & OPERATE',
     'NanoVNA sweep 6.8-7.5 MHz. Motor-tune for target freq.\n'
     'BW ~5-8 kHz: retune for each QSO. Max 50 W recommended.'),
]

row_clrs_n = ['#ffe0b2', '#ffffff']
y0n = 9.1
dyn = 1.30
for i, (num, title, desc) in enumerate(notes):
    y = y0n - i * dyn
    rc = row_clrs_n[i % 2]
    ax_n.add_patch(FancyBboxPatch((0.2, y - 0.52), 9.6, 1.10,
                   boxstyle="round,pad=0.08", facecolor=rc, alpha=0.6))
    ax_n.add_patch(plt.Circle((0.6, y), 0.32, facecolor='#e65100',
                   edgecolor='white', linewidth=2, zorder=10,
                   transform=ax_n.transData))
    ax_n.text(0.6, y, num, fontsize=15, fontweight='bold', color='white',
              ha='center', va='center', fontfamily='sans-serif', zorder=11)
    ax_n.text(1.15, y + 0.24, title, fontsize=14.5, fontweight='bold',
              va='center', color='#bf360c', fontfamily='sans-serif')
    ax_n.text(1.15, y - 0.24, desc, fontsize=11.5, va='center',
              color='#333', fontfamily='sans-serif', linespacing=1.3)

# BOM
ax_n.text(5, 1.15,
          'BOM: 22mm Cu tube $30 | Vacuum cap $120 | NdFeB mounts $30 | '
          'HDPE + clips $12 | RG-213 $8 | RG-58 $10',
          fontsize=11, fontweight='bold', ha='center', va='center',
          color='#e65100', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff8e1',
                    edgecolor='#e65100', linewidth=2, alpha=0.9))
ax_n.text(5, 0.65,
          'Stepper kit $18 | Ferrite balun $8 | IP65 box $10 | '
          'Hardware $12  =  Total ~$258',
          fontsize=11, fontweight='bold', ha='center', va='center',
          color='#e65100', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.25', facecolor='#fff8e1',
                    edgecolor='#e65100', linewidth=2, alpha=0.9))

# NVIS advantage note
ax_n.text(5, 0.08,
          '[OK]  40 m NVIS is HIGHLY RELIABLE: foF2 routinely exceeds '
          '7 MHz day & night, all seasons.  Coverage 0\u2013600 km.',
          fontsize=11.5, fontweight='bold', ha='center', va='center',
          color='#1b5e20', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.25', facecolor='#c8e6c9',
                    edgecolor='#2e7d32', linewidth=2, alpha=0.95))


# ═════════════════════════════════════════════════════════════════════════
# INSET — NVIS Radiation Pattern (polar, bottom-left corner of 3D view)
# ═════════════════════════════════════════════════════════════════════════
ax_rp = fig.add_axes([0.01, 0.06, 0.18, 0.28], projection='polar')
ax_rp.set_facecolor('#111d30')
ax_rp.set_theta_zero_location('N')
ax_rp.set_theta_direction(-1)

# simplified NVIS pattern for horizontal small loop over ground plane
# elevation angle 0-90°, pattern ~ sin(θ) for a horizontal loop
elev = np.linspace(0, np.pi, 180)
# pattern: broadside (max at zenith), with ground reflection reinforcement
pattern_raw = np.abs(np.cos(elev))  # basic pattern of horizontal loop
# ground reflection factor at h = 0.1λ equivalent
h_over_lam = 0.002  # loop very close to ground plane
ground_factor = np.abs(np.sin(2 * np.pi * h_over_lam * np.sin(elev)) + 0.8)
pattern = pattern_raw * ground_factor
pattern = pattern / np.max(pattern)  # normalize

# plot both halves (left = 0-180°, mirrored)
ax_rp.plot(elev, pattern, color='#ff8a65', linewidth=2.5, label='E-plane')
ax_rp.plot(-elev, pattern, color='#ff8a65', linewidth=2.5)
ax_rp.fill_between(elev, 0, pattern, alpha=0.15, color='#ff8a65')
ax_rp.fill_between(-elev, 0, pattern, alpha=0.15, color='#ff8a65')

# NVIS zone highlight (70-90°)
nvis_lo = np.radians(70)
nvis_hi = np.radians(90)
nvis_fill = np.linspace(nvis_lo, nvis_hi, 20)
nvis_r = np.interp(nvis_fill, elev, pattern)
ax_rp.fill_between(nvis_fill, 0, nvis_r, alpha=0.4, color='#ffd600')
ax_rp.fill_between(-nvis_fill, 0, nvis_r, alpha=0.4, color='#ffd600')

ax_rp.set_ylim(0, 1.15)
ax_rp.set_rticks([0.25, 0.5, 0.75, 1.0])
ax_rp.set_yticklabels(['-12', '-6', '-3', '0 dB'], fontsize=8, color='#78909c')
ax_rp.set_xticks(np.radians([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]))
ax_rp.set_xticklabels(['0\u00b0', '30\u00b0', '60\u00b0', '90\u00b0',
                        '120\u00b0', '150\u00b0', '180\u00b0', '210\u00b0',
                        '240\u00b0', '270\u00b0', '300\u00b0', '330\u00b0'],
                       fontsize=8, color='#78909c')
ax_rp.tick_params(colors='#546e7a')
ax_rp.grid(True, color='#37474f', alpha=0.4)
ax_rp.set_title('Elevation Pattern', fontsize=13, fontweight='bold',
                color='#e0e0e0', pad=15, fontfamily='sans-serif')

# NVIS zone annotation
ax_rp.annotate('NVIS\nZone', xy=(np.radians(80), 0.85),
               fontsize=11, fontweight='bold', color=GOLD,
               ha='center', va='center',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a1628',
                         edgecolor=GOLD, alpha=0.9))

# border for inset
for sp in ax_rp.spines.values():
    sp.set_color('#546e7a')
    sp.set_linewidth(1.5)


# ═════════════════════════════════════════════════════════════════════════
# INSET — Coverage Map (small, overlaid in 3D area)
# ═════════════════════════════════════════════════════════════════════════
ax_cov = fig.add_axes([0.365, 0.06, 0.21, 0.28])
ax_cov.set_facecolor('#111d30')
ax_cov.set_aspect('equal')

# simple circle representing coverage radius
theta_cov = np.linspace(0, 2 * np.pi, 100)
for r_km, alpha_c, lbl in [
    (600, 0.15, '600 km'),
    (400, 0.25, '400 km'),
    (200, 0.40, '200 km'),
]:
    r_norm = r_km / 700
    ax_cov.fill(r_norm * np.cos(theta_cov), r_norm * np.sin(theta_cov),
                alpha=alpha_c, color='#4dd0e1')
    ax_cov.plot(r_norm * np.cos(theta_cov), r_norm * np.sin(theta_cov),
                color='#4dd0e1', linewidth=1.2, alpha=0.6)
    ax_cov.text(0, r_norm + 0.03, lbl, fontsize=10, color='#80deea',
                ha='center', va='bottom', fontweight='bold', fontfamily='sans-serif')

# car icon at center
ax_cov.plot(0, 0, 's', color=ACCENT_RED, markersize=8, zorder=10)
ax_cov.text(0.05, -0.05, 'TX', fontsize=10, fontweight='bold', color=ACCENT_RED,
            fontfamily='sans-serif')

# skip zone annotation
ax_cov.annotate('No skip zone!\nNVIS fills in\n0-600 km', xy=(0.45, -0.55),
                fontsize=10, fontweight='bold', color='#a5d6a7',
                fontfamily='sans-serif', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#0a1628',
                          edgecolor='#4caf50', alpha=0.9))

ax_cov.set_xlim(-1.05, 1.05)
ax_cov.set_ylim(-1.05, 1.05)
ax_cov.set_title('NVIS Coverage (40 m)', fontsize=13, fontweight='bold',
                 color='#e0e0e0', pad=10, fontfamily='sans-serif')
ax_cov.axis('off')
for sp in ax_cov.spines.values():
    sp.set_visible(True)
    sp.set_color('#546e7a')
    sp.set_linewidth(1.5)


# ═════════════════════════════════════════════════════════════════════════
# TITLE BANNER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.005, 0.925), 0.99, 0.068,
    boxstyle="round,pad=0.008", facecolor='#0d47a1', alpha=0.95,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.972,
         'NVIS 40 m Mobile Antenna  \u2014  Low-Profile Magnetic Loop on Car Roof  '
         '\u2014  3D Installation View',
         fontsize=36, fontweight='bold', color='#ffffff',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)
fig.text(0.50, 0.940,
         '1.00 m Loop  |  22 mm Copper  |  Vacuum Cap 7.5 kV  |  10 cm Profile  '
         '|  12\u201315% Eff  |  ~6 W ERP  |  Mag-Mount  |  Motor Tuned  '
         '|  NVIS 0\u2013600 km',
         fontsize=20, fontweight='bold', color=GOLD,
         ha='center', va='center', fontfamily='sans-serif', zorder=3)


# ═════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.005, 0.002), 0.99, 0.028,
    boxstyle="round,pad=0.005", facecolor='#0d47a1', alpha=0.85,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.016,
         'NVIS 40m Car-Roof STL  |  HS0ZNR  |  7.000\u20137.300 MHz  |  '
         'Generated 2026-02-23',
         fontsize=18, fontweight='bold', color='#e3f2fd',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)


# ═════════════════════════════════════════════════════════════════════════
# SAVE
# ═════════════════════════════════════════════════════════════════════════
out = r'C:\Users\Jakkrit\.local\bin\NVIS_40m_Car_Roof_3D.jpg'
fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor(),
            pil_kwargs={'quality': 95})
plt.close()
print(f'Saved: {out}')
print(f'Size: {44*DPI} x {30*DPI} px  =  {44}x{30} in @ {DPI} DPI')
