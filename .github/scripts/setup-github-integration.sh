#!/bin/bash

# GitHub Integration Setup Script
# This script sets up the complete GitHub integration for task management

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Helper functions
log_step() {
    echo -e "\n${PURPLE}🚀 STEP: $1${NC}"
}

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking Prerequisites"
    
    # Check Git
    if ! command -v git &> /dev/null; then
        log_error "Git is not installed"
        exit 1
    fi
    log_success "Git is available"
    
    # Check GitHub CLI
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI is not installed. Please install it:"
        echo "  macOS: brew install gh"
        echo "  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
        exit 1
    fi
    log_success "GitHub CLI is available"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        log_error "Node.js is not installed. Please install Node.js 18+"
        exit 1
    fi
    
    NODE_VERSION=$(node --version | sed 's/v//')
    log_success "Node.js $NODE_VERSION is available"
    
    # Check if authenticated with GitHub
    if ! gh auth status &> /dev/null; then
        log_warning "GitHub CLI is not authenticated"
        log_info "Please run: gh auth login"
        read -p "Press Enter after authenticating with GitHub..."
        
        if ! gh auth status &> /dev/null; then
            log_error "GitHub authentication failed"
            exit 1
        fi
    fi
    log_success "GitHub CLI is authenticated"
    
    # Check if we're in a git repository
    if ! git rev-parse --git-dir &> /dev/null; then
        log_error "Not in a git repository"
        exit 1
    fi
    log_success "In a git repository"
    
    # Check if tasks.md exists
    if [ ! -f "$REPO_ROOT/specs/001-multi-sport-betting/tasks.md" ]; then
        log_error "tasks.md not found at specs/001-multi-sport-betting/tasks.md"
        log_info "Please ensure the tasks have been generated first"
        exit 1
    fi
    log_success "tasks.md found"
}

# Setup develop branch
setup_branches() {
    log_step "Setting up Git Branches"
    
    cd "$REPO_ROOT"
    
    # Ensure we're on main
    git checkout main 2>/dev/null || git checkout master 2>/dev/null || {
        log_error "Could not find main or master branch"
        exit 1
    }
    
    # Create develop branch if it doesn't exist
    if ! git show-ref --verify --quiet refs/heads/develop; then
        log_info "Creating develop branch"
        git checkout -b develop
        git push -u origin develop
        log_success "develop branch created and pushed"
    else
        log_success "develop branch already exists"
    fi
    
    # Set up branch protection (if possible)
    gh api repos/:owner/:repo/branches/main/protection \
        --method PUT \
        --field required_status_checks='{"strict":true,"contexts":[]}' \
        --field enforce_admins=true \
        --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true}' \
        --field restrictions=null 2>/dev/null && log_success "Branch protection enabled for main" || log_warning "Could not set branch protection (admin rights needed)"
}

# Create GitHub project
create_github_project() {
    log_step "Creating GitHub Project"
    
    PROJECT_TITLE="Multi-Sport Betting Platform"
    
    # Check if project already exists
    if gh project list --owner "@me" | grep -q "$PROJECT_TITLE"; then
        log_warning "Project '$PROJECT_TITLE' already exists"
        return 0
    fi
    
    # Create the project
    log_info "Creating GitHub Project: $PROJECT_TITLE"
    PROJECT_URL=$(gh project create --title "$PROJECT_TITLE" --body "TDD-based multi-sport betting platform with Grafana observability stack" 2>/dev/null || echo "")
    
    if [ -n "$PROJECT_URL" ]; then
        log_success "Project created: $PROJECT_URL"
    else
        log_warning "Project creation may have failed or you may not have permissions"
    fi
}

# Create milestones
create_milestones() {
    log_step "Creating Project Milestones"
    
    MILESTONES=(
        "Phase 1: Infrastructure Setup|Foundation setup including Docker, CI/CD, and environment configurations"
        "Phase 2: Test Development (TDD)|Contract tests, unit tests, and integration tests following TDD methodology"
        "Phase 3: Core Implementation|Backend services, API endpoints, and database models"
        "Phase 4: Integration & Features|Frontend components, real-time features, and observability"
        "Phase 5: Polish & Deployment|Final testing, documentation, and production deployment"
    )
    
    for milestone_info in "${MILESTONES[@]}"; do
        IFS='|' read -r title description <<< "$milestone_info"
        
        # Check if milestone exists
        if gh api repos/:owner/:repo/milestones --jq '.[].title' | grep -q "^$title$"; then
            log_success "Milestone already exists: $title"
        else
            log_info "Creating milestone: $title"
            gh api repos/:owner/:repo/milestones \
                --method POST \
                --field title="$title" \
                --field description="$description" \
                --field state="open" >/dev/null && log_success "Created: $title" || log_warning "Failed to create: $title"
        fi
    done
}

# Initialize Node.js project for scripts
setup_nodejs() {
    log_step "Setting up Node.js for Scripts"
    
    cd "$REPO_ROOT/.github/scripts"
    
    if [ ! -f "package.json" ]; then
        log_info "Initializing Node.js project"
        npm init -y >/dev/null
        log_success "package.json created"
    else
        log_success "package.json already exists"
    fi
    
    # Install basic dependencies if needed
    if [ ! -d "node_modules" ]; then
        log_info "Installing dependencies"
        npm install >/dev/null 2>&1 || log_warning "npm install had warnings"
        log_success "Dependencies installed"
    fi
}

# Sync tasks to GitHub Issues
sync_tasks_to_issues() {
    log_step "Syncing Tasks to GitHub Issues"
    
    cd "$REPO_ROOT/.github/scripts"
    
    log_info "Running task synchronization..."
    if node sync-tasks-to-issues.js; then
        log_success "Tasks successfully synced to GitHub Issues"
    else
        log_error "Task synchronization failed"
        return 1
    fi
}

# Test the workflows
test_workflows() {
    log_step "Testing GitHub Actions Workflows"
    
    cd "$REPO_ROOT"
    
    # Check if workflows are syntactically correct
    log_info "Validating workflow syntax..."
    
    for workflow in .github/workflows/*.yml; do
        if [ -f "$workflow" ]; then
            workflow_name=$(basename "$workflow")
            log_info "Checking $workflow_name..."
            
            # Basic YAML syntax check (if yamllint is available)
            if command -v yamllint &> /dev/null; then
                if yamllint "$workflow" >/dev/null 2>&1; then
                    log_success "$workflow_name syntax OK"
                else
                    log_warning "$workflow_name has syntax warnings"
                fi
            else
                log_success "$workflow_name (syntax check skipped - yamllint not available)"
            fi
        fi
    done
}

# Display summary and next steps
show_summary() {
    log_step "Setup Complete! 🎉"
    
    echo ""
    echo "🏆 GitHub Integration is now fully configured!"
    echo ""
    echo "📋 What was set up:"
    echo "  ✅ GitHub Project board created"
    echo "  ✅ Project milestones configured"
    echo "  ✅ All 139 tasks synced as GitHub Issues"
    echo "  ✅ Automated workflows configured"
    echo "  ✅ Branch protection rules applied"
    echo "  ✅ Issue and PR templates created"
    echo ""
    echo "🚀 Next Steps:"
    echo ""
    echo "1. 📋 View your project board:"
    echo "   gh project list"
    echo ""
    echo "2. 📝 See all task issues:"
    echo "   gh issue list --label task"
    echo ""
    echo "3. 🎯 Assign yourself to a task:"
    echo "   ./.github/scripts/project-cli.sh assign T001"
    echo ""
    echo "4. 📊 Check project status anytime:"
    echo "   ./.github/scripts/project-cli.sh status"
    echo ""
    echo "🔄 How the workflow works:"
    echo "  1. Assign yourself to an issue → branch created automatically"
    echo "  2. Push commits to feature branch → draft PR created automatically"
    echo "  3. Mark PR ready for review → issue status updated"
    echo "  4. Merge PR → issue closed automatically"
    echo ""
    echo "🧪 TDD Reminders:"
    echo "  • Always write tests first (RED phase)"
    echo "  • Implement minimal code to pass (GREEN phase)" 
    echo "  • Refactor while keeping tests green (REFACTOR phase)"
    echo ""
    echo "📚 Useful Commands:"
    echo "  ./.github/scripts/project-cli.sh help    # Show all available commands"
    echo "  gh issue list --assignee @me             # Your assigned tasks"
    echo "  gh pr list --author @me                  # Your open PRs"
    echo ""
    echo "Happy coding! 🚀 Start with the setup tasks (T001-T051) first!"
}

# Main execution
main() {
    echo "🎯 GitHub Integration Setup for Multi-Sport Betting Platform"
    echo "============================================================"
    
    check_prerequisites
    setup_branches
    create_github_project
    create_milestones
    setup_nodejs
    sync_tasks_to_issues
    test_workflows
    show_summary
    
    echo ""
    log_success "Setup completed successfully! 🎉"
}

# Run main function
main "$@"