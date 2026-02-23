# Dual-Band NVIS 80m / 40m Mobile Magnetic Loop Antenna

## Overview

A **relay-switched dual-band NVIS magnetic loop** designed for vehicle-roof deployment,
covering **80 m (3.5-4.0 MHz)** and **40 m (7.0-7.3 MHz)** with automatic band switching
and stepper-motor tuning.

The antenna uses a **2-turn / 1-turn switching topology**: both turns in series for 80 m
(quadrupling radiation resistance), and a single turn for 40 m (bypassing Turn 2 via DPDT relay).

---

## Design Variants

### 1. Baseline Circular Loop on Sedan
- **File:** `gen_nvis_80_40m_car_roof.py`
- **Output:** `NVIS_80_40m_Car_Roof_3D.jpg`
- **Loop:** 1.00 m diameter circular, 22 mm Cu tube
- **Efficiency:** 80 m ~1.7% | 40 m ~12%

### 2. Optimized Circular Loop on SUV
- **File:** `gen_nvis_80_40m_optimized.py` (historical version)
- **Output:** `NVIS_80_40m_Optimized_SUV_3D.jpg`
- **Loop:** 1.20 m diameter circular, 28 mm Ag-plated Cu
- **Efficiency:** 80 m ~5.2% | 40 m ~23.6%
- **Improvements:** +44% area, -25% Cu loss (Ag plating), 2-turn for 80 m

### 3. Optimized Rectangular Loop on Sedan (Latest)
- **File:** `gen_nvis_80_40m_optimized.py`
- **Output:** `NVIS_80_40m_Optimized_Sedan_3D.jpg`
- **Loop:** 1.40 x 0.80 m rectangular, 28 mm Ag-plated Cu
- **Area:** 1.12 m^2 (equivalent to 1.20 m circle)
- **Efficiency:** 80 m ~5.2% | 40 m ~23.6%
- **Vehicle:** Metallic dark blue sedan with detailed 3D rendering
- **Features:** Rounded corners (50 mm radius), 100 mm turn spacing, 4 corner standoffs

---

## Key Specifications

| Parameter | 80 m (2-Turn) | 40 m (1-Turn) |
|---|---|---|
| Frequency | 3.500 - 4.000 MHz | 7.000 - 7.300 MHz |
| Loop Size | 1.40 x 0.80 m rect | 1.40 x 0.80 m rect |
| Tube | 28 mm Ag-plated Cu | 28 mm Ag-plated Cu |
| Turns | 2 series, 100 mm gap | 1 (Turn 2 bypassed) |
| Radiation Res. | ~3.3 mOhm | ~12.9 mOhm |
| Efficiency | 5.2% (was 1.7%) | 23.6% (was 12%) |
| ERP @ 50 W | 2.6 W | 11.8 W |
| Bandwidth | ~2.5 kHz | ~8 kHz |
| Cap Voltage | ~5.5 kV | ~3.9 kV |
| NVIS Range | 0 - 600 km (24h) | 0 - 600 km (day) |

---

## System Components

- **Dual Vacuum Capacitor Banks**
  - Bank A: 30-150 pF, 5 kV (40 m)
  - Bank B: 100-500 pF, 7.5 kV (80 m)
- **DPDT Band Relay** — switches cap banks
- **DPDT Turn-Switch Relay** — bypasses Turn 2 on 40 m
- **NEMA17 Stepper Motor** — auto-tunes capacitor
- **ESP32 Controller** — band selection + stepper control
- **Faraday Feed Loop** — 240 mm dia, RG-213, shielded both ends
- **4x NdFeB Mag-Mount** — 40 kg each, HDPE standoff posts

---

## Build Cost (Approximate)

| Item | Cost |
|---|---|
| 28 mm Ag-Cu tube | $65 |
| Vacuum caps x2 | $240 |
| DPDT relays x2 | $30 |
| NdFeB mag-mounts x4 | $30 |
| HDPE posts + clips | $18 |
| Stepper motor kit | $18 |
| ESP32 module | $12 |
| IP65 enclosure | $14 |
| Silver plating | $40 |
| Solder + hardware | $20 |
| **Total** | **~$487** |

---

## NVIS Propagation Notes

- **80 m NVIS** is reliable **24 hours** (F2 layer always supports 3.5 MHz)
- **40 m NVIS** works best during **daytime** (foF2 > 7 MHz required)
- 2.6 W ERP on 80 m is sufficient for SSB/CW contacts within 300-500 km
- Elevation angle: 70-90 degrees (near-vertical incidence)
- F2 layer reflection at ~250 km altitude

---

## Single-Band Designs

### 20 m NVIS Loop
- **File:** `gen_nvis_20m_car_roof.py`
- **Output:** `NVIS_20m_Car_Roof_3D.jpg`
- Single-turn loop optimized for 14 MHz NVIS

### 40 m NVIS Loop
- **File:** `gen_nvis_40m_car_roof.py`
- **Output:** `NVIS_40m_Car_Roof_3D.jpg`
- Single-turn loop optimized for 7 MHz NVIS on sedan

---

## How to Generate Posters

```bash
# Requires Python 3 + matplotlib + numpy
pip install matplotlib numpy

# Generate all posters
python gen_nvis_20m_car_roof.py
python gen_nvis_40m_car_roof.py
python gen_nvis_80_40m_car_roof.py
python gen_nvis_80_40m_optimized.py
```

Each script produces a high-resolution JPG poster (9600x6800 px @ 200 DPI) with:
- 3D vehicle + antenna installation view
- Complete specifications table
- Build & installation guide
- Efficiency comparison charts
- Loss budget pie charts

---

*HS0ZNR | 2026*
