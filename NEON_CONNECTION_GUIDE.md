# Neon Database Connection Guide

## Current Status
The application is currently using SQLite for development because the Neon database credentials in the `.env` file are incorrect or expired. This is expected behavior based on the improved error handling.

## How to Connect to Neon

1. **Get your correct Neon credentials**:
   - Log into your Neon Console at https://console.neon.tech
   - Navigate to your project
   - Go to "Connection Details" or "Settings"
   - Copy the connection string

2. **Update the environment file**:
   ```bash
   # In /backend/.env, change the DATABASE_URL to your actual Neon connection string:
   DATABASE_URL=postgresql://your_username:your_password@your_endpoint.region.aws.neon.tech:5432/your_database_name?sslmode=require
   ```

3. **Restart the application**:
   ```bash
   cd backend
   python3 -m src.main
   ```

## Error Handling
The application now has robust error handling:
- If Neon connection fails, it falls back to SQLite automatically
- You'll see a clear error message indicating the connection failure
- All functionality remains available through the fallback database
- When Neon credentials are fixed, it will automatically connect to Neon

## Verification
After updating your Neon credentials:
1. Check the server logs for "Successfully connected to PostgreSQL database"
2. Verify data is stored in your Neon database rather than the local SQLite file
3. Test user registration and task creation to ensure everything works

## For Your Information
The password `VHSM6twE2WJG` in the current connection string appears to be invalid. Please replace it with your actual Neon password from the Neon Console.