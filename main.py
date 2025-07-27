import os
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew
from github import Github
import uuid

# Prompt user for the project idea
PROJECT_IDEA = input("Enter your project idea (e.g., 'A note-taking app with user authentication'): ").strip()
if not PROJECT_IDEA:
    raise ValueError("Project idea cannot be empty. Please provide a valid project idea.")

# Check if OPENAI_API_KEY is set
if not os.getenv("OPENAI_API_KEY"):
    raise EnvironmentError(
        "OPENAI_API_KEY environment variable is not set. Set it using 'export OPENAI_API_KEY=your-key'.")

# Check if GITHUB_TOKEN is set
if not os.getenv("GITHUB_TOKEN"):
    raise EnvironmentError(
        "GITHUB_TOKEN environment variable is not set. Set it using 'export GITHUB_TOKEN=your-token'.")

# Initialize LLM with error handling
try:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
except Exception as e:
    raise Exception(f"Failed to initialize ChatOpenAI: {str(e)}")

# Project directory setup
PROJECT_DIR = "auto_project"
os.makedirs(PROJECT_DIR, exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/frontend", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/backend", exist_ok=True)
os.makedirs(f"{PROJECT_DIR}/docs", exist_ok=True)

# GitHub setup
REPO_NAME = f"auto-project-{uuid.uuid4().hex[:8]}"

# Agent 1: Project Manager
project_manager = Agent(
    role="Project Manager",
    goal="Define project requirements based on the provided idea.",
    backstory="Experienced in breaking down project ideas into actionable tasks.",
    llm=llm,
    verbose=True
)

# Agent 2: Architect
architect = Agent(
    role="System Architect",
    goal="Design the technical architecture based on the project requirements.",
    backstory="Expert in designing scalable systems.",
    llm=llm,
    verbose=True
)

# Agent 3: Frontend Developer
frontend_dev = Agent(
    role="Frontend Developer",
    goal="Generate a complete React frontend with Tailwind CSS for the project idea.",
    backstory="Expert in building modular, responsive, and user-friendly React applications with Tailwind CSS.",
    llm=llm,
    verbose=True
)

# Agent 4: Backend Developer
backend_dev = Agent(
    role="Backend Developer",
    goal="Generate a secure and scalable FastAPI backend with SQLite for the project idea .",
    backstory="Proficient in building RESTful APIs with FastAPI, focusing on security and performance.",
    llm=llm,
    verbose=True
)

# Agent 5: Code Reviewer
code_reviewer = Agent(
    role="Code Reviewer",
    goal="Review generated code and provide improvement feedback.",
    backstory="Detail-oriented expert in code quality.",
    llm=llm,
    verbose=True
)

# Agent 6: Documentation Writer
doc_writer = Agent(
    role="Documentation Writer",
    goal="Write a comprehensive README.md based on the project.",
    backstory="Experienced in creating technical documentation.",
    llm=llm,
    verbose=True
)

# Agent 7: GitHub Manager
github_manager = Agent(
    role="GitHub Manager",
    goal="Create a GitHub repository and push all files.",
    backstory="Expert in version control and GitHub automation.",
    llm=llm,
    verbose=True
)

# Tasks
task1 = Task(
    description=f"Define requirements for the project idea: '{PROJECT_IDEA}'. Output a JSON file with detailed requirements including features, target users, and scope.",
    agent=project_manager,
    expected_output="A JSON file 'requirements.json' with project requirements.",
    output_file=f"{PROJECT_DIR}/requirements.json"
)

task2 = Task(
    description=f"Design the technical architecture for the project based on the requirements in '{PROJECT_DIR}/requirements.json'. Use React with Tailwind CSS for the frontend and FastAPI with SQLite for the backend unless the requirements suggest otherwise. Output a markdown file.",
    agent=architect,
    expected_output="A markdown file 'architecture.md' with the architecture.",
    output_file=f"{PROJECT_DIR}/docs/architecture.md"
)

task3 = Task(
    description=f"Generate React and Tailwind CSS code for the UI of the project based on the requirements in '{PROJECT_DIR}/requirements.json'. Save in the frontend directory.",
    agent=frontend_dev,
    expected_output="React components and CSS in frontend directory.",
    output_file=f"{PROJECT_DIR}/frontend/App.jsx"
)

task4 = Task(
    description=f"Generate FastAPI code for CRUD operations with SQLite and a requirements.txt file based on the requirements in '{PROJECT_DIR}/requirements.json'. Save in the backend directory.",
    agent=backend_dev,
    expected_output="FastAPI code and requirements.txt in backend directory.",
    output_file=f"{PROJECT_DIR}/backend/main.py"
)

task5 = Task(
    description=f"Review the generated frontend and backend code in '{PROJECT_DIR}/frontend' and '{PROJECT_DIR}/backend', providing feedback in a markdown file.",
    agent=code_reviewer,
    expected_output="A markdown file 'code_review.md' with feedback.",
    output_file=f"{PROJECT_DIR}/docs/code_review.md"
)

task6 = Task(
    description=f"Write a README.md based on the project requirements in '{PROJECT_DIR}/requirements.json', architecture in '{PROJECT_DIR}/docs/architecture.md', and code review feedback in '{PROJECT_DIR}/docs/code_review.md'.",
    agent=doc_writer,
    expected_output="A README.md file in the project root.",
    output_file=f"{PROJECT_DIR}/README.md"
)

task7 = Task(
    description=f"Create a GitHub repository '{REPO_NAME}' and push all files from '{PROJECT_DIR}'.",
    agent=github_manager,
    expected_output="Confirmation that the repository was created and files pushed.",
    callback=lambda output: push_to_github(output)
)


# Custom callback for GitHub push
def push_to_github(output):
    try:
        g = Github(os.getenv("GITHUB_TOKEN"))
        user = g.get_user()
        repo = user.create_repo(REPO_NAME, private=False)

        for root, _, files in os.walk(PROJECT_DIR):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                repo_path = os.path.relpath(file_path, PROJECT_DIR)
                repo.create_file(repo_path, f"Add {repo_path}", content, branch="main")

        return f"Repository '{REPO_NAME}' created and files pushed successfully."
    except Exception as e:
        return f"Failed to push to GitHub: {str(e)}"


# Crew setup
crew = Crew(
    agents=[project_manager, architect, frontend_dev, backend_dev, code_reviewer, doc_writer, github_manager],
    tasks=[task1, task2, task3, task4, task5, task6, task7],
    verbose=True
)

# Kickoff the crew
if __name__ == "__main__":
    try:
        print(f"Starting CrewAI workflow for project idea: '{PROJECT_IDEA}'...")
        crew.kickoff()
        print("CrewAI workflow completed successfully.")
    except Exception as e:
        print(f"Error running the crew: {str(e)}")