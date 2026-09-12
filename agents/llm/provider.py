import json, os
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMResult:
    content: str; provider: str; model: str; input_tokens: int=0; output_tokens: int=0; estimated_cost_usd: float=0.0

class LLMProvider:
    def generate(self, system: str, user: str, temperature: float=.7) -> LLMResult: raise NotImplementedError

class MockLLMProvider(LLMProvider):
    def generate(self, system, user, temperature=.7):
        return LLMResult(json.dumps({"hook":"Stop doing this manually.","problem":"Repetitive work slows creators down.","value":"Use one repeatable workflow to turn an idea into multiple assets.","proof_or_example":"Build the workflow once, then reuse it for every content batch.","cta":"Follow for practical AI automation workflows.","caption":"A simple workflow can turn one idea into an entire content system.","hashtags":["#ai","#automation","#contentcreator","#socialcommerce"],"disclosure":None}),"mock","mock-v1",0,45)

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str]=None, model: Optional[str]=None): self.api_key=api_key or os.getenv("OPENAI_API_KEY"); self.model=model or os.getenv("OPENAI_MODEL","gpt-5.6-mini")
    def generate(self, system, user, temperature=.7):
        if not self.api_key: raise RuntimeError("OPENAI_API_KEY is not configured")
        from openai import OpenAI
        response=OpenAI(api_key=self.api_key).responses.create(model=self.model,instructions=system,input=user,temperature=temperature)
        usage=getattr(response,"usage",None)
        return LLMResult(response.output_text,"openai",self.model,getattr(usage,"input_tokens",0) or 0,getattr(usage,"output_tokens",0) or 0)

def build_provider(): return OpenAIProvider() if os.getenv("LLM_PROVIDER","mock").lower()=="openai" else MockLLMProvider()
