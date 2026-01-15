# Import Error Resolution Skill

## Purpose
This skill resolves import/export errors in TypeScript/JavaScript modules systematically.

## When to Use
- When encountering "Export X doesn't exist in target module" errors
- When facing "Module has no exported member" errors
- When dealing with circular dependency issues
- When mixing default and named exports causes issues

## Approach
1. **Analyze the Error**: Identify the specific import/export issue
2. **Trace the Module Chain**: Follow import paths to identify where the issue originates
3. **Check Export Definitions**: Verify that the requested export exists in the source module
4. **Verify Import Syntax**: Ensure import statements match export patterns
5. **Resolve Type vs Value Exports**: Separate type-only imports when needed
6. **Fix Circular Dependencies**: Restructure imports to break cycles
7. **Test Resolution**: Verify the fix works

## Process
The skill will:
- Read the source file where the export is expected
- Identify missing or incorrectly defined exports
- Fix export definitions to match import requirements
- Update import statements to match export patterns
- Separate types and runtime code when needed
- Create intermediate index files if necessary

## Success Criteria
- Import errors are resolved
- All exports are properly accessible
- No circular dependencies remain
- Type and value exports are correctly separated