Project Brief: CLI Onboarding Agent

**Project Name:** CLI Onboarding Agent

**Project Goal:** Develop a command-line interface (CLI) tool that leverages the OpenAI Agents SDK to generate a standardized folder structure for new domain projects, pre-populated with template documents.

**Core Requirements:**

- Accept a folder path as a CLI argument to specify the location for the new domain folder structure.
- Generate a predefined folder structure based on a specified Template Folder.
- Populate the generated folders with template documents, excluding any guide documents (identified by "_guide" in their names).
- Ensure the tool is testable and validate its functionality through:
  - CLI execution success rate.
  - Accuracy of the generated folder structure.
  - Accuracy of the template document generation.
- Utilize the tool in a dogfooding exercise to generate the initial folder structure for the Gherkin Feature Agent component.

**Source of Truth:** This document serves as the source of truth for the project's scope, core requirements, and overall vision. All other documentation and development efforts should align with the principles and goals outlined here.
