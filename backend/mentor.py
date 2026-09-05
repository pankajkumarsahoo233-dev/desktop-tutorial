import json, os, urllib.request, urllib.error

def demo(action, p, q):
    if action == "ideas":
        return {"mode":"demo","ideas":[
            {"title":"Skill2Project AI","problem":"Students struggle to choose feasible capstone topics.","solution":"Map skills, interests and constraints to ranked project ideas.","ai":"Skill-to-project matching","mvp":"Profile, ranking, tech stack, roadmap"},
            {"title":"CampusCare AI","problem":"Students struggle to find the right campus resources.","solution":"AI assistant that understands requests and recommends relevant resources.","ai":"Intent detection and recommendations","mvp":"Chat, recommendations, resource cards, feedback"},
            {"title":"FinSight Student","problem":"Financial concepts can be difficult for students to understand.","solution":"AI tutor that explains scenarios and creates simple action plans.","ai":"Personalized explanations","mvp":"Scenario input, explanation, action plan, progress"}],
                "next":"Pick one idea, then generate its stack and roadmap."}
    if action == "stack":
        return {"mode":"demo","stack":{"Frontend":"Streamlit","Backend":"FastAPI","AI":"Gemini API","Database":"PostgreSQL","Vector DB":"Chroma (optional)","Deployment":"Render"},"why":"Fast Python-friendly MVP stack with clear separation between UI and AI API."}
    return {"mode":"demo","answer":f"For {p.get('domain','AI/ML')} using {p.get('skills','Python')}, build one measurable MVP first. Milestones: validate problem -> data/API -> AI core -> UI -> testing -> deployment."}

def gemini(prompt):
    key=os.getenv("GEMINI_API_KEY")
    if not key: return None
    model=os.getenv("GEMINI_MODEL","gemini-2.5-flash")
    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body=json.dumps({"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"temperature":0.7}}).encode()
    try:
        req=urllib.request.Request(url,data=body,headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=60) as r: data=json.loads(r.read())
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None

def generate(action, profile, question=""):
    prompt=f'''You are an expert final-year capstone mentor. Challenge: AI Project Idea Generator & Mentor for Final-Year Projects.
Student profile: {json.dumps(profile)}
Action: {action}
Question: {question}
Give practical, semester-feasible, industry-relevant advice. Avoid cliché ideas.
For ideas: give 3 ranked ideas with problem, target users, solution, AI role, novelty, MVP features and 6-week milestones.
For stack: recommend frontend, backend, AI, database, optional vector search and deployment with reasons.
For mentor: answer the question and give concrete next steps. Return Markdown.'''
    result=gemini(prompt)
    return {"mode":"gemini","answer":result} if result else demo(action,profile,question)
