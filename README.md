# AgentDevTeam

## Overview
AgentDevTeam is an innovative Multi-Agent System powered by **CrewAI** that automates software development by simulating a professional development team. It takes a user-defined project idea and orchestrates AI agents to generate, review, document, and deploy code to a GitHub repository, streamlining the creation of production-ready software projects.

## Purpose
AgentDevTeam aims to accelerate software development by:
- Generating high-quality frontend and backend code tailored to the user’s project idea.
- Ensuring code quality through automated reviews.
- Producing clear documentation and automating deployment to GitHub.

## Agents
The system comprises the following AI agents, each with a specialized role:
- **Frontend Developer**: Builds a modular React frontend with Tailwind CSS, ensuring responsive design, error handling, and accessibility.
- **Backend Developer**: Creates a secure FastAPI backend with SQLite, implementing RESTful APIs and security features like JWT authentication when needed.
- **Code Reviewer**: Evaluates generated code for quality, adherence to best practices, and potential improvements, outputting feedback to `docs/code_review.md`.
- **Documentation Writer**: Produces this README to explain the system and its output, acting as the team’s technical communicator.
- **GitHub Manager**: Automates the creation of a GitHub repository and pushes all files, handling deployment like a DevOps engineer.

## How the Multi-Agent System Works as a Development Team
CodeCraftAI mimics a professional software development team through its agents, each contributing to a specific stage of the project lifecycle:

- **Collaboration**: The agents operate in a coordinated, sequential workflow, sharing context through generated files:
  1. The **Frontend Developer** generates React components (`frontend/src/App.jsx`, `App.css`, `package.json`) based on the user’s project idea.
  2. Simultaneously, the **Backend Developer** creates a FastAPI backend (`backend/main.py`, `requirements.txt`) tailored to the same idea.
  3. The **Code Reviewer** assesses both frontend and backend code, producing feedback in `docs/code_review.md` to ensure quality and adherence to best practices.
  4. The **Documentation Writer** uses the project idea and code review feedback to generate this README, providing clear documentation.
  5. The **GitHub Manager** pushes all files to a user-specified GitHub repository, completing the deployment process.

- **Team Dynamics**:
  - **Specialization**: Each agent has a distinct role, mirroring a real team’s division of labor (e.g., developers, QA, technical writers, DevOps).
  - **Quality Assurance**: The Code Reviewer acts as a senior developer, catching issues like missing error handling or security vulnerabilities.
  - **Communication**: The Documentation Writer ensures the project is well-documented, making it accessible to users and contributors.
  - **Automation**: The GitHub Manager streamlines deployment, similar to a CI/CD pipeline in a professional team.

This collaborative approach ensures efficiency, quality, and a polished final product with minimal user intervention.

## Technologies Used
AgentDevTeam is built with the following technologies:
- **CrewAI**: Orchestrates the multi-agent system.
- **LangChain**: Integrates language models and tools for agent functionality.
- **OpenAI API**: Powers the agents with advanced language understanding and code generation.
- **PyGithub**: Enables interaction with the GitHub API for repository creation and file uploads.
- **Python**: The primary programming language for the system.

## Example
For a project idea like "A note-taking app with user authentication":
- **Frontend**: A React application with login/registration forms and note management features, styled with Tailwind CSS.
- **Backend**: A FastAPI server with endpoints for user authentication and note CRUD operations, secured with JWT and bcrypt.
- **Output Files**:
  - `frontend/src/App.jsx`, `frontend/src/App.css`, `frontend/package.json`
  - `backend/main.py`, `backend/requirements.txt`
  - `docs/code_review.md`
  - `README.md`

## Generated Code Details
The generated code is customized to the user’s project idea. For specifics on the generated application, including features and suggested improvements, see `docs/code_review.md`.


## License
This project is licensed under the MIT License.
