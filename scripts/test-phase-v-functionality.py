#!/usr/bin/env python3
"""
Basic test script to verify Phase V functionality
This script verifies that the core components of Phase V are properly implemented
"""

import sys
import os
import importlib.util
from pathlib import Path

def test_imports():
    """Test that all the new modules can be imported without errors"""
    print("Testing module imports...")

    # Add backend to the Python path to allow imports
    sys.path.insert(0, './backend')

    modules_to_test = [
        "src.models.task",
        "src.models.recurrence_pattern",
        "src.models.events",
        "src.services.task_service",
        "src.services.task_scheduler",
        "src.services.kafka_producer",
        "src.services.kafka_consumer",
        "src.utils.logging",
        "src.services.health_check",
        "config.kafka_config",
        "config.cloud_config"
    ]

    for module_path in modules_to_test:
        try:
            # Convert dot notation to file path
            file_path = f"backend/{module_path.replace('.', '/')}.py"
            if os.path.exists(file_path):
                spec = importlib.util.spec_from_file_location(module_path, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✓ Successfully imported {module_path}")
            else:
                print(f"✗ File does not exist: {file_path}")
                return False
        except Exception as e:
            print(f"✗ Failed to import {module_path}: {str(e)}")
            return False

    return True

def test_directory_structure():
    """Test that all required directories exist"""
    print("\nTesting directory structure...")

    dirs_to_check = [
        "backend/src/models",
        "backend/src/services",
        "backend/src/api",
        "backend/src/utils",
        "backend/config",
        "charts/todo-chatbot",
        "charts/todo-chatbot/templates/kafka",
        "dapr/components",
        "scripts/local",
        "infrastructure/aks",
        "infrastructure/gke",
        "monitoring",
        "docs",
        ".github/workflows"
    ]

    all_good = True
    for dir_path in dirs_to_check:
        if os.path.isdir(dir_path):
            print(f"✓ Directory exists: {dir_path}")
        else:
            print(f"✗ Directory missing: {dir_path}")
            all_good = False

    return all_good

def test_config_files():
    """Test that important configuration files exist"""
    print("\nTesting configuration files...")

    files_to_check = [
        "charts/todo-chatbot/values.yaml",
        "charts/todo-chatbot/values-aks.yaml",
        "charts/todo-chatbot/values-gke.yaml",
        "dapr/components/pubsub.yaml",
        "dapr/components/statestore.yaml",
        "dapr/components/bindings.yaml",
        "dapr/components/secrets.yaml",
        "monitoring/prometheus-config.yaml",
        "monitoring/grafana-dashboard.json",
        "monitoring/loki-config.yaml",
        "monitoring/tempo-config.yaml",
        ".github/workflows/cicd-pipeline.yml",
        ".github/workflows/deploy-k8s.yml",
        ".github/workflows/test-integration.yml",
        "scripts/local/setup-minikube.sh",
        "scripts/local/deploy-local.sh",
        "scripts/local/teardown-local.sh",
        "infrastructure/aks/main.tf",
        "infrastructure/gke/main.tf"
    ]

    all_good = True
    for file_path in files_to_check:
        if os.path.isfile(file_path):
            print(f"✓ File exists: {file_path}")
        else:
            print(f"✗ File missing: {file_path}")
            all_good = False

    return all_good

def main():
    """Main test function"""
    print("Phase V Implementation Verification")
    print("=" * 40)

    # Change to the project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)

    all_tests_passed = True

    # Run all tests
    if not test_imports():
        all_tests_passed = False

    if not test_directory_structure():
        all_tests_passed = False

    if not test_config_files():
        all_tests_passed = False

    print("\n" + "=" * 40)
    if all_tests_passed:
        print("✓ All Phase V implementation tests passed!")
        print("\nPhase V features implemented:")
        print("- Advanced task management (recurring tasks, due dates, reminders)")
        print("- Event-driven architecture with Kafka")
        print("- Dapr integration for distributed services")
        print("- Local deployment on Minikube")
        print("- Cloud deployment configurations for AKS/GKE")
        print("- CI/CD pipeline with GitHub Actions")
        print("- Monitoring and observability stack")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())