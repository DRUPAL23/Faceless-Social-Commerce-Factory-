import random
from dataclasses import dataclass, asdict
from typing import List

PILLARS = [
    ("Educational", 1.00), ("Tools/Products", .95), ("Problem/Solution", .92),
    ("Opportunity", .88), ("Storytelling", .80), ("Trend", .86)
]

TEMPLATES = {
    "Educational": ["5 things {audience} should know about {topic}", "The beginner's guide to {topic}", "3 mistakes people make with {topic}"],
    "Tools/Products": ["3 tools that simplify {topic}", "The AI workflow I would build for {topic}", "One tool that saves time on {topic}"],
    "Problem/Solution": ["If {audience} struggle with {topic}, try this", "Why your {topic} workflow is failing", "Turn this {topic} problem into a system"],
    "Opportunity": ["A practical opportunity around {topic}", "How creators can monetize {topic}", "A simple business model built around {topic}"],
    "Storytelling": ["The hidden lesson behind {topic}", "From manual work to a {topic} system", "The 30-day experiment: {topic}"],
    "Trend": ["What's changing in {topic} right now", "The trend reshaping {topic}", "Why {topic} is getting attention"]
}
SUBTOPICS = ["content creation", "automation", "AI tools", "customer acquisition", "social commerce", "productivity", "lead generation", "digital products", "affiliate marketing", "analytics", "workflow design", "creator monetization"]

@dataclass
class Idea:
    title: str; pillar: str; hook: str; pain_point: str; value_proposition: str; cta: str; monetization: str
    viral_score: float; audience_fit: float; save_score: float; share_score: float; commercial_intent: float
    novelty: float; production_score: float; total_score: float

class ContentDirector:
    def generate_candidates(self, niche: str, audience: str, count: int, seed: int = 42) -> List[dict]:
        rng = random.Random(seed); ideas=[]; seen=set()
        for i in range(count*4):
            pillar, weight=PILLARS[i % len(PILLARS)]; topic=rng.choice(SUBTOPICS)
            title=rng.choice(TEMPLATES[pillar]).format(audience=audience, topic=topic)
            if title.lower() in seen: continue
            seen.add(title.lower())
            viral=rng.uniform(65,98); fit=rng.uniform(75,99)*weight; save=rng.uniform(60,96); share=rng.uniform(55,94)
            commercial=rng.uniform(55,96) if pillar in ("Tools/Products","Opportunity") else rng.uniform(35,82)
            novelty=rng.uniform(55,95); production=rng.uniform(70,98)
            total=viral*.30+fit*.20+save*.15+share*.15+commercial*.10+novelty*.05+production*.05
            ideas.append(asdict(Idea(title,pillar,self._hook(pillar),f"{audience} want a simpler, faster way to handle {topic}.",f"Show one practical workflow, example, or tool for {topic}.","Follow for practical AI and social-commerce workflows.","Relevant affiliate tool or owned digital product" if pillar in ("Tools/Products","Opportunity") else "Audience growth / lead capture",*(round(x,2) for x in [viral,fit,save,share,commercial,novelty,production,total])))
            if len(ideas)>=count: break
        return sorted(ideas,key=lambda x:x["total_score"],reverse=True)

    def select_top(self, ideas: List[dict], count: int) -> List[dict]:
        chosen=[]; used={}; cap=max(1,count//10)
        for idea in sorted(ideas,key=lambda x:x["total_score"],reverse=True):
            p=idea["pillar"]
            if used.get(p,0)<cap: chosen.append(idea); used[p]=used.get(p,0)+1
            if len(chosen)>=count: break
        if len(chosen)<count: chosen += [x for x in sorted(ideas,key=lambda x:x["total_score"],reverse=True) if x not in chosen][:count-len(chosen)]
        return chosen[:count]

    @staticmethod
    def _hook(pillar):
        return {"Educational":"Save this before you build your next workflow.","Tools/Products":"These tools can remove hours of repetitive work.","Problem/Solution":"Change the system—not the effort.","Opportunity":"Here's a practical opportunity worth testing.","Storytelling":"Here's the lesson most people miss.","Trend":"This shift could change how creators work."}[pillar]
