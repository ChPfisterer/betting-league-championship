# Test-Driven Development (TDD) Guide

## Core TDD Methodology

This project strictly follows Test-Driven Development (TDD) methodology throughout all implementation phases. TDD is not optional but a core requirement for all code development.

### 🔄 **Red-Green-Refactor Cycle**

#### **1. RED Phase: Write Failing Test**
```python
# Example: Backend unit test (MUST fail initially)
def test_place_bet_should_create_bet_record():
    # Arrange
    user = create_test_user()
    match = create_test_match()
    bet_data = {"predicted_winner": "team_a", "predicted_score": "2-1"}
    
    # Act
    result = betting_service.place_bet(user.id, match.id, bet_data)
    
    # Assert
    assert result.success is True
    assert result.bet_id is not None
    # This will fail because betting_service.place_bet doesn't exist yet
```

#### **2. GREEN Phase: Minimal Implementation**
```python
# Write ONLY enough code to make the test pass
class BettingService:
    def place_bet(self, user_id, match_id, bet_data):
        # Minimal implementation to pass the test
        bet_id = str(uuid.uuid4())
        return BetResult(success=True, bet_id=bet_id)
```

#### **3. REFACTOR Phase: Improve Code Quality**
```python
# Improve implementation while keeping tests green
class BettingService:
    def __init__(self, bet_repository, match_repository):
        self.bet_repository = bet_repository
        self.match_repository = match_repository
    
    def place_bet(self, user_id, match_id, bet_data):
        # Proper implementation with validation, database persistence, etc.
        match = self.match_repository.get_by_id(match_id)
        if not match or match.betting_deadline_passed():
            return BetResult(success=False, error="Betting deadline passed")
        
        bet = Bet(
            user_id=user_id,
            match_id=match_id,
            predicted_winner=bet_data["predicted_winner"],
            predicted_score=bet_data["predicted_score"]
        )
        saved_bet = self.bet_repository.save(bet)
        return BetResult(success=True, bet_id=saved_bet.id)
```

## 📊 **TDD Testing Pyramid**

### **1. Contract Tests (API Level)**
```python
# tests/contract/test_betting_api.py
def test_post_bet_endpoint_contract():
    """Test API contract matches OpenAPI specification"""
    response = client.post("/api/bets", json={
        "match_id": "uuid-here",
        "predicted_winner": "team_a",
        "predicted_score": "2-1"
    })
    
    # Validate against OpenAPI schema
    assert response.status_code == 201
    assert validate_response_schema(response.json(), "BetResponse")
```

### **2. Unit Tests (Component Level)**
```python
# tests/unit/test_bet_validation.py
def test_bet_validation_rejects_invalid_score():
    """Test business rule validation"""
    validator = BetValidator()
    
    invalid_bet = {"predicted_score": "invalid-score"}
    result = validator.validate(invalid_bet)
    
    assert result.is_valid is False
    assert "Invalid score format" in result.errors
```

### **3. Integration Tests (Service Level)**
```python
# tests/integration/test_betting_integration.py
def test_place_bet_integration_with_database():
    """Test service integration with real database"""
    with test_database_session():
        # Test with real database connection
        result = betting_service.place_bet(user_id, match_id, valid_bet_data)
        
        # Verify database state
        saved_bet = bet_repository.get_by_id(result.bet_id)
        assert saved_bet is not None
        assert saved_bet.user_id == user_id
```

### **4. End-to-End Tests (User Journey)**
```typescript
// tests/e2e/betting-flow.spec.ts
test('user can place bet through complete flow', async ({ page }) => {
  // Navigate to betting page
  await page.goto('/betting/matches');
  
  // Select match and place bet
  await page.click('[data-testid="match-123"]');
  await page.fill('[data-testid="predicted-score"]', '2-1');
  await page.click('[data-testid="place-bet"]');
  
  // Verify success
  await expect(page.locator('[data-testid="bet-success"]')).toBeVisible();
});
```

## 🛠️ **TDD Implementation Strategy**

### **Backend TDD Workflow**
```bash
# 1. Write failing test
touch tests/unit/test_new_feature.py
# Write test that describes desired behavior

# 2. Run test (should fail)
pytest tests/unit/test_new_feature.py -v

# 3. Write minimal implementation
touch src/services/new_feature_service.py
# Implement just enough to pass

# 4. Run test (should pass)
pytest tests/unit/test_new_feature.py -v

# 5. Refactor while keeping tests green
# Improve code quality, add error handling, etc.

# 6. Run all tests to ensure no regressions
pytest tests/ -v
```

### **Frontend TDD Workflow**
```bash
# 1. Write failing component test
ng generate component new-feature --skip-import
# Edit component.spec.ts with desired behavior

# 2. Run test (should fail)
ng test --watch=false --code-coverage

# 3. Implement component
# Edit component.ts with minimal implementation

# 4. Run test (should pass)
ng test --watch=false

# 5. Refactor while keeping tests green
# Improve component structure, add proper types, etc.
```

## 🎯 **TDD Quality Gates**

### **Code Coverage Requirements**
- **Backend**: Minimum 80% line coverage
- **Frontend**: Minimum 70% line coverage
- **Critical Paths**: 100% coverage for betting logic, authentication, scoring

### **Test Categories Coverage**
- **Unit Tests**: All business logic components
- **Integration Tests**: All database interactions
- **Contract Tests**: All API endpoints
- **End-to-End Tests**: All user workflows

### **CI/CD Integration**
```yaml
# .github/workflows/ci-test.yml (example)
- name: Run Backend Tests
  run: |
    pytest tests/ -v --cov=src --cov-report=term-missing --cov-fail-under=80

- name: Run Frontend Tests
  run: |
    ng test --watch=false --code-coverage --karma-config=karma.conf.ci.js
    
- name: Check Coverage Thresholds
  run: |
    # Fail if coverage below thresholds
    coverage report --fail-under=80
```

## 📚 **TDD Best Practices**

### **Test Naming Convention**
```python
# Pattern: test_[method]_should_[expected_behavior]_when_[condition]
def test_place_bet_should_return_error_when_deadline_passed():
    pass

def test_calculate_ranking_should_award_three_points_when_exact_score_correct():
    pass

def test_create_group_should_generate_invitation_code_when_private_group():
    pass
```

### **Test Data Management**
```python
# Use factory patterns for test data
class UserFactory:
    @staticmethod
    def create(email="test@example.com", **kwargs):
        return User(
            id=str(uuid.uuid4()),
            email=email,
            **kwargs
        )

class MatchFactory:
    @staticmethod
    def create(scheduled_at=None, **kwargs):
        return Match(
            id=str(uuid.uuid4()),
            scheduled_at=scheduled_at or datetime.utcnow() + timedelta(hours=1),
            **kwargs
        )
```

### **Mocking and Test Doubles**
```python
# Mock external dependencies
@pytest.fixture
def mock_keycloak_client():
    with patch('src.auth.keycloak_client') as mock:
        mock.verify_token.return_value = {'sub': 'user-123', 'email': 'test@example.com'}
        yield mock

def test_protected_endpoint_should_require_valid_token(mock_keycloak_client):
    # Test uses mocked Keycloak client
    response = client.get("/api/protected", headers={"Authorization": "Bearer valid-token"})
    assert response.status_code == 200
```

## 🚀 **TDD Benefits in This Project**

### **Learning Benefits**
- **Professional Practices**: Learn industry-standard TDD methodology
- **Quality Mindset**: Develop quality-first thinking approach
- **Design Skills**: TDD naturally leads to better API and component design
- **Confidence**: Safe refactoring and feature addition with test safety net

### **Project Benefits**
- **Reliability**: Comprehensive test coverage prevents regressions
- **Documentation**: Tests serve as living documentation of system behavior
- **Maintainability**: Well-tested code is easier to modify and extend
- **Integration**: TDD works perfectly with CI/CD and observability goals

### **Grafana Stack Integration**
- **Test Metrics**: Monitor test execution time and success rates
- **Coverage Tracking**: Track code coverage trends over time
- **Performance Testing**: Integration with load testing and performance monitoring
- **Quality Dashboards**: Visualize test results and quality metrics

## 📈 **TDD Success Metrics**

### **Development Metrics**
- **Test Coverage**: >80% backend, >70% frontend
- **Test Execution Time**: <2 minutes for unit tests, <10 minutes for full suite
- **Defect Rate**: <5% post-deployment defects
- **TDD Compliance**: 100% of features developed using TDD

### **Learning Metrics**
- **TDD Cycle Time**: Average Red-Green-Refactor cycle completion
- **Test Quality**: Mutation testing scores
- **Refactoring Confidence**: Frequency of successful refactoring sessions
- **Code Review Quality**: Reduced code review iterations due to better test coverage

This TDD approach ensures high-quality, well-tested code while providing excellent learning experience with modern development practices.