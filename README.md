# Hypertrophy Toolbox v3

Design your workout plan using science - all the tools you need to design, track, and monitor your workouts.

## 🚀 Running the Application

### Option 1: One-Click Start (Recommended for Windows Users)

**Double-click `START.bat`** - That's it!

**Requirement:** Python 3.14.6 or newer. The launcher reads `.python-version`,
selects the registered Python 3.14 runtime through the Windows Python launcher,
and checks any existing `venv` before starting.

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

1. **Install Python 3.14.6 or newer:**

   Use the [Python 3.14.6 release](https://www.python.org/downloads/release/python-3146/)
   or another compatible 3.14.6+ distribution. The committed
   `.python-version` is the canonical interpreter pin used by CI and
   version-aware environment managers.

2. **Create and activate virtual environment:**
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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   npm install
   npm run build:css
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open** `http://localhost:5000`

---

## 📁 Launcher Files

| File | Description |
|------|-------------|
| `START.bat` | 1-click launcher (requires Python installed) |
| `build_exe.bat` | Builds standalone .exe for distribution |
| `app_launcher.py` | Wrapper script for executable build |
| `QUICK_START.md` | Feature walkthrough (starter generator, progression, pattern coverage) and troubleshooting |

## 💾 Recovering Data from an Automatic Snapshot

The app keeps two independent backups. **Only the first can be restored from inside the app.**

| | Backup Center | Startup database snapshots |
|---|---|---|
| What it saves | Your workout plan | The entire database file |
| Where it lives | Inside `database.db` | `auto_backup\database_<timestamp>.db` |
| Survives a lost or corrupted `database.db`? | **No** — it lives inside that file | **Yes** — separate files |
| How to restore | In the app — Backup Center → **Restore To Current Plan** | **By hand — steps below** |

Startup snapshots are disaster recovery. They are never listed in the Backup Center, and there is deliberately no in-app restore button for them — recovering one means copying a file yourself.

> ### ⚠️ Before you restart the app, read this
>
> The app keeps only the **7 most recent** snapshots and deletes the oldest each time it takes a new one — which is every normal start. It takes one **even when your data is already gone**, because the check that skips it counts the built-in exercise library, not your workouts, and that library is always present.
>
> So from the **very first restart after a problem appears**, each launch destroys one real snapshot, oldest first — the one most likely to predate the problem. Seven restarts and every genuine snapshot is gone.
>
> **Close the app and copy the whole `auto_backup` folder somewhere safe — your Desktop is fine — before you restart anything or try any fix.** Everything below works on that copy.

### When a snapshot is taken

- Every time the app starts, except the very first launch of a brand-new install.
- Immediately before **Erase All Data** wipes everything, so a full erase stays recoverable. The confirmation message names the file it just wrote.

### Where the snapshots are

The folder sits beside whichever database the app is using. **Start the app normally with `START.bat`? Use the first row. Running the standalone `.exe`? Use the last row.** The middle two apply only if you set those variables yourself.

| How you run it | Snapshot folder |
|---|---|
| `START.bat` from a source checkout | `<repo>\data\auto_backup\` |
| With `HT_RUNTIME_DIR` set | `<HT_RUNTIME_DIR>\data\auto_backup\` |
| With `DB_FILE` set | an `auto_backup\` folder beside that file |
| Standalone executable (Windows) | `%LOCALAPPDATA%\HypertrophyToolbox\data\auto_backup\` |

If you set both variables, `DB_FILE` wins — it decides the database path outright, and the folder follows the database.

If none of those has what you expect, the app records the exact path every time it writes one. Open `logs\app.log` and search for `Auto-backup written to`.

If you upgraded from an older version, an older set may still sit in the `data\auto_backup\` folder next to the app itself. Copy that folder out too.

Files are named `database_<YYYYMMDD>_<HHMMSS>.db`, stamped in local time.

### Restoring one by hand

> Do this with the app **closed**, on the copy you made above.

1. **Stop the app.** Close the console window, or quit the executable.
2. **Pick a snapshot** — the newest one timestamped *before* the problem appeared.
3. **Rename the current database out of the way — do not delete anything.** In the folder holding `database.db`, rename **every** file whose name starts with `database.db` to start with `database.broken.db` instead, keeping the rest of the name exactly:
   - `database.db` → `database.broken.db`
   - `database.db-wal` → `database.broken.db-wal` *(if present)*
   - `database.db-shm` → `database.broken.db-shm` *(if present)*
   - `database.db-journal` → `database.broken.db-journal` *(if present)*

   Those extra files are not junk — they hold your most recent changes, and they belong to the database they are named after. Renaming them together keeps the broken copy intact and, just as importantly, stops them being applied to the snapshot you are about to put in their place.
4. **Check the folder.** Nothing named `database.db` or `database.db-…` should be left.
5. **Copy the snapshot into place.** Copy — do not move — your chosen `database_<timestamp>.db` into that folder and rename the copy to `database.db`. Copying keeps the snapshot intact if you picked the wrong one.
6. **Start the app and check.** Open Workout Plan and Weekly Summary and confirm the data is the version you expected. If it is not, stop the app and repeat from step 3 with a different snapshot — your `database.broken.db` and your copied folder are both still there.

Once you are satisfied, delete the `database.broken.db*` files yourself; nothing removes them for you.

### Good to know

- **If the database is corrupted, the app does not recover your data for you.** It renames the damaged file to `database.db.corrupted_<timestamp>` and starts with an empty database. That file is worth keeping too — but note it deletes the `-wal` and `-shm` files first, so the quarantined copy loses whatever was still only in them. One more reason to copy things out before you restart.
- **A Backup Center restore replaces your whole current plan and deletes your workout log.** Do not reach for it while you are investigating a lost or corrupted database — finish the file steps above first.
- The Backup Center also has its own entries under **Auto Recovery**. Those are a different thing with a different limit, stored inside the database, and unrelated to the snapshot files described here.

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
- **Python**: 3.14.6+ (source, CI, type analysis, and executable builds)
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Styling**: Custom Bootstrap 5.1.3 build + custom CSS
- **Testing**: pytest, Playwright (Chromium), Vitest

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📄 License

All rights reserved.
