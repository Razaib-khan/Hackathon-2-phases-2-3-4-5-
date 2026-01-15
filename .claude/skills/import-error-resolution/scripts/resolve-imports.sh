#!/bin/bash
# Script to analyze and resolve import/export patterns in TypeScript files

# Function to check if a specific export exists in a file
check_export_exists() {
    local file_path="$1"
    local export_name="$2"

    if grep -q "export.*${export_name}" "$file_path" || grep -q "export.*{.*${export_name}.*}" "$file_path"; then
        echo "✓ Export ${export_name} found in $file_path"
        return 0
    else
        echo "✗ Export ${export_name} NOT found in $file_path"
        return 1
    fi
}

# Function to analyze import statements in a file
analyze_imports() {
    local file_path="$1"
    echo "Analyzing imports in: $file_path"

    # Extract import statements
    if [[ -f "$file_path" ]]; then
        grep -o "import.*from.*" "$file_path" || echo "No import statements found"
    else
        echo "File $file_path does not exist"
    fi
}

# Function to find all files with a specific export
find_files_with_export() {
    local export_name="$1"
    local search_dir="${2:-.}"

    echo "Searching for files containing export '$export_name' in $search_dir:"
    find "$search_dir" -name "*.ts" -o -name "*.tsx" | xargs grep -l "export.*${export_name}" 2>/dev/null || echo "No files found with export $export_name"
}

# Function to fix common import issues
resolve_import_issue() {
    local error_message="$1"
    local affected_file="$2"

    echo "Attempting to resolve import issue in $affected_file"
    echo "Error: $error_message"

    # Check if the issue is about Task export not existing
    if [[ "$error_message" == *"Task"* ]] && [[ "$error_message" == *"doesn't exist"* ]]; then
        echo "Detected missing Task export issue"

        # Check if the file importing Task exists
        if [[ -f "$affected_file" ]]; then
            # Look for the import statement
            if grep -q "import.*Task.*from" "$affected_file"; then
                echo "Found Task import in $affected_file"

                # Check the API file to see if Task is properly exported
                api_file_dir=$(dirname "$affected_file")
                # Navigate up to find the services/api.ts file
                for i in {1..5}; do
                    api_file="${api_file_dir}/services/api.ts"
                    if [[ -f "$api_file" ]]; then
                        echo "Found API file: $api_file"

                        # Check if Task is exported from the API file
                        if grep -q "export.*interface.*Task" "$api_file" || grep -q "export.*{.*Task" "$api_file"; then
                            echo "Task interface is properly exported from API file"
                            echo "Issue may be with module resolution or transitive dependencies"
                        else
                            echo "Task interface is NOT properly exported from API file"
                            echo "This may require manual fix in the API service file"
                        fi
                        break
                    fi
                    api_file_dir="../$api_file_dir"
                done
            fi
        fi
    fi
}

# Main execution
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <file_path> <export_name> [search_directory]"
    echo "Example: $0 ./src/services/api.ts Task ./src"
    echo "Or: $0 --resolve \"error message\" <affected_file>"
else
    case "$1" in
        --check)
            if [[ -n "$2" && -n "$3" ]]; then
                check_export_exists "$2" "$3"
            else
                echo "Usage: $0 --check <file_path> <export_name>"
            fi
            ;;
        --analyze)
            if [[ -n "$2" ]]; then
                analyze_imports "$2"
            else
                echo "Usage: $0 --analyze <file_path>"
            fi
            ;;
        --find)
            if [[ -n "$2" ]]; then
                find_files_with_export "$2" "${3:-.}"
            else
                echo "Usage: $0 --find <export_name> [search_directory]"
            fi
            ;;
        --resolve)
            if [[ -n "$2" && -n "$3" ]]; then
                resolve_import_issue "$2" "$3"
            else
                echo "Usage: $0 --resolve \"error_message\" <affected_file>"
            fi
            ;;
        *)
            echo "Unknown option. Use --check, --analyze, --find, or --resolve"
            ;;
    esac
fi