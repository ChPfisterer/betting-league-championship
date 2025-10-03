const fs = require('fs');
const { execSync } = require('child_process');

// Parse tasks.md and extract task information
function parseTasks() {
  const path = require('path');
  const tasksPath = path.join(process.cwd(), 'specs/001-multi-sport-betting/tasks.md');
  
  // If running from .github/scripts, adjust the path
  let finalPath = tasksPath;
  if (!fs.existsSync(tasksPath)) {
    finalPath = path.join(process.cwd(), '../../specs/001-multi-sport-betting/tasks.md');
  }
  
  if (!fs.existsSync(finalPath)) {
    throw new Error(`tasks.md not found at ${finalPath}. Please ensure you're running from the repository root or the tasks.md file exists.`);
  }
  
  const tasksContent = fs.readFileSync(finalPath, 'utf8');
  const tasks = [];
  let currentPhase = '';
  
  const lines = tasksContent.split('\n');
  
  for (const line of lines) {
    // Extract phase information
    if (line.startsWith('## Phase')) {
      currentPhase = line.replace('## Phase ', '').replace(/[^\w\s]/g, '').trim();
      continue;
    }
    
    // Extract task information
    const taskMatch = line.match(/- \[ \] (T\d+) (\[P\])? (.+)/);
    if (taskMatch) {
      const [, taskId, parallel, description] = taskMatch;
      tasks.push({
        id: taskId,
        title: `${taskId}: ${description}`,
        body: generateIssueBody(taskId, description, parallel, currentPhase),
        labels: generateLabels(taskId, description, parallel, currentPhase),
        assignees: [],
        milestone: determineMilestone(taskId, currentPhase)
      });
    }
  }
  
  return tasks;
}

function generateIssueBody(taskId, description, parallel, phase) {
  const dependencies = extractDependencies(taskId);
  const files = extractFiles(description);
  
  return `## Task Description
${description}

## Phase
${phase}

## Implementation Requirements
- [ ] Follow TDD methodology (Red-Green-Refactor)
- [ ] Write tests first before implementation
- [ ] Ensure code coverage meets requirements (80% backend, 70% frontend)
- [ ] Update documentation if needed
- [ ] Follow code style guidelines (ruff, black, ESLint)

## Acceptance Criteria
- [ ] All tests pass (unit, integration, contract)
- [ ] Code review completed
- [ ] No merge conflicts
- [ ] CI/CD pipeline passes
- [ ] Performance requirements met (<500ms API response)

## Files to Modify
${files.length > 0 ? files.map(f => `- \`${f}\``).join('\n') : '_To be determined during implementation_'}

## Dependencies
${dependencies.length > 0 ? dependencies.map(d => `- [ ] ${d} must be completed first`).join('\n') : '_No specific dependencies_'}

## TDD Workflow
1. **RED**: Write failing test(s) first
2. **GREEN**: Write minimal code to pass the test(s)
3. **REFACTOR**: Improve code quality while keeping tests green
4. **VALIDATE**: Ensure all existing tests still pass

## Notes
${parallel ? '⚡ **Can run in parallel** with other [P] tasks in the same phase' : '🔄 **Sequential task** - complete phase dependencies first'}

${getTDDSpecificNotes(taskId, description)}

---
**Auto-generated from tasks.md | Task ID: ${taskId} | Phase: ${phase}**
`;
}

function getTDDSpecificNotes(taskId, description) {
  if (description.includes('test')) {
    return `## TDD Focus: Test Implementation
- This is a **TEST task** - implement comprehensive test coverage
- Write test cases for happy path, edge cases, and error conditions
- Use appropriate test patterns (mocks, fixtures, factories)
- Ensure tests are deterministic and independent`;
  }
  
  if (taskId.match(/T0(8[0-9]|9[0-9]|10[0-9])/)) {
    return `## TDD Focus: Implementation
- **Tests must be written first** in corresponding test tasks
- Implement only enough code to make tests pass
- Follow SOLID principles and clean code practices
- Refactor incrementally while keeping tests green`;
  }
  
  if (description.includes('Docker') || description.includes('infrastructure')) {
    return `## Infrastructure Focus
- Ensure configurations are environment-specific
- Test configurations in isolated environments
- Document any manual setup steps required
- Validate services start correctly`;
  }
  
  return '';
}

function extractFiles(description) {
  const files = [];
  
  // Extract file paths from common patterns
  const pathMatches = description.match(/`([^`]+\.(py|ts|yml|yaml|json|md|sh))`/g);
  if (pathMatches) {
    files.push(...pathMatches.map(match => match.replace(/`/g, '')));
  }
  
  // Extract directory patterns
  const dirMatches = description.match(/in `([^`]+\/)`/g);
  if (dirMatches) {
    files.push(...dirMatches.map(match => match.replace(/in `|`/g, '')));
  }
  
  return [...new Set(files)]; // Remove duplicates
}

function extractDependencies(taskId) {
  const taskNum = parseInt(taskId.replace('T', ''));
  const dependencies = [];
  
  // Define dependency rules based on TDD methodology
  if (taskNum >= 80 && taskNum <= 91) {
    // Model implementation depends on contract tests
    dependencies.push('Contract tests (T052-T060) must be completed');
  }
  
  if (taskNum >= 92 && taskNum <= 98) {
    // Service implementation depends on model tests
    dependencies.push('Model tests (T061-T072) must be completed');
  }
  
  if (taskNum >= 99 && taskNum <= 106) {
    // API implementation depends on service tests
    dependencies.push('Service tests (T073-T079) must be completed');
  }
  
  if (taskNum >= 111 && taskNum <= 120) {
    // Frontend depends on API contracts
    dependencies.push('API contracts (T052-T060) must be defined');
  }
  
  if (taskNum >= 121 && taskNum <= 124) {
    // Integration tests depend on implementations
    dependencies.push('Core implementations (T080-T106) must be completed');
  }
  
  return dependencies;
}

function generateLabels(taskId, description, parallel, phase) {
  const labels = ['task'];
  
  // Phase-based labels
  const phaseLabel = phase.toLowerCase().replace(/[^\w]/g, '-');
  labels.push(`phase:${phaseLabel}`);
  
  // TDD-specific labels
  if (description.includes('test') || description.includes('Test')) {
    labels.push('tdd:tests');
  } else if (taskId.match(/T0(8[0-9]|9[0-9]|10[0-9])/)) {
    labels.push('tdd:implementation');
  }
  
  // Technology labels
  if (description.includes('backend') || description.includes('FastAPI') || description.includes('Python')) {
    labels.push('backend');
  }
  if (description.includes('frontend') || description.includes('Angular') || description.includes('TypeScript')) {
    labels.push('frontend');
  }
  if (description.includes('Docker') || description.includes('infrastructure') || description.includes('environment')) {
    labels.push('infrastructure');
  }
  if (description.includes('Grafana') || description.includes('observability') || description.includes('OpenTelemetry')) {
    labels.push('observability');
  }
  if (description.includes('Keycloak') || description.includes('auth') || description.includes('OAuth')) {
    labels.push('authentication');
  }
  if (description.includes('PostgreSQL') || description.includes('database') || description.includes('model')) {
    labels.push('database');
  }
  if (description.includes('GitHub') || description.includes('CI/CD') || description.includes('workflow')) {
    labels.push('devops');
  }
  
  // Priority labels based on task number and phase
  if (taskId.match(/T0[0-2][0-9]/)) {
    labels.push('priority:critical'); // Setup tasks
  } else if (taskId.match(/T0[5-7][0-9]/)) {
    labels.push('priority:high'); // Test tasks
  } else if (taskId.match(/T0[8-9][0-9]|T10[0-9]/)) {
    labels.push('priority:high'); // Core implementation
  } else if (taskId.match(/T11[0-9]|T12[0-9]/)) {
    labels.push('priority:medium'); // Integration
  } else {
    labels.push('priority:low'); // Polish tasks
  }
  
  // Parallel execution
  if (parallel) {
    labels.push('parallel-ok');
  }
  
  // Effort estimation
  if (description.includes('Create') && !description.includes('test')) {
    labels.push('effort:medium');
  } else if (description.includes('Setup') || description.includes('Configure')) {
    labels.push('effort:large');
  } else {
    labels.push('effort:small');
  }
  
  return labels;
}

function determineMilestone(taskId, phase) {
  const taskNum = parseInt(taskId.replace('T', ''));
  
  if (taskNum <= 51) return 'Phase 1: Infrastructure Setup';
  if (taskNum <= 79) return 'Phase 2: Test Development (TDD)';
  if (taskNum <= 110) return 'Phase 3: Core Implementation';
  if (taskNum <= 129) return 'Phase 4: Integration & Features';
  return 'Phase 5: Polish & Deployment';
}

// Create GitHub issues
async function createIssues() {
  console.log('🚀 Starting GitHub Issues creation from tasks.md...\n');
  
  try {
    // Check if GitHub CLI is available
    execSync('gh --version', { stdio: 'pipe' });
  } catch (error) {
    console.error('❌ GitHub CLI not found. Please install: https://cli.github.com/');
    process.exit(1);
  }
  
  const tasks = parseTasks();
  console.log(`📋 Found ${tasks.length} tasks to create as issues\n`);
  
  let created = 0;
  let skipped = 0;
  
  for (const task of tasks) {
    try {
      // Check if issue already exists
      const existingIssues = execSync(
        `gh issue list --search "in:title ${task.id}" --json title,number`,
        { encoding: 'utf8' }
      );
      
      const issues = JSON.parse(existingIssues);
      if (issues.length > 0) {
        console.log(`⏭️  Skipping ${task.id}: Issue already exists (#${issues[0].number})`);
        skipped++;
        continue;
      }
      
      // Create the issue
      const cmd = [
        'gh', 'issue', 'create',
        '--title', `"${task.title}"`,
        '--body', `"${task.body.replace(/"/g, '\\"')}"`,
        '--label', task.labels.join(',')
      ];
      
      if (task.milestone) {
        cmd.push('--milestone', `"${task.milestone}"`);
      }
      
      console.log(`📝 Creating: ${task.title}`);
      const result = execSync(cmd.join(' '), { encoding: 'utf8' });
      const issueUrl = result.trim();
      console.log(`✅ Created: ${issueUrl}\n`);
      
      created++;
      
      // Small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 500));
      
    } catch (error) {
      console.error(`❌ Failed to create issue for ${task.id}:`, error.message);
    }
  }
  
  console.log(`\n🎉 Summary:`);
  console.log(`   ✅ Created: ${created} issues`);
  console.log(`   ⏭️  Skipped: ${skipped} existing issues`);
  console.log(`   📊 Total: ${tasks.length} tasks processed`);
  
  if (created > 0) {
    console.log(`\n🔗 View all issues: https://github.com/${process.env.GITHUB_REPOSITORY || 'your-repo'}/issues`);
    console.log(`📋 View project board: https://github.com/${process.env.GITHUB_REPOSITORY || 'your-repo'}/projects`);
  }
}

// Run the script
if (require.main === module) {
  createIssues().catch(error => {
    console.error('💥 Script failed:', error);
    process.exit(1);
  });
}

module.exports = { parseTasks, generateIssueBody, generateLabels };