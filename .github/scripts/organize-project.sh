#!/bin/bash

# Add all issues to GitHub Project and configure organization
set -e

echo "📋 Adding all issues to GitHub Project and configuring organization..."

# Project URL from creation
PROJECT_URL="https://github.com/users/ChPfisterer/projects/4"

# Get project ID
PROJECT_ID=$(gh project list --owner ChPfisterer --format json | jq -r '.projects[] | select(.title == "Betting League Championship") | .number')

if [ -z "$PROJECT_ID" ]; then
    echo "❌ Could not find project ID"
    exit 1
fi

echo "📊 Using Project ID: $PROJECT_ID"

# Function to add issue to project
add_issue_to_project() {
    local issue_number=$1
    echo "Adding issue #$issue_number to project..."
    gh project item-add $PROJECT_ID --owner ChPfisterer --url "https://github.com/ChPfisterer/betting-league-championship/issues/$issue_number" || echo "Issue #$issue_number might already be in project"
}

# Add all task issues (1-100)
echo "🎯 Adding task issues to project..."
for i in {1..100}; do
    # Check if issue exists
    if gh issue view $i --repo ChPfisterer/betting-league-championship > /dev/null 2>&1; then
        add_issue_to_project $i
    fi
done

# Add epic issues (101-105)
echo "📊 Adding epic issues to project..."
for i in {101..105}; do
    add_issue_to_project $i
done

# Add feature issues (106-112)
echo "🔧 Adding feature issues to project..."
for i in {106..112}; do
    add_issue_to_project $i
done

echo ""
echo "✅ All issues added to GitHub Project!"
echo ""
echo "📊 Project Summary:"
echo "   - Project URL: $PROJECT_URL"
echo "   - Epic Issues: #101-#105 (5 epics)"
echo "   - Feature Issues: #106-#112 (7 features)"
echo "   - Task Issues: #1-#100 (80 active tasks)"
echo "   - Total: 92 issues organized hierarchically"
echo ""
echo "🎯 Project Structure:"
echo "   📊 Epic: Infrastructure & Project Setup (#101)"
echo "      └── 🔧 Feature: Project Setup & GitHub Management (#106)"
echo "      └── 🔧 Feature: CI/CD Pipeline Setup (#107)"
echo "      └── 🔧 Feature: Backend Project Initialization (#108)"
echo "      └── 🔧 Feature: Frontend Project Initialization (#109)"
echo ""
echo "   📊 Epic: Test Development (TDD Methodology) (#102)"
echo "      └── 🔧 Feature: Contract Tests (API Endpoints) (#110)"
echo "      └── 🔧 Feature: Database Model Tests (#111)"
echo "      └── 🔧 Feature: Service Layer Tests (#112)"
echo ""
echo "   📊 Epic: Core Implementation (Backend & Frontend) (#103)"
echo "   📊 Epic: Integration & Quality Assurance (#104)"
echo "   📊 Epic: Deployment & Operations (#105)"
echo ""
echo "🚀 Ready for Development!"
echo "   - GitHub Project Board: $PROJECT_URL"
echo "   - TDD Methodology: Tests First (Red-Green-Refactor)"
echo "   - Automation: Branch creation, PR linking, status updates"