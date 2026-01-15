# TypeScript Module Patterns for Proper Imports/Exports

## Common Issues and Solutions

### Issue: "Export X doesn't exist in target module"
**Cause**: The export is not properly declared or accessible
**Solution**:
- Ensure the export is declared with `export` keyword
- Check that the export is available at runtime (not just type level)
- Verify the export is not conditional

### Issue: Mixing Types and Values in Same Import
**Cause**: Importing both types and runtime values together
**Solution**:
- Use `import type` for types-only imports
- Separate type imports from value imports
- Use separate files for types vs runtime code

### Issue: Circular Dependencies
**Cause**: Modules importing each other
**Solution**:
- Create intermediate files to break cycles
- Move shared types to separate files
- Restructure module hierarchy

## Best Practices

### Export Patterns
```typescript
// Named exports
export interface MyInterface { ... }
export class MyClass { ... }
export function myFunction() { ... }

// Default export
export default MyClass;

// Mixed exports
export { MyInterface, MyClass, myFunction };
export default MyClass;
```

### Import Patterns
```typescript
// Named imports
import { MyInterface, MyClass, myFunction } from './module';

// Default import
import MyClass from './module';

// Mixed imports
import MyClass, { MyInterface, myFunction } from './module';

// Type-only imports
import type { MyInterface } from './module';
```

## File Structure Recommendations

### For API Services
```
services/
├── api.ts          // Runtime functions and class
├── types.ts        // Type definitions only
└── index.ts        // Unified exports
```

This separates type information from runtime code and prevents import conflicts.