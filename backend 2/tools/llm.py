import os
import json
import httpx
import re
from typing import Optional


LLMProvider = str | None


def parse_json_response(text: str) -> dict:
    """Extract and parse JSON from LLM response."""
    try:
        # Try direct parse
        return json.loads(text)
    except json.JSONDecodeError:
        # Find JSON block
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Look for markdown block
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
                
    return {}


def get_llm_client(provider: Optional[str] = None) -> "BaseLLMClient":
    if provider is None:
        provider = os.getenv("LLM_PROVIDER", "openrouter")
    
    provider = provider.lower()
    
    if provider == "anthropic":
        return AnthropicClient()
    elif provider == "openrouter":
        return OpenRouterClient()
    elif provider == "blackbox":
        return BlackboxClient()
    else:
        return OpenRouterClient()


class BaseLLMClient:
    def chat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        raise NotImplementedError

    async def achat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        raise NotImplementedError


class AnthropicClient(BaseLLMClient):
    def __init__(self):
        self._client = None
        self._async_client = None
        self._api_key = os.getenv("ANTHROPIC_API_KEY")
        self._model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    
    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import Anthropic
                if self._api_key:
                    self._client = Anthropic(api_key=self._api_key)
            except ImportError:
                pass
        return self._client

    def _get_async_client(self):
        if self._async_client is None:
            try:
                from anthropic import AsyncAnthropic
                if self._api_key:
                    self._async_client = AsyncAnthropic(api_key=self._api_key)
            except ImportError:
                pass
        return self._async_client
    
    def chat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        client = self._get_client()
        
        if client:
            try:
                response = client.messages.create(
                    model=self._model,
                    max_tokens=kwargs.get("max_tokens", 500),
                    temperature=kwargs.get("temperature", 0.3),
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text.strip()
            except Exception as e:
                raise e
        
        raise ValueError("Anthropic client not initialized")

    async def achat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        client = self._get_async_client()
        
        if client:
            try:
                response = await client.messages.create(
                    model=self._model,
                    max_tokens=kwargs.get("max_tokens", 500),
                    temperature=kwargs.get("temperature", 0.3),
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text.strip()
            except Exception as e:
                raise e
        
        raise ValueError("Anthropic async client not initialized")


class OpenRouterClient(BaseLLMClient):
    def __init__(self):
        self._api_key = os.getenv("OPENROUTER_API_KEY")
        self._base_url = "https://openrouter.ai/api/v1"
        self._model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        self._site_url = os.getenv("OPENROUTER_SITE_URL", "https://travel-planner.example.com")
        self._site_name = os.getenv("OPENROUTER_SITE_NAME", "Travel Planner")
    
    def _get_headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self._site_url,
            "X-Title": self._site_name,
        }
        return headers

    def _prepare_payload(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> dict:
        payload = {
            "model": self._model,
            "messages": messages.copy(),
        }
        
        # Explicitly disable reasoning if it's a Nemotron model and hitting limits
        if "nemotron" in self._model.lower():
            payload["include_reasoning"] = False

        final_system_prompt = system_prompt or ""
        # Add hint to skip reasoning if the model tends to over-reason and hit limits
        if "nemotron" in self._model.lower():
            reasoning_hint = "\nIMPORTANT: Provide the response immediately in the requested JSON format. DO NOT provide lengthy internal thought or reasoning."
            final_system_prompt += reasoning_hint

        if final_system_prompt:
            payload["messages"].insert(0, {
                "role": "system",
                "content": final_system_prompt
            })
        
        if "max_tokens" in kwargs:
            payload["max_tokens"] = kwargs["max_tokens"]
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]
        
        return payload
    
    def chat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        if not self._api_key:
            raise ValueError("OpenRouter API key not configured")
        
        payload = self._prepare_payload(messages, system_prompt, **kwargs)
        
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{self._base_url}/chat/completions",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def achat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        if not self._api_key:
            raise ValueError("OpenRouter API key not configured")
        
        # Increase max_tokens significantly if not specified, 
        # as reasoning models use them for the reasoning phase too.
        if "max_tokens" not in kwargs:
            kwargs["max_tokens"] = 4000
            
        payload = self._prepare_payload(messages, system_prompt, **kwargs)
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self._base_url}/chat/completions",
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            if not data or "choices" not in data or not data["choices"]:
                raise ValueError(f"OpenRouter returned an empty or invalid response: {data}")
                
            choice = data["choices"][0]
            message = choice.get("message", {})
            content = message.get("content")
            
            if content is None:
                # Check for reasoning field (used by some providers via OpenRouter)
                reasoning = message.get("reasoning")
                if reasoning:
                    if choice.get("finish_reason") == "length":
                         raise ValueError(f"Model hit token limit during reasoning. Increase max_tokens. Partial Reasoning: {reasoning[:200]}...")
                    # If there's NO content but there IS reasoning, 
                    # it might be the model just finished without outputting the final JSON.
                    raise ValueError(f"Model finished reasoning but produced no content output. Reasoning: {reasoning[:500]}...")
                
                raise ValueError(f"OpenRouter returned a null content: {data}")
                
            return content


class BlackboxClient(BaseLLMClient):
    def __init__(self):
        self._api_key = os.getenv("BLACKBOX_API_KEY")
        self._base_url = "https://api.blackbox.ai/chat/completions"
        self._model = os.getenv("BLACKBOX_MODEL", "gpt-4")
    
    def _get_headers(self) -> dict:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        return headers

    def _prepare_payload(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> dict:
        final_messages = messages.copy()
        if system_prompt:
            final_messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })
            
        payload = {
            "model": self._model,
            "messages": final_messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 500),
            "stream": False
        }
        return payload

    async def achat(self, messages: list[dict], system_prompt: Optional[str] = None, **kwargs) -> str:
        if not self._api_key:
            raise ValueError("Blackbox API key not configured")
            
        payload = self._prepare_payload(messages, system_prompt, **kwargs)
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self._base_url,
                headers=self._get_headers(),
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            
            if not data or "choices" not in data or not data["choices"]:
                raise ValueError(f"Blackbox returned an empty or invalid response: {data}")
                
            content = data["choices"][0]["message"].get("content")
            if content is None:
                raise ValueError(f"Blackbox returned a null content: {data}")
                
            return content


async def aget_llm_client(provider: Optional[str] = None) -> BaseLLMClient:
    return get_llm_client(provider)
