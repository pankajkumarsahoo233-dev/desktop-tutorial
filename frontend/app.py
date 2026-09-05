import os, json, requests, streamlit as st

st.set_page_config(page_title="ProjectMentor AI", page_icon="🎓", layout="wide")
st.title("🎓 ProjectMentor AI")
st.caption("Turn your skills and interests into a feasible final-year project.")

backend=os.getenv("BACKEND_URL","http://127.0.0.1:8000")
with st.sidebar:
    st.header("Student Profile")
    domain=st.selectbox("Domain",["AI/ML","FinTech","Healthcare","Cybersecurity","EdTech","Data Science","Other"])
    skills=st.text_input("Skills","Python, Machine Learning, SQL")
    interests=st.text_input("Interests","AI automation and real-world problems")
    duration=st.selectbox("Duration",["1 semester","2 semesters"])
    difficulty=st.select_slider("Difficulty",["Beginner","Intermediate","Advanced"],value="Intermediate")
profile={"domain":domain,"skills":skills,"interests":interests,"duration":duration,"difficulty":difficulty}

def call(action, question=""):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        if action == "ideas":
            task = """Generate exactly 3 practical final-year project ideas.
Return ONLY valid JSON:
{
  "ideas": [
    {
      "title": "...",
      "problem": "...",
      "solution": "...",
      "ai": "...",
      "mvp": "..."
    }
  ]
}"""

        elif action == "stack":
            task = """Recommend a practical technology stack for this student.
Return ONLY valid JSON:
{
  "stack": {
    "Frontend": "...",
    "Backend": "...",
    "Database": "...",
    "AI": "...",
    "Deployment": "..."
  },
  "why": "..."
}"""

        else:
            task = f"""You are an expert AI project mentor.
Answer this student question clearly and practically:

{question}

Give useful advice suitable for a final-year student."""

        prompt = f"""
Student profile:
Domain: {domain}
Skills: {skills}
Interests: {interests}
Duration: {duration}
Difficulty: {difficulty}

{task}
"""

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            },
            timeout=120
        )

        response.raise_for_status()

        text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

        if action == "mentor":
            return {"answer": text}

        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)

    except Exception as e:
        st.error(f"AI error: {e}")
        return None

a,b,c=st.tabs(["💡 Idea Generator","🧩 Tech Stack","🤖 AI Mentor"])

with a:
    st.subheader("Generate project ideas")
    if st.button("✨ Generate 3 Ideas",type="primary",use_container_width=True):
        with st.spinner("Analyzing profile..."): x=call("ideas")
        if x:
            if "ideas" in x:
                for i,z in enumerate(x["ideas"],1):
                    with st.container(border=True):
                        st.markdown(f"### {i}. {z['title']}")
                        st.write(z["problem"])
                        st.markdown(f"**Solution:** {z['solution']}")
                        st.markdown(f"**AI role:** {z['ai']}")
                        st.markdown(f"**MVP:** {z['mvp']}")
            else: st.markdown(x.get("answer",str(x)))

with b:
    st.subheader("Recommended technology")
    if st.button("🧩 Recommend My Tech Stack",type="primary",use_container_width=True):
        with st.spinner("Selecting stack..."): x=call("stack")
        if x:
            if "stack" in x:
                cols=st.columns(3)
                for i,(k,v) in enumerate(x["stack"].items()):
                    cols[i%3].metric(k,v)
                st.info(x["why"])
            else: st.markdown(x.get("answer",str(x)))

with c:
    st.subheader("Ask your AI Mentor")
    q=st.text_area("Question",placeholder="How can I make my project innovative and finish it in one semester?",height=130)
    if st.button("🤖 Ask Mentor",type="primary",use_container_width=True) and q.strip():
        with st.spinner("Mentor is thinking..."): x=call("mentor",q)
        if x: st.markdown(x.get("answer",str(x)))
    elif st.button("🤖 Ask Mentor") and not q.strip():
        st.warning("Enter a question first.")

st.divider()
st.caption("Build the core three features first. Add database, semantic search and advanced roadmap visualization only after the demo is stable.")
