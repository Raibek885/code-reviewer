import argparse
from src.gitlab_client import GitLabClient
from src.gemini_client import GeminiClient

def main():
    # Setup CLI arguments (принимаем ID проекта и MR)
    parser = argparse.ArgumentParser(description="AI Code Reviewer powered by Gemini")
    parser.add_argument("--project_id", required=True, help="GitLab Project ID")
    parser.add_argument("--mr_id", required=True, help="Merge Request IID")
    args = parser.parse_args()

    print(f"🚀 Starting AI Review for Project {args.project_id}, MR {args.mr_id}...")

    # 1. Initialize Clients
    gl_client = GitLabClient()
    gemini_client = GeminiClient()

    # 2. Fetch MR Data
    try:
        mr = gl_client.get_merge_request(args.project_id, args.mr_id)
        print(f"✅ Found MR: {mr.title}")
    except Exception as e:
        print(f"❌ Error fetching MR: {e}")
        return

    # 3. Get Changes (Diff)
    diff_text = gl_client.get_diff_string(mr)
    if not diff_text:
        print("⚠️ No changes found in this MR.")
        return
    
    print(f"📊 Diff size: {len(diff_text)} characters. Sending to Gemini...")

    # 4. Analyze with Gemini
    review_text = gemini_client.analyze_diff(diff_text, mr.title, mr.description)
    
    # Add a header to identify the bot
    final_comment = f"🤖 **AI Code Review (Gemini)**\n\n{review_text}"

    # 5. Post Feedback to GitLab
    gl_client.post_comment(mr, final_comment)
    print("🎉 Review completed successfully!")

if __name__ == "__main__":
    main()