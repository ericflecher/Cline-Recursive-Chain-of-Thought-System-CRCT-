# Active Context:

**Purpose:** This file provides a concise overview of the current work focus, immediate next steps, and active decisions for the CLI Onboarding Agent project. It is intended to be a frequently referenced, high-level summary to maintain project momentum and team alignment.

**Use Guidelines:**
- **Current Work Focus:**  List the 2-3 *most critical* tasks currently being actively worked on. Keep descriptions concise and action-oriented.
- **Next Steps:**  List the immediate next steps required to advance the project. Prioritize and order these steps for clarity.
- **Active Decisions and Considerations:** Document key decisions currently being considered or actively debated. Capture the essence of the decision and any open questions.
- **Do NOT include:** Detailed task breakdowns, historical changes, long-term plans (these belong in other memory bank files like `progress.md` or dedicated documentation).
- **Maintain Brevity:** Keep this file concise and focused on the *current* state of the project. Regularly review and prune outdated information.

## Current Work Focus:

- Developing the CLI Onboarding Agent to generate standardized folder structures for new domain projects
- Creating a modular architecture that separates concerns for template reading, folder generation, and document population

## Next Steps:

1. Implement the CLI Tool Setup (Task 1) - Create the basic CLI structure with argument parsing
2. Implement Template Folder Management (Task 2) - Create functionality to read from template folders
3. Implement Folder Structure Generation (Task 3) - Generate directory structures based on templates
4. Implement Template Document Population (Task 4) - Copy template documents to the target structure
5. Implement Validation and Testing (Task 5) - Ensure reliability and correctness

## Active Decisions and Considerations:

- Whether to implement template variables for customizing generated documents
- How to handle conflicts when target directories or files already exist
- Whether to implement a dry-run mode for previewing changes without making them
- How to structure the OpenAI Agents SDK integration for optimal performance and flexibility
