import anthropic
import re
from claude import CLAUDE_MODEL, MAX_TOKENS, TEMPERATURE, MATCH_PATTERN


class ClaudeAPIIntegration:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)

    def send_prompt(self, prompt):
        message = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        return self.extract_text_from_response(message.content)

    @staticmethod
    def extract_text_from_response(response):
        match = re.search(MATCH_PATTERN, str(response), re.DOTALL)
        if match:
            text = match.group(1).strip('"').replace('\\"', '"')
            text = re.sub(r'```\w*\n?|```', '', text)
            text = re.sub(r'`([^`\n]+)`', r'\1', text)
            return text.replace('\\n', '\n').strip("'").strip()
        return ""