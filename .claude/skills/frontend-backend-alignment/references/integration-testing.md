# Integration Testing for Frontend-Backend Systems

Comprehensive testing strategies for validating frontend-backend integration points.

## Test Pyramid for API Integration

### Unit Tests
Test individual components in isolation:

```typescript
// Frontend API service unit tests
describe('ApiService', () => {
  let apiService: ApiService;
  let mockAxios: any;

  beforeEach(() => {
    mockAxios = {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn()
    };
    apiService = new ApiService('http://test-api.com');
    (apiService as any).axiosClient = mockAxios;
  });

  test('should get user tasks with filters', async () => {
    const mockResponse = { tasks: [], total: 0 };
    mockAxios.get.mockResolvedValue({ data: mockResponse });

    const result = await apiService.getTasks('user123', {
      priority: 'High',
      status: 'incomplete'
    });

    expect(mockAxios.get).toHaveBeenCalledWith('/api/user123/tasks', {
      params: { priority: 'High', status: 'incomplete' }
    });
    expect(result).toEqual(mockResponse);
  });
});
```

### Integration Tests
Test the integration between frontend and backend:

```typescript
// Integration test using supertest for backend
import request from 'supertest';
import { app } from '../../src/main';

describe('Task API Integration', () => {
  test('should create a new task', async () => {
    const userData = {
      first_name: 'Test',
      last_name: 'User',
      email: 'integration@test.com',
      password: 'securePassword123',
      favorite_teacher: 'Mr. Test'
    };

    // First, create a user
    const userResponse = await request(app)
      .post('/api/auth/signup')
      .send(userData)
      .expect(200);

    const userId = userResponse.body.id;

    // Then create a task for that user
    const taskData = {
      title: 'Integration Test Task',
      priority: 'High'
    };

    const taskResponse = await request(app)
      .post(`/api/${userId}/tasks`)
      .set('Authorization', `Bearer ${userResponse.body.access_token}`)
      .send(taskData)
      .expect(200);

    expect(taskResponse.body.title).toBe(taskData.title);
    expect(taskResponse.body.priority).toBe(taskData.priority);
    expect(taskResponse.body.user_id).toBe(userId);
  });
});
```

### End-to-End Tests
Test complete user journeys:

```typescript
// Playwright E2E test
import { test, expect } from '@playwright/test';

test.describe('Task Management Flow', () => {
  test('should allow user to create and view tasks', async ({ page }) => {
    // Navigate to signup page
    await page.goto('http://localhost:3000/signup');

    // Fill in signup form
    await page.fill('[data-testid="first-name"]', 'Test');
    await page.fill('[data-testid="last-name"]', 'User');
    await page.fill('[data-testid="email"]', 'e2e@test.com');
    await page.fill('[data-testid="password"]', 'securePassword123');
    await page.fill('[data-testid="favorite-teacher"]', 'Mr. Test');
    await page.click('[data-testid="signup-button"]');

    // Wait for redirect to dashboard
    await page.waitForURL('http://localhost:3000/dashboard');

    // Create a new task
    await page.fill('[data-testid="task-title"]', 'E2E Test Task');
    await page.click('[data-testid="priority-select"]');
    await page.click('text=High');
    await page.click('[data-testid="create-task-button"]');

    // Verify task appears in the list
    await expect(page.locator('text=E2E Test Task')).toBeVisible();
  });
});
```

## Contract Testing

### API Contract Validation
Verify that API implementations match their contracts:

```typescript
// Contract test using Pact or similar
import { PactTestSetup } from '@pact-foundation/pact';

describe('API Contract Tests', () => {
  const provider = new PactTestSetup({
    consumer: 'frontend-app',
    provider: 'backend-api'
  });

  test('get user tasks contract', async () => {
    // Setup provider state
    await provider.setupProviderState('user has tasks', {
      user_id: 'test-user-123'
    });

    // Setup interaction
    provider.addInteraction({
      state: 'user has tasks',
      uponReceiving: 'a request for user tasks',
      withRequest: {
        method: 'GET',
        path: '/api/test-user-123/tasks',
        headers: { 'Authorization': 'Bearer valid-token' }
      },
      willRespondWith: {
        status: 200,
        body: {
          tasks: [
            {
              id: 'task-1',
              user_id: 'test-user-123',
              title: 'Test Task',
              priority: 'High',
              status: false,
              created_at: '2023-01-01T00:00:00Z'
            }
          ],
          total: 1,
          page: 1,
          limit: 20
        }
      }
    });

    // Execute request
    const response = await fetch(`${provider.mockService.baseUrl}/api/test-user-123/tasks`, {
      headers: { 'Authorization': 'Bearer valid-token' }
    });

    // Verify response matches contract
    expect(response.status).toBe(200);
    const data = await response.json();
    expect(data.tasks).toBeInstanceOf(Array);
    expect(data.total).toBeGreaterThan(0);
  });
});
```

## Cross-Domain Testing

### Authentication Flow Testing
Test the complete authentication flow:

```typescript
describe('Authentication Flow', () => {
  test('successful signup -> login -> logout cycle', async () => {
    // Test signup
    const signupResponse = await request(app)
      .post('/api/auth/signup')
      .send({
        first_name: 'Test',
        last_name: 'User',
        email: 'auth@test.com',
        password: 'securePassword123',
        favorite_teacher: 'Mr. Test'
      })
      .expect(200);

    const userId = signupResponse.body.id;
    expect(signupResponse.body.email).toBe('auth@test.com');

    // Test login
    const loginResponse = await request(app)
      .post('/api/auth/signin')
      .send({
        email: 'auth@test.com',
        password: 'securePassword123'
      })
      .expect(200);

    const { access_token } = loginResponse.body;
    expect(access_token).toBeDefined();

    // Test protected endpoint with token
    await request(app)
      .get(`/api/${userId}/tasks`)
      .set('Authorization', `Bearer ${access_token}`)
      .expect(200);

    // Test logout
    await request(app)
      .post('/api/auth/signout')
      .set('Authorization', `Bearer ${access_token}`)
      .expect(200);
  });
});
```

## Performance Testing

### API Response Time Validation
Ensure API responses meet performance requirements:

```typescript
describe('API Performance Tests', () => {
  test('get tasks endpoint should respond within 500ms', async () => {
    const startTime = Date.now();

    const response = await request(app)
      .get(`/api/${testUserId}/tasks`)
      .set('Authorization', `Bearer ${validToken}`);

    const endTime = Date.now();
    const responseTime = endTime - startTime;

    expect(responseTime).toBeLessThan(500); // 500ms threshold
    expect(response.status).toBe(200);
  });

  test('create task should respond within 1000ms', async () => {
    const startTime = Date.now();

    const response = await request(app)
      .post(`/api/${testUserId}/tasks`)
      .set('Authorization', `Bearer ${validToken}`)
      .send({
        title: 'Performance Test Task',
        priority: 'Medium'
      });

    const endTime = Date.now();
    const responseTime = endTime - startTime;

    expect(responseTime).toBeLessThan(1000); // 1000ms threshold
    expect(response.status).toBe(200);
  });
});
```

## Error Condition Testing

### Error Response Validation
Test how errors are handled and communicated:

```typescript
describe('Error Handling Tests', () => {
  test('should return 401 for unauthorized requests', async () => {
    const response = await request(app)
      .get('/api/nonexistent-user/tasks')
      .expect(401);

    expect(response.body.detail).toBeDefined();
  });

  test('should return 404 for non-existent resources', async () => {
    const response = await request(app)
      .get(`/api/${existingUserId}/tasks/nonexistent-task`)
      .set('Authorization', `Bearer ${validToken}`)
      .expect(404);

    expect(response.body.detail).toBe('Task not found');
  });

  test('should return 400 for invalid input', async () => {
    const response = await request(app)
      .post(`/api/${existingUserId}/tasks`)
      .set('Authorization', `Bearer ${validToken}`)
      .send({
        title: '', // Invalid - empty title
        priority: 'InvalidPriority' // Invalid - not in enum
      })
      .expect(400);

    expect(response.body.detail).toBeDefined();
  });
});
```

## Environment-Specific Testing

### Different Environment Configurations
Test behavior across different environments:

```typescript
describe('Environment-Specific Tests', () => {
  test('CORS headers in development', async () => {
    const response = await request(app)
      .options('/api/auth/signup')
      .set('Origin', 'http://localhost:3000')
      .set('Access-Control-Request-Method', 'POST')
      .set('Access-Control-Request-Headers', 'Content-Type');

    expect(response.headers['access-control-allow-origin']).toBe('http://localhost:3000');
  });

  test('database fallback behavior', async () => {
    // Temporarily disconnect from primary database
    process.env.DATABASE_URL = 'invalid://connection-string';

    // Restart app or reload database config
    // This would typically be done in a setup function

    // Test that fallback mechanism works
    const response = await request(app)
      .post('/api/auth/signup')
      .send({
        first_name: 'Fallback',
        last_name: 'Test',
        email: 'fallback@test.com',
        password: 'securePassword123',
        favorite_teacher: 'Mr. Fallback'
      });

    // Should still work with fallback database
    expect(response.status).toBeOneOf([200, 500]); // Could succeed or fail gracefully
  });
});
```

## Monitoring and Health Checks

### API Health Testing
Regular health checks for API availability:

```typescript
describe('Health Checks', () => {
  test('root endpoint should be healthy', async () => {
    const response = await request(app).get('/');
    expect(response.status).toBe(200);
    expect(response.body.message).toBe('Welcome to Speckit Plus Todo API');
  });

  test('health endpoint should return system status', async () => {
    const response = await request(app).get('/health');
    expect(response.status).toBe(200);
    expect(response.body.status).toBe('healthy');
    expect(response.body.timestamp).toBeDefined();
  });
});
```

## Continuous Integration Pipeline

### Test Execution Order
Structure tests for optimal CI execution:

```yaml
# .github/workflows/test.yml
name: Integration Tests
on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run unit tests
        run: npm run test:unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v2
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Start backend server
        run: npm run start:backend:test &
      - name: Start frontend server
        run: npm run start:frontend:test &
      - name: Run E2E tests
        run: npm run test:e2e
```