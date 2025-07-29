# Bioreactor Instrumentation and Growth Condition Logging

This repository contains all code used for operating, controlling, and logging environmental parameters from a custom-built bioreactor system designed for cyanobacterial cultivation. The system integrates multiple sensors and actuators to monitor and regulate conditions such as temperature, light, dissolved oxygen, and pH, and includes an online optical density (OD) measurement system for real-time biomass tracking.

## 📁 Repository Structure

### `controls/`
Contains all scripts needed to operate and log data from:
- pH probe (including a dedicated calibration script)
- Dissolved oxygen (DO) probe (with calibration handled internally)
- RTD temperature probe  
- Custom optical density instrument (with built-in calibration)
- Godox LED lighting system  
- Recirculating chiller for temperature control

### `main4.py`
The primary script responsible for operating the **online optical density system**, which automatically collects samples and records OD measurements **every hour**.

### `analysis/`
Includes scripts for analyzing documented growth conditions and sensor readings. The most critical analysis focuses on **optical density**, which uses light intensity measurements to calculate OD and reconstruct the **growth curve** over time.

## Features

- Real-time monitoring and logging of environmental parameters
- Automated sampling and OD measurement system
- Calibrated pH and DO probes
- Integrated LED light and chiller control for consistent bioreactor conditions
- Post-experiment data analysis and visualization of growth trends

## Contributions

This code was written and developed by **Ingie Baho**, with support from the MIT Bioinstrumentation Lab.  
The work was carried out under the supervision of **Professor Ian Hunter**, who provided mentorship, lab space, and equipment.
This project was funded by the **MIT Bioinstrumentation Lab**. Special thanks to **Ian Hunter** for his continued support and guidance throughout the development of this system.

---

Please feel free to use, adapt, or extend this work. Contributions and feedback are always welcome!
