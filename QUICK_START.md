# Hypertrophy Toolbox - Quick Start Guide

## 🚀 For Users (Running the App)

### Option 1: Easy Start (Requires Python)
1. **Double-click `START.bat`**
2. Wait for setup to complete (first time only)
3. Browser opens automatically to the app!

### Option 2: Standalone Executable (No Python Needed)
If you received a zip file with the executable:
1. Extract the zip to any folder
2. Double-click `Hypertrophy-Toolbox.exe`
3. Browser opens automatically!

---

## ✨ Key Features

### 🎯 Auto Starter Plan Generator
Generate evidence-based workout plans with one click:
1. Go to **Workout Plan** page
2. Click the green **Generate Plan** button
3. Configure your preferences:
   - **Training Days**: 1-5 days per week
   - **Environment**: Gym (full equipment) or Home (bodyweight/minimal)
   - **Experience Level**: Novice, Intermediate, or Advanced
   - **Goal**: Hypertrophy, Strength, or General fitness
   - **Priority Muscles**: Select up to 2 muscles to get extra volume
4. Click **Generate Plan** to create your personalized routine

### 📈 Double Progression System
The progression tracker automatically suggests when to increase weight:
- **Hit top of rep range** (e.g., 3×10 when range is 6-10) → Increase weight
- **Below minimum reps** → Focus on adding reps first
- **In range but not at top** → Continue current load

View suggestions on the **Progression Plan** page.

### 🔍 Pattern Coverage Analysis
Monitor your program balance on the **Weekly Summary** page:
- See total sets per movement pattern (squat, hinge, push, pull)
- Get warnings for missing patterns or volume imbalances
- Track sets per routine (target: 15-24 sets per session)

---

## 🔧 For Developers

**Python 3.11+** (CI runs 3.11; developed and built on 3.14).

Build and distribution steps live in one place — see
[Building the Standalone Executable](README.md#-building-the-standalone-executable-for-developers)
in `README.md`. In short: run `build_exe.bat`, then zip `dist/Hypertrophy-Toolbox/`.

The build installs its own pinned toolchain into `venv/` from `requirements.txt`
and `requirements-build.txt`. Don't install PyInstaller by hand — an unpinned
version makes "the build succeeded" a claim about whatever release happened to be
current that day.

---

## ❓ Troubleshooting

### "Python is not installed" Error
- Download Python from https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation

### App Won't Start
- Make sure no other app is using port 5000
- Try running as Administrator

### Browser Doesn't Open
- Manually open: http://localhost:5000

### Executable Build Fails
- Re-run `build_exe.bat`. It installs everything it needs into `venv/` on every
  run, from `requirements.txt` and `requirements-build.txt`.
- Do **not** `pip install pyinstaller` manually. The version is pinned in
  `requirements-build.txt` on purpose; installing an unpinned one is how builds
  stop being reproducible.
- If it still fails, delete the `venv/`, `build/`, and `dist/` folders and run the
  script again.

---

## 📁 File Overview

See [Launcher Files](README.md#-launcher-files) in `README.md`.
