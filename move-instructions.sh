#!/bin/bash

# Move Claude-generated instructional files to do-not-move-git directory
# This keeps your GitHub repo clean with only essential files

echo "Moving instructional files to do-not-move-git directory..."

# Create directory structure
mkdir -p do-not-move-git/claude-instructions
mkdir -p do-not-move-git/documentation-guides

# Move all instructional/guide files
echo "Moving setup and guide files..."
mv -v QUICKSTART.md do-not-move-git/documentation-guides/ 2>/dev/null
mv -v SETUP_GUIDE.md do-not-move-git/documentation-guides/ 2>/dev/null
mv -v GET_STARTED.md do-not-move-git/documentation-guides/ 2>/dev/null
mv -v QUICK_REFERENCE.txt do-not-move-git/documentation-guides/ 2>/dev/null
mv -v GITIGNORE_GUIDE.md do-not-move-git/documentation-guides/ 2>/dev/null

# Move UI and feature documentation
echo "Moving feature documentation..."
mv -v UI_REDESIGN.md do-not-move-git/documentation-guides/ 2>/dev/null
mv -v DETAILED_COVERAGE_UPDATE.md do-not-move-git/documentation-guides/ 2>/dev/null
mv -v PREVIEW_AND_SUMMARY_UPDATE.md do-not-move-git/documentation-guides/ 2>/dev/null

# Move changelog
echo "Moving changelog..."
mv -v CHANGELOG.md do-not-move-git/documentation-guides/ 2>/dev/null

# Move all diagram instruction files
echo "Moving diagram instruction files..."
mv -v GENERATE_DIAGRAMS.md do-not-move-git/claude-instructions/ 2>/dev/null
mv -v DIAGRAMS_GENERATED.md do-not-move-git/claude-instructions/ 2>/dev/null
mv -v ARCHITECTURE_DIAGRAMS_SUMMARY.md do-not-move-git/claude-instructions/ 2>/dev/null
mv -v QUICK_START_DIAGRAMS.txt do-not-move-git/claude-instructions/ 2>/dev/null
mv -v INDEX_ARCHITECTURE_DOCS.md do-not-move-git/claude-instructions/ 2>/dev/null

# Move project overview (keep ARCHITECTURE.md)
echo "Moving project overview..."
mv -v PROJECT_OVERVIEW.md do-not-move-git/documentation-guides/ 2>/dev/null

# Move docs directory instructional files
echo "Moving docs directory instructions..."
mv -v docs/README-DIAGRAMS.md do-not-move-git/claude-instructions/ 2>/dev/null
mv -v docs/images/README.md do-not-move-git/claude-instructions/ 2>/dev/null

# Move verification script
echo "Moving verification script..."
mv -v verify-setup.js do-not-move-git/documentation-guides/ 2>/dev/null

# Move this instruction file itself
echo "Moving GitHub ready instructions..."
mv -v GITHUB_READY.md do-not-move-git/claude-instructions/ 2>/dev/null
mv -v CLEANUP_SUMMARY.txt do-not-move-git/claude-instructions/ 2>/dev/null

# Move the move script itself to the directory (after completion)
echo "Moving cleanup script to archive..."
cp move-instructions.sh do-not-move-git/claude-instructions/
echo "  (Keeping copy in root - delete manually after use if desired)"

echo ""
echo "✅ Done! Instructional files moved to do-not-move-git/"
echo ""
echo "Files kept in repository (for GitHub):"
echo "  ✓ README.md - Main project documentation"
echo "  ✓ ARCHITECTURE.md - Architecture documentation"
echo "  ✓ package.json - Dependencies"
echo "  ✓ server.js - Application code"
echo "  ✓ lib/*.js - Application code"
echo "  ✓ public/*.html, *.css, *.js - Frontend code"
echo "  ✓ .gitignore - Git configuration"
echo "  ✓ .env.example - Environment template"
echo "  ✓ generate-diagrams.py - Diagram generator"
echo ""
echo "Files moved to do-not-move-git/ (excluded from git):"
echo "  • All setup guides (QUICKSTART, SETUP_GUIDE, GET_STARTED, etc.)"
echo "  • All diagram instructions (GENERATE_DIAGRAMS, etc.)"
echo "  • Feature documentation (UI_REDESIGN, COVERAGE_UPDATE, etc.)"
echo "  • Changelog and reference files"
echo ""
echo "Your repository is now clean and ready for GitHub! 🚀"
