# Guide for {{ project_name }}

This is a guide document that will be excluded by default when using the CLI Onboarding Agent.

## Template Variables

The following template variables are available:

- `{{ project_name }}`: The name of the project
- `{{ package_name }}`: The name of the package (usually a snake_case version of the project name)
- `{{ project_description }}`: A description of the project
- `{{ author }}`: The author of the project
- `{{ author_email }}`: The email of the author
- `{{ current_year }}`: The current year

## Customizing the Template

You can customize this template by modifying the files in the template directory.
Any files with "_guide" in their name will be excluded by default when generating
a new project structure.

## Adding More Files

Feel free to add more files to this template as needed for your project.
