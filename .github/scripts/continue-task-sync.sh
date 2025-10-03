#!/bin/bash

# Continue creating GitHub issues from tasks.md, skipping already created ones
set -e

echo "🔄 Continuing GitHub Issues creation from tasks.md..."

# Check if we're in the right directory and find tasks.md
TASKS_FILE=""
if [ -f "tasks.md" ]; then
    TASKS_FILE="tasks.md"
elif [ -f "specs/001-multi-sport-betting/tasks.md" ]; then
    TASKS_FILE="specs/001-multi-sport-betting/tasks.md"
else
    echo "❌ tasks.md not found. Please run from the repository root."
    exit 1
fi

echo "📄 Using tasks file: $TASKS_FILE"

# Check GitHub CLI authentication
if ! gh auth status > /dev/null 2>&1; then
    echo "❌ Not authenticated with GitHub CLI. Run 'gh auth login' first."
    exit 1
fi

# Get list of existing task IDs from GitHub
echo "📋 Checking existing GitHub issues..."
existing_tasks=$(gh issue list --label task --limit 1000 --json title --jq '.[].title' | grep -o 'T[0-9]\+' | sort | uniq)
existing_count=$(echo "$existing_tasks" | wc -l)
echo "📊 Found $existing_count existing task issues"

# Extract tasks and create them, skipping already created ones
count=0
created_count=0
skipped_count=0

echo "🚀 Processing tasks from tasks.md..."

while IFS= read -r line; do
    if [[ $line =~ ^-\ \[\ \]\ (T[0-9]+)\ (\[P\])?\ (.+) ]]; then
        task_id="${BASH_REMATCH[1]}"
        parallel="${BASH_REMATCH[2]}"
        description="${BASH_REMATCH[3]}"
        
        # Check if this task already exists
        if echo "$existing_tasks" | grep -q "^$task_id$"; then
            echo "⏭️  Skipping $task_id (already exists)"
            skipped_count=$((skipped_count + 1))
            continue
        fi
        
        # Determine priority and labels
        task_num=${task_id#T}
        task_num=$((10#$task_num))
        
        labels="task"
        if [[ $task_num -le 51 ]]; then
            labels="$labels,priority:high,setup"
        elif [[ $task_num -le 79 ]]; then
            labels="$labels,priority:high,tdd"
        else
            labels="$labels,priority:medium"
        fi
        
        # Create issue body
        body="## Task Description
$description

## TDD Workflow
- [ ] **RED**: Write failing tests first
- [ ] **GREEN**: Implement minimal code to pass tests  
- [ ] **REFACTOR**: Improve code quality while keeping tests green

## Acceptance Criteria
- [ ] All tests pass
- [ ] Code follows project conventions
- [ ] Ready for code review

**Task ID**: $task_id
**Parallel**: ${parallel:-"No"}
"
        
        echo "📝 Creating: $task_id - $description"
        
        # Create the issue
        url=$(gh issue create \
            --title "$task_id: $description" \
            --body "$body" \
            --label "$labels" \
            --repo ChPfisterer/betting-league-championship)
        
        if [ $? -eq 0 ]; then
            echo "✅ Created: $url"
            created_count=$((created_count + 1))
        else
            echo "❌ Failed to create issue for $task_id"
        fi
        
        count=$((count + 1))
        
        # Rate limiting: pause after every 5 issues
        if [ $((created_count % 5)) -eq 0 ] && [ $created_count -gt 0 ]; then
            echo "⏳ Pausing for rate limiting..."
            sleep 2
        fi
        
        # Stop after 25 new issues to avoid overwhelming
        if [ $created_count -ge 25 ]; then
            echo "📊 Created $created_count new issues in this batch"
            break
        fi
    fi
done < "$TASKS_FILE"

echo ""
echo "📊 Summary:"
echo "   - Skipped (already exist): $skipped_count"
echo "   - Created this run: $created_count"
echo "   - Total processed: $count"

if [ $created_count -eq 25 ]; then
    echo ""
    echo "🔄 Run this script again to create more issues!"
elif [ $created_count -eq 0 ]; then
    echo ""
    echo "🎉 All tasks have been converted to GitHub issues!"
else
    echo ""
    echo "✨ Batch complete!"
fi