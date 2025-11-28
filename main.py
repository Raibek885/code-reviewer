import argparse
from src.gitlab_client import GitLabClient
from src.gemini_client import GeminiClient
from src.context_manager import ContextManager

def main():
    parser = argparse.ArgumentParser(description="AI Code Reviewer powered by Gemini")
    parser.add_argument("--project_id", required=True, help="GitLab Project ID")
    parser.add_argument("--mr_id", required=True, help="Merge Request IID")
    args = parser.parse_args()

    print(f"Starting AI Review for Project {args.project_id}, MR {args.mr_id}...")

    # 1. Initialize Clients
    gl_client = GitLabClient()
    gemini_client = GeminiClient()
    context_manager = ContextManager(gl_client)

    # 2. Fetch MR Data
    try:
        mr = gl_client.get_merge_request(args.project_id, args.mr_id)
        print(f"Found MR: {mr.title}")
    except Exception as e:
        print(f"Error fetching MR: {e}")
        return

    # 3. Get Changes (Diff)
    diff_text = gl_client.get_diff_string(mr)
    if not diff_text:
        print("No changes found in this MR.")
        return
    
    print(f"Diff size: {len(diff_text)} characters.")

    # 4. RAG / Context Retrieval Step
    extra_context = context_manager.retrieve_context(args.project_id, diff_text)
    
    if extra_context:
        print(f"Added Reference Context ({len(extra_context)} chars).")

    # 5. Analyze with Gemini
    print("Sending to Gemini...")
    review_text = gemini_client.analyze_diff(diff_text, mr.title, mr.description, extra_context)
    
    # Parse Verdict
    verdict_label = "ai-review-pending" 
    if "VERDICT: APPROVE" in review_text:
        verdict_label = "ai-approved"
        review_text = review_text.replace("VERDICT: APPROVE", "") 
    elif "VERDICT: NEEDS_FIXES" in review_text:
        verdict_label = "ai-changes-requested"
        review_text = review_text.replace("VERDICT: NEEDS_FIXES", "")
    
    final_comment = f" **AI Code Review (Gemini)**\n\n{review_text}"

    # 6. Post Feedback
    gl_client.post_comment(mr, final_comment)

    # 7. Update Labels
    gl_client.update_labels(mr, 
                            add_labels=[verdict_label], 
                            remove_labels=["ai-review-pending", "ai-approved", "ai-changes-requested"])

    print(f"Review completed successfully! Verdict: {verdict_label}")

if __name__ == "__main__":
    main()