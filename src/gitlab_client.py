import gitlab
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
        """
        Collects all changes into a single string for the LLM.
        """
        changes = mr.changes()
        diff_output = ""
        
        for change in changes['changes']:
            file_path = change['new_path']
            diff = change['diff']
            diff_output += f"--- File: {file_path} ---\n{diff}\n\n"
            
        return diff_output

    def post_comment(self, mr, comment_body: str):
        """
        Posts the AI review as a main comment on the MR.
        """
        mr.notes.create({'body': comment_body})
        print(f"Comment posted on MR {mr.iid}")