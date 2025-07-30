import os
import requests
import traceback

# === CONFIGURATION ===
GROQ_API_KEY = "" # Set your Groq API key in the environment
if not GROQ_API_KEY:
    raise Exception("❌ GROQ_API_KEY environment variable is not set.")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-70b-8192"
HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

TEST_FILE_PATH = "groq_generated_test.py"

# === STEP 1: Generate a Selenium test case from description ===
def generate_test_code(description, url):
    prompt = (
        f"You are a Python Selenium expert.\n\n"
        f"Write a complete Python Selenium test script for the following:\n\n"
        f"Test Goal: {description}\n"
        f"Target URL: {url}\n\n"
        "Requirements:\n"
        "- Use Chrome WebDriver\n"
        "- Use the latest Selenium syntax (e.g. find_element with By)\n"
        "- Include all necessary imports\n"
        "- Use explicit waits (WebDriverWait) to find elements\n"
        "- Do not include markdown, code fences, or explanations\n"
        "- Do not use backticks (`). Use repr() or str() for debugging output\n"
        "- The code must be complete and runnable as is\n"
    )

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']




# === STEP 2: Run the generated test case ===
def run_test():
    try:
        exec(open(TEST_FILE_PATH).read(), {})
        return True, None
    except Exception:
        return False, traceback.format_exc()

# === STEP 3: Self-heal the test if it fails ===
def heal_test_code(broken_code, error_trace):
    prompt = (
        "You previously wrote the following Selenium Python code, but it failed.\n\n"
        "--- Code ---\n"
        f"{broken_code}\n\n"
        "--- Error ---\n"
        f"{error_trace}\n\n"
        "Please fix the code. Return only the corrected Python code. "
        "Do not include any explanation or extra text.\n"
        "Do not use backticks (`). Use repr() or str() if needed.\n"
    )


    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    response = requests.post(GROQ_API_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# === AGENTIC TEST LOOP ===
def run_agentic_test(description, url, max_attempts=3):
    print("🤖 Generating test case from Groq...")
    test_code = generate_test_code(description, url)

    for attempt in range(max_attempts):
        print(f"\n🔁 Attempt {attempt + 1} of {max_attempts}")
        with open(TEST_FILE_PATH, 'w') as f:
            f.write(test_code)

        passed, error = run_test()

        if passed:
            print("✅ Test passed successfully!")
            return
        else:
            print("❌ Test failed. Healing...")

            test_code = heal_test_code(test_code, error)

    print("🛑 Test failed after maximum retries. Manual debugging required.")

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    # Customize this test goal and URL as needed
    test_goal = "Verify that clicking the login button on https://www.amazon.co.uk/ navigates to the dashboard page"
    test_url = "https://www.amazon.co.uk/"

    run_agentic_test(test_goal, test_url)
