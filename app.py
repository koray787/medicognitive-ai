import os
from typing import List, Dict

import requests
import streamlit as st

st.set_page_config(
    page_title="MO DARK AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --bg:#080b12; --panel:#101522; --line:#202a3a; --text:#edf2ff; --muted:#8793aa; --accent:#8b5cf6; --cyan:#22d3ee; }
.stApp { background: radial-gradient(circle at 75% -10%, #1d1642 0, transparent 35%), var(--bg); color:var(--text); font-family:'Cairo', sans-serif; }
.block-container { max-width: 1400px; padding-top: 2rem; }
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0d111b,#090c13); border-left:1px solid var(--line); }
[data-testid="stSidebar"] * { font-family:'Cairo',sans-serif; }
.hero { padding: 1.4rem 0 1rem; }
.brand { font-family:'Space Grotesk',sans-serif; font-size: clamp(2.3rem,5vw,4.8rem); letter-spacing:-.08em; line-height:1; font-weight:700; background:linear-gradient(90deg,#fff,#b9a1ff 48%,#22d3ee); -webkit-background-clip:text; color:transparent; }
.tagline { color:#a6b2ca; font-size:1.05rem; margin-top:.65rem; }
.badge { display:inline-block; padding:.25rem .7rem; border:1px solid #4d3f8e; border-radius:999px; color:#c7bbff; background:#181334; font-size:.78rem; margin-bottom:.8rem; }
.panel { background:rgba(16,21,34,.78); border:1px solid var(--line); border-radius:20px; padding:1.2rem; box-shadow:0 12px 40px #0002; }
.metric { border:1px solid var(--line); border-radius:14px; padding:.8rem; background:#0b101a; }
.metric b { display:block; color:#fff; font-size:1.1rem; }
.metric span { color:var(--muted); font-size:.78rem; }
[data-testid="stChatMessage"] { border:1px solid var(--line); border-radius:18px; padding:.8rem 1rem; background:#0e1420; }
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { background:#17142b; border-color:#3a2d6a; }
.stButton > button { border-radius:12px; border:1px solid #303b51; background:#141b2a; color:#e9edff; font-weight:600; }
.stButton > button:hover { border-color:var(--accent); color:#fff; }
.stTextArea textarea, .stTextInput input { background:#0b101a!important; border:1px solid #2a3548!important; color:#eef2ff!important; border-radius:12px!important; }
small, .muted { color:var(--muted); }
hr { border-color:var(--line); }
</style>
""", unsafe_allow_html=True)

# ---------- State ----------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "attached_context" not in st.session_state:
    st.session_state.attached_context = ""

# ---------- Helpers ----------
def secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, os.getenv(name, default))
    except Exception:
        return os.getenv(name, default)


def extract_file(uploaded) -> str:
    if not uploaded:
        return ""
    name = uploaded.name.lower()
    raw = uploaded.getvalue()
    if name.endswith((".txt", ".md", ".csv", ".json", ".py", ".js", ".html", ".css")):
        return raw.decode("utf-8", errors="ignore")[:120000]
    return f"[ملف مرفوع: {uploaded.name} — هذا النوع يحتاج معالجة خارجية قبل قراءته]"


def call_model(messages: List[Dict[str, str]], provider: str, model: str, api_key: str, base_url: str, temperature: float, max_tokens: int, code_mode: bool):
    if not api_key:
        raise ValueError("أضف مفتاح API في الشريط الجانبي أو في Secrets قبل الإرسال.")
    url = base_url.rstrip("/") + "/chat/completions"
    code_instruction = """عند طلب كود طويل: قدّم حلاً كاملاً قابلاً للتشغيل، لا تختصر الملفات ولا تضع عبارات مثل 'أكمل بنفس النمط'. قسّم الناتج إلى ملفات واضحة، واذكر إن وصل حد الإخراج وكيفية المتابعة.""" if code_mode else ""
    system = {
        "role": "system",
        "content": "أنت MO DARK AI، مساعد عربي متقدم متعدد المهارات. كن مباشراً وذكياً وعملياً. أجب بلغة المستخدم، ونظّم الإجابات بعناوين وقوائم عند الحاجة. افصل الحقائق عن التخمين، ولا تدّعِ تنفيذ أفعال لم تنفذها. احترم الخصوصية والقانون والسلامة؛ لا تساعد على أذى حقيقي أو اختراق أو احتيال، لكن قدّم بديلاً تعليمياً ودفاعياً مفيداً عند الرفض. " + code_instruction
    }
    payload = {"model": model, "messages": [system] + messages, "temperature": temperature, "max_tokens": max_tokens, "stream": False}
    r = requests.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=120)
    if r.status_code >= 400:
        try: detail = r.json().get("error", {}).get("message", r.text)
        except Exception: detail = r.text
        raise RuntimeError(f"{provider}: {detail}")
    data = r.json()
    return data["choices"][0]["message"]["content"]

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## ◈ MO DARK AI")
    st.caption("مركز قيادة ذكاء اصطناعي شخصي")
    st.divider()
    provider = st.selectbox("مزود النموذج", ["OpenRouter", "Groq", "OpenAI-compatible"], index=0)
    defaults = {
        "OpenRouter": ("https://openrouter.ai/api/v1", "openai/gpt-oss-20b:free"),
        "Groq": ("https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"),
        "OpenAI-compatible": ("https://api.openai.com/v1", "gpt-4o-mini"),
    }
    default_url, default_model = defaults[provider]
    api_key = st.text_input("مفتاح API", value=secret("OPENAI_API_KEY"), type="password", help="لا تضع المفتاح داخل GitHub. استخدم Streamlit Secrets.")
    base_url = st.text_input("Base URL", value=secret("BASE_URL", default_url))
    model = st.text_input("النموذج", value=secret("MODEL", default_model))
    temperature = st.slider("الإبداع", 0.0, 1.5, 0.7, 0.1)
    code_mode = st.checkbox("وضع الكود الطويل", value=True, help="يرفع حد الإخراج ويطلب ملفات كاملة، لكن الحد الفعلي يحدده النموذج المجاني.")
    max_tokens = st.slider("حد الإخراج", 2048, 32768, 16384, 1024)
    st.divider()
    mode = st.selectbox("الوضع", ["محادثة خارقة", "مبرمج", "باحث ومحلل", "كاتب إبداعي", "مخطط مشاريع"])
    if mode == "مبرمج":
        st.session_state.mode_hint = "ركّز على كود قابل للتشغيل، اشرح الأخطاء، واذكر الملفات والخطوات."
    elif mode == "باحث ومحلل":
        st.session_state.mode_hint = "حلّل بعمق، افصل الحقائق عن الافتراضات، واقترح مصادر أو طرق تحقق."
    elif mode == "كاتب إبداعي":
        st.session_state.mode_hint = "اكتب بأسلوب أصلي ومؤثر، مع الحفاظ على وضوح الهدف والجمهور."
    elif mode == "مخطط مشاريع":
        st.session_state.mode_hint = "حوّل الفكرة إلى مراحل ومهام وأولويات ومخاطر ومخرجات واضحة."
    else:
        st.session_state.mode_hint = "كن مساعداً متعدد الاستخدامات ومتقدم التفكير."
    uploaded = st.file_uploader("أرفق ملفاً نصياً", type=["txt","md","csv","json","py","js","html","css"])
    if uploaded:
        st.session_state.attached_context = extract_file(uploaded)
        st.success(f"تم إرفاق {uploaded.name}")
    if st.button("مسح المحادثة", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("النشر المجاني: GitHub + Streamlit Community Cloud")

# ---------- Main ----------
st.markdown('<div class="hero"><span class="badge">PRIVATE INTELLIGENCE CONSOLE · v1.0</span><div class="brand">MO DARK AI</div><div class="tagline">ذكاء اصطناعي شخصي، مرن، ومتعدد الأوضاع — في واجهة واحدة.</div></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
for col, title, value in [(c1,"الحالة","ONLINE"),(c2,"الوضع",mode),(c3,"المرفق","جاهز" if st.session_state.attached_context else "لا يوجد"),(c4,"المحرك",provider)]:
    with col:
        st.markdown(f'<div class="metric"><span>{title}</span><b>{value}</b></div>', unsafe_allow_html=True)
st.write("")

if not st.session_state.messages:
    st.markdown('<div class="panel"><h3>ابدأ من هنا</h3><p class="muted">اطلب منه بناء مشروع، تحليل ملف، كتابة كود، توليد خطة، أو تطوير فكرة. كل ما تحتاجه هو مفتاح مزود نموذج في Secrets.</p></div>', unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="◈" if msg["role"] == "assistant" else "●"):
        st.markdown(msg["content"])

prompt = st.chat_input("اكتب أمرك إلى MO DARK AI…")
if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt})
    with st.chat_message("user", avatar="●"):
        st.markdown(prompt)
    context = st.session_state.attached_context
    enhanced = f"الوضع الحالي: {mode}. تعليمات الوضع: {st.session_state.mode_hint}\n"
    if context:
        enhanced += f"\nمحتوى الملف المرفق (استخدمه كسياق):\n{context}\n"
    api_messages = [{"role":"system", "content": enhanced}] + st.session_state.messages
    with st.chat_message("assistant", avatar="◈"):
        with st.spinner("MO DARK AI يفكر…"):
            try:
                answer = call_model(api_messages, provider, model, api_key, base_url, temperature, max_tokens, code_mode)
                st.markdown(answer)
                st.session_state.messages.append({"role":"assistant", "content":answer})
            except Exception as e:
                st.error(str(e))
                st.info("للنشر المجاني استخدم مفتاحاً من OpenRouter أو Groq، ثم ضعه في Streamlit Cloud → Settings → Secrets.")

