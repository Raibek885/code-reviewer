import re
from .gitlab_client import GitLabClient

class ContextManager:
    def __init__(self, gl_client: GitLabClient):
        self.gl_client = gl_client

        self.IGNORED_KEYWORDS = {
            'print', 'len', 'str', 'int', 'list', 'dict', 'set', 'super', 
            '__init__', 'range', 'enumerate', 'isinstance', 'float', 'bool'
        }

    def extract_potential_definitions(self, diff_text: str) -> set:
        """
        Extracts function calls from the added lines in the diff using Regex.
        Looks for patterns like 'some_function('
        """
        potential_calls = set()
        

        pattern = re.compile(r'\+.*(?<!def\s)(\b[a-zA-Z_][a-zA-Z0-9_]*)\(')
        
        lines = diff_text.split('\n')
        for line in lines:
            if line.startswith('+') and not line.startswith('+++'):
                matches = pattern.findall(line)
                for match in matches:
                    if match not in self.IGNORED_KEYWORDS:
                        potential_calls.add(match)
        
        return potential_calls

    def retrieve_context(self, project_id, diff_text: str) -> str:
        """
        Orchestrates the context retrieval:
        1. Find unknown calls in diff.
        2. Search GitLab for their definitions.
        3. Download file content.
        """
        print("Scanning diff for external dependencies...")
        calls = self.extract_potential_definitions(diff_text)
        
        if not calls:
            return ""

        context_output = "\n\n## Reference Context (Definitions from other files):\n"
        found_something = False
        
  
        for func_name in list(calls)[:3]: 
            print(f"Searching definition for: {func_name}...")
            

            search_query = f"def {func_name}"
            found_file = self.gl_client.search_file_in_repo(project_id, search_query)
            
            if found_file:
                print(f"   Found in: {found_file}")
                content = self.gl_client.get_file_content(project_id, found_file)
                
                if content:
                    context_output += f"\n--- Reference File: {found_file} ---\n"
                    context_output += content + "\n"
                    found_something = True
            else:
                print(f"Definition not found for {func_name}")

        return context_output if found_something else ""