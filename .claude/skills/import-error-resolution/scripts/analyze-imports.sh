#!/bin/bash
# Script to analyze import/export patterns in TypeScript files

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

# Main execution
if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <file_path> <export_name> [search_directory]"
    echo "Example: $0 ./src/services/api.ts Task ./src"
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
        *)
            echo "Unknown option. Use --check, --analyze, or --find"
            ;;
    esac
fi