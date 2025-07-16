**# Reddit-Persona-Generator
This project extracts a Reddit user's activity (posts and comments) and uses the **Gemini LLM API** to generate a detailed user persona. Each trait in the persona includes citations from specific posts or comments to ensure traceability and transparency.

---

## Features

-- Scrapes Reddit posts and comments (up to 100 each).
-- Uses Google Gemini Pro to generate insightful psychological personas.
-- Outputs persona to a `.txt` file with source citations.
-- Includes three sample user personas as part of the assignment.
-- Clean and modular Python implementation.


---

## Requirements

Install the required packages using pip:
    pip install -r requirements.txt

## How to Run this code

1) Clone the Repository or download the files.

2) Set Up API Keys:

    --Open persona_generator.py.
    --Replace:
          GEMINI_API_KEY with your Gemini Pro API key from Google MakerSuite.
          REDDIT_CLIENT_ID, REDDIT_SECRET, and REDDIT_USER_AGENT with your Reddit Developer App credentials.

3) Run the Script:**
    python persona_generator.py

4) Input the Reddit Profile URL when prompted.
    https://www.reddit.com/user/kojied/    (example)

5) Output: A .txt file (e.g., kojied_persona.txt) will be created in the same folder, containing the generated user persona with cited posts/comments.
