#!/bin/bash
# Script to update Neon database connection string
# Usage: ./update_neon_connection.sh "your_actual_connection_string_here"

if [ $# -eq 0 ]; then
    echo "Usage: $0 \"your_neon_connection_string\""
    echo "Example: $0 \"postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech:5432/neondb?sslmode=require\""
    exit 1
fi

CONNECTION_STRING=$1

# Update the backend .env file
sed -i "s|DATABASE_URL=YOUR_NEON_CONNECTION_STRING_HERE|DATABASE_URL=$CONNECTION_STRING|" /mnt/d/Hackathon-2-all-five-phases/backend/.env

echo "Neon database connection string updated in /mnt/d/Hackathon-2-all-five-phases/backend/.env"
echo "Please restart the backend server for changes to take effect"