import praw
import requests
import prawcore

# -----------------------------------------
# Gemini API Key (from https://makersuite.google.com/app)
GEMINI_API_KEY = "AIzaSyA_-TEAQ0P9nEUXJl3o2vaqBKcWjFqEYuM" 

# Reddit API Credentials
REDDIT_CLIENT_ID = "aiBTtMPZl8imIgLS-W5ACA"
REDDIT_SECRET = "5wM7TUCBsgFe1GXSh89ugA9qrhqIEg"
REDDIT_USER_AGENT = "PersonaScraperBot/0.1 by Key_Economy_7342"


# Fetch Reddit User Posts & Comments
def get_user_data(username):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )

    user = reddit.redditor(username)

    try:
        _ = user.id  # Triggers fetch to confirm user exists

        posts = [
            f"[POST] {submission.title}\n{submission.selftext}"
            for submission in user.submissions.new(limit=100)
        ]
        comments = [
            f"[COMMENT] {comment.body}"
            for comment in user.comments.new(limit=100)
        ]

        return posts, comments

    except prawcore.exceptions.NotFound:
        print(f"User '{username}' not found, suspended, or private.")
        return [], []

    except Exception as e:
        print(f"Unexpected error: {e}")
        return [], []


# Generate Persona using Gemini REST API
def generate_persona_gemini(posts, comments):
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
    )

    reddit_data = "\n".join(posts + comments)

    prompt = f"""
    Based on the following Reddit posts and comments, generate a detailed user persona.
    For each trait, cite the specific post or comment that supports it.

    --- BEGIN REDDIT DATA ---
    {reddit_data}
    --- END REDDIT DATA ---
    """

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return "Persona generation failed."

# -----------------------------------------
# 🔹 Step 3: Save Persona to File
def save_persona_to_file(username, persona):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(persona)
    print(f"Persona saved to {filename}")

# -----------------------------------------
# 🔹 Main Program
def main():
    profile_url = input("Enter the Reddit profile URL: ").strip().replace('"', '')
    username = profile_url.rstrip("/").split("/")[-1]

    print(f"\n------Scraping Reddit data for user: {username} ...")
    posts, comments = get_user_data(username)

    if not posts and not comments:
        print("No content found for this user. Skipping persona generation.")
        return

    print(f"------Total posts: {len(posts)}, Total comments: {len(comments)}")
    print("\nGenerating persona using Gemini Pro...")

    persona = generate_persona_gemini(posts, comments)
    save_persona_to_file(username, persona)

# -----------------------------------------
if __name__ == "__main__":
    main()
