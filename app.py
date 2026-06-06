import streamlit as st
import json
import random

st.set_page_config(
    page_title="Ankim-Card & Calc",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_data():
    with open("data/flashcards.json", "r", encoding="utf-8") as f:
        return json.load(f)

def load_materi():
    with open("data/materi.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()
categories = data["categories"]
materi_data = load_materi()
all_materi = materi_data["materi"]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap');
:root {
    --cream:#F5F0E8;--cream2:#EDE6D6;--green:#2D5A3D;--green2:#3D7A52;
    --green3:#4E9A68;--green-lt:#C8DDD1;--brown:#6B4F3A;--brown-lt:#C4A882;
    --text:#2C2416;--text2:#5C4A32;--white:#FEFCF8;
    --shadow:0 4px 20px rgba(45,90,61,0.12);--shadow2:0 8px 32px rgba(45,90,61,0.18);
}
html,body,[class*="css"]{font-family:'Lato',sans-serif;background-color:var(--cream);color:var(--text);}
.stApp{background:linear-gradient(160deg,var(--cream) 0%,var(--cream2) 100%);min-height:100vh;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding-top:2rem;padding-bottom:4rem;max-width:760px;}
h1,h2,h3{font-family:'Playfair Display',serif;color:var(--green);}

/* HERO */
.hero-container{text-align:center;padding:1.5rem 1rem 1.5rem;
  background:linear-gradient(135deg,#1a3d2b 0%,#2D5A3D 55%,#3D7A52 100%);
  border-radius:20px;margin-bottom:1.5rem;box-shadow:0 12px 40px rgba(45,90,61,0.30);
  position:relative;overflow:hidden;}
.hero-container::before{content:'';position:absolute;top:-40px;right:-40px;
  width:200px;height:200px;background:rgba(255,255,255,0.04);border-radius:50%;}
.hero-container::after{content:'';position:absolute;bottom:-60px;left:-30px;
  width:250px;height:250px;background:rgba(255,255,255,0.03);border-radius:50%;}
.hero-icons{display:flex;justify-content:center;align-items:center;gap:0.8rem;
  margin-bottom:0.6rem;position:relative;z-index:1;}
.hero-icon-main{font-size:2.6rem;animation:float 3s ease-in-out infinite;
  filter:drop-shadow(0 4px 8px rgba(0,0,0,0.3));}
.hero-icon-side{font-size:1.6rem;opacity:0.75;animation:float 3s ease-in-out infinite;}
.hero-icon-side:first-child{animation-delay:-1s;}
.hero-icon-side:last-child{animation-delay:-2s;}
@keyframes float{0%,100%{transform:translateY(0px);}50%{transform:translateY(-8px);}}
.hero-title{font-size:clamp(1.4rem,5vw,2.4rem);font-weight:800;font-family:'Playfair Display',serif;
  background:linear-gradient(90deg,#a8e6c0,#ffffff,#a8e6c0);background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  animation:shine 4s linear infinite;margin:0.2rem 0;position:relative;z-index:1;}
@keyframes shine{to{background-position:200% center;}}
.hero-subtitle{font-size:clamp(0.72rem,2.5vw,0.88rem);color:rgba(255,255,255,0.72);margin-top:0.4rem;
  font-style:italic;position:relative;z-index:1;}
.hero-welcome{margin-top:0.9rem;position:relative;z-index:1;
  color:rgba(255,255,255,0.90);font-size:clamp(0.78rem,2.5vw,0.92rem);line-height:1.6;}

/* COMPACT HEADER */
.site-header-compact{text-align:center;padding:1rem 1rem 0.8rem;
  border-bottom:2px solid var(--green-lt);margin-bottom:1.5rem;}
.site-header-compact .logo{font-size:1.5rem;font-family:'Playfair Display',serif;
  color:var(--green);}
.site-header-compact .logo span{color:var(--brown);}

/* CATEGORY CARDS */
.cat-card{background:var(--white);border:1.5px solid var(--green-lt);border-radius:16px;
  padding:1.6rem 1.2rem;text-align:center;box-shadow:var(--shadow);margin-bottom:1rem;}
.cat-card .cat-icon{font-size:2.4rem;margin-bottom:0.6rem;}
.cat-card .cat-name{font-family:'Playfair Display',serif;font-size:1.1rem;color:var(--green);margin-bottom:0.4rem;}
.cat-card .cat-desc{font-size:0.78rem;color:var(--text2);line-height:1.5;margin-bottom:0.6rem;}
.cat-card .cat-count{font-size:0.75rem;color:var(--green3);font-weight:700;margin-bottom:0.8rem;}

/* FLASHCARD */
.flashcard-wrap{perspective:1200px;width:100%;max-width:600px;height:290px;
  margin:1.2rem auto;cursor:pointer;user-select:none;}
.flashcard-inner{position:relative;width:100%;height:100%;transform-style:preserve-3d;
  transition:transform 0.55s cubic-bezier(0.4,0,0.2,1);}
.flashcard-inner.flipped{transform:rotateY(180deg);}
.flashcard-face{position:absolute;width:100%;height:100%;backface-visibility:hidden;
  -webkit-backface-visibility:hidden;border-radius:20px;display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:2rem;box-sizing:border-box;text-align:center;}
.flashcard-front{background:var(--white);border:2px solid var(--green-lt);box-shadow:var(--shadow2);}
.flashcard-back{background:linear-gradient(135deg,var(--green) 0%,var(--green2) 100%);
  border:2px solid var(--green2);box-shadow:var(--shadow2);transform:rotateY(180deg);}
.flashcard-front .fc-label{font-size:0.68rem;font-weight:700;letter-spacing:0.12em;
  text-transform:uppercase;color:var(--brown-lt);margin-bottom:0.8rem;}
.flashcard-front .fc-question{font-family:'Playfair Display',serif;font-size:1.1rem;
  color:var(--text);line-height:1.6;}
.flashcard-front .fc-hint{position:absolute;bottom:1rem;font-size:0.7rem;
  color:var(--brown-lt);font-style:italic;}
.flashcard-back .fc-label{font-size:0.68rem;font-weight:700;letter-spacing:0.12em;
  text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:0.8rem;}
.flashcard-back .fc-answer{font-family:'Playfair Display',serif;font-size:1.2rem;
  color:#FFFFFF;line-height:1.6;font-weight:600;}

/* PROGRESS */
.progress-wrap{margin:0.5rem 0 0.8rem;}
.progress-label{font-size:0.78rem;color:var(--text2);margin-bottom:0.3rem;
  display:flex;justify-content:space-between;}
.progress-bar-bg{background:var(--green-lt);border-radius:50px;height:8px;overflow:hidden;}
.progress-bar-fill{background:linear-gradient(90deg,var(--green2),var(--green3));
  height:100%;border-radius:50px;transition:width 0.4s ease;}

/* BADGES */
.score-badges{display:flex;gap:1rem;justify-content:center;margin:0.4rem 0;}
.badge{padding:0.3rem 1rem;border-radius:50px;font-size:0.8rem;font-weight:700;}
.badge-ingat{background:#D4EDDA;color:#155724;}
.badge-lupa{background:#F8D7DA;color:#721C24;}

/* RESULT */
.result-box{background:var(--white);border:1.5px solid var(--green-lt);border-radius:20px;
  padding:2.5rem 2rem;text-align:center;box-shadow:var(--shadow2);margin-top:1rem;}
.result-box .result-emoji{font-size:4rem;margin-bottom:0.5rem;}
.result-box .result-title{font-family:'Playfair Display',serif;font-size:1.8rem;color:var(--green);}
.result-box .result-score{font-size:3rem;font-weight:700;color:var(--green2);margin:0.5rem 0;}
.result-box .result-sub{font-size:0.9rem;color:var(--text2);}

/* KALKULATOR */
.calc-formula{background:var(--cream2);border-left:4px solid var(--green3);
  border-radius:0 8px 8px 0;padding:0.7rem 1rem;font-size:0.88rem;color:var(--text2);
  margin-bottom:1.2rem;font-family:'Georgia',serif;font-style:italic;}
.result-output{background:linear-gradient(135deg,var(--green) 0%,var(--green2) 100%);
  color:#fff;border-radius:12px;padding:1rem 1.5rem;text-align:center;margin-top:1rem;
  font-family:'Playfair Display',serif;font-size:1.4rem;}
.result-output small{display:block;font-family:'Lato',sans-serif;font-size:0.75rem;
  opacity:0.75;margin-bottom:0.2rem;}

/* ABOUT */
.about-card{background:var(--white);border:1.5px solid var(--green-lt);border-radius:16px;
  padding:1.5rem;box-shadow:var(--shadow);margin-bottom:1rem;}
.about-card .about-title{font-family:'Playfair Display',serif;font-size:1.15rem;
  color:var(--green);margin-bottom:0.8rem;border-bottom:1px solid var(--green-lt);padding-bottom:0.5rem;}
.member-row{display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;
  border-bottom:1px dashed var(--green-lt);}
.member-row:last-child{border-bottom:none;}
.member-num{width:28px;height:28px;background:var(--green);color:white;border-radius:50%;
  display:flex;align-items:center;justify-content:center;font-size:0.8rem;font-weight:700;flex-shrink:0;}
.member-name{font-size:0.92rem;color:var(--text);font-weight:600;}
.member-nim{font-size:0.78rem;color:var(--text2);}

/* REVIEW */
.review-item{background:#FFF8F5;border:1.5px solid #F0CFC0;border-radius:12px;
  padding:0.8rem 1rem;margin-bottom:0.6rem;font-size:0.85rem;color:var(--text);}
.review-item strong{color:var(--green2);}

/* BUTTONS */
.stButton>button{background:var(--green)!important;color:var(--white)!important;
  border:none!important;border-radius:50px!important;font-family:'Lato',sans-serif!important;
  font-weight:700!important;font-size:0.9rem!important;padding:0.55rem 1.5rem!important;
  transition:all 0.2s!important;}
.stButton>button:hover{background:var(--green2)!important;transform:translateY(-1px)!important;
  box-shadow:0 4px 12px rgba(45,90,61,0.25)!important;}
.btn-ingat>button{background:#1A6B3A!important;}
.btn-lupa>button{background:#9B2020!important;}
.btn-back>button{background:transparent!important;color:var(--green)!important;
  border:1.5px solid var(--green)!important;}
.btn-flip>button{background:transparent!important;color:var(--green)!important;
  border:2px dashed var(--green-lt)!important;}
.btn-flip>button:hover{background:var(--cream2)!important;transform:none!important;box-shadow:none!important;}
.styled-hr{border:none;border-top:1.5px solid var(--green-lt);margin:1.2rem 0;}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
def init_state():
    defaults = {
        "mode":"home","view":"menu","materi_view":"menu",
        "materi_id":None,"category_id":None,"deck":[],
        "current_idx":0,"flipped":False,"score_ingat":0,
        "score_lupa":0,"wrong_cards":[],"review_mode":False,
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

def get_category(cat_id):
    return next((c for c in categories if c["id"]==cat_id),None)

def start_session(cat_id,shuffle=True,review_cards=None):
    cat = get_category(cat_id)
    deck = review_cards if review_cards else list(cat["cards"])
    if shuffle: random.shuffle(deck)
    st.session_state.category_id=cat_id; st.session_state.deck=deck
    st.session_state.current_idx=0; st.session_state.flipped=False
    st.session_state.score_ingat=0; st.session_state.score_lupa=0
    st.session_state.wrong_cards=[]; st.session_state.review_mode=bool(review_cards)
    st.session_state.view="session"

def progress_html(current,total):
    pct=int((current/total)*100) if total>0 else 0
    return f"""<div class="progress-wrap">
  <div class="progress-label"><span>Kartu {current} dari {total}</span><span>{pct}%</span></div>
  <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:{pct}%"></div></div>
</div>"""

# ── HEADER: hero hanya di home ──
if st.session_state.mode=="home":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-icons">
            <span class="hero-icon-side">⚗️</span>
            <span class="hero-icon-main">🔬</span>
            <span class="hero-icon-side">⚖️</span>
        </div>
        <div class="hero-title">Ankim-Card &amp; Calc</div>
        <div class="hero-subtitle">Asisten Pintar Hafalan Reaksi &amp; Perhitungan Larutan Kimia</div>
        <div class="hero-welcome">Selamat Datang! 👋<br>Pilih menu di bawah untuk mulai menggunakan Ankim-Card &amp; Calc.</div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="site-header-compact">
        <div class="logo">Ankim<span>-Card</span> &amp; Calc</div>
    </div>""", unsafe_allow_html=True)

# ── NAVIGASI ──
col_f,col_k,col_m,col_t = st.columns(4)
with col_f:
    if st.button("🃏 Flashcard",key="nav_flash",use_container_width=True):
        st.session_state.mode="flashcard"; st.session_state.view="menu"; st.rerun()
with col_k:
    if st.button("🧮 Kalkulator",key="nav_calc",use_container_width=True):
        st.session_state.mode="kalkulator"; st.rerun()
with col_m:
    if st.button("📖 Materi",key="nav_materi",use_container_width=True):
        st.session_state.mode="materi"; st.session_state.materi_view="menu"; st.rerun()
with col_t:
    if st.button("👥 Tentang Kami",key="nav_about",use_container_width=True):
        st.session_state.mode="tentang"; st.rerun()

st.markdown("<hr class='styled-hr'>",unsafe_allow_html=True)

# ══════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════
if st.session_state.mode=="home":
    pass  # welcome text sudah ada di dalam hero

# ══════════════════════════════════════════════
# FLASHCARD — langsung pilih kategori
# ══════════════════════════════════════════════
elif st.session_state.mode=="flashcard":

    if st.session_state.view=="menu":
        for cat in categories:
            total=len(cat["cards"])
            st.markdown(f"""
            <div class="cat-card">
                <div class="cat-icon">{cat['icon']}</div>
                <div class="cat-name">{cat['name']}</div>
                <div class="cat-desc">{cat['description']}</div>
                <div class="cat-count">📋 {total} kartu</div>
            </div>""", unsafe_allow_html=True)
            c1,c2=st.columns(2)
            with c1:
                if st.button("🚀 Mulai Belajar",key=f"start_{cat['id']}",use_container_width=True):
                    start_session(cat["id"],shuffle=False); st.rerun()
            with c2:
                if st.button("🔀 Acak Kartu",key=f"shuffle_{cat['id']}",use_container_width=True):
                    start_session(cat["id"],shuffle=True); st.rerun()
            st.markdown("<div style='height:0.3rem'></div>",unsafe_allow_html=True)

    elif st.session_state.view=="session":
        cat=get_category(st.session_state.category_id)
        deck=st.session_state.deck; idx=st.session_state.current_idx
        total=len(deck); card=deck[idx]

        bcol,_=st.columns([1,3])
        with bcol:
            st.markdown('<div class="btn-back">',unsafe_allow_html=True)
            if st.button("← Kategori",key="back_btn"):
                st.session_state.view="menu"; st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)

        label="🔁 Sesi Ulang" if st.session_state.review_mode else cat["name"]
        st.markdown(f"<div style='text-align:center;font-family:Playfair Display,serif;font-size:1.2rem;color:var(--green);margin-bottom:0.3rem'>{cat['icon']} {label}</div>",unsafe_allow_html=True)
        st.markdown(progress_html(idx+1,total),unsafe_allow_html=True)
        st.markdown(f"""<div class="score-badges">
            <span class="badge badge-ingat">👍 Ingat: {st.session_state.score_ingat}</span>
            <span class="badge badge-lupa">❌ Lupa: {st.session_state.score_lupa}</span>
        </div>""",unsafe_allow_html=True)

        flip_class="flipped" if st.session_state.flipped else ""
        st.markdown(f"""
        <div class="flashcard-wrap"><div class="flashcard-inner {flip_class}">
            <div class="flashcard-face flashcard-front">
                <div class="fc-label">— Pertanyaan —</div>
                <div class="fc-question">{card['front']}</div>
                <div class="fc-hint">👆 Klik tombol di bawah untuk lihat jawaban</div>
            </div>
            <div class="flashcard-face flashcard-back">
                <div class="fc-label">— Jawaban —</div>
                <div class="fc-answer">{card['back']}</div>
            </div>
        </div></div>""",unsafe_allow_html=True)

        flip_label="👁️ Lihat Jawaban" if not st.session_state.flipped else "🔁 Sembunyikan Jawaban"
        st.markdown('<div class="btn-flip">',unsafe_allow_html=True)
        if st.button(flip_label,key="flip_btn",use_container_width=True):
            st.session_state.flipped=not st.session_state.flipped; st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)

        st.markdown("<div style='text-align:center;font-size:0.8rem;color:var(--text2);margin:0.5rem 0'>Sudah lihat jawaban? Pilih:</div>",unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="btn-lupa">',unsafe_allow_html=True)
            if st.button("❌ Lupa / Salah",key="lupa_btn",use_container_width=True):
                st.session_state.score_lupa+=1; st.session_state.wrong_cards.append(card)
                st.session_state.flipped=False
                st.session_state.view="result" if idx+1>=total else None
                if idx+1<total: st.session_state.current_idx+=1
                st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="btn-ingat">',unsafe_allow_html=True)
            if st.button("👍 Ingat / Benar",key="ingat_btn",use_container_width=True):
                st.session_state.score_ingat+=1; st.session_state.flipped=False
                st.session_state.view="result" if idx+1>=total else None
                if idx+1<total: st.session_state.current_idx+=1
                st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)

    elif st.session_state.view=="result":
        total=st.session_state.score_ingat+st.session_state.score_lupa
        pct=int((st.session_state.score_ingat/total)*100) if total>0 else 0
        if pct==100:   emoji,title="🏆","Sempurna!"
        elif pct>=70:  emoji,title="🌿","Bagus Sekali!"
        elif pct>=40:  emoji,title="📚","Terus Belajar!"
        else:          emoji,title="💪","Jangan Menyerah!"

        st.markdown(f"""
        <div class="result-box">
            <div class="result-emoji">{emoji}</div>
            <div class="result-title">{title}</div>
            <div class="result-score">{st.session_state.score_ingat}/{total}</div>
            <div class="result-sub">Kartu benar &nbsp;•&nbsp; Akurasi <strong>{pct}%</strong></div>
        </div>""",unsafe_allow_html=True)

        wrong=st.session_state.wrong_cards
        if wrong:
            st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:var(--brown);margin:1rem 0 0.5rem'>📌 Kartu yang perlu diulang ({len(wrong)})</div>",unsafe_allow_html=True)
            for w in wrong:
                st.markdown(f'<div class="review-item">❓ {w["front"]}<br><strong>✅ {w["back"]}</strong></div>',unsafe_allow_html=True)

        st.markdown("<div style='height:0.8rem'></div>",unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        with c1:
            if st.button("🔁 Ulangi Semua",use_container_width=True):
                start_session(st.session_state.category_id,shuffle=False); st.rerun()
        with c2:
            if wrong:
                if st.button(f"⚡ Ulang Salah ({len(wrong)})",use_container_width=True):
                    start_session(st.session_state.category_id,shuffle=True,review_cards=wrong); st.rerun()
        with c3:
            if st.button("🏠 Menu Utama",use_container_width=True):
                st.session_state.mode="home"; st.session_state.view="menu"; st.rerun()

# ══════════════════════════════════════════════
# KALKULATOR — langsung expander, tanpa judul
# Hanya: Pengenceran (cari V1 & C2), Molaritas, Normalitas
# ══════════════════════════════════════════════
elif st.session_state.mode=="kalkulator":

    with st.expander("🧪 Pengenceran Larutan (C₁V₁ = C₂V₂)", expanded=True):
        st.markdown('<div class="calc-formula">Rumus: C₁ × V₁ = C₂ × V₂</div>',unsafe_allow_html=True)
        cari=st.radio("Yang ingin dicari:",
            ["Cari V₁ (volume yang diambil)","Cari C₂ (konsentrasi akhir)"],
            key="pengenceran_cari")

        if cari=="Cari V₁ (volume yang diambil)":
            st.markdown("**Masukkan nilai C₁, C₂, dan V₂:**")
            col1,col2,col3=st.columns(3)
            with col1: c1v=st.number_input("C₁ – Konsentrasi Awal",min_value=0.0,value=0.0,step=0.0001,format="%.4f",key="v1_c1")
            with col2: c2v=st.number_input("C₂ – Konsentrasi Akhir",min_value=0.0,value=0.0,step=0.0001,format="%.4f",key="v1_c2")
            with col3: v2v=st.number_input("V₂ – Volume Akhir (mL)",min_value=0.0,value=0.0,step=0.01,format="%.2f",key="v1_v2")
            if st.button("Hitung V₁",key="calc_v1"):
                if c1v>0 and c2v>0 and v2v>0:
                    hasil=(c2v*v2v)/c1v
                    st.markdown(f'<div class="result-output"><small>📢 Volume yang diambil (V₁)</small>{hasil:.4f} mL</div>',unsafe_allow_html=True)
                    if hasil>v2v: st.warning("⚠️ V₁ > V₂ — periksa kembali nilai yang dimasukkan.")
                else: st.error("Isi semua kolom dengan nilai lebih dari 0.")

        else:
            st.markdown("**Masukkan nilai C₁, V₁, dan V₂:**")
            col1,col2,col3=st.columns(3)
            with col1: c1c=st.number_input("C₁ – Konsentrasi Awal",min_value=0.0,value=0.0,step=0.0001,format="%.4f",key="c2_c1")
            with col2: v1c=st.number_input("V₁ – Volume Awal (mL)",min_value=0.0,value=0.0,step=0.01,format="%.2f",key="c2_v1")
            with col3: v2c=st.number_input("V₂ – Volume Akhir (mL)",min_value=0.0,value=0.0,step=0.01,format="%.2f",key="c2_v2")
            if st.button("Hitung C₂",key="calc_c2"):
                if c1c>0 and v1c>0 and v2c>0:
                    hasil=(c1c*v1c)/v2c
                    st.markdown(f'<div class="result-output"><small>📢 Konsentrasi Akhir (C₂)</small>{hasil:.4f} M</div>',unsafe_allow_html=True)
                else: st.error("Isi semua kolom dengan nilai lebih dari 0.")

    with st.expander("⚖️ Molaritas (M)", expanded=False):
        st.markdown('<div class="calc-formula">Rumus: M = massa (g) / [BM (g/mol) × Volume (L)]</div>',unsafe_allow_html=True)
        col1,col2,col3=st.columns(3)
        with col1: massa_m=st.number_input("Massa zat (g)",min_value=0.0,value=0.0,step=0.0001,format="%.4f",key="mol_massa")
        with col2: bm=st.number_input("BM (g/mol)",min_value=0.0,value=0.0,step=1.0,format="%.2f",key="mol_bm")
        with col3: vol_m=st.number_input("Volume (L)",min_value=0.0,value=0.0,step=0.01,format="%.4f",key="mol_vol")
        if st.button("Hitung Molaritas",key="calc_mol"):
            if massa_m>0 and bm>0 and vol_m>0:
                M=float(massa_m)/(float(bm)*float(vol_m))
                st.markdown(f'<div class="result-output"><small>📢 Molaritas</small>{M:.4f} mol/L</div>',unsafe_allow_html=True)
            else: st.error("Isi semua kolom dengan nilai lebih dari 0.")

    with st.expander("⚗️ Normalitas (N)", expanded=False):
        st.markdown('<div class="calc-formula">Rumus: N = massa (g) / [BE (g/grek) × Volume (L)]</div>',unsafe_allow_html=True)
        col1,col2,col3=st.columns(3)
        with col1: massa_n=st.number_input("Massa zat (g)",min_value=0.0,value=0.0,step=0.0001,format="%.4f",key="norm_massa")
        with col2: be=st.number_input("BE (g/grek)",min_value=0.0,value=0.0,step=1.0,format="%.2f",key="norm_be")
        with col3: vol_n=st.number_input("Volume (L)",min_value=0.0,value=0.0,step=0.01,format="%.4f",key="norm_vol")
        if st.button("Hitung Normalitas",key="calc_norm"):
            if massa_n>0 and be>0 and vol_n>0:
                N=float(massa_n)/(float(be)*float(vol_n))
                st.markdown(f'<div class="result-output"><small>📢 Normalitas</small>{N:.4f} grek/L</div>',unsafe_allow_html=True)
            else: st.error("Isi semua kolom dengan nilai lebih dari 0.")

# ══════════════════════════════════════════════
# TENTANG KAMI — langsung konten
# ══════════════════════════════════════════════
elif st.session_state.mode=="tentang":
    st.markdown("""
    <div class="about-card">
        <div class="about-title">🧪 Tentang Aplikasi</div>
        <p style="font-size:0.9rem;color:var(--text2);line-height:1.7;margin:0">
            <b>Ankim-Card &amp; Calc</b> adalah web app interaktif yang dirancang untuk membantu
            mahasiswa AKA menghafal reaksi identifikasi kation, karakteristik endapan gravimetri,
            dan perubahan warna titrimetri — sekaligus menyediakan kalkulator untuk perhitungan
            larutan sehari-hari di laboratorium.
        </p><br>
        <table style="width:100%;font-size:0.85rem;border-collapse:collapse">
            <tr><td style="color:var(--text2);padding:4px 0;width:140px">📚 Mata Kuliah</td><td style="color:var(--text);font-weight:600">Logika Pemrograman Komputer</td></tr>
            <tr><td style="color:var(--text2);padding:4px 0">🏫 Program Studi</td><td style="color:var(--text);font-weight:600">Analisis Kimia</td></tr>
            <tr><td style="color:var(--text2);padding:4px 0">🏛️ Institusi</td><td style="color:var(--text);font-weight:600">Politeknik AKA Bogor</td></tr>
            <tr><td style="color:var(--text2);padding:4px 0">📅 Tahun</td><td style="color:var(--text);font-weight:600">2026</td></tr>
        </table>
    </div>
    <div class="about-card">
        <div class="about-title">🎓 Anggota Kelompok</div>
        <div class="member-row"><div class="member-num">1</div><div><div class="member-name">Anisa Ramanda</div><div class="member-nim">NIM: 2560576</div></div></div>
        <div class="member-row"><div class="member-num">2</div><div><div class="member-name">Galih Pratama</div><div class="member-nim">NIM: 2560634</div></div></div>
        <div class="member-row"><div class="member-num">3</div><div><div class="member-name">M. Djaky Tofanny</div><div class="member-nim">NIM: 2560662</div></div></div>
        <div class="member-row"><div class="member-num">4</div><div><div class="member-name">Natasya Septiani</div><div class="member-nim">NIM: 2560714</div></div></div>
        <div class="member-row"><div class="member-num">5</div><div><div class="member-name">Siti Fadilah Afkar</div><div class="member-nim">NIM: 2560784</div></div></div>
    </div>
    <div class="about-card">
        <div class="about-title">👨‍🏫 Dosen Penanggung Jawab</div>
        <div class="member-row"><div class="member-num">👤</div><div><div class="member-name">Ibu Dewi Pujoningsih, M.Si</div></div></div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# MATERI — langsung konten
# ══════════════════════════════════════════════
elif st.session_state.mode=="materi":

    def get_materi(mid):
        return next((m for m in all_materi if m["id"]==mid),None)

    if st.session_state.materi_view=="menu":
        for m in all_materi:
            st.markdown(f"""
            <div class="cat-card">
                <div class="cat-icon">{m['icon']}</div>
                <div class="cat-name">{m['judul']}</div>
                <div class="cat-desc">{m['deskripsi']}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"📖 Buka {m['judul']}",key=f"open_materi_{m['id']}",use_container_width=True):
                st.session_state.materi_id=m["id"]; st.session_state.materi_view="detail"; st.rerun()
            st.markdown("<div style='height:0.3rem'></div>",unsafe_allow_html=True)

    elif st.session_state.materi_view=="detail":
        m=get_materi(st.session_state.materi_id)
        bcol,_=st.columns([1,3])
        with bcol:
            st.markdown('<div class="btn-back">',unsafe_allow_html=True)
            if st.button("← Materi",key="back_materi"):
                st.session_state.materi_view="menu"; st.rerun()
            st.markdown("</div>",unsafe_allow_html=True)

        st.markdown(f"<div style='font-family:Playfair Display,serif;font-size:1.5rem;color:var(--green);margin-bottom:0.2rem'>{m['icon']} {m['judul']}</div>",unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.85rem;color:var(--text2);margin-bottom:1rem'>{m['deskripsi']}</div>",unsafe_allow_html=True)

        if m["id"]=="anjen":
            with st.expander("🎯 Tujuan & Prinsip",expanded=True):
                st.markdown(f"""
                <div class="about-card" style="margin-bottom:0.5rem">
                    <div class="about-title">🎯 Tujuan</div>
                    <p style="font-size:0.9rem;color:var(--text2);line-height:1.7;margin:0">{m['tujuan']}</p>
                </div>
                <div class="about-card" style="margin-bottom:0">
                    <div class="about-title">🔬 Prinsip</div>
                    <p style="font-size:0.9rem;color:var(--text2);line-height:1.7;margin:0">{m['prinsip']}</p>
                </div>""", unsafe_allow_html=True)

            st.markdown("<div style='font-family:Playfair Display,serif;font-size:1.1rem;color:var(--green);margin:0.8rem 0 0.5rem'>⚗️ Reaksi Identifikasi Kation</div>",unsafe_allow_html=True)
            golongan_map={}
            for k in m["kation"]:
                g=k["golongan"]
                if g not in golongan_map: golongan_map[g]=[]
                golongan_map[g].append(k)
            for gol,kations in golongan_map.items():
                st.markdown(f"<div style='font-weight:700;color:var(--brown);font-size:0.85rem;margin:0.8rem 0 0.3rem;letter-spacing:0.05em'>GOLONGAN {gol}</div>",unsafe_allow_html=True)
                for k in kations:
                    with st.expander(f"Ion {k['ion']}",expanded=False):
                        import pandas as pd
                        rows=[{"Pereaksi":r["pereaksi"],"Persamaan Reaksi":r["persamaan"],"Pengamatan":r["pengamatan"]} for r in k["reaksi"]]
                        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        else:
            for perc in m["percobaan"]:
                with st.expander(f"📌 {perc['judul']}",expanded=False):
                    if perc.get("tujuan"):
                        st.markdown(f'<div class="about-card" style="margin-bottom:0.6rem"><div class="about-title">🎯 Tujuan</div><p style="font-size:0.88rem;color:var(--text2);line-height:1.7;margin:0">{perc["tujuan"]}</p></div>',unsafe_allow_html=True)
                    st.markdown(f'<div class="about-card" style="margin-bottom:0.6rem"><div class="about-title">🔬 Prinsip</div><p style="font-size:0.88rem;color:var(--text2);line-height:1.7;margin:0">{perc["prinsip"]}</p></div>',unsafe_allow_html=True)
                    if perc.get("reaksi"):
                        st.markdown(f'<div class="about-card" style="margin-bottom:0.6rem"><div class="about-title">⚗️ Reaksi yang Terjadi</div><div style="font-family:monospace;font-size:0.85rem;color:var(--text);line-height:2;background:var(--cream2);padding:0.8rem;border-radius:8px">{perc["reaksi"].replace(chr(10),"<br>")}</div></div>',unsafe_allow_html=True)
                    if perc.get("rumus"):
                        ket="".join([f"<div>• {k}</div>" for k in perc["keterangan_rumus"].split(" | ")])
                        st.markdown(f'<div class="about-card"><div class="about-title">📊 Rumus Perhitungan</div><div style="background:linear-gradient(135deg,var(--green),var(--green2));color:white;border-radius:10px;padding:0.8rem 1rem;font-family:monospace;font-size:0.95rem;text-align:center;margin-bottom:0.6rem">{perc["rumus"]}</div><div style="font-size:0.78rem;color:var(--text2);line-height:1.8">{ket}</div></div>',unsafe_allow_html=True)

# FOOTER
st.markdown("""
<hr class='styled-hr'>
<div style='text-align:center;font-size:0.78rem;color:var(--brown-lt);padding-bottom:1rem'>
    🌿 Ankim-Card &amp; Calc &nbsp;·&nbsp; Analisis Kimia 2026
</div>""", unsafe_allow_html=True)
