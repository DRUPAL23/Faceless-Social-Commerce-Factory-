import json, time
from .provider import build_provider

SYSTEM='''You are an expert social-commerce Reel copywriter. Return ONLY valid JSON with keys: hook, problem, value, proof_or_example, cta, caption, hashtags, disclosure. Be concise, factual and useful. Never invent testimonials, guaranteed earnings, fake statistics or unsupported claims.'''

class AIScriptService:
    def __init__(self): self.provider=build_provider()
    def generate(self, idea, brand="Faceless Content Factory", retries=2):
        user=json.dumps({"brand":brand,"idea":idea},ensure_ascii=False); last=None
        for attempt in range(retries+1):
            try:
                result=self.provider.generate(SYSTEM,user); data=json.loads(result.content); self._validate(data); return data,result
            except Exception as exc:
                last=exc
                if attempt<retries: time.sleep(.25*(attempt+1))
        raise RuntimeError(f"LLM generation failed after retries: {last}")
    @staticmethod
    def _validate(data):
        required=["hook","problem","value","proof_or_example","cta","caption","hashtags","disclosure"]
        missing=[k for k in required if k not in data]
        if missing: raise ValueError(f"Missing structured fields: {missing}")
        if not isinstance(data["hashtags"],list): raise ValueError("hashtags must be an array")
