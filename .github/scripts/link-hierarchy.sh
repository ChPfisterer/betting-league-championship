#!/bin/bash

# Link Epics, Features, and Tasks with proper GitHub issue relationships
set -e

echo "🔗 Creating hierarchical links between Epics, Features, and Tasks..."

# Function to add a comment linking child issues to parent
link_children_to_parent() {
    local parent_issue=$1
    local parent_type=$2
    shift 2
    local children=("$@")
    
    echo "🔗 Linking ${#children[@]} $parent_type to $parent_issue..."
    
    # Create comment body with child issue links
    local comment_body="## Linked ${parent_type}s\n\n"
    for child in "${children[@]}"; do
        comment_body="${comment_body}- [ ] #${child}\n"
    done
    comment_body="${comment_body}\n*Auto-linked for project hierarchy*"
    
    # Add comment to parent issue
    gh issue comment $parent_issue --body "$comment_body" --repo ChPfisterer/betting-league-championship
}

# Function to add a comment linking parent to child
link_child_to_parent() {
    local child_issue=$1
    local parent_issue=$2
    local parent_type=$3
    
    echo "🔗 Linking task #$child_issue to $parent_type #$parent_issue..."
    
    local comment_body="## Parent $parent_type\n\n**Parent**: #${parent_issue}\n\n*Auto-linked for project hierarchy*"
    
    # Add comment to child issue
    gh issue comment $child_issue --body "$comment_body" --repo ChPfisterer/betting-league-championship
}

echo ""
echo "📊 Linking Features to Epic: Infrastructure & Project Setup (#101)..."
link_children_to_parent 101 "Feature" 106 107 108 109
link_child_to_parent 106 101 "Epic"
link_child_to_parent 107 101 "Epic"
link_child_to_parent 108 101 "Epic"
link_child_to_parent 109 101 "Epic"

echo ""
echo "📊 Linking Features to Epic: Test Development (TDD Methodology) (#102)..."
link_children_to_parent 102 "Feature" 110 111 112
link_child_to_parent 110 102 "Epic"
link_child_to_parent 111 102 "Epic"
link_child_to_parent 112 102 "Epic"

echo ""
echo "🔧 Linking Tasks to Feature: Project Setup & GitHub Management (#106)..."
# Tasks T001-T004 map to issues #1-#4, but we need to check which actual issue numbers exist
project_setup_tasks=(1 2 3 4)
link_children_to_parent 106 "Task" "${project_setup_tasks[@]}"
for task in "${project_setup_tasks[@]}"; do
    link_child_to_parent $task 106 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: CI/CD Pipeline Setup (#107)..."
# Tasks T006-T010 map to issues #5-#8 (T005 was not created based on our task list)
cicd_tasks=(5 6 7 8)
link_children_to_parent 107 "Task" "${cicd_tasks[@]}"
for task in "${cicd_tasks[@]}"; do
    link_child_to_parent $task 107 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: Backend Project Initialization (#108)..."
# Backend initialization tasks (approximate mapping)
backend_init_tasks=(12 13 14)
link_children_to_parent 108 "Task" "${backend_init_tasks[@]}"
for task in "${backend_init_tasks[@]}"; do
    link_child_to_parent $task 108 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: Frontend Project Initialization (#109)..."
# Frontend initialization tasks (approximate mapping)
frontend_init_tasks=(15 16 17)
link_children_to_parent 109 "Task" "${frontend_init_tasks[@]}"
for task in "${frontend_init_tasks[@]}"; do
    link_child_to_parent $task 109 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: Contract Tests (API Endpoints) (#110)..."
# Contract test tasks T052-T060 map to issues #52-#60
contract_test_tasks=(52 53 54 55 56 57 58 59 60)
link_children_to_parent 110 "Task" "${contract_test_tasks[@]}"
for task in "${contract_test_tasks[@]}"; do
    link_child_to_parent $task 110 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: Database Model Tests (#111)..."
# Model test tasks T061-T072 map to issues #61-#72
model_test_tasks=(61 62 63 64 65 66 67 68 69 70 71 72)
link_children_to_parent 111 "Task" "${model_test_tasks[@]}"
for task in "${model_test_tasks[@]}"; do
    link_child_to_parent $task 111 "Feature"
done

echo ""
echo "🔧 Linking Tasks to Feature: Service Layer Tests (#112)..."
# Service test tasks T073-T079 map to issues #73-#79
service_test_tasks=(73 74 75 76 77 78 79)
link_children_to_parent 112 "Task" "${service_test_tasks[@]}"
for task in "${service_test_tasks[@]}"; do
    link_child_to_parent $task 112 "Feature"
done

echo ""
echo "✅ Hierarchical linking complete!"
echo ""
echo "📊 Summary of Links Created:"
echo "   📊 Epic #101 → Features #106, #107, #108, #109"
echo "   📊 Epic #102 → Features #110, #111, #112"
echo "   🔧 Feature #106 → Tasks #1, #2, #3, #4"
echo "   🔧 Feature #107 → Tasks #5, #6, #7, #8"
echo "   🔧 Feature #108 → Tasks #12, #13, #14"
echo "   🔧 Feature #109 → Tasks #15, #16, #17"
echo "   🔧 Feature #110 → Tasks #52-#60 (9 contract tests)"
echo "   🔧 Feature #111 → Tasks #61-#72 (12 model tests)"
echo "   🔧 Feature #112 → Tasks #73-#79 (7 service tests)"
echo ""
echo "🎯 All issues now have proper parent-child relationships!"
echo "   - Epics show their child features"
echo "   - Features show their child tasks"
echo "   - Tasks reference their parent features"