import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
import google.auth
import json
from typing import Union
import os

print("Current working directory:", os.getcwd())
print("Looking for prompts.json at:", os.path.abspath("prompts.json"))


class Gemini:
    def __init__(self, project_id, location="us-central1", model_name="gemini-2.5-flash"):
        """Initialize the Gemini model client."""
        self.project_id = project_id
        self.location = location
        self.model_name = model_name
        self.chat = None
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel(self.model_name)
        print(f"Initialized Gemini model: {model_name}")

    def start_chat(self, **kwargs):
        self.chat = self.model.start_chat(**kwargs)
        print("Chat session started.")

    def call(self, prompt, **kwargs):
        try:
            if self.chat:
                response = self.chat.send_message(prompt, **kwargs)
            else:
                response = self.model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")


    def process_prompts_from_json(self, input_json_path: str, output_json_path: str, use_chat: bool = True):
        """Load prompts from JSON, run them, and save responses to another JSON file."""
        try:
            with open(input_json_path, 'r') as infile:
                data = json.load(infile)

            # accepts either a list of prompts or a dict {label: prompt}
            if isinstance(data, list):
                prompts = {f"prompt_{i+1}": prompt for i, prompt in enumerate(data)}
            elif isinstance(data, dict):
                prompts = data
            else:
                raise ValueError("JSON must be a list of prompts or a dictionary of key-prompt pairs.")

            responses = {}

            if use_chat:
                self.start_chat()

            for label, prompt in prompts.items():
                print(f"Running prompt: {label}")
                response_text = self.call(prompt)
                responses[label] = {
                    "prompt": prompt,
                    "response": response_text
                }

            with open(output_json_path, 'w') as outfile:
                json.dump(responses, outfile, indent=2)

            print(f"Saved responses to {output_json_path}")

        except Exception as e:
            raise RuntimeError(f"Error processing prompts from JSON: {e}")

"""
project_id must correspond to an existing google colab project id, otherwise default credentials will not be found.
To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc for more information.
"""

if __name__ == "__main__":
    project_id = #############
    location = 'us-central1'
    model_name = 'gemini-2.5-flash-preview-04-17'

    gemini = Gemini(project_id, location, model_name)

    input_file = "prompts.json"
    output_file = "responses.json"

    gemini.start_chat()

    #print(gemini.call('I previously sent this message:  I''m using the CLI version to contact you, are there any interesting features I can use to enhance my communication with you?'))

    #this will only handle the inputs in prompts.json, if desired, could expand with a for loop for items in ./prompts+responses
    gemini.process_prompts_from_json(input_file, output_file, use_chat=True)



"""Big ugly testing block below.  Don't worry about it."""
# gemini.call('Hello Gemini, is everything okay? This is a test for temperature parameter.',
#             generation_config={'temperature': 0.7})
#
# gemini.call('Hello Gemini, is everything okay? This is a test for top_p parameter.',
#             generation_config={'top_p': 0.8})
#
# gemini.start_chat(response_validation=False)  # incomplete response will trigger an error, it is normal and relax
# gemini.call('Hello Gemini, is everything okay? This is a test for max length parameter.',
#             generation_config={'max_output_tokens': 1024})
#
# your_prompt = """Classify the text into neutral, negative or positive.
# Text: I think the vacation is okay.
# Sentiment:"""
# gemini.start_chat()
# gemini.call(your_prompt)
#
# your_prompt = """This is awesome! // Negative
# This is bad! // Positive
# Wow that movie was rad! // Positive
# What a horrible show! //"""
# gemini.start_chat()
# gemini.call(your_prompt)
#
# your_prompt = """I went to the market and bought 10 apples. I gave 2 apples to the neighbor and 2 to the repairman. I then went and bought 5 more apples and ate 1. How many apples did I remain with?
# Let's think step by step."""
# gemini.call(your_prompt)

