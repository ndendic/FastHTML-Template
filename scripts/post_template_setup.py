import os
import sys
import shutil

def setup_template():
    project_name = os.environ.get('TEMPLATE_PROJECT_NAME')
    if not project_name:
        print("Error: Project name not provided")
        sys.exit(1)

    # Rename the project directory
    if os.path.exists('project'):
        os.rename('project', project_name)

    # Update files that need the project name
    files_to_update = [
        'Makefile',
        'pyproject.toml',
        # Add other files that need updating
    ]

    for file_path in files_to_update:
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
            
            # Replace placeholders with actual values
            content = content.replace('${PROJECT_NAME}', project_name)
            
            with open(file_path, 'w') as file:
                file.write(content)

if __name__ == "__main__":
    setup_template()
