def generate_summary(data: dict) -> str:
    """
    Rule-based professional summary generator.
    No AI/API required.
    """
    title = data.get("professional_title", "Professional")
    skills = data.get("skills", [])
    projects = data.get("projects", [])
    experience = data.get("experience", [])

    # Pick top skills (up to 4)
    top_skills = skills[:4] if skills else []
    skills_str = ", ".join(top_skills) if top_skills else "various technologies"

    # First project name (before dash or full string)
    first_project = ""
    if projects:
        raw = projects[0]
        first_project = raw.split("–")[0].split("-")[0].strip()

    # Experience count
    exp_count = len(experience)

    # Build summary
    if first_project and exp_count > 0:
        summary = (
            f"{title} with strong expertise in {skills_str}. "
            f"Experienced in building impactful projects such as {first_project}. "
            f"Proven track record across {exp_count} professional role{'s' if exp_count > 1 else ''}, "
            f"delivering scalable and robust solutions. "
            f"Passionate about solving real-world problems and driving measurable results."
        )
    elif first_project:
        summary = (
            f"{title} with strong expertise in {skills_str}. "
            f"Experienced in building projects such as {first_project}. "
            f"Passionate about solving real-world problems and delivering scalable solutions."
        )
    elif exp_count > 0:
        summary = (
            f"{title} with strong expertise in {skills_str}. "
            f"Brings hands-on experience across {exp_count} professional engagement{'s' if exp_count > 1 else ''}, "
            f"with a focus on quality, performance, and collaboration. "
            f"Committed to continuous learning and impactful engineering."
        )
    else:
        summary = (
            f"{title} with strong expertise in {skills_str}. "
            f"Passionate about building innovative solutions and contributing to high-impact projects. "
            f"Eager to leverage technical skills to solve real-world problems and deliver scalable results."
        )

    return summary
