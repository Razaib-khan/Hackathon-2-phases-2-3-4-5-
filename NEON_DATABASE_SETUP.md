# Database Configuration Guide

## Issue Description
The application was not storing data in the Neon database because of authentication issues with the provided credentials.

## Root Cause
The Neon database connection string in the `.env` file contains incorrect or expired credentials:
```
postgresql://neondb_owner:VHSM6twE2WJG@ep-aged-math-231340.us-east-1.aws.neon.tech:5432/neondb?sslmode=require
```

## Solution Steps

### 1. Get Correct Neon Credentials
1. Log into your Neon Console at https://console.neon.tech
2. Navigate to your project dashboard
3. Click on "Settings" or "Connection Details"
4. Copy the connection string provided by Neon
5. The format should be: `postgresql://username:password@endpoint:port/database_name?sslmode=require`

### 2. Update Environment Variables
Update the `DATABASE_URL` in both locations:

**Backend (.env file):**
```bash
# Database Configuration
DATABASE_URL=your_new_neon_connection_string_here
```

**Root project (.env file):**
```bash
# Database Configuration
DATABASE_URL=your_new_neon_connection_string_here
```

### 3. Verify Connection
After updating the credentials:
1. Restart the backend server
2. Check the server logs for successful PostgreSQL connection
3. Verify tables are created in Neon database

### 4. Troubleshooting Tips
- Make sure your IP address is whitelisted in Neon settings
- Verify the database user has proper permissions
- Check that the database name is correct
- Ensure SSL mode is set to `require` for Neon

## Current Configuration
Currently, the application is configured to use SQLite for development:
```
DATABASE_URL=sqlite:///./test.db
```

This works for local development but will not sync data to Neon.

## Testing the Connection
To test if your Neon connection is working, you can temporarily run:
```bash
cd backend
python3 -c "
from sqlalchemy import create_engine
from database.database import DATABASE_URL

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT version();'))
        print('Database connected successfully!')
        print(result.fetchone()[0])
except Exception as e:
    print(f'Connection failed: {e}')
"
```

## Security Note
Remember to never commit your actual database credentials to version control. Keep them in your `.env` files which should be in `.gitignore`.