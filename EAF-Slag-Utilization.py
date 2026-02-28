import streamlit as st

st.set_page_config(
    page_title="EAF Slag Utilization Decision Tool ( EU-focused)",
    page_icon="U+267B",
    layout="wide",
)

st.title("U+267B EAF Slag Utilization Decision Tool — (EU/Germany-focused screening)")
st.caption(
    "Rule-based, no dataset required. Uses slag chemistry + EU-style environmental screening flags to rank recycling routes.\n\n"
    "Important: This app uses **screening thresholds** (Green/Amber/Red). "
    "You should enter thresholds from your chosen German/EU reference (e.g., ErsatzbaustoffV / DepV / state guidance). "
    "Defaults here are **illustrative placeholders** for teaching/portfolio use."
)


with st.sidebar:
    st.header("Inputs")

    st.subheader("Metallurgical inputs")
    feo_pct = st.number_input("FeO (%)", min_value=0.0, max_value=60.0, value=25.0, step=0.5)
    basicity = st.number_input("Basicity (CaO/SiO₂)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)

    free_cao_risk = st.selectbox(
        "Free CaO expansion risk (qualitative)",
        ["Low", "Medium", "High"],
        index=1,
        help="High free CaO (or free MgO) increases expansion risk; aging/conditioning may be required.",
    )

    st.subheader("Trace metals (total content)")
    cr_wt = st.number_input("Chromium (Cr) total (wt%)", min_value=0.0, max_value=10.0, value=0.8, step=0.1)
    pb_wt = st.number_input("Lead (Pb) total (wt%)", min_value=0.0, max_value=5000.0, value=150.0, step=10.0)
    zn_wt = st.number_input("Zinc (Zn) total (wt%)", min_value=0.0, max_value=10.0, value=0.6, step=0.1)

    st.subheader("Locally available facilities")
    cement_outlet = st.toggle("Cement / binder outlet", value=True)
    road_outlet = st.toggle("Road construction / aggregates outlet", value=True)
    metal_recovery_outlet = st.toggle("Metal recovery ", value=True)
    landfill_outlet = st.toggle("Landfill option (fallback)", value=True)

    st.divider()
    st.subheader("EU/Germany screening thresholds (edit as needed)")
    threshold_mode = st.radio(
        "Threshold mode",
        ["Use illustrative defaults (not legal limits)", "Enter my own thresholds"],
        index=0,
        help="For thesis/real use, set thresholds from ErsatzbaustoffV/DepV or your chosen German guidance.",
    )

    default_thr = {
        "Cr_wt_green": 0.5,
        "Cr_wt_amber": 1.5,
        "Pb_wt_green" : 0.01,
        "Pb_wt_amber" : 0.03,
        "Zn_wt_green": 0.5,
        "Zn_wt_amber": 1.5,
    }

    if threshold_mode == "Use illustrative defaults (not legal limits)":
        cr_wt_green = default_thr["Cr_wt_green"]
        cr_wt_amber = default_thr["Cr_wt_amber"]
        pb_wt_green = default_thr["Pb_wt_green"]
        pb_wt_amber = default_thr["Pb_wt_amber"]
        zn_wt_green = default_thr["Zn_wt_green"]
        zn_wt_amber = default_thr["Zn_wt_amber"]
        st.caption(
            "Defaults are **illustrative** (screening only). Switch to “Enter my own thresholds” to use values from your sources."
        )
    else:
        st.caption("Enter your Green/Amber breakpoints. Values above Amber are treated as Red.")
        cr_wt_green = st.number_input("Cr Green threshold (wt%)", min_value=0.0, value=default_thr["Cr_wt_green"], step=0.1)
        cr_wt_amber = st.number_input("Cr Amber threshold (wt%)", min_value=0.0, value=default_thr["Cr_wt_amber"], step=0.1)

        pb_wt_green = st.number_input("Pb Green threshold (wt%)", min_value=0.0, value=default_thr["pb_wt_green"], step=0.005)
        pb_wt_amber = st.number_input("Pb Amber threshold (wt%)", min_value=0.0, value=default_thr["pb_wt_amber"], step=0.005)

        zn_wt_green = st.number_input("Zn Green threshold (wt%)", min_value=0.0, value=default_thr["Zn_wt_green"], step=0.1)
        zn_wt_amber = st.number_input("Zn Amber threshold (wt%)", min_value=0.0, value=default_thr["Zn_wt_amber"], step=0.1)

    st.divider()
    st.subheader("Optional: paste your source links (for your records)")
    src_ersatz = st.text_input("ErsatzbaustoffV / Mantelverordnung link (optional)", value="")
    src_depv = st.text_input("DepV link (optional)", value="")
    src_state = st.text_input("State guidance / technical rules link (optional)", value="")


def flag_level(value, green, amber):
    """Return (level, score_penalty, label) where level in {'Green','Amber','Red'}.
       Penalty is used to reduce reuse route scores when risk increases."""
    if value <= green:
        return "Green", 0, "🟢 Green"
    if value <= amber:
        return "Amber", 2, "🟡 Amber"
    return "Red", 6, "🔴 Red"

cr_level, cr_penalty, cr_label = flag_level(cr_wt, cr_wt_green, cr_wt_amber)
pb_level, pb_penalty, pb_label = flag_level(pb_wt, pb_wt_green, pb_wt_amber)
zn_level, zn_penalty, zn_label = flag_level(zn_wt, zn_wt_green, zn_wt_amber)


pen_sum = cr_penalty + pb_penalty + zn_penalty
if pen_sum <= 2:
    env_overall = "Low"
    env_badge = "🟢 Low"
elif pen_sum <= 8:
    env_overall = "Medium"
    env_badge = "🟡 Medium"
else:
    env_overall = "High"
    env_badge = "🔴 High"

actions = []
if free_cao_risk == "High":
    actions.append("Aging/conditioning is strongly recommended to control expansion (free CaO/MgO).")
    actions.append("Consider stabilization/carbonation/controlled curing before reuse.")
elif free_cao_risk == "Medium":
    actions.append("Aging/conditioning recommended; verify volumetric stability (expansion tests).")
else:
    actions.append("Low expansion risk assumed; standard QA checks still recommended.")

if feo_pct >= 25:
    actions.append("FeO is relatively high → metal recovery / beneficiation may be attractive (site-specific).")
elif feo_pct >= 15:
    actions.append("Moderate FeO → check metallic content; recovery may still be worthwhile depending on plant.")
else:
    actions.append("Low FeO → metal recovery may be less attractive unless metallic Fe is significant.")

if basicity >= 2.2:
    actions.append("Higher basicity can support binder/aggregate performance but requires stability and compliance testing.")
elif basicity >= 1.6:
    actions.append("Moderate basicity; performance depends on processing and QA testing.")
else:
    actions.append("Low basicity; reuse may still be possible but may require blending/conditioning for target application.")

actions.append("Perform EU/Germany-relevant leaching & compliance testing before unrestricted reuse (especially if Amber/Red flags).")


def base_availability_score(available: bool) -> int:
    return 4 if available else -8

def route_score_road():
    score = 0
    why = []

    score += base_availability_score(road_outlet)
    why.append("Road/aggregate outlet is available." if road_outlet else "No road/aggregate outlet available (major barrier).")

    
    if free_cao_risk == "High":
        score -= 4
        why.append("High free CaO risk penalizes road use unless conditioning/aging is applied.")
    elif free_cao_risk == "Medium":
        score -= 1
        why.append("Medium free CaO risk: road use may require aging and stability testing.")
    else:
        score += 2
        why.append("Low expansion risk supports aggregate use (with QA).")

   
    score -= (cr_penalty + pb_penalty + zn_penalty) * 0.6
    if env_overall == "High":
        why.append("Environmental screening is HIGH → road use likely restricted unless encapsulated/controlled and proven by leaching tests.")
    elif env_overall == "Medium":
        why.append("Environmental screening is MEDIUM → controlled use + leaching testing recommended.")
    else:
        why.append("Environmental screening is LOW → fewer environmental constraints expected (still test).")

    if env_overall in ["Low", "Medium"]:
        score += 2
        why.append("Recycling preference: road/aggregate route favored when compliance risk is not severe.")

    return score, why

def route_score_cement():
    score = 0
    why = []

    score += base_availability_score(cement_outlet)
    why.append("Cement/binder outlet is available." if cement_outlet else "No cement/binder outlet available (major barrier).")

    
    if free_cao_risk == "High":
        score -= 3
        why.append("High free CaO risk penalizes direct cement/binder use without conditioning.")
    elif free_cao_risk == "Medium":
        score -= 1
        why.append("Medium free CaO risk: conditioning recommended.")
    else:
        score += 1

    if basicity >= 2.0:
        score += 2
        why.append("Basicity supports potential binder/encapsulation use (performance must be tested).")
    elif basicity >= 1.5:
        score += 1
        why.append("Basicity is moderate; cement route may still work depending on tests and blending.")
    else:
        score -= 1
        why.append("Low basicity slightly penalizes binder route unless blended/engineered.")

    score -= (cr_penalty + pb_penalty + zn_penalty) * 0.45
    if env_overall == "High":
        why.append("Environmental screening HIGH: cement/encapsulation might still be possible but requires strict QA + compliance proof.")
    elif env_overall == "Medium":
        why.append("Environmental screening MEDIUM: cement route often feasible with testing and controlled formulation.")
    else:
        why.append("Environmental screening LOW: cement route likely feasible subject to product standards/testing.")

    # Recycling tilt bonus if not severe
    if env_overall in ["Low", "Medium"]:
        score += 2
        why.append("Recycling preference: cement/encapsulation favored when compliance risk is not severe.")

    return score, why

def route_score_metal_recovery():
    score = 0
    why = []

    score += base_availability_score(metal_recovery_outlet)
    why.append("Metal recovery facility is available." if metal_recovery_outlet else "No metal recovery facility available (major barrier).")

    if feo_pct >= 25:
        score += 4
        why.append("High FeO suggests higher potential value from beneficiation/metal recovery (site-specific).")
    elif feo_pct >= 15:
        score += 2
        why.append("Moderate FeO: metal recovery may still be worthwhile depending on metallic Fe entrainment.")
    else:
        score += 0
        why.append("Low FeO: metal recovery value may be limited unless metallic Fe content is high.")

    score -= (cr_penalty + pb_penalty + zn_penalty) * 0.2
    if env_overall == "High":
        why.append("Environmental screening HIGH: metal recovery remains useful as a pre-treatment before final outlet selection.")
    else:
        why.append("Environmental screening not severe: metal recovery can improve overall circularity and reduce landfill need.")

    score += 2 if metal_recovery_outlet else 0
    why.append("Recycling preference: metal recovery is recommended as a first step when available.")

    return score, why

def route_score_landfill():
    score = 0
    why = []

    score += (2 if landfill_outlet else -10)
    why.append("Landfill option available." if landfill_outlet else "No landfill option available (constraint).")

    score -= 4
    why.append("Landfill is treated as a last-resort option (circularity preference).")

    if env_overall == "High":
        score += 8
        why.append("Environmental screening HIGH: disposal/controlled landfill may be necessary if reuse cannot meet compliance.")
    elif env_overall == "Medium":
        score += 2
        why.append("Environmental screening MEDIUM: landfill may be used if markets/tests fail.")
    else:
        score -= 1
        why.append("Environmental screening LOW: reuse routes should usually be prioritized over landfill.")

    if (not road_outlet) and (not cement_outlet) and (not metal_recovery_outlet):
        score += 8
        why.append("No valorization infrastructure selected → landfill becomes practical fallback.")
    else:
        why.append("Valorization outlets exist → landfill should remain fallback.")

    return score, why

routes = []

s, why = route_score_road()
routes.append({
    "Route": "Road construction / aggregates (recycling route)",
    "Score": float(s),
    "Why": why,
    "Pros": [
        "High-volume outlet (good for typical slag quantities)",
        "Can replace natural aggregates when compliant",
        "Strong circular-economy pathway in many regions"
    ],
    "Cons": [
        "Requires stability (expansion) control and QA testing",
        "EU/German compliance often requires leaching tests and documented suitability",
        "Amber/Red screening may restrict use to controlled applications"
    ]
})

s, why = route_score_cement()
routes.append({
    "Route": "Cement / binder use (often as encapsulation route)",
    "Score": float(s),
    "Why": why,
    "Pros": [
        "High-value route when technically and environmentally compliant",
        "Encapsulation may reduce leaching risk in some formulations",
        "Can contribute to resource efficiency and reduced virgin material demand"
    ],
    "Cons": [
        "Strict product and compliance requirements",
        "May require blending/conditioning and extensive testing",
        "High-risk screening may still block use depending on regulations"
    ]
})

s, why = route_score_metal_recovery()
routes.append({
    "Route": "Metal recovery first (beneficiation), then choose final outlet",
    "Score": float(s),
    "Why": why,
    "Pros": [
        "Recovers metallic value and improves resource efficiency",
        "Can reduce mass to landfill by enabling better downstream reuse",
        "Works as a pre-treatment even when direct reuse is constrained"
    ],
    "Cons": [
        "Requires equipment and logistics",
        "Economic value depends on metallic Fe and process efficiency",
        "Residual slag still needs a compliant outlet"
    ]
})

s, why = route_score_landfill()
routes.append({
    "Route": "Landfill / disposal (fallback)",
    "Score": float(s),
    "Why": why,
    "Pros": [
        "Clear compliance pathway when reuse is infeasible",
        "Operationally straightforward if permitted"
    ],
    "Cons": [
        "Loss of resource value and circularity benefits",
        "Long-term liability and costs",
        "Should be last resort when recycling routes are feasible"
    ]
})

routes_sorted = sorted(routes, key=lambda r: r["Score"], reverse=True)

st.subheader("EU-style screening summary (from your trace-metal inputs)")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Chromium (Cr)", cr_label)
k2.metric("Lead (Pb)", pb_label)
k3.metric("Zinc (Zn)", zn_label)
k4.metric("Overall screening", env_badge)

st.caption(
    "Green/Amber/Red are **screening flags** based on the thresholds you selected. "
    "They are not a substitute for leaching tests or legal determination."
)

st.divider()
st.subheader("Recommended recycling route ranking")

c1, c2, c3 = st.columns(3)
c1.metric("Recommended", routes_sorted[0]["Route"])
c2.metric("Alternative", routes_sorted[1]["Route"])
c3.metric("Third option", routes_sorted[2]["Route"])

st.divider()
left, right = st.columns([1.25, 1])

with left:
    st.subheader("Route reasoning + pros/cons")
    for i, r in enumerate(routes_sorted):
        tag = "✅ Recommended" if i == 0 else ("🟡 Alternative" if i == 1 else "⚪ Other")
        with st.expander(f"{tag}: {r['Route']}  (Score: {r['Score']:.1f})", expanded=(i == 0)):
            st.markdown("**Key reasons (based on your inputs):**")
            for w in r["Why"]:
                st.write(f"- {w}")

            st.markdown("**Pros:**")
            for p in r["Pros"]:
                st.write(f"- {p}")

            st.markdown("**Cons:**")
            for c in r["Cons"]:
                st.write(f"- {c}")

with right:
    st.subheader("Required actions (recycling-first)")
    st.markdown(
        "These are practical steps commonly needed before recycling/alternative applications."
    )
    for a in actions:
        st.write(f"- {a}")

    st.divider()
    st.subheader("Quick cautions")
    if free_cao_risk == "High":
        st.warning("High expansion risk: prioritize aging/conditioning before any structural application.")
    if env_overall == "High":
        st.warning("High environmental screening: reuse may be restricted; expect strict testing and possible controlled-use requirements.")
    if not (cement_outlet or road_outlet or metal_recovery_outlet):
        st.error("No recycling outlets selected. Landfill may dominate if available.")
    if not landfill_outlet:
        st.info("Landfill OFF: ensure at least one viable recycling outlet is available and compliant.")

    st.divider()
    st.subheader("Source links (optional)")
    if any([src_ersatz, src_depv, src_state]):
        if src_ersatz:
            st.write(f"- ErsatzbaustoffV / Mantelverordnung: {src_ersatz}")
        if src_depv:
            st.write(f"- DepV: {src_depv}")
        if src_state:
            st.write(f"- State/technical guidance: {src_state}")
    else:
        st.caption("Paste your regulation/standard links in the sidebar if you want the app to display them here.")

st.divider()




