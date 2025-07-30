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

       "You are a Python Selenium expert.\n\n"
    "Write a complete Page Object Model (POM)-based Selenium test in Python.\n\n"
    f"Test Goal: {description}\n"
    f"Target URL: {url}\n\n"
    "Requirements:\n"
    "- Follow Page Object Model (POM) design pattern\n"
    "- Create at least two classes: one for the Page Object, and one for the Test Case\n"
    "- Use Chrome WebDriver (assume chromedriver is already installed and added to system PATH)\n"
    "- Do NOT use webdriver_manager or any external dependency managers\n"
    "- Use 5 seconds wait time for page loads after login\n"
    "- Use explicit waits (WebDriverWait) to find elements and verify successful login by waiting for the shopping cart container to be visible\n"
    "- In addition to verifying login, extract and print all inventory item names along with their prices after successful login\n"
    "- Do NOT run Chrome in headless mode; the browser should be visible when the test runs\n"
    "- Use the latest Selenium syntax with 'By' and 'WebDriverWait'\n"
    "- Include all necessary imports\n"
    "- Use repr() or str() for debug output if needed (no backticks)\n"
    "- Return only valid Python code, no markdown or explanations\n"

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

    test_goal = "Verify that entering a valid username and password on https://www.saucedemo.com/ and clicking the login button successfully navigates to the products page."
    test_url = "https://www.saucedemo.com/"


    run_agentic_test(test_goal, test_url)
