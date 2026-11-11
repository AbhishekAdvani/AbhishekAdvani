"""Render the accessible SVG cards used by the GitHub profile README.

Set STATIC=1 to emit a still version without animation.
"""

from html import escape
import os
from pathlib import Path
import re


CARDS = Path(__file__).resolve().parents[1] / "cards"
CARDS.mkdir(exist_ok=True)
STATIC = os.getenv("STATIC") == "1"
PORTRAIT_SOURCE = CARDS / "dotted_portrait (1).svg"
portrait_svg = PORTRAIT_SOURCE.read_text()
PORTRAIT_MARKUP = portrait_svg[portrait_svg.find(">") + 1 : portrait_svg.rfind("</svg>")]
PORTRAIT_MARKUP = re.sub(
    r'(<circle\b[^>]*\br=")([0-9.]+)(")',
    lambda match: f"{match.group(1)}{float(match.group(2)) * 3}{match.group(3)}",
    PORTRAIT_MARKUP,
)

COLORS = {
    "blue": "#0B4885",
    "blue_dark": "#083156",
    "green": "#163D2A",
    "moss": "#8EA97B",
    "ink": "#202A35",
    "muted": "#667384",
    "line": "#E4EAF0",
    "paper": "#F7F8FC",
}

STYLE = """<style>
  text{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}
  .serif{font-family:'Playfair Display',Georgia,'Times New Roman',serif}
  .mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
  .eyebrow{fill:#0B4885;font-size:13px;font-weight:700;letter-spacing:2.2px}
  .muted{fill:#667384}
  @keyframes enter{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
  @keyframes drift{50%{transform:translateY(-5px)}}
  @keyframes dash{to{stroke-dashoffset:-48}}
  .enter{animation:enter .75s ease-out both}
  .drift{animation:drift 5s ease-in-out infinite}
  .dash{animation:dash 6s linear infinite}
  @media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""

STATIC_STYLE = """<style>
  text{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif}
  .serif{font-family:'Playfair Display',Georgia,'Times New Roman',serif}
  .mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
  .eyebrow{fill:#0B4885;font-size:13px;font-weight:700;letter-spacing:2.2px}
  .muted{fill:#667384}
</style>"""


def render(name, width, height, title, description, body):
    safe_title = escape(title)
    safe_description = escape(description)
    style = STATIC_STYLE if STATIC else STYLE
    markup = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{name}-title {name}-description">
  <title id="{name}-title">{safe_title}</title>
  <desc id="{name}-description">{safe_description}</desc>
  <defs>
    <linearGradient id="canvas" x2="1" y2="1"><stop stop-color="#FFFFFF"/><stop offset="1" stop-color="#F7F8FC"/></linearGradient>
    <linearGradient id="brand" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#163D2A"/><stop offset="1" stop-color="#0B4885"/></linearGradient>
  </defs>
  {style}
  <rect width="{width}" height="{height}" rx="24" fill="url(#canvas)"/>
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="23" fill="none" stroke="#E4EAF0"/>
  {body}
</svg>'''
    (CARDS / f"{name}.svg").write_text(markup)


render(
    "hero",
    1200,
    360,
    "Abhishek Advani — engineering profile",
    "I solve business problems with technology. SAP and MERN engineering from architecture through delivery.",
    '''
  <circle cx="1060" cy="35" r="190" fill="#EDF4EF"/>
  <circle cx="1090" cy="320" r="140" fill="#EAF1F8"/>
  <defs><clipPath id="portraitClip"><circle cx="1004" cy="180" r="166"/></clipPath></defs>
  <circle cx="1004" cy="180" r="171" fill="#FFFFFF" stroke="#DCE7E0" stroke-width="2"/>
  <g clip-path="url(#portraitClip)">
    <svg x="838" y="14" width="332" height="332" viewBox="0 0 1200 1200" preserveAspectRatio="xMidYMid meet">
      {PORTRAIT_MARKUP}
    </svg>
  </g>
  <rect x="54" y="48" width="4" height="272" rx="2" fill="url(#brand)"/>
  <g class="enter">
    <text x="82" y="76" class="eyebrow">ENGINEERING  /  ARCHITECTURE  /  DELIVERY</text>
    <text x="78" y="156" class="serif" fill="#163D2A" font-size="66" font-weight="700">Abhishek Advani</text>
    <text x="82" y="202" fill="#0B4885" font-size="22" font-weight="600">SAP BTP · Full-Stack Engineering · Technical Leadership</text>
    <text x="82" y="248" fill="#163D2A" font-size="20" font-weight="700">I solve business problems with technology.</text>
    <text x="82" y="276" fill="#667384" font-size="15">Built, not born. Designing the next version through focus, consistency and judgment.</text>
    <text x="82" y="313" fill="#667384" font-size="15">SAP RAP  /  OData  /  CAP  /  React  /  Node.js  /  Cloud Foundry</text>
  </g>
'''.replace("    {PORTRAIT_MARKUP}", "    " + PORTRAIT_MARKUP),
)


cards = [
    (
        "enterprise",
        "01 / ENTERPRISE",
        "SAP & Integrations",
        "ABAP RAP · CDS · OData · Fiori",
        "Enterprise SAP solutions and integrations using ABAP RAP, CDS, OData and Fiori.",
        "SAP",
        "#0B4885",
        "#EAF1F8",
    ),
    (
        "platform",
        "02 / PLATFORM",
        "Cloud & Full Stack",
        "SAP BTP · CAP · React · Node.js",
        "Cloud and full-stack platforms built with SAP BTP, CAP, React and Node.js.",
        "DEV",
        "#163D2A",
        "#EDF4EF",
    ),
    (
        "leadership",
        "03 / DELIVERY",
        "Engineering Leadership",
        "Architecture · QA · Releases",
        "Technical leadership across architecture, quality assurance and releases.",
        "LEAD",
        "#0B4885",
        "#EAF1F8",
    ),
]

for name, eyebrow, heading, detail, description, badge, accent, tint in cards:
    render(
        name,
        360,
        210,
        heading,
        description,
        f'''
  <rect x="1" y="1" width="358" height="5" rx="2.5" fill="{accent}"/>
  <text x="25" y="39" class="eyebrow" font-size="10">{escape(eyebrow)}</text>
  <circle cx="310" cy="49" r="25" fill="{tint}"/>
  <text x="310" y="53" text-anchor="middle" fill="{accent}" font-size="9" font-weight="800">{escape(badge)}</text>
  <text x="25" y="100" class="serif" fill="#202A35" font-size="24" font-weight="700">{escape(heading)}</text>
  <path d="M25 122H335" stroke="#E4EAF0"/>
  <text x="25" y="153" fill="#667384" font-size="13">{escape(detail)}</text>
  <circle cx="28" cy="180" r="3" fill="{accent}"/>
  <text x="39" y="184" fill="#667384" font-size="11">Enterprise-ready delivery</text>''',
    )


story_cards = [
    (
        "story_patterns",
        "01 / AWARENESS",
        "Recognize the pattern",
        ("When the urge to change everything takes over,", "pause and choose what matters most."),
        "Notice when the urge to change everything competes with the work that matters most.",
        "NOTICE",
        "#0B4885",
        "#EAF1F8",
    ),
    (
        "story_patience",
        "02 / PATIENCE",
        "Stay with the climb",
        ("Consistency lets ambition compound.", "Recovery and patience belong in the plan."),
        "Practice sustainable consistency, patience and recovery as part of long-term growth.",
        "SUSTAIN",
        "#163D2A",
        "#EDF4EF",
    ),
    (
        "story_practice",
        "03 / PRACTICE",
        "Practice the next self",
        ("Prioritize, communicate, delegate, own outcomes—", "one leadership decision at a time."),
        "Build toward leadership through prioritization, communication, delegation and ownership.",
        "REPEAT",
        "#0B4885",
        "#EAF1F8",
    ),
]

for name, eyebrow, heading, detail_lines, description, badge, accent, tint in story_cards:
    detail_first, detail_second = (escape(line) for line in detail_lines)
    render(
        name,
        360,
        220,
        heading,
        description,
        f'''
  <rect x="1" y="1" width="358" height="5" rx="2.5" fill="{accent}"/>
  <text x="25" y="39" class="eyebrow" font-size="10">{escape(eyebrow)}</text>
  <path d="M278 70L295 48L310 65L325 51L345 73" fill="none" stroke="{tint}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M278 70L295 48L310 65L325 51L345 73" fill="none" stroke="{accent}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="25" y="96" class="serif" fill="#202A35" font-size="23" font-weight="700">{escape(heading)}</text>
  <path d="M25 115H335" stroke="#E4EAF0"/>
  <text x="25" y="143" fill="#667384" font-size="12.5"><tspan x="25">{detail_first}</tspan><tspan x="25" dy="18">{detail_second}</tspan></text>
  <rect x="25" y="178" width="77" height="23" rx="11.5" fill="{tint}"/>
  <text x="63.5" y="193" text-anchor="middle" fill="{accent}" font-size="9" font-weight="800" letter-spacing="1">{escape(badge)}</text>''',
    )


render(
    "architecture",
    1200,
    315,
    "SAP and MERN stack architecture",
    "Two distinct architecture paths: SAP S/4HANA, ABAP RAP and CDS, OData and CAP, Fiori and SAPUI5, SAP BTP and Cloud Foundry; and MongoDB, Express, React, Node.js and cloud deployment.",
    '''
  <text x="38" y="47" class="eyebrow">SYSTEMS I BUILD</text>
  <text x="38" y="83" class="serif" fill="#163D2A" font-size="29" font-weight="700">SAP &amp; MERN stack architecture</text>
  <text x="40" y="119" fill="#163D2A" font-size="12" font-weight="800" letter-spacing="1.5">SAP STACK</text>
  <text x="40" y="222" fill="#0B4885" font-size="12" font-weight="800" letter-spacing="1.5">MERN STACK</text>
  <g text-anchor="middle" fill="#202A35" font-size="13" font-weight="600">
    <rect x="40" y="132" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C9D9CC"/><text x="130" y="165">SAP S/4HANA</text>
    <rect x="275" y="132" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C9D9CC"/><text x="365" y="165">ABAP RAP / CDS</text>
    <rect x="510" y="132" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C9D9CC"/><text x="600" y="165">OData / CAP</text>
    <rect x="745" y="132" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C9D9CC"/><text x="835" y="165">Fiori / SAPUI5</text>
    <rect x="980" y="132" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C9D9CC"/><text x="1070" y="165">SAP BTP / Cloud Foundry</text>
    <rect x="40" y="235" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C7D7E8"/><text x="130" y="268">MongoDB</text>
    <rect x="275" y="235" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C7D7E8"/><text x="365" y="268">Express.js</text>
    <rect x="510" y="235" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C7D7E8"/><text x="600" y="268">React</text>
    <rect x="745" y="235" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C7D7E8"/><text x="835" y="268">Node.js</text>
    <rect x="980" y="235" width="180" height="54" rx="13" fill="#FFFFFF" stroke="#C7D7E8"/><text x="1070" y="268">Cloud Deployment</text>
  </g>
  <path d="M220 159H275 M455 159H510 M690 159H745 M925 159H980" stroke="#8EA97B" stroke-width="3" stroke-dasharray="6 6" class="dash"/>
  <path d="M220 262H275 M455 262H510 M690 262H745 M925 262H980" stroke="#0B4885" stroke-width="3" stroke-dasharray="6 6" class="dash"/>''',
)


render(
    "trajectory",
    1200,
    220,
    "The journey: builder, leader, creator, balanced life",
    "A path from building technical depth, to leading delivery, to creating independent products, while protecting balance and personal freedom.",
    '''
  <text x="38" y="43" class="eyebrow">BUILT, NOT BORN</text>
  <text x="38" y="77" class="serif" fill="#163D2A" font-size="27" font-weight="700">From solving technical problems to designing the future</text>
  <path d="M125 133H1072" stroke="#B8C9D8" stroke-width="2" stroke-dasharray="6 7" class="dash"/>
  <g text-anchor="middle">
    <circle cx="140" cy="133" r="13" fill="#0B4885"/><text x="140" y="139" fill="#FFFFFF" font-size="14" font-weight="700">1</text>
    <circle cx="445" cy="133" r="13" fill="#557B60"/><text x="445" y="139" fill="#FFFFFF" font-size="14" font-weight="700">2</text>
    <circle cx="750" cy="133" r="13" fill="#0B4885"/><text x="750" y="139" fill="#FFFFFF" font-size="14" font-weight="700">3</text>
    <circle cx="1055" cy="133" r="13" fill="#557B60"/><text x="1055" y="139" fill="#FFFFFF" font-size="14" font-weight="700">4</text>
    <text x="140" y="171" fill="#202A35" font-size="16" font-weight="700">The Builder</text>
    <text x="140" y="193" fill="#667384" font-size="12">Technical depth</text>
    <text x="445" y="171" fill="#202A35" font-size="16" font-weight="700">The Leader</text>
    <text x="445" y="193" fill="#667384" font-size="12">Architecture &amp; outcomes</text>
    <text x="750" y="171" fill="#202A35" font-size="16" font-weight="700">The Creator</text>
    <text x="750" y="193" fill="#667384" font-size="12">Products &amp; independence</text>
    <text x="1055" y="171" fill="#202A35" font-size="16" font-weight="700">The Balanced Man</text>
    <text x="1055" y="193" fill="#667384" font-size="12">Health, freedom &amp; meaning</text>
  </g>''',
)
