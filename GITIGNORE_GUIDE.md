# .gitignore Guide

## Overview

A comprehensive `.gitignore` file has been created to protect sensitive data, exclude system files, and keep your repository clean.

---

## What's Ignored

### 🔒 Security & Secrets (CRITICAL)
- `.env` - Your Claude API key and other secrets
- `.env.local`, `.env.*.local` - All local environment overrides
- `config.local.js`, `settings.local.json` - Local configurations

**⚠️ NEVER commit your .env file!**

### 📁 Node.js & Dependencies
- `node_modules/` - All npm packages (use package.json instead)
- `npm-debug.log*`, `yarn-error.log*` - Debug logs
- `package-lock.json`, `yarn.lock` - Lock files (optional)
- `.npm/`, `.eslintcache` - Cache directories

### 🍎 Mac-Specific Files
- `.DS_Store` - Finder metadata
- `.AppleDouble`, `.LSOverride` - Resource forks
- `._*` - Mac thumbnail cache
- `.Spotlight-V100` - Spotlight search index
- `.Trashes` - Trash folder
- `.VolumeIcon.icns` - Volume icons
- `.fseventsd` - File system events daemon
- `.DocumentRevisions-V100` - Document revisions
- `.com.apple.timemachine.donotpresent` - Time Machine marker
- `.AppleDB`, `.AppleDesktop` - Apple database files
- `Network Trash Folder`, `Temporary Items` - Network storage
- `.apdisk` - Network disk image

### 🚫 Project-Specific Exclusions
- `do-not-move-git/` - Protected directory (as requested)
- `do-not-move-git/**/*` - All contents within

### 📊 Excel Files
- `*.xlsx`, `*.xls` - User uploaded test files
- `!Mock_*.xlsx`, `!Mock_*.xls` - Exception: Keep example files

### 📝 Logs & Temporary Files
- `logs/`, `*.log` - All log files
- `tmp/`, `temp/` - Temporary directories
- `*.tmp`, `*.temp` - Temporary files

### 🔧 IDE & Editor Files
- `.vscode/` - VS Code settings
- `.idea/` - JetBrains IDEs (IntelliJ, WebStorm, etc.)
- `*.swp`, `*.swo`, `*~` - Vim/editor swap files
- `.sublime-project`, `.sublime-workspace` - Sublime Text

### 🪟 Windows Files
- `Thumbs.db`, `ehthumbs.db` - Windows thumbnails
- `Desktop.ini` - Folder settings
- `$RECYCLE.BIN/` - Recycle bin

### 🏗️ Build & Cache Directories
- `dist/`, `build/`, `out/` - Build outputs
- `coverage/`, `.nyc_output/` - Test coverage
- `.cache/` - Cache directories

### 📄 Backup Files
- `*.bak`, `*.backup`, `*.old`, `*.orig` - All backup variants

---

## What's Tracked

✅ **Source Code**
- `server.js` - Main server
- `lib/*.js` - Backend modules
- `public/*.html` - HTML files
- `public/*.css` - Stylesheets
- `public/*.js` - Frontend JavaScript

✅ **Configuration** (Safe)
- `package.json` - Dependencies list
- `.env.example` - Environment template (no real secrets)
- `.gitignore` - This file

✅ **Documentation**
- `*.md` files - All documentation
- `README.md`, `QUICKSTART.md`, etc.

✅ **Example Data**
- `Mock_*.xlsx` - Example Excel files (exception to .xlsx rule)

---

## Common Git Commands

### Initialize Repository
```bash
cd /Users/Prashanth/Documents/senslytics/github/mock-data/coverage-analyzer
git init
git add .
git commit -m "Initial commit"
```

### Check What's Ignored
```bash
# See all ignored files
git status --ignored

# Check if specific file is ignored
git check-ignore -v .DS_Store
git check-ignore -v .env
git check-ignore -v do-not-move-git/test.txt
```

### View Status
```bash
# Normal status (tracked files only)
git status

# Verbose status with ignored files
git status --ignored --short
```

### Remove Accidentally Tracked Files
```bash
# If you accidentally committed .DS_Store before
git rm --cached .DS_Store
git commit -m "Remove .DS_Store"

# Remove all .DS_Store files recursively
find . -name .DS_Store -print0 | xargs -0 git rm --cached
git commit -m "Remove all .DS_Store files"

# Remove .env if accidentally committed
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

## Special Cases

### do-not-move-git Directory

The `do-not-move-git/` directory and all its contents are fully protected:

```gitignore
do-not-move-git/
do-not-move-git/**/*
```

**This means:**
- Nothing inside this directory will ever be tracked
- Safe for sensitive files, personal notes, etc.
- Even if you run `git add .`, it won't be included

**Test it:**
```bash
# Create a test file
mkdir -p do-not-move-git
echo "secret" > do-not-move-git/secret.txt

# Try to add it
git add do-not-move-git/secret.txt
# Output: "The following paths are ignored by one of your .gitignore files"

# Verify it's ignored
git check-ignore -v do-not-move-git/secret.txt
```

### Excel Files

**General rule:** Ignore all Excel files (user uploads)

```gitignore
*.xlsx
*.xls
```

**Exception:** Keep example files starting with "Mock_"

```gitignore
!Mock_*.xlsx
!Mock_*.xls
```

**Result:**
- ✅ `Mock_Banking_Regulatory_Questionnaire_Detail.xlsx` - Tracked
- ✅ `Mock_2LOD_Full_Population_Test_Inventory.xlsx` - Tracked
- ❌ `my_test_file.xlsx` - Ignored
- ❌ `uploaded_questionnaire.xlsx` - Ignored

---

## Security Best Practices

### ✅ DO Commit
- Source code files
- Documentation
- `.env.example` (template without real keys)
- `package.json` (dependencies list)
- `.gitignore` itself

### ❌ DON'T Commit
- `.env` file (contains API keys!)
- `node_modules/` (too large, rebuilt from package.json)
- `.DS_Store` (Mac system file)
- Log files
- User-uploaded data
- Backup files
- Build outputs

### If You Accidentally Committed Secrets

**If you committed .env with your API key:**

1. **Remove from Git:**
   ```bash
   git rm --cached .env
   git commit -m "Remove .env from tracking"
   ```

2. **Rotate your API key:**
   - Go to https://console.anthropic.com/
   - Delete the exposed key
   - Generate a new key
   - Update your local `.env` file

3. **Force push if needed (be careful!):**
   ```bash
   git push --force
   ```

4. **Consider using git-filter-branch or BFG Repo-Cleaner to remove from history**

---

## Testing Your .gitignore

### Method 1: Check Status
```bash
# Should show only tracked files
git status

# Should show ignored files
git status --ignored
```

### Method 2: Dry Run
```bash
# See what would be added
git add --dry-run .

# Should NOT include .env, node_modules, .DS_Store, etc.
```

### Method 3: Explicit Check
```bash
# Test specific files
git check-ignore -v .env              # Should be ignored
git check-ignore -v node_modules      # Should be ignored
git check-ignore -v .DS_Store         # Should be ignored
git check-ignore -v do-not-move-git   # Should be ignored
git check-ignore -v package.json      # Should NOT be ignored
```

---

## Updating .gitignore

### After Adding to .gitignore

If you add patterns to `.gitignore` after files are already tracked:

```bash
# Update git's index
git rm -r --cached .

# Re-add everything (respecting new .gitignore)
git add .

# Commit the changes
git commit -m "Update .gitignore and remove tracked files"
```

### Common Additions

If you need to ignore more patterns:

```bash
# Edit .gitignore
nano .gitignore

# Add your patterns, for example:
# local-config/
# *.secret
# debug-*.log

# Update git
git rm -r --cached .
git add .
git commit -m "Update gitignore patterns"
```

---

## Platform-Specific Notes

### macOS
All Mac-specific files are already covered:
- Finder metadata (`.DS_Store`)
- Resource forks (`._*`, `.AppleDouble`)
- Spotlight index (`.Spotlight-V100`)
- Time Machine markers
- Network storage artifacts

### Windows
If collaborating with Windows users:
- `Thumbs.db` - Already covered
- `Desktop.ini` - Already covered
- `$RECYCLE.BIN/` - Already covered

### Linux
Linux-specific files:
- `*~` - Backup files (already covered)

---

## File Location

```
/Users/Prashanth/Documents/senslytics/github/mock-data/coverage-analyzer/.gitignore
```

---

## Quick Reference

| File/Directory | Tracked? | Reason |
|----------------|----------|--------|
| `package.json` | ✅ Yes | Required for dependencies |
| `server.js` | ✅ Yes | Source code |
| `.env` | ❌ No | Contains secrets |
| `.env.example` | ✅ Yes | Safe template |
| `node_modules/` | ❌ No | Too large, rebuilt from package.json |
| `.DS_Store` | ❌ No | Mac system file |
| `do-not-move-git/` | ❌ No | Protected directory |
| `Mock_*.xlsx` | ✅ Yes | Example files (exception) |
| `my_file.xlsx` | ❌ No | User uploads ignored |
| `*.log` | ❌ No | Log files |
| `README.md` | ✅ Yes | Documentation |

---

## Summary

The `.gitignore` file provides comprehensive protection for:

1. **Security**: API keys and secrets never committed
2. **Privacy**: Mac system files excluded
3. **Cleanliness**: Dependencies and builds excluded
4. **Flexibility**: Examples kept, user data ignored
5. **Protection**: `do-not-move-git/` fully excluded

**You're safe to commit!** Just run:

```bash
git init
git add .
git commit -m "Initial commit"
```

All sensitive files will be automatically excluded.
