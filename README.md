# selenium-agentic-llm
An agentic AI system using a local LLM (CodeGen) to generate and run Selenium-based browser automation scripts with context-aware memory.
AI Code Agent with Selenium Task Execution
This project provides a simple AI agent loop that uses a code generation model (Salesforce/codegen-350M-mono) to generate Python Selenium scripts based on natural language instructions and optionally executes them.

📦 Features
Uses Hugging Face Transformers to load a code generation model.

Accepts natural language instructions to generate code.

Generates Python scripts for web automation using Selenium.

Optionally executes the generated code and displays results.

Interactive command-line interface.

🛠️ Requirements
Before running the project, ensure the following Python packages are installed:

bash
Copy
Edit
pip install torch transformers selenium
You also need:

Python 3.7+

Chrome browser installed

ChromeDriver in your system PATH (compatible with your Chrome version)

🚀 How to Run
Clone or save the script locally.

Run the script:

bash
Copy
Edit
python your_script_name.py
Interact with the AI Agent:

text
Copy
Edit
💬 Your Command: open google and search something
The AI will generate a Python script using Selenium that performs the described task.

Execute the generated script when prompted:

text
Copy
Edit
⚙  Do you want to run this code? (y/n): y
🧪 Example Instruction
text
Copy
Edit
💬 Your Command: visit example.com and wait 5 seconds
Example output:

python
Copy
Edit
# Task: visit example.com and wait 5 seconds
# Write a simple code using Selenium that:
# - Opens Chrome
# - Navigates to a website
# - Waits 5 seconds
# - Closes the browser
...
📂 Files Generated
generated_task.py: the Python script created based on your input and the model's response.

⚠️ Notes
The model may not always generate valid or executable Python code. Review the output before running.

You can stop the agent anytime by typing exit or quit.

Use in a controlled environment, especially when running unknown or newly generated scripts.

📖 Model Used
Salesforce/codegen-350M-mono

This model is designed for code generation and works well with Python prompts.

🧹 To Do
Add error handling for ChromeDriver issues

Improve prompt templating for more flexible tasks

Add support for other languages or frameworks