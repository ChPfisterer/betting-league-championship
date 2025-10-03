#!/bin/bash

# GitHub Project Management CLI
# Helper script for managing tasks, issues, and project board

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
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

# Check if GitHub CLI is installed
check_gh_cli() {
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed. Please install it first:"
        echo "  macOS: brew install gh"
        echo "  Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
        exit 1
    fi
    
    # Check if authenticated
    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI is not authenticated. Please run: gh auth login"
        exit 1
    fi
}

# Function to sync tasks to issues
sync_tasks() {
    log_info "Syncing tasks from tasks.md to GitHub Issues..."
    
    cd "$REPO_ROOT"
    
    if [ ! -f "specs/001-multi-sport-betting/tasks.md" ]; then
        log_error "tasks.md not found at specs/001-multi-sport-betting/tasks.md"
        exit 1
    fi
    
    if [ ! -f ".github/scripts/sync-tasks-to-issues.js" ]; then
        log_error "Sync script not found. Please ensure .github/scripts/sync-tasks-to-issues.js exists"
        exit 1
    fi
    
    # Run the Node.js sync script
    cd .github/scripts
    node sync-tasks-to-issues.js
    
    log_success "Task synchronization completed!"
}

# Function to create project board
create_project() {
    log_info "Creating GitHub Project board..."
    
    PROJECT_TITLE="Multi-Sport Betting Platform"
    
    # Check if project already exists
    if gh project list | grep -q "$PROJECT_TITLE"; then
        log_warning "Project '$PROJECT_TITLE' already exists"
        return 0
    fi
    
    # Create the project
    gh project create --title "$PROJECT_TITLE" --body "TDD-based multi-sport betting platform with Grafana observability stack"
    
    log_success "Project board created: $PROJECT_TITLE"
}

# Function to show project status
show_status() {
    log_info "Project Status Overview"
    echo ""
    
    # Count issues by status
    TOTAL_TASKS=$(gh issue list --label "task" --limit 1000 --json state | jq '. | length')
    OPEN_TASKS=$(gh issue list --label "task" --state open --limit 1000 --json state | jq '. | length')
    CLOSED_TASKS=$(gh issue list --label "task" --state closed --limit 1000 --json state | jq '. | length')
    
    # Count by phase
    SETUP_TASKS=$(gh issue list --label "task,phase:project-setup" --limit 1000 --json state | jq '. | length')
    TEST_TASKS=$(gh issue list --label "task,tdd:tests" --limit 1000 --json state | jq '. | length')
    IMPL_TASKS=$(gh issue list --label "task,tdd:implementation" --limit 1000 --json state | jq '. | length')
    
    # Count assigned tasks
    ASSIGNED_TASKS=$(gh issue list --label "task" --assignee "@me" --state open --limit 1000 --json state | jq '. | length')
    
    echo "📊 Task Overview:"
    echo "  Total Tasks: $TOTAL_TASKS"
    echo "  Open: $OPEN_TASKS"
    echo "  Closed: $CLOSED_TASKS"
    echo ""
    echo "📋 By Phase:"
    echo "  Setup: $SETUP_TASKS"
    echo "  Tests: $TEST_TASKS"
    echo "  Implementation: $IMPL_TASKS"
    echo ""
    echo "👤 Assigned to me: $ASSIGNED_TASKS"
    echo ""
    
    # Show next available tasks
    log_info "Next available tasks (unassigned, high priority):"
    gh issue list --label "task,priority:high" --state open --limit 5 --json number,title,labels | jq -r '.[] | select(.assignees | length == 0) | "  #\(.number): \(.title)"' 2>/dev/null || echo "  No high priority tasks found or jq not available"
}

# Function to assign task to yourself
assign_task() {
    local task_id="$1"
    
    if [ -z "$task_id" ]; then
        log_error "Please provide a task ID (e.g., T001)"
        exit 1
    fi
    
    # Find the issue with this task ID
    ISSUE_NUMBER=$(gh issue list --label "task" --search "in:title $task_id:" --json number --jq '.[0].number // empty')
    
    if [ -z "$ISSUE_NUMBER" ]; then
        log_error "Task $task_id not found. Make sure it exists and has the 'task' label."
        exit 1
    fi
    
    # Assign to current user
    gh issue edit "$ISSUE_NUMBER" --add-assignee "@me"
    
    log_success "Assigned task $task_id (issue #$ISSUE_NUMBER) to you"
    log_info "A feature branch will be created automatically"
}

# Function to show help
show_help() {
    echo "GitHub Project Management CLI"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  sync          Sync tasks.md to GitHub Issues"
    echo "  create        Create GitHub Project board"
    echo "  status        Show project status overview"
    echo "  assign <id>   Assign task to yourself (e.g., assign T001)"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 sync                 # Sync all tasks to GitHub"
    echo "  $0 create               # Create project board"
    echo "  $0 status               # Show current status"
    echo "  $0 assign T001          # Assign task T001 to yourself"
}

# Main script logic
main() {
    check_gh_cli
    
    case "${1:-help}" in
        sync)
            sync_tasks
            ;;
        create)
            create_project
            ;;
        status)
            show_status
            ;;
        assign)
            assign_task "$2"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"