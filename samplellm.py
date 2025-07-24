import os
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load a local code generation model (you can replace with GPT-style model if available)
model_name = "Salesforce/codegen-350M-mono"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float32)

# Prompt engineering helper
def build_prompt(user_instruction: str) -> str:
    base = f"""# Task: {user_instruction}

# Write a simple code using Selenium that:
# - Opens Chrome
# - Navigates to a website
# - Waits 5 seconds
# - Closes the browser

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Start your code below:
"""
    return base

# Code execution function
def run_generated_code(code: str):
    with open("generated_task.py", "w") as f:
        f.write(code)
    try:
        subprocess.run(["python", "generated_task.py"], check=True)
    except subprocess.CalledProcessError as e:
        print("⚠ Error while executing generated code:", e)

# AI agent loop
def run_agent_loop():
    print("\n🤖 AI Agent is ready! Type 'exit' to stop.")
    while True:
        user_cmd = input("\n💬 Your Command: ").strip()
        if user_cmd.lower() in ["exit", "quit"]:
            print("👋 Exiting agent. Goodbye!")
            break

        # Build and send prompt
        prompt = build_prompt(user_cmd)
        inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(
            inputs.input_ids,
            max_length=512,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=False
        )
        code = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Show generated code
        print("\n🧠 Generated Code:\n" + "-" * 50)
        print(code)
        print("-" * 50)

        confirm = input("⚙  Do you want to run this code? (y/n): ").strip().lower()
        if confirm == "y":
            run_generated_code(code)
        else:
            print("⏩ Skipping execution.")

if __name__ == "__main__":
    run_agent_loop()