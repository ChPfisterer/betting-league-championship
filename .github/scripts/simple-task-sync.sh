#!/bin/bash

# Simple task issue creator - creates basic GitHub issues without complex labels

set -e

cd /Users/chp/repos/GitHub/betting-league-championship

echo "🚀 Creating GitHub Issues from tasks.md (simplified version)..."

# Create basic labels first
gh label create "priority:high" --description "High priority task" --color "d73a4a" 2>/dev/null || echo "Label may exist"
gh label create "priority:medium" --description "Medium priority task" --color "fbca04" 2>/dev/null || echo "Label may exist"
gh label create "priority:low" --description "Low priority task" --color "0e8a16" 2>/dev/null || echo "Label may exist"
gh label create "tdd" --description "Test-driven development" --color "1d76db" 2>/dev/null || echo "Label may exist"
gh label create "setup" --description "Project setup task" --color "5319e7" 2>/dev/null || echo "Label may exist"

# Extract tasks and create them, skipping already created ones
count=0
created_count=0

# Get list of existing task IDs from GitHub
existing_tasks=$(gh issue list --label task --limit 1000 --json title --jq '.[].title' | grep -o 'T[0-9]\+' | sort | uniq)

while IFS= read -r line; do
    if [[ $line =~ ^-\ \[\ \]\ (T[0-9]+)\ (\[P\])?\ (.+) ]]; then
        task_id="${BASH_REMATCH[1]}"
        parallel="${BASH_REMATCH[2]}"
        description="${BASH_REMATCH[3]}"
        
        # Check if this task already exists
        if echo "$existing_tasks" | grep -q "^$task_id$"; then
            echo "⏭️  Skipping $task_id (already exists)"
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
        gh issue create \
            --title "$task_id: $description" \
            --body "$body" \
            --label "$labels" 2>/dev/null || echo "❌ Failed to create $task_id"
        
        count=$((count + 1))
        if [[ $count -ge 20 ]]; then
            echo "✅ Created first 20 tasks. Run script again to create more."
            break
        fi
        
        # Small delay to avoid rate limiting
        sleep 0.5
    fi
done < specs/001-multi-sport-betting/tasks.md

echo "🎉 Created $count GitHub Issues successfully!"
echo ""
echo "Next steps:"
echo "1. View issues: gh issue list --label task"
echo "2. Assign yourself: gh issue edit <number> --add-assignee @me"
echo "3. Start working: The automated branch creation will trigger"