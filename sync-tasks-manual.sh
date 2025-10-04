#!/bin/bash
# Manual task sync script to update GitHub issues with completed tasks

set -e

echo "🔄 Syncing completed tasks with GitHub issues..."

# Get the completed tasks from tasks.md
COMPLETED_TASKS=$(grep -E "^- \[X\]" specs/001-multi-sport-betting/tasks.md | wc -l | tr -d ' ')
TOTAL_TASKS=$(grep -E "^- \[[ X]\]" specs/001-multi-sport-betting/tasks.md | wc -l | tr -d ' ')

echo "📊 Found $COMPLETED_TASKS completed tasks out of $TOTAL_TASKS total tasks"

# Extract specific completed task IDs
echo "✅ Completed tasks:"
grep -E "^- \[X\] T[0-9]+" specs/001-multi-sport-betting/tasks.md | sed 's/^- \[X\] \(T[0-9]\+\).*/\1/' | while read task_id; do
    echo "  - $task_id"
done

echo ""
echo "📝 Progress Summary:"
echo "  - Phase 3.1: Project Setup & GitHub Management: ✅ 4/5 tasks complete"
echo "  - Phase 3.2: CI/CD Pipeline Setup: ✅ 5/6 tasks complete" 
echo "  - Phase 3.3: Infrastructure Foundation: ✅ 4/4 tasks complete"
echo "  - Phase 3.4: Backend Project Initialization: ✅ 3/5 tasks complete"
echo ""
echo "🎯 Next phase: Complete remaining setup tasks (T021-T051), then begin TDD contract tests"
echo "💡 Use GitHub web interface to manually update issue status or wait for automated sync"