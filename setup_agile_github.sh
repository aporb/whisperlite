#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# WhisperLite GitHub Agile Setup Script
# -----------------------------------------------------------------------------
# - Creates GitHub labels, milestones, and a project board
# - Sets up an Agile-friendly environment for tracking sprints and issues
# - Requires: GitHub CLI (`gh`) to be authenticated
# -----------------------------------------------------------------------------

set -euo pipefail

REPO_NAME=$(basename $(git config --get remote.origin.url) .git)
GITHUB_USER="aporb"

echo "🛠️  Setting up GitHub repo '$GITHUB_USER/$REPO_NAME' for Agile development..."

echo "🔖 Creating GitHub labels..."
gh label create "epic" --description "High-level epic grouping multiple tasks" --color "5319e7" || true
gh label create "feature" --description "New user-facing feature" --color "1d76db" || true
gh label create "enhancement" --description "Improvement to an existing feature" --color "84b6eb" || true
gh label create "bug" --description "Bug or defect" --color "d73a4a" || true
gh label create "documentation" --description "Docs, guides, or READMEs" --color "0075ca" || true
gh label create "good first issue" --description "Good for new contributors" --color "7057ff" || true
gh label create "needs design" --description "Needs UX or UI design" --color "c2e0c6" || true
gh label create "needs feedback" --description "Requires input before proceeding" --color "bfdadc" || true
gh label create "blocked" --description "Blocked by another issue" --color "e4e669" || true
gh label create "in progress" --description "Currently being worked on" --color "0e8a16" || true
gh label create "done" --description "Work is completed" --color "1d76db" || true

echo "📅 Creating milestones (sprints)..."
gh milestone create "Sprint 0: Planning" --description "Repo setup and task scoping"
gh milestone create "Sprint 1: MVP Engine" --description "Audio capture and transcription MVP"
gh milestone create "Sprint 2: Display & UX" --description "Overlay window and user interaction"
gh milestone create "Sprint 3: Packaging" --description "Cross-platform build system"
gh milestone create "Sprint 4: Testing & Polish" --description "Test coverage, polish, CI/CD"

echo "📋 Creating GitHub project board..."
gh project create --title "WhisperLite Agile Board" --format "table" --owner "$GITHUB_USER"

echo "✅ GitHub Agile environment setup complete for $REPO_NAME"
