import gitlab
import base64
from .config import Config

class GitLabClient:
    def __init__(self):
        self.gl = gitlab.Gitlab(Config.GITLAB_URL, private_token=Config.GITLAB_TOKEN)
        self.gl.auth()

    def get_merge_request(self, project_id, mr_id):
        project = self.gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)
        return mr

    def get_diff_string(self, mr) -> str:
        """Collects all changes into a single string for the LLM."""
        changes = mr.changes()
        diff_output = ""
        for change in changes['changes']:
            file_path = change['new_path']
            diff = change['diff']
            diff_output += f"--- File: {file_path} ---\n{diff}\n\n"
        return diff_output

    def post_comment(self, mr, comment_body: str):
        mr.notes.create({'body': comment_body})
        print(f"Comment posted on MR {mr.iid}")


    def search_file_in_repo(self, project_id, query_term: str):
        """
        Uses GitLab Search API to find a file containing the definition.
        Returns the first matching file path.
        """
        try:
            project = self.gl.projects.get(project_id)

            results = project.search(scope='blobs', search=query_term)
            if results:

                for res in results:
                    if "test" not in res['filename']:
                        return res['filename']
                return results[0]['filename']
        except Exception as e:
            print(f"Search failed for {query_term}: {e}")
        return None

    def get_file_content(self, project_id, file_path: str, ref='main') -> str:
        """Fetches raw content of a file from the repository."""
        try:
            project = self.gl.projects.get(project_id)
            f = project.files.get(file_path=file_path, ref=ref)
            content = base64.b64decode(f.content).decode('utf-8')
            return content
        except Exception as e:
            print(f"Could not fetch content for {file_path}: {e}")
            return ""