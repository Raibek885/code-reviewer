# AI Code Reviewer for GitLab

This tool automates the code review process for GitLab Merge Requests using Google's Gemini 2.0 Flash model. It integrates directly with the GitLab API to fetch changes, analyze code logic, and post constructive feedback.

Unlike simple linters, this reviewer uses a Context Awareness mechanism to understand function definitions outside the immediate Diff, reducing hallucinations and improving the accuracy of the review.

## Key Features

* **LLM-Powered Analysis**: Utilizes `gemini-2.0-flash` for high-speed and cost-effective inference.
* **Context Retrieval (RAG-lite)**: Automatically scans the Diff for unknown function calls and fetches their definitions from the repository to provide the LLM with full context.
* **Automated Labeling**: Updates Merge Request labels based on the verdict (e.g., adds `ai-approved` or `ai-changes-requested` and removes `ai-review-pending`).
* **Visual Analysis**: Generates Mermaid.js diagrams for complex logic flows to improve readability within the GitLab comment section.
* **Security & Performance**: Specifically prompts the model to look for security vulnerabilities, hardcoded secrets, and performance bottlenecks.

## Project Structure

```text
.
├── src/
│   ├── config.py           # Configuration and environment variable management
│   ├── context_manager.py  # Logic for extracting context (RAG) from the repo
│   ├── gemini_client.py    # Wrapper for Google Generative AI SDK
│   ├── gitlab_client.py    # Wrapper for GitLab API interactions
│   └── prompts.py          # System instructions and prompt engineering
├── main.py                 # Entry point of the application
├── requirements.txt        # Python dependencies
└── .gitignore
```
### Prerequisites
* Python 3.10 or higher
* A GitLab account with a Personal Access Token (API scope)
* A Google Cloud API Key for Gemini

## Installation
### 1.Clone the repository
```bash
git clone <repository_url>
cd code-reviewer
```
### 2.Set up a Virtual Environment
```bash
python -m venv venv
# Linux/MacOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate
```
### 3.Install Dependencies
```bash
pip install -r requirements.txt
```
### Configuration
Create a `.env` file in the root directory. You can use the example below:
```  bash
# GitLab Configuration
GITLAB_URL=[https://gitlab.com](https://gitlab.com)
GITLAB_TOKEN=your_private_gitlab_token

# Google Gemini Configuration
GEMINI_API_KEY=your_google_ai_key
```
**Note:** The application defaults to gemini-2.0-flash. You can modify GEMINI_MODEL_NAME in src/config.py if needed.

## Usage
Run the script manually or trigger it via CI/CD pipelines. You must provide the Project ID and the Merge Request IID.
```bash
python main.py --project_id <PROJECT_ID> --mr_id <MR_IID>
```
## Workflow Description
1. **Initialization:** The script connects to GitLab and Google Gemini APIs.
2. **Diff Extraction:** Fetches the changes from the specified Merge Request.
3. **Context Analysis:**
    * Parses the Diff for function calls.
    * If a function definition is missing from the Diff, the ContextManager searches the repository to retrieve the relevant code block.
4. **Inference:** Sends the Diff + Extra Context to Gemini.
5. **Feedback:**
    * Posts a comment on the Merge Request with a summary, detailed analysis, and optional Mermaid diagrams.
    * Updates the MR labels based on the final verdict.
