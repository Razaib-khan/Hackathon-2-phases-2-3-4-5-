# Frontend-Backend Contract Patterns

Detailed API contract patterns and validation strategies for frontend-backend integration.

## API Contract Definition

### Standard Contract Template
```typescript
interface ApiContract {
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  authRequired: boolean;
  requestSchema: {
    pathParams?: Record<string, any>;
    queryParams?: Record<string, any>;
    requestBody?: Record<string, any>;
    headers?: Record<string, string>;
  };
  responseSchema: {
    success: Record<string, any>;
    error: Record<string, any>;
  };
  validationRules: ValidationRule[];
}

interface ValidationRule {
  field: string;
  type: 'string' | 'number' | 'boolean' | 'date' | 'enum';
  required: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  enumValues?: string[];
}
```

## Common Contract Patterns

### 1. Authentication Contracts
```typescript
const authContracts = {
  signup: {
    endpoint: '/api/auth/signup',
    method: 'POST',
    authRequired: false,
    requestSchema: {
      requestBody: {
        first_name: { type: 'string', required: true, minLength: 1, maxLength: 100 },
        last_name: { type: 'string', required: true, minLength: 1, maxLength: 100 },
        email: { type: 'string', required: true, pattern: '^[^@]+@[^@]+\.[^@]+$' },
        password: { type: 'string', required: true, minLength: 8 },
        favorite_teacher: { type: 'string', required: true }
      }
    },
    responseSchema: {
      success: {
        id: 'string',
        email: 'string',
        first_name: 'string',
        last_name: 'string',
        created_at: 'string'
      },
      error: {
        detail: 'string'
      }
    }
  },

  signin: {
    endpoint: '/api/auth/signin',
    method: 'POST',
    authRequired: false,
    requestSchema: {
      requestBody: {
        email: { type: 'string', required: true },
        password: { type: 'string', required: true }
      }
    },
    responseSchema: {
      success: {
        access_token: 'string',
        token_type: 'string',
        user_id: 'string'
      },
      error: {
        detail: 'string'
      }
    }
  }
};
```

### 2. Resource Management Contracts (Tasks)
```typescript
const taskContracts = {
  getTasks: {
    endpoint: '/api/{user_id}/tasks',
    method: 'GET',
    authRequired: true,
    requestSchema: {
      pathParams: {
        user_id: { type: 'string', required: true }
      },
      queryParams: {
        search: { type: 'string', required: false },
        priority: { type: 'enum', required: false, enumValues: ['Critical', 'High', 'Medium', 'Low'] },
        status: { type: 'enum', required: false, enumValues: ['complete', 'incomplete'] },
        timestamp_from: { type: 'string', required: false }, // ISO date string
        timestamp_to: { type: 'string', required: false },   // ISO date string
        page: { type: 'number', required: false },
        limit: { type: 'number', required: false }
      }
    },
    responseSchema: {
      success: {
        tasks: [
          {
            id: 'string',
            user_id: 'string',
            title: 'string',
            description: 'string',
            priority: 'string',
            timestamp: 'string',
            status: 'boolean',
            created_at: 'string',
            updated_at: 'string'
          }
        ],
        total: 'number',
        page: 'number',
        limit: 'number'
      }
    }
  },

  createTask: {
    endpoint: '/api/{user_id}/tasks',
    method: 'POST',
    authRequired: true,
    requestSchema: {
      pathParams: {
        user_id: { type: 'string', required: true }
      },
      requestBody: {
        title: { type: 'string', required: true, maxLength: 255 },
        description: { type: 'string', required: false },
        priority: { type: 'enum', required: true, enumValues: ['Critical', 'High', 'Medium', 'Low'] },
        timestamp: { type: 'string', required: false }
      }
    },
    responseSchema: {
      success: {
        id: 'string',
        user_id: 'string',
        title: 'string',
        description: 'string',
        priority: 'string',
        timestamp: 'string',
        status: 'boolean',
        created_at: 'string',
        updated_at: 'string'
      }
    }
  }
};
```

## Validation Strategies

### 1. Request Validation
```typescript
function validateRequest(contract: ApiContract, request: any): ValidationResult {
  const errors: string[] = [];

  // Validate path parameters
  if (contract.requestSchema.pathParams) {
    for (const [param, rule] of Object.entries(contract.requestSchema.pathParams)) {
      const value = request.params?.[param];
      const validationError = validateField(value, rule, param);
      if (validationError) errors.push(validationError);
    }
  }

  // Validate query parameters
  if (contract.requestSchema.queryParams) {
    for (const [param, rule] of Object.entries(contract.requestSchema.queryParams)) {
      const value = request.query?.[param];
      if (value !== undefined) { // Allow undefined for optional params
        const validationError = validateField(value, rule, param);
        if (validationError) errors.push(validationError);
      }
    }
  }

  // Validate request body
  if (contract.requestSchema.requestBody) {
    for (const [field, rule] of Object.entries(contract.requestSchema.requestBody)) {
      const value = request.body?.[field];
      const validationError = validateField(value, rule, field);
      if (validationError) errors.push(validationError);
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validateField(value: any, rule: ValidationRule, fieldName: string): string | null {
  if (rule.required && (value === undefined || value === null)) {
    return `${fieldName} is required`;
  }

  if (value !== undefined && value !== null) {
    // Type validation
    if (rule.type === 'string' && typeof value !== 'string') {
      return `${fieldName} must be a string`;
    }
    if (rule.type === 'number' && typeof value !== 'number') {
      return `${fieldName} must be a number`;
    }
    if (rule.type === 'boolean' && typeof value !== 'boolean') {
      return `${fieldName} must be a boolean`;
    }

    // Length validation
    if (rule.minLength !== undefined && value.length < rule.minLength) {
      return `${fieldName} must be at least ${rule.minLength} characters`;
    }
    if (rule.maxLength !== undefined && value.length > rule.maxLength) {
      return `${fieldName} must be at most ${rule.maxLength} characters`;
    }

    // Pattern validation
    if (rule.pattern && !new RegExp(rule.pattern).test(value)) {
      return `${fieldName} does not match required pattern`;
    }

    // Enum validation
    if (rule.enumValues && !rule.enumValues.includes(value)) {
      return `${fieldName} must be one of: ${rule.enumValues.join(', ')}`;
    }
  }

  return null;
}
```

### 2. Response Validation
```typescript
function validateResponse(contract: ApiContract, response: any): ValidationResult {
  const errors: string[] = [];

  // For success responses
  if (response.success) {
    const successSchema = contract.responseSchema.success;
    // Validate response structure against schema
    errors.push(...validateObject(response.data, successSchema));
  }

  // For error responses
  if (response.error) {
    const errorSchema = contract.responseSchema.error;
    errors.push(...validateObject(response.data, errorSchema));
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validateObject(obj: any, schema: any, prefix: string = ''): string[] {
  const errors: string[] = [];

  for (const [key, expectedType] of Object.entries(schema)) {
    const value = obj[key];
    const path = prefix ? `${prefix}.${key}` : key;

    if (typeof expectedType === 'string') {
      // Simple type check
      if (typeof value !== expectedType && value !== undefined) {
        errors.push(`${path} should be of type ${expectedType}, got ${typeof value}`);
      }
    } else if (Array.isArray(expectedType)) {
      // Array validation
      if (!Array.isArray(value)) {
        errors.push(`${path} should be an array`);
      } else {
        expectedType.forEach((itemSchema, index) => {
          errors.push(...validateObject(value[index], itemSchema, `${path}[${index}]`));
        });
      }
    } else if (typeof expectedType === 'object') {
      // Nested object validation
      if (typeof value === 'object' && value !== null) {
        errors.push(...validateObject(value, expectedType, path));
      } else {
        errors.push(`${path} should be an object`);
      }
    }
  }

  return errors;
}
```

## Contract Testing Patterns

### 1. Contract-First Testing
```typescript
// Test that actual API responses match contracts
describe('API Contract Tests', () => {
  test('Auth signup follows contract', async () => {
    const response = await fetch('http://localhost:8000/api/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        first_name: 'John',
        last_name: 'Doe',
        email: 'john.doe@example.com',
        password: 'securePassword123',
        favorite_teacher: 'Mrs. Smith'
      })
    });

    const data = await response.json();
    const validationResult = validateResponse(authContracts.signup, { success: true, data });

    expect(validationResult.isValid).toBe(true);
    expect(validationResult.errors).toHaveLength(0);
  });

  test('Task creation follows contract', async () => {
    // Assuming we have a valid user and auth token
    const authToken = 'valid_jwt_token';
    const userId = 'some-valid-user-id';

    const response = await fetch(`http://localhost:8000/api/${userId}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        title: 'Test Task',
        priority: 'High'
      })
    });

    const data = await response.json();
    const validationResult = validateResponse(taskContracts.createTask, { success: true, data });

    expect(validationResult.isValid).toBe(true);
    expect(validationResult.errors).toHaveLength(0);
  });
});
```

### 2. Mock Contract Validation
```typescript
// Validate that mocks match actual contracts
function createMockFromContract(contract: ApiContract): any {
  const mockResponse: any = {};

  // Build mock based on response schema
  for (const [key, typeDef] of Object.entries(contract.responseSchema.success)) {
    if (typeof typeDef === 'string') {
      mockResponse[key] = generateMockValue(typeDef);
    } else if (Array.isArray(typeDef)) {
      mockResponse[key] = [generateMockObject(typeDef[0])]; // Assume single template in array
    } else if (typeof typeDef === 'object') {
      mockResponse[key] = generateMockObject(typeDef);
    }
  }

  return mockResponse;
}

function generateMockValue(type: string): any {
  switch (type) {
    case 'string': return 'mock_value';
    case 'number': return 123;
    case 'boolean': return true;
    case 'date': return new Date().toISOString();
    default: return 'unknown_type';
  }
}

function generateMockObject(schema: any): any {
  const mockObj: any = {};
  for (const [key, typeDef] of Object.entries(schema)) {
    if (typeof typeDef === 'string') {
      mockObj[key] = generateMockValue(typeDef);
    } else if (typeof typeDef === 'object') {
      mockObj[key] = generateMockObject(typeDef);
    }
  }
  return mockObj;
}
```

## Common Contract Anti-Patterns

### 1. Loose Typing
```typescript
// AVOID: Too loose, no validation
interface BadContract {
  data: any; // Any type accepted
  response: any; // Any response structure
}

// PREFER: Strict typing
interface GoodContract {
  data: {
    id: string;
    name: string;
    timestamp: string;
  };
  response: {
    success: boolean;
    data: DataType;
    error?: string;
  };
}
```

### 2. Inconsistent Naming
```typescript
// AVOID: Inconsistent naming between frontend and backend
// Frontend expects: user_id
// Backend provides: userId

// PREFER: Consistent naming convention
// Both use: user_id or userId (pick one and stick to it)
```

### 3. Missing Error Contracts
```typescript
// AVOID: No error contract defined
const badContract = {
  endpoint: '/api/users',
  method: 'GET',
  // No error response schema defined
};

// PREFER: Define error responses too
const goodContract = {
  endpoint: '/api/users',
  method: 'GET',
  responseSchema: {
    success: { /* success schema */ },
    error: {
      detail: 'string',
      status_code: 'number'
    }
  }
};
```

## Contract Evolution Strategy

### 1. Versioning Contracts
```typescript
// Maintain backward compatibility
const contractVersions = {
  'v1': {
    // Original contract
  },
  'v2': {
    // Updated contract with new fields
  }
};

// Or use optional fields for additive changes
const additiveContract = {
  responseSchema: {
    success: {
      id: 'string',
      name: 'string',
      // New optional field in v2
      email?: 'string'  // Optional in v1, required in v2
    }
  }
};
```

### 2. Deprecation Strategy
```typescript
// Mark fields as deprecated in contracts
interface DeprecatedContract {
  old_field: {
    type: 'string';
    deprecated: true;
    removal_date: '2024-12-31';
    replacement: 'new_field';
  };
  new_field: {
    type: 'string';
    required: true;
  };
}
```