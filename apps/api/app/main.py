from datetime import date,timedelta
from typing import Optional
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from agents.content_director.engine import ContentDirector
from agents.llm.script_service import AIScriptService

app=FastAPI(title="Faceless Social Commerce Factory API",version="0.4.0")
director=ContentDirector(); writer=AIScriptService()

class IdeaRequest(BaseModel): niche:str; audience:str; candidates:int=Field(120,ge=30,le=300); seed:Optional[int]=42
class CalendarRequest(BaseModel): niche:str; audience:str; days:int=Field(30,ge=1,le=90); reels_per_day:int=Field(3,ge=1,le=10); candidates:int=Field(120,ge=30,le=300); seed:Optional[int]=42
class ScriptRequest(BaseModel): idea:dict; brand:str="Faceless Content Factory"

@app.get('/health')
def health(): return {'status':'ok','sprint':'4','service':'ai-script-engine'}

@app.post('/ideas')
def ideas(r:IdeaRequest):
    x=director.generate_candidates(r.niche,r.audience,r.candidates,r.seed); return {'total':len(x),'ideas':x}

@app.post('/scripts')
def scripts(r:ScriptRequest):
    if not r.idea.get('title'): raise HTTPException(422,'idea.title is required')
    data,meta=writer.generate(r.idea,r.brand); return {'copy':data,'generation':meta.__dict__}

@app.post('/calendar')
def calendar(r:CalendarRequest):
    total=r.days*r.reels_per_day; ideas=director.generate_candidates(r.niche,r.audience,max(r.candidates,total),r.seed); selected=director.select_top(ideas,total); rows=[]
    for i,idea in enumerate(selected):
        copy,meta=writer.generate(idea); rows.append({'day':i//r.reels_per_day+1,'date':str(date.today()+timedelta(days=i//r.reels_per_day)),'slot':i%r.reels_per_day+1,**idea,'copy':copy,'generation':meta.__dict__,'status':'SCRIPTED'})
    return {'total':len(rows),'candidates_generated':len(ideas),'calendar':rows}
