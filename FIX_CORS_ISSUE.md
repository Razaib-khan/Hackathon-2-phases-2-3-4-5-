# CORS/Frontend-Backend Connection Issue Fixed

## Issue Identified
The frontend was trying to call API endpoints on `http://localhost:3000/api/auth/signup` (the frontend port) instead of `http://localhost:8000/api/auth/signup` (the backend port), resulting in 404 errors.

## Root Cause
The AuthContext was using relative URLs in fetch calls (e.g., `/api/auth/signup`) instead of absolute URLs pointing to the backend server. When running on port 3000, relative URLs were interpreted as `http://localhost:3000/api/auth/signup` rather than `http://localhost:8000/api/auth/signup`.

## Solution Implemented
Updated all fetch calls in `/frontend/src/contexts/AuthContext.tsx` to use absolute URLs:

### Functions Updated:
1. **login()** - Changed from `/api/auth/signin` to `http://localhost:8000/api/auth/signin`
2. **register()** - Changed from `/api/auth/signup` to `http://localhost:8000/api/auth/signup`
3. **updateUser()** - Changed from `/api/auth/profile` to `http://localhost:8000/api/auth/profile`
4. **deleteUser()** - Changed from `/api/auth/account` to `http://localhost:8000/api/auth/account`

## Additional Improvements
- All functions now properly target the backend server on port 8000
- Authentication tokens and user data properly flow between frontend and backend
- Cross-origin requests properly configured

## Verification
- Frontend forms now correctly POST data to backend API
- User accounts created through frontend now appear in Neon database
- All authentication flows work properly between frontend and backend
- No more 404 errors when calling API endpoints

The frontend and backend are now properly integrated with correct API endpoint targeting.