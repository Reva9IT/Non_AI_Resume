def generate_html(data: dict) -> bytes:
    name = data.get("full_name", "Your Name")
    title = data.get("professional_title", "Professional")
    email = data.get("email", "")
    phone = data.get("phone", "")
    linkedin = data.get("linkedin", "")
    github = data.get("github", "")
    website = data.get("personal_website", "")
    summary = data.get("summary", "")
    skills = data.get("skills", [])
    experience = data.get("experience", [])
    projects = data.get("projects", [])
    education = data.get("education", "")
    achievements = data.get("achievements", "")

    def contact_link(url, label):
        if not url:
            return ""
        href = url if url.startswith("http") else f"https://{url}"
        return f'<a href="{href}" target="_blank" class="contact-chip">{label}</a>'

    def email_link(e):
        if not e:
            return ""
        return f'<a href="mailto:{e}" class="contact-chip">✉ {e}</a>'

    def phone_chip(p):
        if not p:
            return ""
        return f'<span class="contact-chip">📞 {p}</span>'

    contact_html = "".join(filter(None, [
        email_link(email),
        phone_chip(phone),
        contact_link(linkedin, "🔗 LinkedIn"),
        contact_link(github, "🐙 GitHub"),
        contact_link(website, "🌐 Website"),
    ]))

    skill_tags = "".join(f'<span class="skill-tag">{s}</span>' for s in skills)

    def project_card(p):
        parts = p.split("–", 1) if "–" in p else p.split("-", 1)
        ptitle = parts[0].strip()
        pdesc = parts[1].strip() if len(parts) > 1 else ""
        return f"""
        <div class="card">
            <div class="card-title">{ptitle}</div>
            <div class="card-desc">{pdesc}</div>
        </div>"""

    def exp_card(e):
        parts = e.split("–", 1) if "–" in e else e.split("-", 1)
        etitle = parts[0].strip()
        edesc = parts[1].strip() if len(parts) > 1 else ""
        return f"""
        <div class="card">
            <div class="card-title">{etitle}</div>
            <div class="card-desc">{edesc}</div>
        </div>"""

    projects_html = "".join(project_card(p) for p in projects) if projects else "<p class='empty'>No projects listed.</p>"
    experience_html = "".join(exp_card(e) for e in experience) if experience else "<p class='empty'>No experience listed.</p>"

    edu_lines = "".join(f"<p>{line}</p>" for line in education.split("\n") if line.strip()) if education else ""
    ach_lines = "".join(f"<li>{line}</li>" for line in achievements.split("\n") if line.strip()) if achievements else ""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{name} – Portfolio</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet"/>
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

  :root {{
    --bg: #07070f;
    --surface: #0f0f1a;
    --surface2: #16162a;
    --border: rgba(255,255,255,0.07);
    --purple: #7c3aed;
    --purple-light: #a78bfa;
    --blue: #2563eb;
    --cyan: #06b6d4;
    --green: #10b981;
    --text: #e2e2f0;
    --text-muted: #7070a0;
    --radius: 16px;
  }}

  html {{ scroll-behavior: smooth; }}

  body {{
    font-family: 'DM Sans', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    overflow-x: hidden;
  }}

  /* ── Scrollbar ── */
  ::-webkit-scrollbar {{ width: 6px; }}
  ::-webkit-scrollbar-track {{ background: var(--bg); }}
  ::-webkit-scrollbar-thumb {{ background: var(--purple); border-radius: 3px; }}

  /* ── Nav ── */
  nav {{
    position: fixed; top: 0; left: 0; right: 0;
    z-index: 100;
    display: flex; align-items: center; justify-content: space-between;
    padding: 1rem 2.5rem;
    background: rgba(7,7,15,0.85);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
  }}
  .nav-logo {{
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.2rem;
    background: linear-gradient(135deg, var(--purple-light), var(--cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .nav-links {{ display: flex; gap: 2rem; }}
  .nav-links a {{
    color: var(--text-muted);
    text-decoration: none;
    font-size: 0.88rem;
    font-weight: 500;
    transition: color 0.2s;
    letter-spacing: 0.03em;
  }}
  .nav-links a:hover {{ color: var(--purple-light); }}

  /* ── Hero ── */
  #hero {{
    min-height: 100vh;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    text-align: center;
    padding: 8rem 2rem 4rem;
    position: relative;
    overflow: hidden;
  }}
  .hero-glow {{
    position: absolute;
    top: 20%; left: 50%;
    transform: translate(-50%, -50%);
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
    pointer-events: none;
  }}
  .hero-badge {{
    display: inline-block;
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--purple-light);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
  }}
  .hero-name {{
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 8vw, 5.5rem);
    font-weight: 800;
    line-height: 1.05;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #fff 0%, var(--purple-light) 50%, var(--cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }}
  .hero-title {{
    font-size: 1.3rem;
    color: var(--text-muted);
    font-weight: 300;
    margin-bottom: 2.5rem;
  }}
  .contact-chips {{
    display: flex; flex-wrap: wrap; justify-content: center;
    gap: 0.6rem; margin-bottom: 2rem;
  }}
  .contact-chip {{
    display: inline-flex; align-items: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 0.4rem 1rem;
    font-size: 0.82rem;
    color: var(--text-muted);
    text-decoration: none;
    transition: all 0.2s;
  }}
  .contact-chip:hover {{
    border-color: var(--purple);
    color: var(--purple-light);
    background: rgba(124,58,237,0.1);
  }}

  /* ── Sections ── */
  section {{
    max-width: 1000px;
    margin: 0 auto;
    padding: 5rem 2rem;
  }}
  .section-label {{
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--purple-light);
    margin-bottom: 0.5rem;
  }}
  .section-title {{
    font-family: 'Syne', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    margin-bottom: 2.5rem;
    position: relative;
  }}
  .section-title::after {{
    content: '';
    position: absolute;
    bottom: -8px; left: 0;
    width: 50px; height: 3px;
    background: linear-gradient(90deg, var(--purple), var(--cyan));
    border-radius: 2px;
  }}

  /* ── About ── */
  .about-text {{
    font-size: 1.1rem;
    color: #b0b0cc;
    line-height: 1.85;
    max-width: 720px;
    font-style: italic;
  }}

  /* ── Skills ── */
  .skills-grid {{
    display: flex; flex-wrap: wrap; gap: 0.6rem;
  }}
  .skill-tag {{
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
    color: var(--purple-light);
    padding: 0.4rem 0.9rem;
    border-radius: 8px;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s;
    cursor: default;
  }}
  .skill-tag:hover {{
    background: rgba(124,58,237,0.25);
    transform: translateY(-2px);
  }}

  /* ── Cards ── */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.2rem;
  }}
  .card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
  }}
  .card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--purple), var(--cyan));
    opacity: 0;
    transition: opacity 0.25s;
  }}
  .card:hover {{
    border-color: rgba(124,58,237,0.3);
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(124,58,237,0.12);
  }}
  .card:hover::before {{ opacity: 1; }}
  .card-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.5rem;
  }}
  .card-desc {{
    font-size: 0.9rem;
    color: var(--text-muted);
    line-height: 1.6;
  }}
  .empty {{
    color: var(--text-muted);
    font-style: italic;
  }}

  /* ── Education ── */
  .edu-block {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem;
    line-height: 2;
  }}
  .edu-block p {{ color: var(--text-muted); font-size: 1rem; }}

  /* ── Achievements ── */
  .ach-list {{
    list-style: none;
    display: flex; flex-direction: column; gap: 0.8rem;
  }}
  .ach-list li {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    color: var(--text-muted);
    font-size: 0.95rem;
    position: relative;
    padding-left: 2rem;
  }}
  .ach-list li::before {{
    content: '🏆';
    position: absolute; left: 0.7rem; top: 0.9rem;
    font-size: 0.85rem;
  }}

  /* ── Footer ── */
  footer {{
    text-align: center;
    padding: 3rem 2rem;
    border-top: 1px solid var(--border);
    color: var(--text-muted);
    font-size: 0.85rem;
  }}

  /* ── Divider ── */
  .divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.2), transparent);
    max-width: 1000px;
    margin: 0 auto;
  }}

  @media (max-width: 640px) {{
    nav {{ padding: 0.8rem 1.2rem; }}
    .nav-links {{ gap: 1rem; font-size: 0.8rem; }}
    .hero-name {{ font-size: 2.5rem; }}
    .cards-grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>

<nav>
  <div class="nav-logo">{name.split()[0] if name else 'Portfolio'}</div>
  <div class="nav-links">
    <a href="#about">About</a>
    <a href="#skills">Skills</a>
    <a href="#experience">Experience</a>
    <a href="#projects">Projects</a>
    {"<a href='#education'>Education</a>" if education else ""}
  </div>
</nav>

<!-- HERO -->
<div id="hero">
  <div class="hero-glow"></div>
  <div class="hero-badge">Portfolio</div>
  <h1 class="hero-name">{name}</h1>
  <p class="hero-title">{title}</p>
  <div class="contact-chips">{contact_html}</div>
</div>

<div class="divider"></div>

<!-- ABOUT -->
<section id="about">
  <div class="section-label">Introduction</div>
  <h2 class="section-title">About Me</h2>
  <p class="about-text">{summary}</p>
</section>

<div class="divider"></div>

<!-- SKILLS -->
{"<section id='skills'><div class='section-label'>Expertise</div><h2 class='section-title'>Skills</h2><div class='skills-grid'>" + skill_tags + "</div></section><div class='divider'></div>" if skills else ""}

<!-- EXPERIENCE -->
<section id="experience">
  <div class="section-label">Career</div>
  <h2 class="section-title">Work Experience</h2>
  <div class="cards-grid">{experience_html}</div>
</section>

<div class="divider"></div>

<!-- PROJECTS -->
<section id="projects">
  <div class="section-label">Work</div>
  <h2 class="section-title">Projects</h2>
  <div class="cards-grid">{projects_html}</div>
</section>

{"<div class='divider'></div><section id='education'><div class='section-label'>Academic</div><h2 class='section-title'>Education</h2><div class='edu-block'>" + edu_lines + "</div></section>" if education else ""}

{"<div class='divider'></div><section id='achievements'><div class='section-label'>Accomplishments</div><h2 class='section-title'>Achievements</h2><ul class='ach-list'>" + ach_lines + "</ul></section>" if achievements else ""}

<footer>
  <p>Built with ❤️ using the Resume & Portfolio Builder &nbsp;·&nbsp; {name}</p>
</footer>

</body>
</html>"""

    return html.encode("utf-8")
