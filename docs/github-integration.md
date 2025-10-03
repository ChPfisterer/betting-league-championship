# GitHub Integration Guide for Task Management

## Overview

This guide sets up automated synchronization between your `tasks.md` and GitHub Issues, with automatic branch creation and PR management for each task implementation.

## GitHub Project Setup

### 1. Create GitHub Project (Beta)
```bash
# Using GitHub CLI
gh project create --title "Multi-Sport Betting Platform" --body "Comprehensive betting platform with TDD methodology"

# Or via GitHub web interface:
# 1. Go to your repository
# 2. Click "Projects" tab
# 3. Click "New project"
# 4. Choose "Board" layout
# 5. Name: "Multi-Sport Betting Platform"
```

### 2. Configure Project Fields
Add these custom fields to your GitHub Project:
- **Status**: Todo, In Progress, In Review, Done
- **Priority**: Low, Medium, High, Critical
- **Phase**: Setup, Tests, Implementation, Integration, Polish
- **TDD Status**: Contract Test, Unit Test, Implementation, Refactor
- **Estimated Points**: 1, 2, 3, 5, 8 (Fibonacci)

## Automated Issue Creation

### Script: Generate Issues from Tasks
Create `.github/scripts/sync-tasks-to-issues.js`:

```javascript
const fs = require('fs');
const { execSync } = require('child_process');

// Parse tasks.md and extract task information
function parseTasks() {
  const tasksContent = fs.readFileSync('specs/001-multi-sport-betting/tasks.md', 'utf8');
  const tasks = [];
  
  const taskRegex = /- \[ \] (T\d+) (\[P\])? (.+)/g;
  let match;
  
  while ((match = taskRegex.exec(tasksContent)) !== null) {
    const [, taskId, parallel, description] = match;
    tasks.push({
      id: taskId,
      title: `${taskId}: ${description}`,
      body: generateIssueBody(taskId, description, parallel),
      labels: generateLabels(taskId, description, parallel),
      assignees: [],
      milestone: determineMilestone(taskId)
    });
  }
  
  return tasks;
}

function generateIssueBody(taskId, description, parallel) {
  return `
## Task Description
${description}

## Implementation Requirements
- [ ] Follow TDD methodology (Red-Green-Refactor)
- [ ] Write tests first before implementation
- [ ] Ensure code coverage meets requirements
- [ ] Update documentation if needed

## Acceptance Criteria
- [ ] All tests pass
- [ ] Code review completed
- [ ] No merge conflicts
- [ ] CI/CD pipeline passes

## Related Files
<!-- List specific files that will be modified -->

## Dependencies
<!-- List task dependencies (must be completed first) -->

## Notes
${parallel ? '⚡ **Can run in parallel** with other [P] tasks' : '🔄 **Sequential task** - complete dependencies first'}

---
**Auto-generated from tasks.md | Task ID: ${taskId}**
  `;
}

function generateLabels(taskId, description, parallel) {
  const labels = ['task'];
  
  // Phase-based labels
  if (taskId.match(/T0(0[1-9]|1[0-1])/)) labels.push('phase:setup');
  else if (taskId.match(/T0(5[2-9]|6[0-9]|7[0-9])/)) labels.push('phase:tests');
  else if (taskId.match(/T0(8[0-9]|9[0-9]|10[0-9])/)) labels.push('phase:implementation');
  else if (taskId.match(/T1[1-2][0-9]/)) labels.push('phase:integration');
  else if (taskId.match(/T13[0-9]/)) labels.push('phase:polish');
  
  // Technology labels
  if (description.includes('backend')) labels.push('backend');
  if (description.includes('frontend')) labels.push('frontend');
  if (description.includes('Docker')) labels.push('infrastructure');
  if (description.includes('test')) labels.push('testing');
  if (description.includes('Grafana')) labels.push('observability');
  
  // Priority labels
  if (taskId.match(/T0[0-4][0-9]/)) labels.push('priority:high');
  else if (taskId.match(/T0[5-9][0-9]/)) labels.push('priority:medium');
  else labels.push('priority:low');
  
  // Parallel execution
  if (parallel) labels.push('parallel');
  
  return labels;
}

// Create GitHub issues
async function createIssues() {
  const tasks = parseTasks();
  
  for (const task of tasks) {
    try {
      const issueCmd = [
        'gh', 'issue', 'create',
        '--title', `"${task.title}"`,
        '--body', `"${task.body}"`,
        '--label', task.labels.join(','),
        task.milestone ? `--milestone "${task.milestone}"` : ''
      ].filter(Boolean).join(' ');
      
      console.log(`Creating issue: ${task.title}`);
      execSync(issueCmd, { stdio: 'inherit' });
      
      // Add small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      console.error(`Failed to create issue for ${task.id}:`, error.message);
    }
  }
}

// Run the script
createIssues().catch(console.error);
```

## GitHub Actions Workflows

### 1. Task-to-Issue Sync Workflow
Create `.github/workflows/sync-tasks.yml`:

```yaml
name: Sync Tasks to GitHub Issues

on:
  push:
    paths:
      - 'specs/001-multi-sport-betting/tasks.md'
    branches:
      - main
      - develop
  workflow_dispatch:

jobs:
  sync-tasks:
    runs-on: ubuntu-latest
    permissions:
      issues: write
      contents: read
      projects: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install GitHub CLI
        run: |
          curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
          echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
          sudo apt update
          sudo apt install gh
      
      - name: Authenticate GitHub CLI
        run: echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token
      
      - name: Sync tasks to issues
        run: node .github/scripts/sync-tasks-to-issues.js
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Auto Branch Creation Workflow
Create `.github/workflows/auto-branch.yml`:

```yaml
name: Auto Create Feature Branches

on:
  issues:
    types: [opened, assigned]

jobs:
  create-branch:
    if: contains(github.event.issue.labels.*.name, 'task')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Extract task ID from issue title
        id: extract-task
        run: |
          TITLE="${{ github.event.issue.title }}"
          TASK_ID=$(echo "$TITLE" | grep -o "T[0-9]*" | head -1)
          BRANCH_NAME="feature/$TASK_ID-$(echo "$TITLE" | sed 's/T[0-9]*: //' | sed 's/[^a-zA-Z0-9]/-/g' | tr '[:upper:]' '[:lower:]' | sed 's/--*/-/g' | sed 's/-$//')"
          echo "task_id=$TASK_ID" >> $GITHUB_OUTPUT
          echo "branch_name=$BRANCH_NAME" >> $GITHUB_OUTPUT
      
      - name: Create feature branch
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git checkout -b "${{ steps.extract-task.outputs.branch_name }}"
          git push origin "${{ steps.extract-task.outputs.branch_name }}"
      
      - name: Comment on issue with branch info
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🌟 **Branch created:** \`${{ steps.extract-task.outputs.branch_name }}\`
              
              ## Get started:
              \`\`\`bash
              git fetch origin
              git checkout ${{ steps.extract-task.outputs.branch_name }}
              \`\`\`
              
              ## TDD Workflow:
              1. ✅ Write failing tests first
              2. ✅ Implement minimal code to pass tests  
              3. ✅ Refactor for quality
              4. ✅ Create PR when complete
              
              **Remember**: Follow TDD methodology strictly!`
            });
```

### 3. Auto PR Creation Workflow
Create `.github/workflows/auto-pr.yml`:

```yaml
name: Auto Create Pull Request

on:
  push:
    branches:
      - 'feature/T*'

jobs:
  create-pr:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Extract task info from branch
        id: extract-info
        run: |
          BRANCH_NAME="${{ github.ref_name }}"
          TASK_ID=$(echo "$BRANCH_NAME" | grep -o "T[0-9]*")
          echo "task_id=$TASK_ID" >> $GITHUB_OUTPUT
          echo "branch_name=$BRANCH_NAME" >> $GITHUB_OUTPUT
      
      - name: Find related issue
        id: find-issue
        uses: actions/github-script@v7
        with:
          script: |
            const issues = await github.rest.issues.listForRepo({
              owner: context.repo.owner,
              repo: context.repo.repo,
              state: 'open',
              labels: 'task'
            });
            
            const taskId = '${{ steps.extract-info.outputs.task_id }}';
            const issue = issues.data.find(issue => 
              issue.title.includes(taskId)
            );
            
            if (issue) {
              core.setOutput('issue_number', issue.number);
              core.setOutput('issue_title', issue.title);
              return issue.number;
            } else {
              core.setFailed(`No issue found for task ${taskId}`);
            }
      
      - name: Create Pull Request
        uses: actions/github-script@v7
        with:
          script: |
            const { data: pr } = await github.rest.pulls.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '${{ steps.find-issue.outputs.issue_title }}',
              head: '${{ steps.extract-info.outputs.branch_name }}',
              base: 'develop',
              body: `## 🎯 Task Implementation
              
              Implements: #${{ steps.find-issue.outputs.issue_number }}
              
              ## ✅ TDD Checklist
              - [ ] **RED**: Failing tests written first
              - [ ] **GREEN**: Minimal implementation passes tests
              - [ ] **REFACTOR**: Code improved for quality
              - [ ] All existing tests still pass
              - [ ] Code coverage maintained/improved
              
              ## 🧪 Testing
              - [ ] Unit tests added/updated
              - [ ] Integration tests pass
              - [ ] Contract tests pass (if applicable)
              - [ ] Manual testing completed
              
              ## 📋 Implementation Details
              <!-- Describe what was implemented and how -->
              
              ## 🔍 Review Notes
              <!-- Any specific areas that need attention during review -->
              
              ## 📸 Screenshots/Demo
              <!-- If UI changes, include screenshots or demo links -->
              
              ---
              Closes #${{ steps.find-issue.outputs.issue_number }}
              
              **Branch**: \`${{ steps.extract-info.outputs.branch_name }}\`
              **Task ID**: ${{ steps.extract-info.outputs.task_id }}`,
              draft: true
            });
            
            // Add labels to PR
            await github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: pr.number,
              labels: ['task-implementation', 'needs-review']
            });
            
            console.log(`Created draft PR #${pr.number}`);
```

## Project Board Automation

### GitHub Project Configuration
Create `.github/workflows/project-automation.yml`:

```yaml
name: Project Board Automation

on:
  issues:
    types: [opened, closed, assigned]
  pull_request:
    types: [opened, closed, merged, ready_for_review]

jobs:
  update-project:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      projects: write
      issues: write
      pull-requests: write
    
    steps:
      - name: Add issue to project
        if: github.event_name == 'issues' && github.event.action == 'opened'
        uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/users/YOUR_USERNAME/projects/PROJECT_NUMBER
          github-token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Update issue status on assignment
        if: github.event_name == 'issues' && github.event.action == 'assigned'
        uses: actions/github-script@v7
        with:
          script: |
            // Move to "In Progress" when assigned
            // GitHub API calls to update project item status
      
      - name: Update status on PR ready for review
        if: github.event_name == 'pull_request' && github.event.action == 'ready_for_review'
        uses: actions/github-script@v7
        with:
          script: |
            // Move to "In Review" when PR is ready
      
      - name: Update status on PR merge
        if: github.event_name == 'pull_request' && github.event.action == 'closed' && github.event.pull_request.merged
        uses: actions/github-script@v7
        with:
          script: |
            // Move to "Done" when PR is merged
            // Close related issue
```

## Usage Workflow

### 1. Initial Setup
```bash
# 1. Create GitHub project
gh project create --title "Multi-Sport Betting Platform"

# 2. Sync all tasks to issues
git add .github/
git commit -m "Add GitHub integration workflows"
git push origin main

# 3. Run manual sync (first time)
node .github/scripts/sync-tasks-to-issues.js
```

### 2. Daily Development Workflow
```bash
# 1. Pick a task from GitHub project board
# 2. Assign yourself to the issue
# 3. Branch is automatically created
# 4. Check out the branch
git fetch origin
git checkout feature/T001-create-github-project

# 5. Follow TDD methodology
# Write tests first, then implement

# 6. Commit and push
git add .
git commit -m "T001: Implement GitHub project setup"
git push origin feature/T001-create-github-project

# 7. Draft PR is automatically created
# 8. Mark PR as ready for review when complete
# 9. Merge PR to close issue and update project status
```

## Benefits

✅ **Automated Issue Creation**: All 139 tasks become GitHub issues automatically
✅ **Branch Management**: Feature branches created automatically when assigned
✅ **PR Automation**: Draft PRs created with proper templates and issue linking
✅ **Project Board Sync**: Issues move through columns automatically
✅ **TDD Workflow**: Built-in reminders and checklists for TDD methodology
✅ **Traceability**: Complete audit trail from task → issue → branch → PR → merge
✅ **Team Collaboration**: Multiple developers can work on parallel tasks
✅ **Progress Tracking**: Real-time visibility into project progress

This setup provides enterprise-level project management with full automation while maintaining the TDD methodology and learning objectives!

## 🚀 Quick Start Setup

### 1. Automated Setup (Recommended)
Run the automated setup script to configure everything at once:

```bash
# Make sure you're in the repository root
cd betting-league-championship

# Run the automated setup
./.github/scripts/setup-github-integration.sh
```

This script will:
- ✅ Create GitHub Project board
- ✅ Set up project milestones  
- ✅ Sync all 139 tasks as GitHub Issues
- ✅ Configure automated workflows
- ✅ Set up branch protection rules
- ✅ Test the integration

### 2. Manual Setup (Alternative)
If you prefer to set up components individually:

```bash
# 1. Create project and milestones
gh project create --title "Multi-Sport Betting Platform"

# 2. Sync tasks to issues
cd .github/scripts
node sync-tasks-to-issues.js

# 3. Check status
./project-cli.sh status
```

### 3. Start Working on Tasks

```bash
# View available tasks
./github/scripts/project-cli.sh status

# Assign yourself to a task (this triggers branch creation)
./.github/scripts/project-cli.sh assign T001

# Check out the automatically created branch
git fetch origin
git checkout feature/T001-create-github-project

# Follow TDD methodology and push changes
# (This will automatically create a draft PR)
```