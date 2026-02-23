#!/usr/bin/env python3
"""
OPTIMIZED Dual-Band NVIS 80m/40m Rectangular Ag-Cu Loop on Sedan Roof — 3D Poster
Key optimizations vs baseline:
  - 1.40 × 0.80 m rectangular loop (Area = 1.12 m², ≈ same as 1.2 m circle)
  - 22 mm   -> 28 mm tube       (Rl down 25%)
  - Silver-plated copper         (Rs down 6%)
  - 2-turn for 80m / 1-turn for 40m via relay  (Rr up 4x on 80m)
  Result: 40m 12%->24%  |  80m 1.7%->5.2%  |  ~3x improvement
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyBboxPatch
import numpy as np

DPI = 200
fig = plt.figure(figsize=(48, 34), dpi=DPI, facecolor='#080e1a')

# ── palette ────────────────────────────────────────────────────────────
CU       = '#b5651d';  CU_HI  = '#e8a54a';  CU_DK = '#8b4513'
CU_CPL   = '#a0522d';  A_BLUE = '#1565c0';  A_RED = '#c62828'
A_GRN    = '#2e7d32';  GOLD   = '#ffd600';  TD    = '#1a1a2e'
N = 220

# ═════════════════════════════════════════════════════════════════════════
#  MAIN 3-D VIEW  (upper-left)
# ═════════════════════════════════════════════════════════════════════════
ax = fig.add_axes([0.005, 0.30, 0.56, 0.58], projection='3d',
                  computed_zorder=False)
ax.set_facecolor('#0f1a2e')
ax.set_xlim(-2.4, 2.4);  ax.set_ylim(-1.5, 1.5);  ax.set_zlim(-0.40, 1.70)
ax.view_init(elev=24, azim=-46)
ax.set_box_aspect([2.4, 1.5, 1.05])
ax.axis('off')

# ── helpers ────────────────────────────────────────────────────────────
def tube(a, px,py,pz, c, lw=7, hc=None, al=1.0, zo=5):
    a.plot(px,py,pz, color=c, lw=lw, solid_capstyle='round', alpha=al, zorder=zo)
    if hc:
        a.plot(px,py,pz, color=hc, lw=lw*0.4, solid_capstyle='round',
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
    th = np.linspace(0,2*np.pi, n+1)
    for i in range(n):
        face = [[cx+r*np.cos(th[i]),cy+r*np.sin(th[i]),zb],
                [cx+r*np.cos(th[i+1]),cy+r*np.sin(th[i+1]),zb],
                [cx+r*np.cos(th[i+1]),cy+r*np.sin(th[i+1]),zt],
                [cx+r*np.cos(th[i]),cy+r*np.sin(th[i]),zt]]
        qpoly(a, face, fc, ec=ec, al=al, lw=0.5, zo=zo)
    cap = [[cx+r*np.cos(t),cy+r*np.sin(t),zt] for t in th]
    qpoly(a, cap, fc, ec=ec, al=al, zo=zo+1)


# ═════════════════════════════════════════════════════════════════════════
#  SEDAN — realistic mid-size sedan (lower, swoopy, 3-box)
# ═════════════════════════════════════════════════════════════════════════
z_g = -0.15  # sedan sits lower than SUV

# Sedan body profile — 24 cross-sections, more taper front and rear
bx = np.array([-2.30,-2.18,-2.05,-1.90,-1.72,-1.50,-1.28,-1.05,
               -0.80,-0.55,-0.30,-0.05, 0.20, 0.45, 0.70, 0.95,
                1.20, 1.45, 1.70, 1.90, 2.08, 2.22, 2.35, 2.45])
bw = np.array([ 0.42, 0.62, 0.76, 0.84, 0.89, 0.92, 0.93, 0.93,
                0.93, 0.93, 0.93, 0.93, 0.93, 0.93, 0.93, 0.92,
                0.90, 0.86, 0.80, 0.72, 0.62, 0.52, 0.40, 0.28])
# Sedan beltline — lower at 0.48
bzt = np.array([z_g+0.28, z_g+0.36, z_g+0.42, z_g+0.46, z_g+0.47,
                z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48,
                z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48, z_g+0.48,
                z_g+0.48, z_g+0.47, z_g+0.46, z_g+0.44, z_g+0.42,
                z_g+0.38, z_g+0.34, z_g+0.28, z_g+0.22])

# Sedan cabin — curved roofline peaking over front seats, sloping to rear
cx_ = np.array([-1.50,-1.20,-0.85,-0.45, 0.00, 0.40, 0.75, 1.05, 1.25, 1.40])
cw_ = np.array([ 0.78, 0.84, 0.88, 0.90, 0.90, 0.90, 0.88, 0.85, 0.80, 0.72])
# curved roofline — peaks over front seats, slopes down to rear
czt = np.array([z_g+0.48, z_g+0.72, z_g+0.83, z_g+0.87, z_g+0.88,
                z_g+0.88, z_g+0.86, z_g+0.82, z_g+0.76, z_g+0.68])

# metallic dark blue paint — 4-tone shading
paint_l  = '#2c4a7c'   # left side (viewer facing — highlight)
paint_r  = '#1a3058'   # right side (shadow)
paint_t  = '#3a5e96'   # top (brightest)
paint_bt = '#0e1a30'   # bottom (darkest)
paint_f  = '#2a4570'   # front face
paint_re = '#1e3460'   # rear face
paint_hi = '#4a72a8'   # character line highlight
glass_c  = '#5bc0de'
roof_c   = '#3a5e96'
pillar_c = '#0e1a30'
trim_c   = '#b0bec5'   # chrome window trim

# ── lower body shell ─────────────────────────────────────────────────
for i in range(len(bx)-1):
    x0,x1=bx[i],bx[i+1]; w0,w1=bw[i],bw[i+1]; zt0,zt1=bzt[i],bzt[i+1]
    qpoly(ax,[[x0,-w0,z_g],[x1,-w1,z_g],[x1,-w1,zt1],[x0,-w0,zt0]],paint_l)
    qpoly(ax,[[x0,w0,z_g],[x1,w1,z_g],[x1,w1,zt1],[x0,w0,zt0]],paint_r)
    qpoly(ax,[[x0,-w0,zt0],[x1,-w1,zt1],[x1,w1,zt1],[x0,w0,zt0]],paint_t)
    qpoly(ax,[[x0,-w0,z_g],[x1,-w1,z_g],[x1,w1,z_g],[x0,w0,z_g]],paint_bt,zo=1)

# front face (sloped nose for sedan)
qpoly(ax,[[bx[-1],-bw[-1],z_g],[bx[-1],bw[-1],z_g],
          [bx[-1],bw[-1],bzt[-1]],[bx[-1],-bw[-1],bzt[-1]]],paint_f)
# rear face (sedan trunk — shorter)
qpoly(ax,[[bx[0],-bw[0],z_g],[bx[0],bw[0],z_g],
          [bx[0],bw[0],bzt[0]],[bx[0],-bw[0],bzt[0]]],paint_re)

# ── character line (body crease at beltline — sedan signature) ───────
for s in [-1, 1]:
    cl_xs = np.linspace(bx[2], bx[-3], 60)
    cl_ys = np.array([s*(np.interp(x, bx, bw)+0.003) for x in cl_xs])
    cl_zs = np.array([np.interp(x, bx, bzt)-0.04 for x in cl_xs])
    ax.plot(cl_xs, cl_ys, cl_zs, color=paint_hi, lw=2.0, alpha=0.7, zorder=3)

# ── side skirts (subtle lower body trim) ─────────────────────────────
for s in [-1, 1]:
    sk_x0, sk_x1 = -1.40, 1.40
    sk_xs = np.linspace(sk_x0, sk_x1, 40)
    sk_ys = np.array([s*(np.interp(x, bx, bw)+0.004) for x in sk_xs])
    sk_zs = np.full(40, z_g+0.02)
    ax.plot(sk_xs, sk_ys, sk_zs, color='#1a2a40', lw=3.5, alpha=0.85, zorder=3)

# ── cabin greenhouse ─────────────────────────────────────────────────
for i in range(len(cx_)-1):
    x0,x1=cx_[i],cx_[i+1]; w0,w1=cw_[i],cw_[i+1]
    zb0=np.interp(x0,bx,bzt); zb1=np.interp(x1,bx,bzt)
    zt0,zt1=czt[i],czt[i+1]
    # left glass
    qpoly(ax,[[x0,-w0,zb0],[x1,-w1,zb1],[x1,-w1,zt1],[x0,-w0,zt0]],
          glass_c,al=0.28,lw=1.2,zo=3)
    # right glass
    qpoly(ax,[[x0,w0,zb0],[x1,w1,zb1],[x1,w1,zt1],[x0,w0,zt0]],
          glass_c,al=0.28,lw=1.2,zo=3)
    # roof
    qpoly(ax,[[x0,-w0,zt0],[x1,-w1,zt1],[x1,w1,zt1],[x0,w0,zt0]],
          roof_c,al=0.95,lw=0.8,zo=4)

# ── chrome window trim (sedan detail) ───────────────────────────────
for s in [-1, 1]:
    tr_xs = [cx_[j] for j in range(len(cx_))]
    tr_ys = [s*cw_[j] for j in range(len(cx_))]
    tr_zb = [np.interp(cx_[j], bx, bzt) for j in range(len(cx_))]
    tr_zt = [czt[j] for j in range(len(cx_))]
    # bottom trim (along beltline)
    ax.plot(tr_xs, tr_ys, tr_zb, color=trim_c, lw=2.0, alpha=0.6, zorder=5)
    # top trim (along roofline)
    ax.plot(tr_xs, tr_ys, tr_zt, color=trim_c, lw=1.5, alpha=0.5, zorder=5)

# windshield (more sloped — sedan style)
xwf=cx_[-1]; wwf=cw_[-1]; zbwf=np.interp(xwf,bx,bzt); ztwf=czt[-1]
qpoly(ax,[[xwf,-wwf,zbwf],[xwf,wwf,zbwf],
          [xwf-0.20,wwf*0.92,ztwf],[xwf-0.20,-wwf*0.92,ztwf]],
      glass_c,al=0.30,lw=2,zo=3)

# rear glass (sloped — sedan fastback style)
xrg=cx_[0]; wrg=cw_[0]; zbrg=np.interp(xrg,bx,bzt); ztrg=czt[0]
qpoly(ax,[[xrg,-wrg,zbrg],[xrg,wrg,zbrg],
          [xrg+0.12,wrg*0.92,ztrg],[xrg+0.12,-wrg*0.92,ztrg]],
      glass_c,al=0.30,lw=2,zo=3)

# ── interior headrests (visible through glass as simple shapes) ──────
for hx_, hy_ in [(0.30, -0.28), (0.30, 0.28), (-0.40, -0.28), (-0.40, 0.28)]:
    hr_zb = np.interp(hx_, bx, bzt) + 0.10
    hr_zt = hr_zb + 0.08
    box3d(ax, hx_, hy_, (hr_zb+hr_zt)/2, 0.04, 0.03, 0.04,
          ['#1a1a1a','#222','#2a2a2a','#1a1a1a','#151515','#222'],
          ec='#111', al=0.35, zo=3)

# ── A / B / C pillars (sedan — 3 pillars, no D-pillar) ──────────────
pw=0.065
pillar_locs = [
    (cx_[-1], cw_[-1]),   # A-pillar (front)
    (cx_[4],  cw_[4]),    # B-pillar (middle)
    (cx_[1],  cw_[1]),    # C-pillar (rear)
]
for px_,pw_ in pillar_locs:
    zb_=np.interp(px_,bx,bzt); zt_=np.interp(px_,cx_,czt)
    for s in [-1,1]:
        qpoly(ax,[[px_-pw,s*pw_,zb_],[px_+pw,s*pw_,zb_],
                  [px_+pw,s*pw_,zt_],[px_-pw,s*pw_,zt_]],
              pillar_c,al=0.92,lw=1.5,zo=4)

# ── door panel lines (4 doors) ──────────────────────────────────────
for dx in [-0.50, 0.25, 0.95]:
    wd=np.interp(dx,bx,bw); zbd=z_g+0.04; ztd=np.interp(dx,bx,bzt)-0.02
    for s in [-1,1]:
        ax.plot([dx,dx],[s*(wd+0.006),s*(wd+0.006)],[zbd,ztd],
                color='#0e1a30',lw=2,zorder=3)

# ── door handles (chrome) ───────────────────────────────────────────
for hx in [-0.85, -0.10, 0.60, 1.15]:
    hw_=np.interp(hx,bx,bw); hz_=np.interp(hx,bx,bzt)-0.06
    for s in [-1,1]:
        ax.plot([hx-0.06,hx+0.06],[s*(hw_+0.008),s*(hw_+0.008)],[hz_,hz_],
                color='#b0bec5',lw=3.0,solid_capstyle='round',zorder=4)

# ── side mirrors (sedan-style, more compact) ────────────────────────
for s in [-1,1]:
    mx_=cx_[-1]-0.05; mw_=np.interp(mx_,bx,bw)
    my_=s*(mw_+0.15); mz_=np.interp(mx_,bx,bzt)+0.04
    # mirror arm
    ax.plot([mx_,mx_],[s*mw_,my_],[mz_,mz_],color=pillar_c,lw=3,zorder=4)
    # housing (compact)
    qpoly(ax,[[mx_-0.05,my_,mz_-0.035],[mx_+0.05,my_,mz_-0.035],
              [mx_+0.05,my_,mz_+0.035],[mx_-0.05,my_,mz_+0.035]],
          pillar_c,al=0.9,zo=4)
    # mirror glass
    qpoly(ax,[[mx_-0.04,my_+s*0.005,mz_-0.028],[mx_+0.04,my_+s*0.005,mz_-0.028],
              [mx_+0.04,my_+s*0.005,mz_+0.028],[mx_-0.04,my_+s*0.005,mz_+0.028]],
          '#90caf9',al=0.5,zo=5)

# ── headlights (sleek sedan-style, swept-back) ──────────────────────
for s in [-1,1]:
    hlx=bx[-1]+0.015
    # main projector beam
    qpoly(ax,[[hlx,s*0.06,z_g+0.18],[hlx,s*bw[-3]*0.80,z_g+0.18],
              [hlx,s*bw[-3]*0.75,z_g+0.30],[hlx,s*0.06,z_g+0.30]],
          '#fff9c4',ec='#fdd835',al=0.85,lw=1.2,zo=3)
    # lower fog light
    qpoly(ax,[[hlx,s*0.10,z_g+0.06],[hlx,s*bw[-3]*0.60,z_g+0.06],
              [hlx,s*bw[-3]*0.60,z_g+0.12],[hlx,s*0.10,z_g+0.12]],
          '#e0e0e0',ec='#bdbdbd',al=0.75,lw=1,zo=3)
    # DRL strip (thin LED line)
    ax.plot([hlx+0.005,hlx+0.005],[s*0.06,s*bw[-3]*0.78],
            [z_g+0.31,z_g+0.31],color='#bbdefb',lw=2.0,alpha=0.6,zorder=4)

# ── taillights (horizontal, sedan-style LED strip) ──────────────────
for s in [-1,1]:
    tlx=bx[0]-0.015
    qpoly(ax,[[tlx,s*0.10,z_g+0.16],[tlx,s*bw[2]*0.82,z_g+0.16],
              [tlx,s*bw[2]*0.82,z_g+0.28],[tlx,s*0.10,z_g+0.28]],
          '#d32f2f',ec='#b71c1c',al=0.85,lw=1.2,zo=3)
    # LED strip
    ax.plot([tlx-0.005,tlx-0.005],[s*0.12,s*bw[2]*0.78],
            [z_g+0.22,z_g+0.22],color='#ff8a80',lw=2.5,alpha=0.7,zorder=4)
# trunk lid tail light bridge (connects left and right)
tlx_b=bx[0]-0.012
qpoly(ax,[[tlx_b,-0.10,z_g+0.24],[tlx_b,0.10,z_g+0.24],
          [tlx_b,0.10,z_g+0.27],[tlx_b,-0.10,z_g+0.27]],
      '#d32f2f',ec='#b71c1c',al=0.6,lw=0.8,zo=3)

# ── sedan trunk lip / spoiler ────────────────────────────────────────
trunk_x = bx[2]
trunk_w = bw[2]
trunk_z = bzt[2] + 0.005
ax.plot([trunk_x, trunk_x], [-trunk_w*0.85, trunk_w*0.85], [trunk_z, trunk_z],
        color=paint_hi, lw=3.0, alpha=0.7, zorder=4)

# ── front grille (split-pattern sedan grille) ────────────────────────
gx_=bx[-1]+0.02; gw_=bw[-2]*0.82
# upper grille (narrower, more elegant)
qpoly(ax,[[gx_,-gw_,z_g+0.16],[gx_,gw_,z_g+0.16],
          [gx_,gw_,z_g+0.30],[gx_,-gw_,z_g+0.30]],
      '#111820',al=0.92,zo=3)
# chrome surround
for gz_ in [z_g+0.16, z_g+0.30]:
    ax.plot([gx_+0.005,gx_+0.005],[-gw_*0.95,gw_*0.95],[gz_,gz_],
            color='#b0bec5',lw=2,zorder=4)
# split pattern — horizontal bars with centre division
for gz_ in np.linspace(z_g+0.18, z_g+0.28, 4):
    ax.plot([gx_+0.004,gx_+0.004],[-gw_*0.88,-0.02],[gz_,gz_],
            color='#37474f',lw=1.5,zorder=4)
    ax.plot([gx_+0.004,gx_+0.004],[0.02,gw_*0.88],[gz_,gz_],
            color='#37474f',lw=1.5,zorder=4)
# lower intake (wider, sportier)
qpoly(ax,[[gx_,-gw_*0.90,z_g+0.02],[gx_,gw_*0.90,z_g+0.02],
          [gx_,gw_*0.90,z_g+0.12],[gx_,-gw_*0.90,z_g+0.12]],
      '#0a0f15',al=0.92,zo=3)

# ── brand badge (on grille) ──────────────────────────────────────────
bt_=np.linspace(0,2*np.pi,16)
qpoly(ax,[[gx_+0.01,0.04*np.cos(t),z_g+0.23+0.04*np.sin(t)] for t in bt_],
      '#b0bec5',ec='#78909c',al=0.9,zo=5)

# ── license plates ───────────────────────────────────────────────────
for lx_ in [bx[0]-0.018, bx[-1]+0.018]:
    qpoly(ax,[[lx_,-0.15,z_g+0.04],[lx_,0.15,z_g+0.04],
              [lx_,0.15,z_g+0.12],[lx_,-0.15,z_g+0.12]],
          '#f5f5f5',ec='#555',al=0.9,zo=3)

# ── front bumper ─────────────────────────────────────────────────────
qpoly(ax,[[bx[-1]+0.01,-bw[-3]*0.88,z_g],[bx[-1]+0.01,bw[-3]*0.88,z_g],
          [bx[-1]+0.01,bw[-3]*0.88,z_g+0.04],[bx[-1]+0.01,-bw[-3]*0.88,z_g+0.04]],
      paint_f,al=0.92,zo=3)

# rear bumper
qpoly(ax,[[bx[0]-0.01,-bw[2]*0.88,z_g],[bx[0]-0.01,bw[2]*0.88,z_g],
          [bx[0]-0.01,bw[2]*0.88,z_g+0.04],[bx[0]-0.01,-bw[2]*0.88,z_g+0.04]],
      paint_re,al=0.92,zo=3)

# ── fuel door detail (right side, rear quarter) ─────────────────────
fd_x = -0.90; fd_w = np.interp(fd_x, bx, bw)
fd_z = np.interp(fd_x, bx, bzt) - 0.10
qpoly(ax,[[fd_x-0.04, fd_w+0.006, fd_z-0.04],
          [fd_x+0.04, fd_w+0.006, fd_z-0.04],
          [fd_x+0.04, fd_w+0.006, fd_z+0.04],
          [fd_x-0.04, fd_w+0.006, fd_z+0.04]],
      paint_hi, ec='#4a72a8', al=0.7, lw=1.0, zo=3)

# ── ground shadow (dark ellipse under car) ───────────────────────────
sh_th = np.linspace(0, 2*np.pi, 60)
sh_rx, sh_ry = 2.20, 0.85
qpoly(ax, [[sh_rx*np.cos(t), sh_ry*np.sin(t), z_g-0.008] for t in sh_th],
      '#050810', ec='#050810', al=0.55, lw=0, zo=0)

# ── wheels (18" sedan wheels — smaller) ──────────────────────────────
wt=np.linspace(0,2*np.pi,40)
wr=0.19   # sedan tyre (smaller)
rr=0.13   # sedan rim
dr=0.08   # brake disc
wlocs = [(1.55,-0.93,z_g+0.02),(1.55,0.93,z_g+0.02),
         (-1.48,-0.93,z_g+0.02),(-1.48,0.93,z_g+0.02)]
for wx_,wy_,wz_ in wlocs:
    # tyre
    qpoly(ax,[[wx_+wr*np.cos(t)*0.38,wy_,wz_+wr*np.sin(t)] for t in wt],
          '#151515',ec='#0a0a0a',al=0.92,zo=3)
    # rim (alloy)
    qpoly(ax,[[wx_+rr*np.cos(t)*0.38,wy_,wz_+rr*np.sin(t)] for t in wt],
          '#d0d8dc',ec='#a0a8ae',al=0.88,zo=4)
    # centre cap
    qpoly(ax,[[wx_+0.035*np.cos(t)*0.38,wy_,wz_+0.035*np.sin(t)] for t in wt],
          '#888',ec='#666',al=0.85,zo=6)
    # brake disc
    qpoly(ax,[[wx_+dr*np.cos(t)*0.38,wy_,wz_+dr*np.sin(t)] for t in wt],
          '#78909c',ec='#546e7a',al=0.7,zo=5)
    # 5-spoke pattern
    for sp_a in np.linspace(0,2*np.pi,6)[:-1]:
        sx0=wx_+dr*np.cos(sp_a)*0.38
        sz0=wz_+dr*np.sin(sp_a)
        sx1=wx_+rr*np.cos(sp_a)*0.38
        sz1=wz_+rr*np.sin(sp_a)
        ax.plot([sx0,sx1],[wy_,wy_],[sz0,sz1],color='#d0d8dc',lw=2.2,zorder=5)
    # wheel arch (pressed into body — sedan style)
    aa=np.linspace(-0.4,np.pi+0.4,45)
    ax.plot(wx_+(wr+0.03)*np.cos(aa)*0.38,np.full(45,wy_),
            wz_+(wr+0.03)*np.sin(aa),
            color=paint_l if wy_<0 else paint_r,lw=3.5,zorder=3)

# ── shark-fin antenna ────────────────────────────────────────────────
sfx=cx_[2]; sfzb=np.interp(sfx,cx_,czt)+0.008; sfzt=sfzb+0.06
qpoly(ax,[[sfx-0.04,0,sfzb],[sfx+0.04,0,sfzb],[sfx+0.01,0,sfzt],[sfx-0.01,0,sfzt]],
      '#1a3058',al=0.9,zo=6)

# ── windshield wipers ────────────────────────────────────────────────
wp_x0=cx_[-1]-0.10
for sw in [-0.28,0.28]:
    wpz=np.interp(wp_x0,bx,bzt)+0.005
    ax.plot([wp_x0,wp_x0+0.35],[sw,sw*0.65],[wpz,wpz+0.003],
            color='#111',lw=1.8,zorder=5)

# ── dual exhaust tips ────────────────────────────────────────────────
for ey in [-0.30,0.30]:
    cylinder(ax,bx[0]-0.04,ey,z_g-0.01,z_g+0.02,0.024,10,
             '#78909c',ec='#546e7a',al=0.8,zo=3)


# ═════════════════════════════════════════════════════════════════════════
#  OPTIMIZED ANTENNA — 1.40×0.80 m RECTANGULAR, 28 mm Ag-Cu, 2-turn/1-turn
#  ** ENLARGED & HIGH-VISIBILITY rendering **
# ═════════════════════════════════════════════════════════════════════════
Lx_loop = 0.70    # half-length along X (1.40 m total)
Ly_loop = 0.40    # half-width along Y (0.80 m total)
R_corner = 0.05   # rounded corner radius (50 mm)
z_roof = np.interp(0, cx_, czt) + 0.008
standoff_h = 0.14
z_lp = z_roof + standoff_h
z_lp2 = z_lp + 0.10   # 100 mm turn spacing
gap_len = 0.08         # gap at front centre (for cap leads)

# silver-plated copper colours
AG_CU   = '#d4852e'
AG_HI   = '#ffe0a0'
AG_GLOW = '#ff9800'

def rect_loop_pts(lx, ly, rc, n_corner=12):
    """Generate rectangular loop points with rounded corners, gap at +Y centre."""
    pts = []
    # Start from gap at +Y side (front), go clockwise looking from above
    # Front-right corner → right side → back-right → back side → back-left → left side → front-left
    corners = [
        ( lx-rc,  ly-rc, 0),          # front-right
        ( lx-rc, -ly+rc, -np.pi/2),   # back-right
        (-lx+rc, -ly+rc, -np.pi),     # back-left
        (-lx+rc,  ly-rc, np.pi/2),    # front-left
    ]
    # Start from gap right side: (gap_len/2, ly)
    # Straight to front-right corner
    pts.append((gap_len/2, ly))
    # straight segment to corner
    pts.append((lx-rc, ly))
    # front-right corner arc
    for a in np.linspace(np.pi/2, 0, n_corner):
        pts.append((lx-rc + rc*np.cos(a), ly-rc + rc*np.sin(a)))
    # right side straight
    pts.append((lx, -ly+rc))
    # back-right corner arc
    for a in np.linspace(0, -np.pi/2, n_corner):
        pts.append((lx-rc + rc*np.cos(a), -ly+rc + rc*np.sin(a)))
    # back side straight
    pts.append((-lx+rc, -ly))
    # back-left corner arc
    for a in np.linspace(-np.pi/2, -np.pi, n_corner):
        pts.append((-lx+rc + rc*np.cos(a), -ly+rc + rc*np.sin(a)))
    # left side straight
    pts.append((-lx, ly-rc))
    # front-left corner arc
    for a in np.linspace(np.pi, np.pi/2, n_corner):
        pts.append((-lx+rc + rc*np.cos(a), ly-rc + rc*np.sin(a)))
    # straight to gap left side
    pts.append((-gap_len/2, ly))
    return np.array(pts)

loop_pts = rect_loop_pts(Lx_loop, Ly_loop, R_corner)
loop_x = loop_pts[:, 0]
loop_y = loop_pts[:, 1]
Npts = len(loop_x)

# ── GLOW RECTANGLES (soft outer halo) ────────────────────────────────
for z_glow in [z_lp, z_lp2]:
    ax.plot(loop_x, loop_y, np.full(Npts, z_glow),
            color=AG_GLOW, lw=22, solid_capstyle='round', alpha=0.12, zorder=9)
    ax.plot(loop_x, loop_y, np.full(Npts, z_glow),
            color=AG_GLOW, lw=16, solid_capstyle='round', alpha=0.18, zorder=9)

# ── TURN 1 (bottom, always active) ──────────────────────────────────
ax.plot(loop_x, loop_y, np.full(Npts, z_lp),
        color='#4a2800', lw=16, solid_capstyle='round', alpha=0.7, zorder=9)
tube(ax, loop_x, loop_y, np.full(Npts, z_lp), AG_CU, lw=13, hc=AG_HI, zo=10)

# ── TURN 2 (top, relay-switched for 80m) ────────────────────────────
ax.plot(loop_x, loop_y, np.full(Npts, z_lp2),
        color='#4a2800', lw=16, solid_capstyle='round', alpha=0.7, zorder=9)
tube(ax, loop_x, loop_y, np.full(Npts, z_lp2), AG_CU, lw=13, hc=AG_HI, zo=10)

# ── SERIES JUMPER (at back-left corner, connects turn 1 end to turn 2 start)
jx = -gap_len/2
jy = Ly_loop
jz_arr = np.linspace(z_lp, z_lp2, 25)
ax.plot(np.full(25, jx), np.full(25, jy), jz_arr,
        color='#4a2800', lw=14, solid_capstyle='round', alpha=0.7, zorder=9)
tube(ax, np.full(25, jx), np.full(25, jy), jz_arr, '#cd7f32', lw=10, hc=AG_HI, zo=10)

ax.text(jx-0.14, jy+0.06, (z_lp+z_lp2)/2, 'Ag-Cu Jumper\n100 mm',
        fontsize=12, fontweight='bold', color='#ffe0a0',
        fontfamily='sans-serif', ha='right', zorder=20,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#3e2723', alpha=0.92,
                  edgecolor=AG_CU, lw=1.5))

# ── TURN LABELS ──────────────────────────────────────────────────────
ax.text(-Lx_loop-0.18, 0.30, z_lp, 'TURN 1\n(always ON)\n28 mm Ag-Cu',
        fontsize=13, fontweight='bold', color=AG_CU,
        fontfamily='sans-serif', ha='right', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a1208', alpha=0.93,
                  edgecolor=AG_CU, lw=2))
ax.text(-Lx_loop-0.18, 0.30, z_lp2, 'TURN 2\n(80m only)\n28 mm Ag-Cu',
        fontsize=13, fontweight='bold', color='#ef5350',
        fontfamily='sans-serif', ha='right', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#1a0808', alpha=0.93,
                  edgecolor='#ef5350', lw=2))

# ── RELAY BOX (near jumper on front side) ────────────────────────────
relay_x = jx - 0.10
relay_y = jy + 0.04
relay_z = (z_lp+z_lp2)/2
box3d(ax, relay_x, relay_y, relay_z, 0.05, 0.035, 0.03,
      ['#c62828','#e53935','#ef5350','#c62828','#b71c1c','#e53935'],
      ec='#b71c1c', zo=16)
ax.text(relay_x-0.12, relay_y+0.08, relay_z,
        'Turn-Switch\nRelay (DPDT)', fontsize=10, fontweight='bold', color='#ef9a9a',
        fontfamily='sans-serif', ha='right', zorder=20,
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#1a0808', alpha=0.9,
                  edgecolor='#ef5350', lw=1.2))

# ── CAPACITOR ENCLOSURE (on front long side) ─────────────────────────
cap_x, cap_y, cap_z = 0.0, Ly_loop+0.06, (z_lp+z_lp2)/2
box3d(ax, cap_x, cap_y, cap_z, 0.18, 0.10, 0.08,
      ['#0d47a1','#1565c0','#1976d2','#0d47a1','#0a3d8f','#1565c0'],
      ec='#0d47a1', zo=15)

# leads from loop gap to cap box
for gx_, sx in [(gap_len/2, 0.10), (-gap_len/2, -0.10)]:
    for z_t in [z_lp, z_lp2]:
        ax.plot([gx_, cap_x+sx], [Ly_loop, cap_y], [z_t, cap_z],
                color=AG_CU, lw=7, solid_capstyle='round', zorder=11)

# bank indicator stripes
ax.plot([cap_x-0.12, cap_x-0.12],[cap_y-0.10, cap_y-0.10],
        [cap_z-0.08, cap_z+0.08], color='#42a5f5', lw=4, zorder=16)
ax.plot([cap_x+0.12, cap_x+0.12],[cap_y-0.10, cap_y-0.10],
        [cap_z-0.08, cap_z+0.08], color='#ef5350', lw=4, zorder=16)

# stepper motor
cylinder(ax, cap_x, cap_y, cap_z+0.08, cap_z+0.14, 0.038, 16,
         '#455a64', ec='#37474f', zo=16)
ax.plot([cap_x,cap_x],[cap_y,cap_y],[cap_z+0.14,cap_z+0.17],
        color='#b0bec5', lw=2.5, zorder=17)

# cap label
ax.plot([cap_x, cap_x+0.45],[cap_y+0.10, cap_y+0.38],
        [cap_z+0.14, cap_z+0.40], color='#90caf9', lw=2, zorder=19)
ax.text(cap_x+0.47, cap_y+0.40, cap_z+0.42,
        'DUAL-BAND CAP ASSEMBLY\n'
        'Bank A: Vacuum 30-150 pF (40m)\n'
        'Bank B: Vacuum 100-500 pF (80m)\n'
        'DPDT Band Relay  |  NEMA17 Stepper\n'
        'Turn-Switch Relay (2T / 1T)',
        fontsize=11, fontweight='bold', color='#bbdefb',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#0d47a1', alpha=0.94,
                  edgecolor='#64b5f6', lw=2))

# dome outline
dome_t = np.linspace(0,2*np.pi,40)
ax.plot(cap_x+0.22*np.cos(dome_t), cap_y+0.14*np.sin(dome_t),
        np.full(40,cap_z+0.10), color='#80cbc4', lw=2, ls='--', alpha=0.45, zorder=14)

# ── coupling loop (at bottom/rear side of rectangle) ─────────────────
R_cpl = 0.15
th_c = np.linspace(0.12, 2*np.pi-0.12, N)
cpl_cy = -Ly_loop   # at rear side
ax.plot(R_cpl*np.cos(th_c), R_cpl*np.sin(th_c)+cpl_cy,
        np.full(N, z_lp), color='#d2691e', lw=12,
        solid_capstyle='round', alpha=0.15, zorder=9)
tube(ax, R_cpl*np.cos(th_c), R_cpl*np.sin(th_c)+cpl_cy,
     np.full(N, z_lp), CU_CPL, lw=7, hc='#e8a060', zo=10)

ax.plot([R_cpl*0.7, R_cpl+0.28],[cpl_cy, cpl_cy-0.24],
        [z_lp, z_lp+0.16], color='#bcaaa4', lw=2, zorder=19)
ax.text(R_cpl+0.30, cpl_cy-0.26, z_lp+0.18,
        'FARADAY FEED LOOP\n240 mm dia  |  RG-213\nShield both ends',
        fontsize=11, fontweight='bold', color='#d7ccc8',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#3e2723', alpha=0.93,
                  edgecolor='#8d6e63', lw=2))

# SO-239
hex_t = np.linspace(0, 2*np.pi, 7)
qpoly(ax,[[0.025*np.cos(t), cpl_cy-R_cpl+0.025*np.sin(t), z_lp] for t in hex_t],
      '#b0bec5', ec='#78909c', al=0.9, zo=12)
ax.text(0, cpl_cy-R_cpl-0.06, z_lp-0.04, 'SO-239',
        fontsize=10, fontweight='bold', color='#b0bec5',
        fontfamily='sans-serif', ha='center', zorder=20)

# ── standoffs at 4 corners of rectangle ──────────────────────────────
spos = [( Lx_loop*0.85,  Ly_loop*0.85),
        ( Lx_loop*0.85, -Ly_loop*0.85),
        (-Lx_loop*0.85,  Ly_loop*0.85),
        (-Lx_loop*0.85, -Ly_loop*0.85)]
for sx_, sy_ in spos:
    zr_ = np.interp(sx_, cx_, czt)+0.008
    # mag-mount base
    cylinder(ax, sx_, sy_, zr_, zr_+0.018, 0.050, 14, '#212121', ec='#111', al=0.9, zo=8)
    cylinder(ax, sx_, sy_, zr_+0.018, zr_+0.025, 0.045, 14, '#37474f', ec='#263238', al=0.85, zo=9)
    # HDPE rod
    ax.plot([sx_,sx_],[sy_,sy_],[zr_+0.025, z_lp],
            color='#eceff1', lw=7, solid_capstyle='round', zorder=8)
    # clip for turn 1
    cylinder(ax, sx_, sy_, z_lp-0.010, z_lp+0.010, 0.032, 12, '#e0e0e0', ec='#bdbdbd', al=0.9, zo=11)
    # extension rod between turns
    ax.plot([sx_,sx_],[sy_,sy_],[z_lp, z_lp2],
            color='#eceff1', lw=5.5, solid_capstyle='round', zorder=8)
    # clip for turn 2
    cylinder(ax, sx_, sy_, z_lp2-0.010, z_lp2+0.010, 0.032, 12, '#e0e0e0', ec='#bdbdbd', al=0.9, zo=11)

ax.plot([Lx_loop*0.85+0.05, Lx_loop*0.85+0.36],
        [-Ly_loop*0.85, -Ly_loop*0.85-0.25],
        [(z_roof+z_lp)/2, (z_roof+z_lp)/2-0.12],
        color='#b0bec5', lw=2, zorder=19)
ax.text(Lx_loop*0.85+0.38, -Ly_loop*0.85-0.27, (z_roof+z_lp)/2-0.14,
        'HDPE Post 140 mm\nNdFeB Mag-Mount 40 kg\n+ Extension for Turn 2',
        fontsize=10, fontweight='bold', color='#cfd8dc',
        fontfamily='sans-serif', ha='left', zorder=20,
        bbox=dict(boxstyle='round,pad=0.25', facecolor='#1a2530', alpha=0.93,
                  edgecolor='#78909c', lw=1.5))

# ── coax + control cable ────────────────────────────────────────────
cp = np.array([[0, cpl_cy-R_cpl, z_lp],
               [0.05, cpl_cy-R_cpl-0.05, z_lp-0.02],
               [0.12,-(np.interp(0.12,cx_,cw_)+0.03), z_roof-0.05],
               [0.15,-(np.interp(0.15,bx,bw)+0.01), z_g+0.35]])
ax.plot(cp[:,0],cp[:,1],cp[:,2],color='#222',lw=4,ls='--',alpha=0.7,zorder=6)
ax.plot(cp[:,0]+0.03,cp[:,1]+0.01,cp[:,2],color='#4a148c',lw=2.5,ls='-.',alpha=0.5,zorder=6)
ax.text(0.25,cp[3,1]-0.08,z_g+0.32,'RG-58 Coax +\nMotor + Relay cables\nthrough window seal',
        fontsize=10,fontweight='bold',color='#90a4ae',fontfamily='sans-serif',ha='left',zorder=20)

# choke balun (larger)
bb = np.linspace(0,2*np.pi,30)
bxb=0.14; byb=cp[2,1]; bzb=z_roof-0.02
ax.plot(bxb+0.04*np.cos(bb)*0.35, byb+0.04*np.cos(bb)*0.35,
        bzb+0.04*np.sin(bb), color='#4e342e',lw=6,zorder=7)
ax.text(bxb+0.09,byb,bzb,'Choke\nBalun',fontsize=10,color='#a1887f',
        fontweight='bold',fontfamily='sans-serif',zorder=20)

# controller box
box3d(ax, 0.18,-(np.interp(0.18,bx,bw)-0.08),z_g+0.22,
      0.06,0.04,0.03,
      ['#263238','#37474f','#455a64','#263238','#1a2530','#37474f'],
      ec='#1a2530',al=0.8,zo=6)
ax.text(0.30,-(np.interp(0.18,bx,bw)-0.08),z_g+0.22,
        'ESP32 Band/Tune\nController',
        fontsize=9,fontweight='bold',color='#78909c',fontfamily='sans-serif',ha='left',zorder=20)


# ═════════════════════════════════════════════════════════════════════════
#  NVIS RADIATION + IONOSPHERE
# ═════════════════════════════════════════════════════════════════════════
z_mid = (z_lp+z_lp2)/2
ac='#ff8a65'
for ax_,ay_,sp in [(0,0,0),(0.22,0.14,0.06),(-0.22,0.14,0.06),
                   (0.16,-0.18,0.05),(-0.16,-0.18,0.05),
                   (0.30,0,0.08),(-0.30,0,0.08),
                   (0.12,0.26,0.04),(-0.12,0.26,0.04)]:
    z0_=z_mid+0.12; z1_=z_mid+0.72
    ax.plot([ax_,ax_*0.12+sp*0.08],[ay_,ay_*0.12],[z0_,z1_],
            color=ac,lw=2.2,alpha=0.6,zorder=17)
    for dx_ in [-0.015,0.015]:
        ax.plot([ax_*0.12+sp*0.08,ax_*0.12+sp*0.08+dx_],
                [ay_*0.12,ay_*0.12],[z1_,z1_-0.045],
                color=ac,lw=2,alpha=0.6,zorder=17)

ax.text(0,0,z_mid+0.82,
        'NVIS Radiation\n70\u00b0 - 90\u00b0 Elevation',
        fontsize=14,fontweight='bold',color='#ff8a65',
        fontfamily='sans-serif',ha='center',zorder=20,
        bbox=dict(boxstyle='round,pad=0.3',facecolor='#080e1a',alpha=0.93,
                  edgecolor='#ff8a65',lw=2))

for r_s,z_off,c_,a_ in [(1.6,0,'#4dd0e1',0.50),(1.4,0.10,'#80deea',0.28)]:
    it=np.linspace(-0.6,0.6,60)
    ax.plot(r_s*np.sin(it),r_s*0.3*np.cos(it),np.full(60,z_mid+1.25+z_off),
            color=c_,lw=3,ls=':',alpha=a_,zorder=16)
ax.text(0,0,z_mid+1.48,
        'F2 Layer ~250 km  |  foF2 > 3.5 MHz (24h)  |  > 7 MHz (daytime)',
        fontsize=11,fontweight='bold',color='#4dd0e1',
        fontfamily='sans-serif',ha='center',zorder=20,
        bbox=dict(boxstyle='round,pad=0.2',facecolor='#080e1a',alpha=0.88,
                  edgecolor='#4dd0e1',lw=1.2))

for rx_,ry_ in [(0.9,0.35),(-0.9,0.35),(0.7,-0.45),(-0.7,-0.45)]:
    ax.plot([rx_*0.25,rx_],[ry_*0.25,ry_],[z_mid+1.20,z_mid+0.35],
            color='#26c6da',lw=1.5,ls='--',alpha=0.35,zorder=16)

# dimensions — length (X axis)
dz_=z_lp2+0.07
ax.plot([-Lx_loop,Lx_loop],[0,0],[dz_,dz_],color=A_RED,lw=2.5,zorder=18)
for s in [-1,1]:
    ax.plot([s*Lx_loop,s*(Lx_loop-0.05)],[0,0.03],[dz_,dz_],color=A_RED,lw=2.5,zorder=18)
    ax.plot([s*Lx_loop,s*(Lx_loop-0.05)],[0,-0.03],[dz_,dz_],color=A_RED,lw=2.5,zorder=18)
ax.text(0,-0.10,dz_+0.03,'1.40 m \u00d7 0.80 m  (55" \u00d7 31.5")',
        fontsize=14,fontweight='bold',color='#ef9a9a',
        fontfamily='sans-serif',ha='center',zorder=20,
        bbox=dict(boxstyle='round,pad=0.2',facecolor='#080e1a',alpha=0.9,
                  edgecolor=A_RED,lw=1.5))

# width dimension (Y axis)
dz_w = z_lp2+0.04
ax.plot([Lx_loop+0.08,Lx_loop+0.08],[-Ly_loop,Ly_loop],[dz_w,dz_w],
        color=A_RED,lw=2.0,alpha=0.7,zorder=18)
for s in [-1,1]:
    ax.plot([Lx_loop+0.08,Lx_loop+0.08],[s*Ly_loop,s*(Ly_loop-0.03)],
            [dz_w,dz_w],color=A_RED,lw=2.0,alpha=0.7,zorder=18)

# turn spacing
sp_x=-Lx_loop-0.10
ax.plot([sp_x,sp_x],[0,0],[z_lp,z_lp2],color='#ab47bc',lw=2.5,zorder=18)
for dz__ in [z_lp,z_lp2]:
    ax.plot([sp_x-0.025,sp_x+0.025],[0,0],[dz__,dz__],color='#ab47bc',lw=2.5,zorder=18)
ax.text(sp_x-0.06,0,(z_lp+z_lp2)/2,'100 mm\nspacing',
        fontsize=11,fontweight='bold',color='#ce93d8',
        fontfamily='sans-serif',ha='right',zorder=20,
        bbox=dict(boxstyle='round,pad=0.15',facecolor='#080e1a',alpha=0.9,
                  edgecolor='#ab47bc',lw=1.2))

# profile height
ph=Lx_loop+0.22
ax.plot([ph,ph],[0,0],[z_roof,z_lp2+0.06],color=A_GRN,lw=2.5,zorder=18)
for dz__ in [z_roof,z_lp2+0.06]:
    ax.plot([ph-0.025,ph+0.025],[0,0],[dz__,dz__],color=A_GRN,lw=2.5,zorder=18)
ax.text(ph+0.06,0,(z_roof+z_lp2)/2+0.03,'Profile\n~17 cm',
        fontsize=12,fontweight='bold',color='#a5d6a7',
        fontfamily='sans-serif',ha='left',zorder=20,
        bbox=dict(boxstyle='round,pad=0.2',facecolor='#080e1a',alpha=0.9,
                  edgecolor=A_GRN,lw=1.5))

ax.text(2.65,0,z_g+0.25,'FRONT \u25b6',fontsize=13,fontweight='bold',
        color='#546e7a',fontfamily='sans-serif',ha='left',zorder=20)

# ground grid
for g in np.linspace(-2.0,2.0,14):
    ax.plot([g,g],[-1.2,1.2],[z_g-0.01,z_g-0.01],color='#131d2e',lw=0.4,alpha=0.25,zorder=1)
    ax.plot([-2.0,2.0],[g*0.6,g*0.6],[z_g-0.01,z_g-0.01],color='#131d2e',lw=0.4,alpha=0.25,zorder=1)
ax.plot([-2.0,2.0],[0,0],[z_g-0.008,z_g-0.008],color='#ffd600',lw=1.5,ls='--',alpha=0.15,zorder=1)


# ═════════════════════════════════════════════════════════════════════════
#  PANEL A — Optimized Specs  (right, upper)
# ═════════════════════════════════════════════════════════════════════════
ax_s = fig.add_axes([0.58, 0.51, 0.41, 0.39])
ax_s.set_facecolor('#e3f2fd')
ax_s.set_xlim(0,10); ax_s.set_ylim(0,10); ax_s.axis('off')
for sp in ax_s.spines.values():
    sp.set_visible(True); sp.set_color(A_BLUE); sp.set_linewidth(2.5)

ax_s.text(5,9.70,'OPTIMIZED Dual-Band NVIS Loop -- Efficiency-Focused Design',
          fontsize=20,fontweight='bold',ha='center',va='top',
          color=TD,fontfamily='sans-serif')

# column headers
ax_s.add_patch(FancyBboxPatch((0.1,9.00),9.8,0.50,
               boxstyle="round,pad=0.06",facecolor='#0d47a1',alpha=0.92))
ax_s.text(0.3,9.25,'Parameter',fontsize=13,fontweight='bold',
          color='white',va='center',fontfamily='sans-serif')
ax_s.text(5.0,9.25,'80 m (2-Turn)',fontsize=13,fontweight='bold',
          color='#ffab40',va='center',ha='center',fontfamily='sans-serif')
ax_s.text(8.0,9.25,'40 m (1-Turn)',fontsize=13,fontweight='bold',
          color='#69f0ae',va='center',ha='center',fontfamily='sans-serif')

specs = [
    ('Frequency',       '3.500 - 4.000 MHz',       '7.000 - 7.300 MHz'),
    ('Loop Size',       '1.40 \u00d7 0.80 m rect',  '1.40 \u00d7 0.80 m rect'),
    ('Turns',           '2 series, 100 mm gap',     '1  (Turn 2 bypassed)'),
    ('Tube',            '28 mm Ag-plated Cu',       '28 mm Ag-plated Cu'),
    ('Inductance',      '~8.7 \u03bcH (2T+M)',     '~2.9 \u03bcH'),
    ('Reactance (XL)',  '~196 \u03a9',              '~130 \u03a9'),
    ('Tuning Cap',      '~205 pF  (Bank B)',        '~85 pF  (Bank A)'),
    ('Radiation Res.',  '~3.3 m\u03a9  (4\u00d7 \u2191)', '~12.9 m\u03a9  (2\u00d7 \u2191)'),
    ('Cu Loss (Ag)',    '~40.7 m\u03a9',            '~28.7 m\u03a9'),
    ('Cap ESR (Q=10k)', '~19.6 m\u03a9',           '~13.0 m\u03a9'),
    ('EFFICIENCY',      '5.2 %  (was 1.7%)',        '23.6 %  (was 12%)'),
    ('ERP @ 50 W',     '2.6 W  (was 0.9W)',        '11.8 W  (was 6.0W)'),
    ('Improvement',     '3.1\u00d7 better',         '2.0\u00d7 better'),
    ('Cap Voltage @50W','~5.5 kV',                  '~3.9 kV'),
    ('Bandwidth',       '~2.5 kHz',                 '~8 kHz'),
    ('NVIS Range',      '0 - 600 km  (24h)',        '0 - 600 km  (day)'),
    ('Weight',          '~4.5 kg (9.9 lb)',         '(same loop)'),
    ('Max Power',       '50 W (7.5 kV cap)',        '50 W (5 kV cap)'),
]

rc=['#bbdefb','#ffffff']
y0=8.75; dy=0.46
for i,(lbl,v80,v40) in enumerate(specs):
    y=y0-i*dy
    bg = rc[i%2]
    # highlight efficiency and ERP rows
    if lbl in ('EFFICIENCY','ERP @ 50 W','Improvement'):
        bg = '#c8e6c9' if i%2==0 else '#e8f5e9'
    ax_s.add_patch(FancyBboxPatch((0.1,y-0.18),9.8,0.42,
                   boxstyle="round,pad=0.04",facecolor=bg,alpha=0.75))
    ax_s.text(0.3,y,lbl,fontsize=11.5,fontweight='bold',va='center',
              color=TD,fontfamily='sans-serif')
    # bold the efficiency values
    fw = 'bold' if lbl in ('EFFICIENCY','ERP @ 50 W','Improvement') else 'normal'
    c80 = '#b71c1c' if 'was' in v80 else TD
    c40 = '#1b5e20' if 'was' in v40 else TD
    if lbl == 'Improvement': c80 = '#e65100'; c40 = '#1b5e20'
    ax_s.text(5.0,y,v80,fontsize=11.5,fontweight=fw,va='center',ha='center',
              color=c80,fontfamily='sans-serif')
    ax_s.text(8.0,y,v40,fontsize=11.5,fontweight=fw,va='center',ha='center',
              color=c40,fontfamily='sans-serif')

ax_s.plot([3.7,3.7],[0.2,9.00],color='#90caf9',lw=1.5,alpha=0.5)
ax_s.plot([6.5,6.5],[0.2,9.00],color='#90caf9',lw=1.5,alpha=0.5)

ax_s.text(5,0.28,
    'KEY OPTIMIZATIONS:  1.40\u00d70.80m rect (+44% area)  |  '
    'Tube 22\u219228mm Ag-plated (-25% loss)  |  '
    '2-Turn for 80m (Rr 4\u00d7 boost)  |  Turn-switching relay',
    fontsize=10.5,fontweight='bold',ha='center',va='center',
    color='#0d47a1',fontfamily='sans-serif',
    bbox=dict(boxstyle='round,pad=0.2',facecolor='#e1f5fe',
              edgecolor='#0d47a1',lw=1.5,alpha=0.95))


# ═════════════════════════════════════════════════════════════════════════
#  PANEL B — Installation Guide  (right, lower)
# ═════════════════════════════════════════════════════════════════════════
ax_n = fig.add_axes([0.58, 0.06, 0.41, 0.39])
ax_n.set_facecolor('#fff3e0')
ax_n.set_xlim(0,10); ax_n.set_ylim(0,10); ax_n.axis('off')
for sp in ax_n.spines.values():
    sp.set_visible(True); sp.set_color('#ff9800'); sp.set_linewidth(2.5)

ax_n.text(5,9.78,'Build & Installation Guide (Optimized)',
          fontsize=20,fontweight='bold',ha='center',va='top',
          color=TD,fontfamily='sans-serif')

notes = [
    ('1.','FORM 2 RECT LOOPS',
     'Cut 2x 4.30 m of 28mm Cu tube. Silver-plate (electroless).\n'
     'Fill w/ sand, bend into 1.40\u00d70.80 m rectangles. 20 mm gap.'),
    ('2.','SERIES JUMPER',
     'Stack loops coaxially, 100 mm apart. Silver-solder 100 mm\n'
     'Cu jumper on one side. Use PVC spacers on 4 corner posts.'),
    ('3.','COUPLING LOOP',
     'Bend 78 cm of RG-213 into 240 mm Faraday loop. Mount\n'
     'at bottom. Shield both ends, center conductor one end.'),
    ('4.','DUAL CAP + RELAY',
     'In IP65 box: Bank A vacuum (30-150 pF, 5 kV) for 40m.\n'
     'Bank B vacuum (100-500 pF, 7.5 kV) for 80m. Wire DPDT.'),
    ('5.','TURN SWITCH RELAY',
     'Install DPDT relay to bypass Turn 2 on 40m. On 80m both\n'
     'turns series. Relay at jumper location. 12V coil.'),
    ('6.','MAG-MOUNT INSTALL',
     '4x NdFeB 40 kg mounts on clean sedan roof. 140 mm HDPE\n'
     'posts with extension clips for Turn 2. Loop horizontal.'),
    ('7.','TUNE & OPERATE',
     'ESP32 selects band (cap bank + turn relay). Stepper auto-\n'
     'tunes. BW: ~2.5 kHz (80m), ~8 kHz (40m). Max 50 W.'),
]

rcn=['#ffe0b2','#ffffff']
y0n=9.15; dyn=1.12
for i,(num,title,desc) in enumerate(notes):
    y=y0n-i*dyn
    ax_n.add_patch(FancyBboxPatch((0.2,y-0.44),9.6,0.95,
                   boxstyle="round,pad=0.08",facecolor=rcn[i%2],alpha=0.6))
    ax_n.add_patch(plt.Circle((0.55,y),0.28,facecolor='#e65100',
                   edgecolor='white',lw=2,zorder=10,transform=ax_n.transData))
    ax_n.text(0.55,y,num,fontsize=13,fontweight='bold',color='white',
              ha='center',va='center',fontfamily='sans-serif',zorder=11)
    ax_n.text(1.0,y+0.20,title,fontsize=13,fontweight='bold',
              va='center',color='#bf360c',fontfamily='sans-serif')
    ax_n.text(1.0,y-0.20,desc,fontsize=10.5,va='center',
              color='#333',fontfamily='sans-serif',linespacing=1.3)

ax_n.text(5,1.05,
    'BOM: 28mm Ag-Cu tube $65  |  Vacuum caps x2 $240  |  '
    'DPDT relays x2 $30  |  NdFeB mounts $30  |  HDPE+clips $18',
    fontsize=10,fontweight='bold',ha='center',va='center',
    color='#e65100',fontfamily='sans-serif',
    bbox=dict(boxstyle='round,pad=0.22',facecolor='#fff8e1',
              edgecolor='#e65100',lw=2,alpha=0.9))
ax_n.text(5,0.58,
    'Stepper kit $18  |  ESP32 $12  |  IP65 box $14  |  '
    'Ag plating $40  |  Solder+HW $20  =  Total ~$487',
    fontsize=10,fontweight='bold',ha='center',va='center',
    color='#e65100',fontfamily='sans-serif',
    bbox=dict(boxstyle='round,pad=0.22',facecolor='#fff8e1',
              edgecolor='#e65100',lw=2,alpha=0.9))

ax_n.text(5,0.12,
    'NVIS on 80m is reliable 24 hours.  2.6 W ERP is sufficient '
    'for SSB/CW contacts within 300-500 km.',
    fontsize=10.5,fontweight='bold',ha='center',va='center',
    color='#1b5e20',fontfamily='sans-serif',
    bbox=dict(boxstyle='round,pad=0.22',facecolor='#c8e6c9',
              edgecolor='#2e7d32',lw=2,alpha=0.95))


# ═════════════════════════════════════════════════════════════════════════
#  INSET 1 — Efficiency Improvement Bar Chart
# ═════════════════════════════════════════════════════════════════════════
ax_eff = fig.add_axes([0.005, 0.03, 0.185, 0.24])
ax_eff.set_facecolor('#0f1a2e')

bands = ['80 m', '40 m']
eff_old = [1.7, 12.0]
eff_new = [5.2, 23.6]
x_b = np.arange(2)
w_ = 0.32

bars_old = ax_eff.bar(x_b-w_/2, eff_old, w_, label='Baseline (1.0m, 22mm)',
                       color='#78909c', edgecolor='white', lw=1.5)
bars_new = ax_eff.bar(x_b+w_/2, eff_new, w_, label='Optimized (1.2m, 28mm Ag)',
                       color='#66bb6a', edgecolor='white', lw=1.5)

for b,v in zip(bars_old, eff_old):
    ax_eff.text(b.get_x()+b.get_width()/2, v+0.5, f'{v}%',
                ha='center',va='bottom',fontsize=12,fontweight='bold',
                color='#b0bec5',fontfamily='sans-serif')
for b,v in zip(bars_new, eff_new):
    ax_eff.text(b.get_x()+b.get_width()/2, v+0.5, f'{v}%',
                ha='center',va='bottom',fontsize=12,fontweight='bold',
                color='#a5d6a7',fontfamily='sans-serif')

# improvement arrows
for i,(vo,vn) in enumerate(zip(eff_old, eff_new)):
    ratio = vn/vo
    ax_eff.annotate(f'{ratio:.1f}\u00d7',
                    xy=(i+w_/2, vn+2.5), fontsize=14, fontweight='bold',
                    color=GOLD, ha='center', fontfamily='sans-serif',
                    bbox=dict(boxstyle='round,pad=0.15',facecolor='#080e1a',
                              edgecolor=GOLD,alpha=0.9))

ax_eff.set_xticks(x_b); ax_eff.set_xticklabels(bands, fontsize=14, color='#e0e0e0')
ax_eff.set_ylabel('Efficiency (%)', fontsize=13, fontweight='bold', color='#e0e0e0')
ax_eff.set_title('Efficiency: Before vs After', fontsize=14, fontweight='bold',
                 color='#e0e0e0', pad=10, fontfamily='sans-serif')
ax_eff.set_ylim(0, 32)
ax_eff.tick_params(labelsize=12, colors='#90a4ae')
ax_eff.legend(fontsize=10, loc='upper left', facecolor='#1a2530',
              edgecolor='#546e7a', labelcolor='#e0e0e0')
ax_eff.grid(axis='y', alpha=0.2, color='#37474f')
for sp in ax_eff.spines.values():
    sp.set_color('#37474f')


# ═════════════════════════════════════════════════════════════════════════
#  INSET 2 — ERP Comparison
# ═════════════════════════════════════════════════════════════════════════
ax_erp = fig.add_axes([0.20, 0.03, 0.185, 0.24])
ax_erp.set_facecolor('#0f1a2e')

erp_old = [0.9, 6.0]
erp_new = [2.6, 11.8]

bars_eo = ax_erp.bar(x_b-w_/2, erp_old, w_, label='Baseline',
                      color='#78909c', edgecolor='white', lw=1.5)
bars_en = ax_erp.bar(x_b+w_/2, erp_new, w_, label='Optimized',
                      color='#42a5f5', edgecolor='white', lw=1.5)

for b,v in zip(bars_eo, erp_old):
    ax_erp.text(b.get_x()+b.get_width()/2, v+0.2, f'{v}W',
                ha='center',va='bottom',fontsize=12,fontweight='bold',
                color='#b0bec5',fontfamily='sans-serif')
for b,v in zip(bars_en, erp_new):
    ax_erp.text(b.get_x()+b.get_width()/2, v+0.2, f'{v}W',
                ha='center',va='bottom',fontsize=12,fontweight='bold',
                color='#90caf9',fontfamily='sans-serif')

for i,(vo,vn) in enumerate(zip(erp_old, erp_new)):
    ratio = vn/vo
    ax_erp.annotate(f'{ratio:.1f}\u00d7',
                    xy=(i+w_/2, vn+1.0), fontsize=14, fontweight='bold',
                    color=GOLD, ha='center', fontfamily='sans-serif',
                    bbox=dict(boxstyle='round,pad=0.15',facecolor='#080e1a',
                              edgecolor=GOLD,alpha=0.9))

ax_erp.set_xticks(x_b); ax_erp.set_xticklabels(bands, fontsize=14, color='#e0e0e0')
ax_erp.set_ylabel('ERP (Watts @ 50W)', fontsize=13, fontweight='bold', color='#e0e0e0')
ax_erp.set_title('ERP: Before vs After', fontsize=14, fontweight='bold',
                 color='#e0e0e0', pad=10, fontfamily='sans-serif')
ax_erp.set_ylim(0, 16)
ax_erp.tick_params(labelsize=12, colors='#90a4ae')
ax_erp.legend(fontsize=10, loc='upper left', facecolor='#1a2530',
              edgecolor='#546e7a', labelcolor='#e0e0e0')
ax_erp.grid(axis='y', alpha=0.2, color='#37474f')
for sp in ax_erp.spines.values():
    sp.set_color('#37474f')


# ═════════════════════════════════════════════════════════════════════════
#  INSET 3 — Loss Budget Pie Charts
# ═════════════════════════════════════════════════════════════════════════
# 80m loss budget
ax_p80 = fig.add_axes([0.395, 0.03, 0.09, 0.20])
ax_p80.set_facecolor('#0f1a2e')
sizes_80 = [3.31, 40.7, 19.6]  # Rr, Rl, Rc in mOhm
labels_80 = ['Rr 3.3m\u03a9\n(radiated)', 'Rl 40.7m\u03a9\n(Cu loss)', 'Rc 19.6m\u03a9\n(cap ESR)']
colors_80 = ['#66bb6a', '#ef5350', '#42a5f5']
wedges80, texts80 = ax_p80.pie(sizes_80, labels=None, colors=colors_80,
                                startangle=90, wedgeprops=dict(edgecolor='white',lw=1.5))
ax_p80.set_title('80m Loss Budget', fontsize=11, fontweight='bold',
                 color='#e0e0e0', pad=8, fontfamily='sans-serif')
# legend below
ax_p80.legend(labels_80, loc='upper center', bbox_to_anchor=(0.5, -0.02),
              fontsize=8, facecolor='#1a2530', edgecolor='#546e7a',
              labelcolor='#e0e0e0', ncol=1)

# 40m loss budget
ax_p40 = fig.add_axes([0.495, 0.03, 0.09, 0.20])
ax_p40.set_facecolor('#0f1a2e')
sizes_40 = [12.86, 28.7, 13.0]
labels_40 = ['Rr 12.9m\u03a9\n(radiated)', 'Rl 28.7m\u03a9\n(Cu loss)', 'Rc 13.0m\u03a9\n(cap ESR)']
colors_40 = ['#66bb6a', '#ef5350', '#42a5f5']
wedges40, texts40 = ax_p40.pie(sizes_40, labels=None, colors=colors_40,
                                startangle=90, wedgeprops=dict(edgecolor='white',lw=1.5))
ax_p40.set_title('40m Loss Budget', fontsize=11, fontweight='bold',
                 color='#e0e0e0', pad=8, fontfamily='sans-serif')
ax_p40.legend(labels_40, loc='upper center', bbox_to_anchor=(0.5, -0.02),
              fontsize=8, facecolor='#1a2530', edgecolor='#546e7a',
              labelcolor='#e0e0e0', ncol=1)


# ═════════════════════════════════════════════════════════════════════════
#  INSET 4 — Switching Schematic (compact)
# ═════════════════════════════════════════════════════════════════════════
# (switching schematic omitted — space used by loss budget pies)


# ═════════════════════════════════════════════════════════════════════════
#  TITLE BANNER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.003,0.925),0.994,0.070,
    boxstyle="round,pad=0.008",facecolor='#0d47a1',alpha=0.95,
    transform=fig.transFigure,zorder=2))
fig.text(0.50,0.975,
    'OPTIMIZED Dual-Band NVIS 80m / 40m  \u2014  1.40\u00d70.80 m Rectangular Ag-Cu Loop on Sedan  '
    '\u2014  3D Installation View',
    fontsize=34,fontweight='bold',color='#ffffff',
    ha='center',va='center',fontfamily='sans-serif',zorder=3)
fig.text(0.50,0.938,
    '1.40 \u00d7 0.80 m  |  28 mm Ag-Plated Cu  |  2-Turn/1-Turn Relay Switch  '
    '|  17 cm Profile  |  80m: 5.2% (+3.1\u00d7)  40m: 23.6% (+2.0\u00d7)  '
    '|  Mag-Mount  |  ESP32 Auto-Tune',
    fontsize=19,fontweight='bold',color=GOLD,
    ha='center',va='center',fontfamily='sans-serif',zorder=3)


# ═════════════════════════════════════════════════════════════════════════
#  FOOTER
# ═════════════════════════════════════════════════════════════════════════
fig.patches.append(FancyBboxPatch(
    (0.003,0.001),0.994,0.025,
    boxstyle="round,pad=0.005",facecolor='#0d47a1',alpha=0.85,
    transform=fig.transFigure,zorder=2))
fig.text(0.50,0.014,
    'OPTIMIZED NVIS 80m/40m Sedan-Roof STL  |  HS0ZNR  |  '
    '3.5\u20134.0 / 7.0\u20137.3 MHz  |  \u03b7-Optimized  |  Generated 2026-02-23',
    fontsize=17,fontweight='bold',color='#e3f2fd',
    ha='center',va='center',fontfamily='sans-serif',zorder=3)


# ═════════════════════════════════════════════════════════════════════════
#  SAVE
# ═════════════════════════════════════════════════════════════════════════
out = r'C:\Users\Jakkrit\.local\bin\NVIS_80_40m_Optimized_Sedan_3D.jpg'
fig.savefig(out, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor(),
            pil_kwargs={'quality': 95})
plt.close()
print(f'Saved: {out}')
print(f'Size: {48*DPI} x {34*DPI} px = {48}x{34} in @ {DPI} DPI')
