#!/usr/bin/env python3
"""
Dual-Band NVIS 80m/40m Magnetic Loop on Car Roof — 3D Poster
Highly detailed sedan, relay-switched cap banks, radiation patterns,
coverage map, link budget comparison.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch
import numpy as np

DPI = 200
fig = plt.figure(figsize=(48, 32), dpi=DPI, facecolor='#080e1a')

# ── palette ────────────────────────────────────────────────────────────
CU       = '#b5651d'
CU_HI    = '#e8a54a'
CU_DK    = '#8b4513'
CU_CPL   = '#a0522d'
A_BLUE   = '#1565c0'
A_RED    = '#c62828'
A_GRN    = '#2e7d32'
GOLD     = '#ffd600'
TD       = '#1a1a2e'
N = 220


# ═════════════════════════════════════════════════════════════════════════
#  MAIN 3-D VIEW  (upper-left 56 %)
# ═════════════════════════════════════════════════════════════════════════
ax = fig.add_axes([0.005, 0.28, 0.56, 0.62], projection='3d',
                  computed_zorder=False)
ax.set_facecolor('#0f1a2e')
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-1.3, 1.3)
ax.set_zlim(-0.40, 1.70)
ax.view_init(elev=24, azim=-50)
ax.set_box_aspect([2.2, 1.3, 1.05])
ax.axis('off')


# ── drawing helpers ────────────────────────────────────────────────────
def tube(a, px, py, pz, c, lw=7, hc=None, al=1.0, zo=5):
    a.plot(px, py, pz, color=c, lw=lw, solid_capstyle='round', alpha=al, zorder=zo)
    if hc:
        a.plot(px, py, pz, color=hc, lw=lw*0.4, solid_capstyle='round',
               alpha=0.35, zorder=zo+1)

def qpoly(a, v, fc, ec='#1a2530', al=0.92, lw=1.0, zo=2):
    p = Poly3DCollection([v], alpha=al, zorder=zo)
    p.set_facecolor(fc); p.set_edgecolor(ec); p.set_linewidth(lw)
    a.add_collection3d(p)

def box3d(a, cx,cy,cz, hw,hd,hh, cols, ec='#333', al=0.85, zo=12):
    fs = [
        [[cx-hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx-hw,cy+hd,cz-hh]],
        [[cx-hw,cy-hd,cz+hh],[cx+hw,cy-hd,cz+hh],[cx+hw,cy+hd,cz+hh],[cx-hw,cy+hd,cz+hh]],
        [[cx-hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz-hh],[cx+hw,cy-hd,cz+hh],[cx-hw,cy-hd,cz+hh]],
        [[cx-hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz+hh],[cx-hw,cy+hd,cz+hh]],
        [[cx-hw,cy-hd,cz-hh],[cx-hw,cy+hd,cz-hh],[cx-hw,cy+hd,cz+hh],[cx-hw,cy-hd,cz+hh]],
        [[cx+hw,cy-hd,cz-hh],[cx+hw,cy+hd,cz-hh],[cx+hw,cy+hd,cz+hh],[cx+hw,cy-hd,cz+hh]],
    ]
    for face, fc_ in zip(fs, cols):
        qpoly(a, face, fc_, ec=ec, al=al, zo=zo)

def cylinder(a, cx,cy,zb,zt, r, n, fc, ec='#222', al=0.85, zo=12):
    th = np.linspace(0, 2*np.pi, n+1)
    for i in range(n):
        face = [[cx+r*np.cos(th[i]),   cy+r*np.sin(th[i]),   zb],
                [cx+r*np.cos(th[i+1]), cy+r*np.sin(th[i+1]), zb],
                [cx+r*np.cos(th[i+1]), cy+r*np.sin(th[i+1]), zt],
                [cx+r*np.cos(th[i]),   cy+r*np.sin(th[i]),   zt]]
        qpoly(a, face, fc, ec=ec, al=al, lw=0.5, zo=zo)
    # top cap
    cap = [[cx+r*np.cos(t), cy+r*np.sin(t), zt] for t in th]
    qpoly(a, cap, fc, ec=ec, al=al, zo=zo+1)


# ═════════════════════════════════════════════════════════════════════════
#  CAR — high-detail sedan with 20 cross-sections, metallic look
# ═════════════════════════════════════════════════════════════════════════
z_g = -0.20  # ground

# body profile — 20 stations for smooth curves
bx = np.array([-2.30,-2.15,-2.00,-1.80,-1.50,-1.20,-0.80,-0.40,
                0.00, 0.30, 0.60, 0.90, 1.20, 1.50, 1.75,
                2.00, 2.15, 2.30, 2.42, 2.50])
bw = np.array([ 0.28, 0.52, 0.72, 0.79, 0.82, 0.83, 0.84, 0.84,
                0.84, 0.84, 0.84, 0.84, 0.82, 0.79, 0.74,
                0.67, 0.56, 0.42, 0.30, 0.18])
bzt = np.array([z_g+0.15, z_g+0.30, z_g+0.40, z_g+0.45, z_g+0.48,
                z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48,
                z_g+0.48, z_g+0.48, z_g+0.47, z_g+0.45, z_g+0.42,
                z_g+0.38, z_g+0.33, z_g+0.26, z_g+0.20, z_g+0.14])

# cabin profile — 10 stations
cx_ = np.array([-1.50,-1.20,-0.80,-0.40, 0.00, 0.40, 0.70, 1.00, 1.25, 1.45])
cw_ = np.array([ 0.60, 0.72, 0.77, 0.78, 0.78, 0.78, 0.77, 0.74, 0.68, 0.58])
czt = np.array([z_g+0.48, z_g+0.68, z_g+0.78, z_g+0.82, z_g+0.84,
                z_g+0.82, z_g+0.78, z_g+0.72, z_g+0.64, z_g+0.55])

# metallic paint — 3-tone shading (viewer faces left-side & top)
paint_l  = '#4a6878'   # left (facing viewer — highlight)
paint_r  = '#2a3e4a'   # right (shadow)
paint_t  = '#5a7888'   # top (brightest)
paint_bt = '#1a2830'   # bottom (darkest)
paint_f  = '#3a5565'   # front face
paint_re = '#283c48'   # rear face

# ── body shell ─────────────────────────────────────────────────────────
for i in range(len(bx)-1):
    x0,x1 = bx[i],bx[i+1]; w0,w1 = bw[i],bw[i+1]
    zt0,zt1 = bzt[i],bzt[i+1]
    # left
    qpoly(ax,[[x0,-w0,z_g],[x1,-w1,z_g],[x1,-w1,zt1],[x0,-w0,zt0]],
          paint_l, zo=2)
    # right
    qpoly(ax,[[x0,w0,z_g],[x1,w1,z_g],[x1,w1,zt1],[x0,w0,zt0]],
          paint_r, zo=2)
    # top
    qpoly(ax,[[x0,-w0,zt0],[x1,-w1,zt1],[x1,w1,zt1],[x0,w0,zt0]],
          paint_t, zo=2)
    # bottom
    qpoly(ax,[[x0,-w0,z_g],[x1,-w1,z_g],[x1,w1,z_g],[x0,w0,z_g]],
          paint_bt, zo=1)

# front face
qpoly(ax,[[bx[-1],-bw[-1],z_g],[bx[-1],bw[-1],z_g],
          [bx[-1],bw[-1],bzt[-1]],[bx[-1],-bw[-1],bzt[-1]]],
      paint_f, zo=2)
# rear face
qpoly(ax,[[bx[0],-bw[0],z_g],[bx[0],bw[0],z_g],
          [bx[0],bw[0],bzt[0]],[bx[0],-bw[0],bzt[0]]],
      paint_re, zo=2)

# ── cabin greenhouse ───────────────────────────────────────────────────
glass_c = '#5bc0de'; glass_a = 0.28
roof_c  = '#5a7888'; roof_a  = 0.95
pillar_c= '#1a2530'

for i in range(len(cx_)-1):
    x0,x1 = cx_[i],cx_[i+1]; w0,w1 = cw_[i],cw_[i+1]
    zb0 = np.interp(x0, bx, bzt); zb1 = np.interp(x1, bx, bzt)
    zt0,zt1 = czt[i],czt[i+1]
    # left glass
    qpoly(ax,[[x0,-w0,zb0],[x1,-w1,zb1],[x1,-w1,zt1],[x0,-w0,zt0]],
          glass_c, al=glass_a, lw=1.2, zo=3)
    # right glass
    qpoly(ax,[[x0,w0,zb0],[x1,w1,zb1],[x1,w1,zt1],[x0,w0,zt0]],
          glass_c, al=glass_a, lw=1.2, zo=3)
    # roof
    qpoly(ax,[[x0,-w0,zt0],[x1,-w1,zt1],[x1,w1,zt1],[x0,w0,zt0]],
          roof_c, al=roof_a, lw=0.8, zo=4)

# windshield (raked forward)
xwf = cx_[-1]; wwf = cw_[-1]
zbwf = np.interp(xwf, bx, bzt); ztwf = czt[-1]
qpoly(ax,[[xwf,-wwf,zbwf],[xwf,wwf,zbwf],
          [xwf-0.20,wwf*0.93,ztwf],[xwf-0.20,-wwf*0.93,ztwf]],
      glass_c, al=0.32, lw=2, zo=3)
# rear glass
xrg = cx_[0]; wrg = cw_[0]
zbrg = np.interp(xrg, bx, bzt); ztrg = czt[0]
qpoly(ax,[[xrg,-wrg,zbrg],[xrg,wrg,zbrg],
          [xrg+0.12,wrg*0.93,ztrg],[xrg+0.12,-wrg*0.93,ztrg]],
      glass_c, al=0.32, lw=2, zo=3)

# ── A / B / C pillars ─────────────────────────────────────────────────
pw = 0.065
for px_,pw_ in [(cx_[-1],cw_[-1]),(cx_[3],cw_[3]),(cx_[0],cw_[0])]:
    zb_ = np.interp(px_, bx, bzt)
    zt_ = np.interp(px_, cx_, czt)
    for s in [-1,1]:
        qpoly(ax,[[px_-pw,s*pw_,zb_],[px_+pw,s*pw_,zb_],
                  [px_+pw,s*pw_,zt_],[px_-pw,s*pw_,zt_]],
              pillar_c, al=0.92, lw=1.5, zo=4)

# ── door panel lines ──────────────────────────────────────────────────
for dx in [-0.25, 0.70]:
    wd = np.interp(dx, bx, bw)
    zbd = z_g+0.03; ztd = np.interp(dx, bx, bzt)-0.02
    for s in [-1,1]:
        ax.plot([dx,dx],[s*(wd+0.005),s*(wd+0.005)],[zbd,ztd],
                color='#1a2530', lw=1.8, zorder=3)

# ── door handles (chrome) ────────────────────────────────────────────
for hx in [-0.65, 0.35]:
    hw_ = np.interp(hx, bx, bw)
    hz_ = np.interp(hx, bx, bzt) - 0.07
    for s in [-1,1]:
        hy_ = s*(hw_ + 0.008)
        ax.plot([hx-0.06,hx+0.06],[hy_,hy_],[hz_,hz_],
                color='#b0bec5', lw=3.5, solid_capstyle='round', zorder=4)

# ── side mirrors ─────────────────────────────────────────────────────
for s in [-1,1]:
    mx_ = cx_[-1]-0.08; mw_ = np.interp(mx_, bx, bw)
    my_ = s*(mw_+0.14); mz_ = np.interp(mx_, bx, bzt)+0.05
    ax.plot([mx_,mx_],[s*mw_,my_],[mz_,mz_], color='#2d3a45', lw=3, zorder=4)
    # housing
    qpoly(ax,[[mx_-0.05,my_,mz_-0.035],[mx_+0.05,my_,mz_-0.035],
              [mx_+0.05,my_,mz_+0.035],[mx_-0.05,my_,mz_+0.035]],
          '#2d3a45', al=0.9, zo=4)
    # mirror glass
    qpoly(ax,[[mx_-0.04,my_+s*0.005,mz_-0.025],[mx_+0.04,my_+s*0.005,mz_-0.025],
              [mx_+0.04,my_+s*0.005,mz_+0.025],[mx_-0.04,my_+s*0.005,mz_+0.025]],
          '#90caf9', al=0.5, zo=5)

# ── headlights (LED-style, two segments each side) ───────────────────
for s in [-1,1]:
    hlx = bx[-1]+0.015
    for y0h,y1h in [(s*0.05,s*0.20),(s*0.22,s*bw[-2]*0.9)]:
        qpoly(ax,[[hlx,y0h,z_g+0.14],[hlx,y1h,z_g+0.14],
                  [hlx,y1h,z_g+0.24],[hlx,y0h,z_g+0.24]],
              '#fff9c4', ec='#fdd835', al=0.85, lw=1.2, zo=3)
    # DRL strip
    ax.plot([hlx+0.005,hlx+0.005],[s*0.05,s*bw[-2]*0.88],
            [z_g+0.25,z_g+0.25], color='#bbdefb', lw=2, alpha=0.6, zorder=4)

# ── taillights (wrap-around LED style) ───────────────────────────────
for s in [-1,1]:
    tlx = bx[0]-0.015
    qpoly(ax,[[tlx,s*0.08,z_g+0.06],[tlx,s*bw[1]*0.88,z_g+0.06],
              [tlx,s*bw[1]*0.88,z_g+0.22],[tlx,s*0.08,z_g+0.22]],
          '#d32f2f', ec='#b71c1c', al=0.85, lw=1.2, zo=3)
    # light bar accent
    ax.plot([tlx-0.005,tlx-0.005],[s*0.10,s*bw[1]*0.85],
            [z_g+0.14,z_g+0.14], color='#ff8a80', lw=2.5, alpha=0.7, zorder=4)

# ── front grille (split design with chrome accent) ───────────────────
gx_ = bx[-1]+0.02; gw_ = bw[-1]*0.85
# upper grille
qpoly(ax,[[gx_,-gw_,z_g+0.10],[gx_,gw_,z_g+0.10],
          [gx_,gw_,z_g+0.18],[gx_,-gw_,z_g+0.18]],
      '#1a2530', al=0.92, zo=3)
# lower intake
qpoly(ax,[[gx_,-gw_*0.8,z_g+0.01],[gx_,gw_*0.8,z_g+0.01],
          [gx_,gw_*0.8,z_g+0.08],[gx_,-gw_*0.8,z_g+0.08]],
      '#111820', al=0.92, zo=3)
# chrome bar
ax.plot([gx_+0.005,gx_+0.005],[-gw_*0.9,gw_*0.9],[z_g+0.135,z_g+0.135],
        color='#b0bec5', lw=2.5, zorder=4)
# grille mesh lines
for gz_ in np.linspace(z_g+0.11, z_g+0.17, 3):
    ax.plot([gx_+0.003,gx_+0.003],[-gw_*0.85,gw_*0.85],[gz_,gz_],
            color='#37474f', lw=1.2, zorder=4)

# ── brand badge (small circle on grille) ─────────────────────────────
badge_t = np.linspace(0, 2*np.pi, 16)
badge_pts = [[gx_+0.008, 0.03*np.cos(t), z_g+0.14+0.03*np.sin(t)]
             for t in badge_t]
qpoly(ax, badge_pts, '#b0bec5', ec='#78909c', al=0.9, zo=5)

# ── license plates ───────────────────────────────────────────────────
for lx_,ls in [(bx[0]-0.018, 'rear'), (bx[-1]+0.018, 'front')]:
    qpoly(ax,[[lx_,-0.14,z_g+0.04],[lx_,0.14,z_g+0.04],
              [lx_,0.14,z_g+0.12],[lx_,-0.14,z_g+0.12]],
          '#f5f5f5', ec='#555', al=0.9, zo=3)

# ── bumpers (body-colored with lower black trim) ────────────────────
# front
qpoly(ax,[[bx[-1]+0.01,-bw[-2]*0.92,z_g],[bx[-1]+0.01,bw[-2]*0.92,z_g],
          [bx[-1]+0.01,bw[-2]*0.92,z_g+0.04],[bx[-1]+0.01,-bw[-2]*0.92,z_g+0.04]],
      '#1a2530', al=0.9, zo=3)
# rear
qpoly(ax,[[bx[0]-0.01,-bw[1]*0.88,z_g],[bx[0]-0.01,bw[1]*0.88,z_g],
          [bx[0]-0.01,bw[1]*0.88,z_g+0.04],[bx[0]-0.01,-bw[1]*0.88,z_g+0.04]],
      '#1a2530', al=0.9, zo=3)

# ── rocker panels (side skirts) ──────────────────────────────────────
for s in [-1,1]:
    rx0, rx1 = -1.80, 2.10
    rw0 = np.interp(rx0, bx, bw); rw1 = np.interp(rx1, bx, bw)
    qpoly(ax,[[rx0,s*rw0,z_g],[rx1,s*rw1,z_g],
              [rx1,s*rw1,z_g+0.04],[rx0,s*rw0,z_g+0.04]],
          '#1a2530', al=0.9, lw=0.8, zo=3)

# ── wheels (multi-spoke with brake disc visible) ────────────────────
wt = np.linspace(0, 2*np.pi, 36)
wr = 0.18; rr = 0.12; dr = 0.08
wlocs = [(1.60,-0.84,z_g+0.01),(1.60,0.84,z_g+0.01),
         (-1.50,-0.84,z_g+0.01),(-1.50,0.84,z_g+0.01)]
for wx_,wy_,wz_ in wlocs:
    # tyre
    tpts = [[wx_+wr*np.cos(t)*0.35, wy_, wz_+wr*np.sin(t)] for t in wt]
    qpoly(ax, tpts, '#1a1a1a', ec='#0a0a0a', al=0.92, zo=3)
    # rim
    rpts = [[wx_+rr*np.cos(t)*0.35, wy_, wz_+rr*np.sin(t)] for t in wt]
    qpoly(ax, rpts, '#cfd8dc', ec='#90a4ae', al=0.88, zo=4)
    # brake disc
    dpts = [[wx_+dr*np.cos(t)*0.35, wy_, wz_+dr*np.sin(t)] for t in wt]
    qpoly(ax, dpts, '#78909c', ec='#546e7a', al=0.7, zo=5)
    # 5 spokes
    for sp_a in np.linspace(0, 2*np.pi, 6)[:-1]:
        sx0 = wx_ + dr*np.cos(sp_a)*0.35
        sz0 = wz_ + dr*np.sin(sp_a)
        sx1 = wx_ + rr*np.cos(sp_a)*0.35
        sz1 = wz_ + rr*np.sin(sp_a)
        ax.plot([sx0,sx1],[wy_,wy_],[sz0,sz1],
                color='#cfd8dc', lw=2, zorder=5)
    # wheel arch
    arch_a = np.linspace(-0.4, np.pi+0.4, 40)
    ax.plot(wx_+(wr+0.03)*np.cos(arch_a)*0.35,
            np.full(40, wy_),
            wz_+(wr+0.03)*np.sin(arch_a),
            color='#1a2530', lw=3.5, zorder=3)
    # fender lip
    ax.plot(wx_+(wr+0.04)*np.cos(arch_a)*0.35,
            np.full(40, wy_),
            wz_+(wr+0.04)*np.sin(arch_a),
            color=paint_l if wy_ < 0 else paint_r, lw=2, zorder=3)

# ── roof rails ───────────────────────────────────────────────────────
for s in [-1,1]:
    rrx = np.linspace(cx_[0]+0.15, cx_[-1]-0.15, 40)
    rry = np.array([s*np.interp(x, cx_, cw_) for x in rrx])
    rrz = np.array([np.interp(x, cx_, czt)+0.008 for x in rrx])
    ax.plot(rrx, rry, rrz, color='#90a4ae', lw=3, solid_capstyle='round', zorder=5)

# ── shark-fin antenna (OEM, rear of roof) ────────────────────────────
sfx = cx_[1]; sfz_b = np.interp(sfx, cx_, czt)+0.008
sfz_t = sfz_b + 0.06
qpoly(ax,[[sfx-0.04,0,sfz_b],[sfx+0.04,0,sfz_b],
          [sfx+0.01,0,sfz_t],[sfx-0.01,0,sfz_t]],
      '#2d3a45', al=0.9, zo=6)

# ── windshield wipers (rest position) ────────────────────────────────
wiper_x0 = cx_[-1] - 0.12
for s_w in [-0.25, 0.25]:
    wiper_y = s_w
    wiper_zb = np.interp(wiper_x0, bx, bzt) + 0.005
    ax.plot([wiper_x0, wiper_x0 + 0.35], [wiper_y, wiper_y * 0.7],
            [wiper_zb, wiper_zb + 0.005],
            color='#1a1a1a', lw=2, zorder=5)

# ── exhaust pipes (rear, dual tips) ─────────────────────────────────
for ey in [-0.30, 0.30]:
    cylinder(ax, bx[0]-0.04, ey, z_g-0.01, z_g+0.02, 0.025, 10,
             '#78909c', ec='#546e7a', al=0.8, zo=3)


# ═════════════════════════════════════════════════════════════════════════
#  ANTENNA — 1.0 m dual-band loop with relay-switched cap banks
# ═════════════════════════════════════════════════════════════════════════
R_loop = 0.50
z_roof = np.interp(0, cx_, czt) + 0.008
standoff_h = 0.10
z_lp = z_roof + standoff_h
gap_a = 0.07

# ── main loop (22 mm Cu, horizontal) ────────────────────────────────
th_l = np.linspace(np.pi/2+gap_a, np.pi/2+2*np.pi-gap_a, N)
tube(ax, R_loop*np.cos(th_l), R_loop*np.sin(th_l),
     np.full(N, z_lp), CU, lw=9, hc=CU_HI, zo=10)

# ── CAPACITOR ENCLOSURE (larger, houses relay + 2 cap banks) ────────
cap_x, cap_y, cap_z = 0.0, R_loop, z_lp
box_cols = ['#0d47a1','#1565c0','#1976d2','#0d47a1','#0a3d8f','#1565c0']
box3d(ax, cap_x, cap_y, cap_z, 0.14, 0.08, 0.06, box_cols, ec='#0d47a1', zo=15)

# leads
for angle,sx in [(np.pi/2+gap_a,-0.7),(np.pi/2+2*np.pi-gap_a,0.7)]:
    ex,ey = R_loop*np.cos(angle), R_loop*np.sin(angle)
    ax.plot([ex,cap_x+sx*0.08],[ey,cap_y],[z_lp,cap_z],
            color=CU, lw=6, solid_capstyle='round', zorder=11)

# relay indicator (small red box on cap enclosure)
box3d(ax, cap_x-0.06, cap_y+0.04, cap_z+0.06,
      0.025, 0.02, 0.015,
      ['#c62828','#e53935','#ef5350','#c62828','#b71c1c','#e53935'],
      ec='#b71c1c', zo=16)

# stepper motor
cylinder(ax, cap_x+0.06, cap_y, cap_z+0.06, cap_z+0.10, 0.030, 16,
         '#455a64', ec='#37474f', zo=16)

# worm gear shaft (thin line from motor to cap shaft)
ax.plot([cap_x+0.06, cap_x], [cap_y, cap_y], [cap_z+0.08, cap_z+0.06],
        color='#b0bec5', lw=2, zorder=17)

# ── cap assembly label ───────────────────────────────────────────────
ax.plot([cap_x, cap_x+0.35],[cap_y+0.08, cap_y+0.32],
        [cap_z+0.10, cap_z+0.30], color='#90caf9', lw=1.5, zorder=19)
ax.text(cap_x+0.37, cap_y+0.34, cap_z+0.32,
        'Dual-Band Cap Assembly\n'
        'Bank A: Vacuum 30-250 pF (40 m)\n'
        'Bank B: Vacuum 150-900 pF (80 m)\n'
        'DPDT Relay Switch  |  Stepper Motor',
        fontsize=10.5, fontweight='bold', color='#bbdefb',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0d47a1', alpha=0.93,
                  edgecolor='#64b5f6', lw=1.5))

# ── weatherproof dome outline ────────────────────────────────────────
dome_t = np.linspace(0, 2*np.pi, 40)
ax.plot(cap_x+0.16*np.cos(dome_t), cap_y+0.10*np.sin(dome_t),
        np.full(40, cap_z+0.07),
        color='#80cbc4', lw=1.5, ls='--', alpha=0.45, zorder=14)

# ── coupling loop ────────────────────────────────────────────────────
R_cpl = 0.10
th_c = np.linspace(0.12, 2*np.pi-0.12, N)
tube(ax, R_cpl*np.cos(th_c), R_cpl*np.sin(th_c)-R_loop,
     np.full(N, z_lp), CU_CPL, lw=5, hc='#d2691e', zo=10)

ax.plot([R_cpl*0.7, R_cpl+0.22],[-R_loop, -R_loop-0.18],
        [z_lp, z_lp+0.14], color='#bcaaa4', lw=1.5, zorder=19)
ax.text(R_cpl+0.24, -R_loop-0.20, z_lp+0.16,
        'Faraday Feed Loop\n200 mm  |  RG-213\nShield both ends',
        fontsize=10.5, fontweight='bold', color='#d7ccc8',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#3e2723', alpha=0.92,
                  edgecolor='#8d6e63', lw=1.5))

# SO-239
hex_t = np.linspace(0,2*np.pi,7)
qpoly(ax,[[0.02*np.cos(t), -R_loop-R_cpl+0.02*np.sin(t), z_lp]
           for t in hex_t], '#b0bec5', ec='#78909c', al=0.9, zo=12)
ax.text(0, -R_loop-R_cpl-0.05, z_lp-0.03, 'SO-239',
        fontsize=9, fontweight='bold', color='#90a4ae',
        fontfamily='sans-serif', ha='center', zorder=20)

# ── 4 standoff posts ────────────────────────────────────────────────
spos = [( R_loop*0.65, R_loop*0.65),( R_loop*0.65,-R_loop*0.65),
        (-R_loop*0.65, R_loop*0.65),(-R_loop*0.65,-R_loop*0.65)]
for sx_,sy_ in spos:
    zr_ = np.interp(sx_, cx_, czt)+0.008
    # mag-mount base
    cylinder(ax, sx_, sy_, zr_, zr_+0.015, 0.042, 14,
             '#212121', ec='#111', al=0.9, zo=8)
    # rubber pad
    cylinder(ax, sx_, sy_, zr_+0.015, zr_+0.020, 0.038, 14,
             '#37474f', ec='#263238', al=0.85, zo=9)
    # HDPE rod
    ax.plot([sx_,sx_],[sy_,sy_],[zr_+0.02, z_lp],
            color='#eceff1', lw=5.5, solid_capstyle='round', zorder=8)
    # top nylon clip
    cylinder(ax, sx_, sy_, z_lp-0.008, z_lp+0.008, 0.028, 12,
             '#e0e0e0', ec='#bdbdbd', al=0.9, zo=11)

ax.plot([R_loop*0.65+0.04, R_loop*0.65+0.30],
        [-R_loop*0.65, -R_loop*0.65-0.20],
        [(z_roof+z_lp)/2, (z_roof+z_lp)/2-0.08],
        color='#b0bec5', lw=1.5, zorder=19)
ax.text(R_loop*0.65+0.32, -R_loop*0.65-0.22, (z_roof+z_lp)/2-0.10,
        'HDPE Post 100 mm\nNdFeB Mag-Mount 40 kg\nNo-drill | Quick deploy',
        fontsize=10, fontweight='bold', color='#cfd8dc',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.22', facecolor='#1a2530', alpha=0.92,
                  edgecolor='#78909c', lw=1.2))

# ── coax + control cable routing ─────────────────────────────────────
coax_pts = np.array([
    [0, -R_loop-R_cpl, z_lp],
    [0.05, -R_loop-R_cpl-0.05, z_lp-0.02],
    [0.12, -(np.interp(0.12, cx_, cw_)+0.02), z_roof-0.05],
    [0.15, -(np.interp(0.15, bx, bw)+0.01), z_g+0.38],
])
ax.plot(coax_pts[:,0], coax_pts[:,1], coax_pts[:,2],
        color='#222', lw=3.5, ls='--', alpha=0.7, zorder=6)
# control cable (parallel, slightly offset)
ax.plot(coax_pts[:,0]+0.03, coax_pts[:,1]+0.01, coax_pts[:,2],
        color='#4a148c', lw=2, ls='-.', alpha=0.5, zorder=6)
ax.text(0.25, coax_pts[3,1]-0.06, z_g+0.35,
        'RG-58 Coax + Motor\ncontrol cable\nthrough window seal',
        fontsize=9.5, fontweight='bold', color='#78909c',
        fontfamily='sans-serif', ha='left', zorder=20)

# ── choke balun (ferrite toroid) ─────────────────────────────────────
bx_ = 0.14; by_ = coax_pts[2,1]; bz_ = z_roof-0.02
balun_t = np.linspace(0, 2*np.pi, 30)
ax.plot(bx_+0.03*np.cos(balun_t)*0.3,
        by_+0.03*np.cos(balun_t)*0.3,
        bz_+0.03*np.sin(balun_t),
        color='#4e342e', lw=5, zorder=7)
ax.text(bx_+0.07, by_, bz_, 'Choke\nBalun', fontsize=9, color='#8d6e63',
        fontweight='bold', fontfamily='sans-serif', zorder=20)

# ── band switch control box inside car (small box near window) ───────
box3d(ax, 0.18, -(np.interp(0.18, bx, bw)-0.08), z_g+0.30,
      0.06, 0.04, 0.03,
      ['#263238','#37474f','#455a64','#263238','#1a2530','#37474f'],
      ec='#1a2530', al=0.8, zo=6)
ax.text(0.30, -(np.interp(0.18, bx, bw)-0.08), z_g+0.30,
        'Band Switch\n& Tune Controller',
        fontsize=9, fontweight='bold', color='#78909c',
        fontfamily='sans-serif', ha='left', zorder=20)

# ═════════════════════════════════════════════════════════════════════════
#  NVIS RADIATION ARROWS + IONOSPHERE
# ═════════════════════════════════════════════════════════════════════════
ac = '#ff8a65'
for ax_, ay_, sp in [(0,0,0),(0.20,0.12,0.05),(-0.20,0.12,0.05),
                     (0.14,-0.16,0.04),(-0.14,-0.16,0.04),
                     (0.28,0,0.07),(-0.28,0,0.07),
                     (0.10,0.24,0.03),(-0.10,0.24,0.03)]:
    z0_ = z_lp+0.12; z1_ = z_lp+0.72
    ax.plot([ax_, ax_*0.12+sp*0.08],[ay_, ay_*0.12],[z0_, z1_],
            color=ac, lw=2.2, alpha=0.6, zorder=17)
    for dx_ in [-0.015, 0.015]:
        ax.plot([ax_*0.12+sp*0.08, ax_*0.12+sp*0.08+dx_],
                [ay_*0.12, ay_*0.12],[z1_, z1_-0.045],
                color=ac, lw=2, alpha=0.6, zorder=17)

ax.text(0, 0, z_lp+0.82,
        'NVIS Radiation\n70\u00b0 - 90\u00b0 Elevation\nHorizontal Polarisation',
        fontsize=14, fontweight='bold', color='#ff8a65',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#080e1a', alpha=0.93,
                  edgecolor='#ff8a65', lw=2))

# ionosphere layers
for r_s, z_off, c_, a_, lbl in [
    (1.5, 0, '#4dd0e1', 0.55, 'F2 Layer ~250 km'),
    (1.3, 0.10, '#80deea', 0.30, 'F1 Layer ~200 km'),
]:
    it = np.linspace(-0.6, 0.6, 60)
    ax.plot(r_s*np.sin(it), r_s*0.3*np.cos(it),
            np.full(60, z_lp+1.25+z_off),
            color=c_, lw=3, ls=':', alpha=a_, zorder=16)

ax.text(0, 0, z_lp+1.48,
        'F2 Layer ~250 km  |  foF2 > 3.5 MHz always  |  > 7 MHz daytime',
        fontsize=11, fontweight='bold', color='#4dd0e1',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#080e1a', alpha=0.88,
                  edgecolor='#4dd0e1', lw=1.2))

# reflected waves
for rx_,ry_ in [(0.9,0.35),(-0.9,0.35),(0.7,-0.45),(-0.7,-0.45),
                (0.5,0.55),(-0.5,-0.55)]:
    ax.plot([rx_*0.25,rx_],[ry_*0.25,ry_],
            [z_lp+1.20, z_lp+0.35],
            color='#26c6da', lw=1.5, ls='--', alpha=0.35, zorder=16)

# ── dimension callouts ───────────────────────────────────────────────
# diameter
dz_ = z_lp + 0.07
ax.plot([-R_loop,R_loop],[0,0],[dz_,dz_], color=A_RED, lw=2.5, zorder=18)
for s in [-1,1]:
    ax.plot([s*R_loop,s*(R_loop-0.04)],[0,0.03],[dz_,dz_],
            color=A_RED, lw=2.5, zorder=18)
    ax.plot([s*R_loop,s*(R_loop-0.04)],[0,-0.03],[dz_,dz_],
            color=A_RED, lw=2.5, zorder=18)
ax.text(0,-0.08,dz_+0.03,'D = 1.00 m (39.4")',
        fontsize=14, fontweight='bold', color='#ef9a9a',
        fontfamily='sans-serif', ha='center', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#080e1a', alpha=0.9,
                  edgecolor=A_RED, lw=1.5))

# profile height
ph = R_loop + 0.20
ax.plot([ph,ph],[0,0],[z_roof, z_lp+0.06], color=A_GRN, lw=2.5, zorder=18)
for dz__ in [z_roof, z_lp+0.06]:
    ax.plot([ph-0.025,ph+0.025],[0,0],[dz__,dz__],
            color=A_GRN, lw=2.5, zorder=18)
ax.text(ph+0.06,0,(z_roof+z_lp)/2+0.03,'Profile\n~10 cm',
        fontsize=12, fontweight='bold', color='#a5d6a7',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#080e1a', alpha=0.9,
                  edgecolor=A_GRN, lw=1.5))

# FRONT label
ax.text(2.65,0,z_g+0.18,'FRONT \u25b6', fontsize=13, fontweight='bold',
        color='#546e7a', fontfamily='sans-serif', ha='left', zorder=20)

# ── ground / road ────────────────────────────────────────────────────
for g in np.linspace(-2.0,2.0,14):
    ax.plot([g,g],[-1.2,1.2],[z_g-0.01,z_g-0.01],
            color='#131d2e', lw=0.4, alpha=0.25, zorder=1)
    ax.plot([-2.0,2.0],[g*0.6,g*0.6],[z_g-0.01,z_g-0.01],
            color='#131d2e', lw=0.4, alpha=0.25, zorder=1)
# road lane markings
ax.plot([-2.0,2.0],[0,0],[z_g-0.008,z_g-0.008],
        color='#ffd600', lw=1.5, ls='--', alpha=0.15, zorder=1)


# ═════════════════════════════════════════════════════════════════════════
#  PANEL A — Dual-Band Specifications  (right, upper)
# ═════════════════════════════════════════════════════════════════════════
ax_s = fig.add_axes([0.58, 0.52, 0.41, 0.38])
ax_s.set_facecolor('#e3f2fd')
ax_s.set_xlim(0, 10); ax_s.set_ylim(0, 10); ax_s.axis('off')
for sp in ax_s.spines.values():
    sp.set_visible(True); sp.set_color(A_BLUE); sp.set_linewidth(2.5)

ax_s.text(5, 9.65, 'Dual-Band NVIS Loop  --  80 m / 40 m Specifications',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TD, fontfamily='sans-serif')

# sub-headers
ax_s.add_patch(FancyBboxPatch((0.1,8.85), 9.8, 0.55,
               boxstyle="round,pad=0.06", facecolor='#1565c0', alpha=0.9))
ax_s.text(0.3, 9.12, 'Parameter', fontsize=14, fontweight='bold',
          color='white', va='center', fontfamily='sans-serif')
ax_s.text(5.0, 9.12, '80 m Band', fontsize=14, fontweight='bold',
          color='#ffd600', va='center', ha='center', fontfamily='sans-serif')
ax_s.text(8.0, 9.12, '40 m Band', fontsize=14, fontweight='bold',
          color='#ffd600', va='center', ha='center', fontfamily='sans-serif')

specs = [
    ('Frequency',       '3.500 - 4.000 MHz',       '7.000 - 7.300 MHz'),
    ('Wavelength',      '85.7 m (\u03bb)',          '42.3 m (\u03bb)'),
    ('Loop / \u03bb',   '0.037\u03bb',              '0.074\u03bb'),
    ('NVIS Reliability','Excellent (24h)',           'Excellent (daytime)'),
    ('Inductance',      '2.45 \u03bcH',             '2.45 \u03bcH'),
    ('Reactance (XL)',  '~58 \u03a9',               '~109 \u03a9'),
    ('Tuning Cap',      '~735 pF (Bank B)',         '~210 pF (Bank A)'),
    ('Cap Voltage @50W','~2.4 kV peak',             '~3.6 kV peak'),
    ('Radiation Res.',  '~0.5 m\u03a9',             '~6.0 m\u03a9'),
    ('Loss Res. (Cu)',  '~23 m\u03a9',              '~32 m\u03a9'),
    ('Cap ESR (Q=10k)', '~5.8 m\u03a9',            '~11 m\u03a9'),
    ('Efficiency',      '~1.7 %',                   '~12 %'),
    ('ERP @ 50 W',     '~0.9 W',                   '~6.0 W'),
    ('Bandwidth',       '~1.5 kHz',                 '~5-8 kHz'),
    ('Q Factor',        '~2000',                    '~1000'),
    ('NVIS Range',      '0 - 600 km (night)',       '0 - 600 km (day)'),
]

rc = ['#bbdefb', '#ffffff']
y0 = 8.60; dy = 0.50
for i, (lbl, v80, v40) in enumerate(specs):
    y = y0 - i * dy
    ax_s.add_patch(FancyBboxPatch((0.1,y-0.20), 9.8, 0.44,
                   boxstyle="round,pad=0.04", facecolor=rc[i%2], alpha=0.7))
    ax_s.text(0.3, y, lbl, fontsize=12, fontweight='bold', va='center',
              color=TD, fontfamily='sans-serif')
    ax_s.text(5.0, y, v80, fontsize=12, va='center', ha='center',
              color=TD, fontfamily='sans-serif')
    ax_s.text(8.0, y, v40, fontsize=12, va='center', ha='center',
              color=TD, fontfamily='sans-serif')

# vertical dividers
ax_s.plot([3.7,3.7],[0.2,8.85], color='#90caf9', lw=1.5, alpha=0.5)
ax_s.plot([6.5,6.5],[0.2,8.85], color='#90caf9', lw=1.5, alpha=0.5)

# note
ax_s.text(5, 0.30,
          '80 m: low efficiency but NVIS propagation is extremely reliable '
          '24h  |  0.9 W ERP is usable for NVIS SSB/CW within 400 km',
          fontsize=10.5, fontweight='bold', ha='center', va='center',
          color='#0d47a1', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.2', facecolor='#e1f5fe',
                    edgecolor='#0d47a1', lw=1.5, alpha=0.9))


# ═════════════════════════════════════════════════════════════════════════
#  PANEL B — Installation Guide  (right, lower)
# ═════════════════════════════════════════════════════════════════════════
ax_n = fig.add_axes([0.58, 0.06, 0.41, 0.40])
ax_n.set_facecolor('#fff3e0')
ax_n.set_xlim(0, 10); ax_n.set_ylim(0, 10); ax_n.axis('off')
for sp in ax_n.spines.values():
    sp.set_visible(True); sp.set_color('#ff9800'); sp.set_linewidth(2.5)

ax_n.text(5, 9.75, 'Installation & Dual-Band Operation Guide',
          fontsize=22, fontweight='bold', ha='center', va='top',
          color=TD, fontfamily='sans-serif')

notes = [
    ('1.', 'BUILD LOOP',
     'Cut 3.20 m of 22 mm Cu tube. Fill with sand, cap ends,\n'
     'bend into 1.00 m circle. Leave 20 mm gap at top for cap box.'),
    ('2.', 'COUPLING LOOP',
     'Bend 65 cm of RG-213 into 200 mm Faraday loop. Shield\n'
     'both ends, center conductor one end. Mount at loop bottom.'),
    ('3.', 'DUAL-BAND CAP BOX',
     'Install 2 vacuum caps in IP65 box: Bank A (30-250 pF)\n'
     'for 40m, Bank B (150-900 pF) for 80m. Wire DPDT relay.'),
    ('4.', 'MOTOR + CONTROLLER',
     'Mount NEMA17 stepper with worm gear on active cap shaft.\n'
     'Wire ESP32/Arduino controller with band-switch + tune knob.'),
    ('5.', 'MAG-MOUNT INSTALL',
     'Place 4x NdFeB mag-mounts (40 kg each) on clean roof.\n'
     'Attach 100 mm HDPE standoffs. Clip loop horizontal on top.'),
    ('6.', 'ROUTE & CONNECT',
     'Run RG-58 + 4-wire motor cable through window seal gap.\n'
     'Add ferrite choke balun at feedpoint. Connect controller.'),
    ('7.', 'TUNE & OPERATE',
     'Select band on controller. Motor auto-tunes cap to target\n'
     'freq. BW: ~1.5 kHz (80m), ~6 kHz (40m). Max 50 W.'),
]

rcn = ['#ffe0b2', '#ffffff']
y0n = 9.15; dyn = 1.18
for i, (num, title, desc) in enumerate(notes):
    y = y0n - i * dyn
    ax_n.add_patch(FancyBboxPatch((0.2,y-0.48), 9.6, 1.02,
                   boxstyle="round,pad=0.08", facecolor=rcn[i%2], alpha=0.6))
    ax_n.add_patch(plt.Circle((0.55, y), 0.30, facecolor='#e65100',
                   edgecolor='white', lw=2, zorder=10,
                   transform=ax_n.transData))
    ax_n.text(0.55, y, num, fontsize=14, fontweight='bold', color='white',
              ha='center', va='center', fontfamily='sans-serif', zorder=11)
    ax_n.text(1.05, y+0.22, title, fontsize=14, fontweight='bold',
              va='center', color='#bf360c', fontfamily='sans-serif')
    ax_n.text(1.05, y-0.22, desc, fontsize=11, va='center',
              color='#333', fontfamily='sans-serif', linespacing=1.3)

# BOM
ax_n.text(5, 0.85,
          'BOM: 22mm Cu tube $30  |  Vacuum cap x2 $220  |  '
          'DPDT relay $15  |  NdFeB mounts $30  |  HDPE + clips $12',
          fontsize=10.5, fontweight='bold', ha='center', va='center',
          color='#e65100', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.22', facecolor='#fff8e1',
                    edgecolor='#e65100', lw=2, alpha=0.9))
ax_n.text(5, 0.38,
          'RG-213 $8  |  RG-58 $10  |  Stepper kit $18  |  '
          'ESP32 controller $12  |  IP65 box $12  |  Hardware $15  =  Total ~$382',
          fontsize=10.5, fontweight='bold', ha='center', va='center',
          color='#e65100', fontfamily='sans-serif',
          bbox=dict(boxstyle='round,pad=0.22', facecolor='#fff8e1',
                    edgecolor='#e65100', lw=2, alpha=0.9))


# ═════════════════════════════════════════════════════════════════════════
#  INSET — Radiation Pattern (bottom-left)
# ═════════════════════════════════════════════════════════════════════════
ax_rp = fig.add_axes([0.005, 0.03, 0.18, 0.24], projection='polar')
ax_rp.set_facecolor('#0f1a2e')
ax_rp.set_theta_zero_location('N')
ax_rp.set_theta_direction(-1)

elev = np.linspace(0, np.pi, 180)
pat_base = np.abs(np.cos(elev))
gf = np.abs(np.sin(2*np.pi*0.002*np.sin(elev)) + 0.8)
pat = pat_base * gf; pat /= pat.max()

ax_rp.plot(elev, pat, color='#ff8a65', lw=2.5)
ax_rp.plot(-elev, pat, color='#ff8a65', lw=2.5)
ax_rp.fill_between(elev, 0, pat, alpha=0.12, color='#ff8a65')
ax_rp.fill_between(-elev, 0, pat, alpha=0.12, color='#ff8a65')

# NVIS zone
nv = np.linspace(np.radians(70), np.radians(90), 20)
nv_r = np.interp(nv, elev, pat)
ax_rp.fill_between(nv, 0, nv_r, alpha=0.4, color=GOLD)
ax_rp.fill_between(-nv, 0, nv_r, alpha=0.4, color=GOLD)

ax_rp.set_ylim(0,1.15)
ax_rp.set_rticks([0.25,0.5,0.75,1.0])
ax_rp.set_yticklabels(['-12','-6','-3','0 dB'], fontsize=7, color='#78909c')
ax_rp.set_xticks(np.radians(range(0,360,30)))
ax_rp.set_xticklabels([f'{d}\u00b0' for d in range(0,360,30)],
                       fontsize=7, color='#78909c')
ax_rp.tick_params(colors='#546e7a')
ax_rp.grid(True, color='#37474f', alpha=0.4)
ax_rp.set_title('Elevation Pattern (Both Bands)', fontsize=12,
                fontweight='bold', color='#e0e0e0', pad=14,
                fontfamily='sans-serif')
ax_rp.annotate('NVIS\nZone', xy=(np.radians(80), 0.85),
               fontsize=10, fontweight='bold', color=GOLD, ha='center',
               bbox=dict(boxstyle='round,pad=0.15', facecolor='#080e1a',
                         edgecolor=GOLD, alpha=0.9))
for sp in ax_rp.spines.values():
    sp.set_color('#546e7a'); sp.set_linewidth(1.5)


# ═════════════════════════════════════════════════════════════════════════
#  INSET — Coverage Map
# ═════════════════════════════════════════════════════════════════════════
ax_cov = fig.add_axes([0.195, 0.03, 0.18, 0.24])
ax_cov.set_facecolor('#0f1a2e')
ax_cov.set_aspect('equal')

ct = np.linspace(0, 2*np.pi, 100)
for r_km, al_, lbl in [(600,0.12,'600 km'),(400,0.22,'400 km'),
                        (200,0.38,'200 km'),(50,0.55,'50 km')]:
    rn = r_km/700
    ax_cov.fill(rn*np.cos(ct), rn*np.sin(ct), alpha=al_, color='#4dd0e1')
    ax_cov.plot(rn*np.cos(ct), rn*np.sin(ct), color='#4dd0e1', lw=1, alpha=0.5)
    ax_cov.text(0, rn+0.03, lbl, fontsize=9, color='#80deea',
                ha='center', va='bottom', fontweight='bold',
                fontfamily='sans-serif')

ax_cov.plot(0, 0, 's', color=A_RED, ms=8, zorder=10)
ax_cov.text(0.05, -0.06, 'TX', fontsize=10, fontweight='bold', color=A_RED,
            fontfamily='sans-serif')

ax_cov.annotate('No skip zone!\n80m covers 0-600 km\n'
                'night & day\n40m covers 0-600 km\ndaytime',
                xy=(0.50, -0.60), fontsize=9, fontweight='bold',
                color='#a5d6a7', fontfamily='sans-serif', ha='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#080e1a',
                          edgecolor='#4caf50', alpha=0.92))

ax_cov.set_xlim(-1.05,1.05); ax_cov.set_ylim(-1.05,1.05)
ax_cov.set_title('NVIS Coverage (80m + 40m)', fontsize=12,
                 fontweight='bold', color='#e0e0e0', pad=10,
                 fontfamily='sans-serif')
ax_cov.axis('off')


# ═════════════════════════════════════════════════════════════════════════
#  INSET — Switching Diagram (schematic)
# ═════════════════════════════════════════════════════════════════════════
ax_sw = fig.add_axes([0.39, 0.03, 0.18, 0.24])
ax_sw.set_facecolor('#0f1a2e')
ax_sw.set_xlim(0, 10); ax_sw.set_ylim(0, 10)
ax_sw.axis('off')
for sp in ax_sw.spines.values():
    sp.set_visible(True); sp.set_color('#78909c'); sp.set_linewidth(1.5)

ax_sw.set_title('Band Switching Schematic', fontsize=12,
                fontweight='bold', color='#e0e0e0', pad=10,
                fontfamily='sans-serif')

# loop symbol (top)
loop_t = np.linspace(0, 2*np.pi, 60)
ax_sw.plot(5+1.5*np.cos(loop_t), 8.2+0.6*np.sin(loop_t),
           color=CU, lw=3)
ax_sw.text(5, 8.2, 'Main Loop\n1.0 m  |  22 mm Cu',
           fontsize=9, fontweight='bold', color=CU_HI,
           ha='center', va='center', fontfamily='sans-serif')

# gap lines down to relay
ax_sw.plot([3.5, 3.5], [7.6, 6.2], color=CU, lw=2.5)
ax_sw.plot([6.5, 6.5], [7.6, 6.2], color=CU, lw=2.5)

# DPDT relay box
ax_sw.add_patch(FancyBboxPatch((3.0, 5.0), 4.0, 1.2,
                boxstyle="round,pad=0.1", facecolor='#37474f',
                edgecolor='#78909c', lw=2))
ax_sw.text(5, 5.6, 'DPDT Relay', fontsize=11, fontweight='bold',
           color='#e0e0e0', ha='center', va='center', fontfamily='sans-serif')
# relay indicator LED
ax_sw.add_patch(plt.Circle((3.4, 5.3), 0.12, facecolor='#f44336',
                edgecolor='white', lw=1, transform=ax_sw.transData))

# Bank A line (left) — 40m
ax_sw.plot([3.5, 2.0], [5.0, 3.8], color='#42a5f5', lw=2.5)
ax_sw.plot([6.5, 2.0], [5.0, 3.8], color='#42a5f5', lw=2.5, ls='--', alpha=0.4)
ax_sw.add_patch(FancyBboxPatch((0.5, 2.8), 3.0, 1.0,
                boxstyle="round,pad=0.08", facecolor='#0d47a1',
                edgecolor='#42a5f5', lw=1.5))
ax_sw.text(2.0, 3.3, 'Bank A\n30-250 pF\n40 m', fontsize=9,
           fontweight='bold', color='#bbdefb', ha='center', va='center',
           fontfamily='sans-serif')

# Bank B line (right) — 80m
ax_sw.plot([3.5, 8.0], [5.0, 3.8], color='#ef5350', lw=2.5, ls='--', alpha=0.4)
ax_sw.plot([6.5, 8.0], [5.0, 3.8], color='#ef5350', lw=2.5)
ax_sw.add_patch(FancyBboxPatch((6.5, 2.8), 3.0, 1.0,
                boxstyle="round,pad=0.08", facecolor='#b71c1c',
                edgecolor='#ef5350', lw=1.5))
ax_sw.text(8.0, 3.3, 'Bank B\n150-900 pF\n80 m', fontsize=9,
           fontweight='bold', color='#ffcdd2', ha='center', va='center',
           fontfamily='sans-serif')

# stepper motor (bottom center)
ax_sw.add_patch(FancyBboxPatch((3.5, 1.0), 3.0, 1.0,
                boxstyle="round,pad=0.08", facecolor='#455a64',
                edgecolor='#78909c', lw=1.5))
ax_sw.text(5, 1.5, 'NEMA17 Stepper\n+ Worm Gear', fontsize=9,
           fontweight='bold', color='#e0e0e0', ha='center', va='center',
           fontfamily='sans-serif')
ax_sw.plot([5, 5], [2.0, 2.8], color='#78909c', lw=2)
ax_sw.plot([5, 5], [2.0, 2.8], color='#78909c', lw=2)
# arrows to both banks
ax_sw.annotate('', xy=(2.0, 2.8), xytext=(5, 2.0),
               arrowprops=dict(arrowstyle='->', color='#78909c', lw=1.5))
ax_sw.annotate('', xy=(8.0, 2.8), xytext=(5, 2.0),
               arrowprops=dict(arrowstyle='->', color='#78909c', lw=1.5))

# ESP32 controller
ax_sw.add_patch(FancyBboxPatch((3.5, -0.2), 3.0, 0.8,
                boxstyle="round,pad=0.08", facecolor='#1b5e20',
                edgecolor='#4caf50', lw=1.5))
ax_sw.text(5, 0.2, 'ESP32 Controller', fontsize=9, fontweight='bold',
           color='#c8e6c9', ha='center', va='center', fontfamily='sans-serif')
ax_sw.plot([5, 5], [0.6, 1.0], color='#4caf50', lw=1.5)


# ═════════════════════════════════════════════════════════════════════════
#  TITLE BANNER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.003, 0.925), 0.994, 0.070,
    boxstyle="round,pad=0.008", facecolor='#0d47a1', alpha=0.95,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.975,
         'Dual-Band NVIS 80 m / 40 m Mobile Antenna  \u2014  '
         'Low-Profile Magnetic Loop on Car Roof  \u2014  3D Installation View',
         fontsize=34, fontweight='bold', color='#ffffff',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)
fig.text(0.50, 0.940,
         '1.00 m Loop  |  22 mm Cu  |  Relay-Switched Dual Vacuum Cap  '
         '|  10 cm Profile  |  80m: ~1.7%  40m: ~12%  |  Mag-Mount  '
         '|  ESP32 + Stepper Tuning  |  NVIS 0\u2013600 km',
         fontsize=19, fontweight='bold', color=GOLD,
         ha='center', va='center', fontfamily='sans-serif', zorder=3)


# ═════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.003, 0.001), 0.994, 0.025,
    boxstyle="round,pad=0.005", facecolor='#0d47a1', alpha=0.85,
    transform=fig.transFigure, zorder=2))
fig.text(0.50, 0.014,
         'Dual-Band NVIS 80m/40m Car-Roof STL  |  HS0ZNR  |  '
         '3.5\u20134.0 / 7.0\u20137.3 MHz  |  Generated 2026-02-23',
         fontsize=17, fontweight='bold', color='#e3f2fd',
         ha='center', va='center', fontfamily='sans-serif', zorder=3)


# ═════════════════════════════════════════════════════════════════════════
#  SAVE
# ═════════════════════════════════════════════════════════════════════════
out = r'C:\Users\Jakkrit\.local\bin\NVIS_80_40m_Car_Roof_3D.jpg'
fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor(),
            pil_kwargs={'quality': 95})
plt.close()
print(f'Saved: {out}')
print(f'Size: {48*DPI} x {32*DPI} px = {48}x{32} in @ {DPI} DPI')
