

class ClaudeAPIIntegration:
    def __init__(self, api_key):
        print("Initializing Claude API...")
        self.client = anthropic.Anthropic(api_key=api_key)  # Initialize the Anthropic client with the provided API key
        print("Claude API initialized.")

    def send_prompt(self, prompt):
        print("Sending prompt to Claude API...", prompt)
        message = self.client.messages.create(
            model=CLAUDE_MODEL,  # Use the specified Claude model
            max_tokens=MAX_TOKENS,  # Set the maximum number of tokens for the response
            temperature=TEMPERATURE,  # Set the temperature for response generation
            messages=[
                {"role": "user", "content": prompt}  # Create a message with the user's prompt
            ]
        )
        response = self.extract_text_from_response(message.content)  # Extract the text from Claude's response
        print(f"Received response from Claude API: {response}...")
        return response

    @staticmethod
    def extract_text_from_response(response):
        print("Extracting text from Claude API response...")
        match = re.search(r"TextBlock\(text=(.*?), type='text'\)", str(response), re.DOTALL)  # Search for the text content in the response
        if match:
            text = match.group(1).strip('"').replace('\\"', '"')  # Extract and clean the text
            text = re.sub(r'```\w*\n?|```', '', text)  # Remove code block markers
            text = re.sub(r'`([^`\n]+)`', r'\1', text)  # Remove inline code markers
            text = text.replace('\\n', '\n')  # Replace escaped newlines with actual newlines
            return text.strip("'").strip()  # Remove any leading/trailing quotes and whitespace
        print("No text block found in response.")
        return ""