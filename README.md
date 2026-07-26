# Hypertrophy Toolbox v3

Design your workout plan using science - all the tools you need to design, track, and monitor your workouts.

## 🚀 Running the Application

### Option 1: One-Click Start (Recommended for Windows Users)

**Double-click `START.bat`** - That's it!

This will automatically:
- Check for Python installation
- Create a virtual environment
- Install all dependencies
- Start the Flask server
- Open your browser to `http://127.0.0.1:5000`

> **Note:** If the browser doesn't open automatically, manually navigate to `http://127.0.0.1:5000`

### Option 2: Standalone Executable (No Installation Required)

**This option is for users who received a pre-packaged zip file.**

**Requirements:** None! No Python, no installation, no setup needed.

**Steps:**
1. Extract the zip file to any folder on your computer
2. Open the extracted folder
3. Double-click `Hypertrophy-Toolbox.exe`
4. Your browser will open automatically to the app

> **Troubleshooting:** 
> - If Windows shows a security warning, click "More info" → "Run anyway"
> - If browser doesn't open, manually go to `http://127.0.0.1:5000`

---

### Option 3: Manual Setup (For Developers)

1. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

   > **Why `.venv` and not `venv`?** They are two environments with different
   > jobs, and the split is deliberate. `.venv` is the development environment —
   > the one `playwright.config.ts`, `pyrightconfig.json`, and the test commands
   > all expect. `venv` belongs to `START.bat` and `build_exe.bat`; the build
   > installs the pinned toolchain there from the committed requirements files, so
   > a release never depends on packages that happen to be in a developer's
   > environment. Don't build from `.venv`, and don't point the tools at `venv`.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   npm run build:css
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open** `http://localhost:5000`

---

## 📁 Launcher Files

| File | Description |
|------|-------------|
| `START.bat` | 1-click launcher (requires Python installed) |
| `build_exe.bat` | Builds standalone .exe for distribution |
| `app_launcher.py` | Wrapper script for executable build |
| `QUICK_START.md` | Feature walkthrough (starter generator, progression, pattern coverage) and troubleshooting |

## 📦 Building the Standalone Executable (For Developers)

To create the standalone `.exe` package for distribution to end users:

1. **Run the build script:**
   ```bash
   build_exe.bat
   ```
   (the pinned build toolchain is installed into `venv/`, from
   `requirements.txt` + `requirements-build.txt` — not from your `.venv`)

2. **Find the output in the `dist` folder (NOT `build`):**
   ```
   dist/                              ← CORRECT folder
   └── Hypertrophy-Toolbox/
       ├── Hypertrophy-Toolbox.exe   ← Run this!
       ├── RUN_APP.bat
       └── _internal/                 ← Required support files (do not delete)
   ```

   > **Important:** The `build` folder contains temporary files and will NOT work. Always use `dist`.

3. **Fresh-install data:** The package contains an immutable exercise catalog
   seed. The first launch copies it to the runtime `database.db`; it never
   overwrites an existing database.

4. **Distribute:** Zip the entire `dist/Hypertrophy-Toolbox/` folder and share with users

## ✨ Features

- **Auto Starter Plan Generator** - Generate complete workout plans based on movement patterns with customizable experience, goals, and priority muscles
- **Double Progression System** - Smart progression suggestions that tell you when to increase weight or reps
- **Movement Pattern Coverage** - Analyze your program balance (squat, hinge, push, pull) with actionable warnings
- **Workout Plan Builder** - Create custom routines with exercises filtered by muscle groups, equipment, and more
- **Exercise Database** - Comprehensive library with scientific parameters (RIR, RPE, rep ranges)
- **Workout Logging** - Track actual performance vs. planned workouts
- **Weekly & Session Summaries** - Analytics with volume tracking and data visualization
- **Volume Splitter** - Volume distribution and muscle group allocation tools
- **Program Backups** - Save and restore workout programs
- **Data Export** - Export to Excel with proper formatting
- **Dark Mode** - System-aware theme
- **Responsive Tables** - Adaptive tables with sticky headers and column prioritization

## 📚 Documentation

See the [`docs/`](docs/) folder:

- [README.md](docs/README.md) - Documentation index
- [CLAUDE.md](CLAUDE.md) - Architecture, module boundaries, and conventions
- [CHANGELOG.md](docs/CHANGELOG.md) - Version history
- [CSS_OWNERSHIP_MAP.md](docs/CSS_OWNERSHIP_MAP.md) - CSS file organization
- [muscle_selector.md](docs/muscle_selector.md) - Muscle selector component
- [program_backups.md](docs/program_backups.md) - Backup/restore feature

## 🛠️ Tech Stack

- **Backend**: Flask 3.1+, SQLite
- **Python**: 3.11+ (CI runs 3.11; developed and built on 3.14)
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Styling**: Custom Bootstrap 5.1.3 build + custom CSS
- **Testing**: pytest, Playwright (Chromium), Vitest

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📄 License

All rights reserved.
