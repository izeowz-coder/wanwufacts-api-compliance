from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "evidence"
OUTPUT.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#5F6B7D")
BLUE = colors.HexColor("#3157D5")
BLUE_DEEP = colors.HexColor("#17358F")
PALE = colors.HexColor("#EEF2FB")
MINT = colors.HexColor("#DFF5F2")
LINE = colors.HexColor("#D9DFEB")
WHITE = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverEyebrow",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8,
    leading=11,
    textColor=BLUE,
    spaceAfter=14,
    tracking=1.5,
    uppercase=True,
))
styles.add(ParagraphStyle(
    name="CoverTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=34,
    leading=38,
    textColor=INK,
    alignment=TA_LEFT,
    spaceAfter=16,
))
styles.add(ParagraphStyle(
    name="CoverSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=13,
    leading=20,
    textColor=MUTED,
    spaceAfter=24,
))
styles.add(ParagraphStyle(
    name="SectionTitle",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=21,
    leading=25,
    textColor=INK,
    spaceBefore=6,
    spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="Subhead",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=15,
    textColor=BLUE_DEEP,
    spaceBefore=12,
    spaceAfter=7,
))
styles.add(ParagraphStyle(
    name="Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.4,
    leading=14.2,
    textColor=MUTED,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="Small",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=7.7,
    leading=11,
    textColor=MUTED,
))
styles.add(ParagraphStyle(
    name="BulletBody",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=9.2,
    leading=13.8,
    textColor=MUTED,
    leftIndent=14,
    firstLineIndent=-8,
    bulletIndent=2,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="Callout",
    parent=styles["BodyText"],
    fontName="Helvetica-Bold",
    fontSize=10,
    leading=15,
    textColor=INK,
    borderColor=BLUE,
    borderWidth=0,
    borderPadding=10,
    backColor=MINT,
    spaceBefore=8,
    spaceAfter=12,
))


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 9.5 * mm, "Wanwu Facts Publisher - API Compliance Evidence")
    canvas.drawRightString(190 * mm, 9.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def p(text: str, style: str = "Body") -> Paragraph:
    return Paragraph(text, styles[style])


def bullets(items: list[str]) -> list[Paragraph]:
    return [Paragraph(f"- {item}", styles["BulletBody"]) for item in items]


def info_table(rows: list[list[str]], widths: list[float] | None = None) -> Table:
    data = [[p(cell, "Small") for cell in row] for row in rows]
    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PALE),
        ("TEXTCOLOR", (0, 0), (-1, 0), INK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.55, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def cover_story() -> list:
    identifiers = info_table([
        ["Field", "Value"],
        ["API client", "Wanwu Facts Publisher"],
        ["Operator", "Independent developer / sole proprietor"],
        ["Google Cloud project ID", "vaulted-acolyte-503301-u0"],
        ["Google Cloud project number", "32758473057"],
        ["Authorized channel ID", "UCr240l6wo4xEH45LKd1TreA"],
        ["Public documentation", "https://izeowz-coder.github.io/wanwufacts-api-compliance/"],
    ], [48 * mm, 117 * mm])
    return [
        Spacer(1, 22 * mm),
        p("YOUTUBE DATA API SERVICES", "CoverEyebrow"),
        p("Wanwu Facts Publisher", "CoverTitle"),
        p(
            "Compliance evidence for a private, single-owner publishing client "
            "that uploads original educational videos to one owner-controlled channel.",
            "CoverSubtitle",
        ),
        p(
            "Single authorized owner  |  Two minimum OAuth scopes  |  "
            "No public accounts  |  No engagement automation  |  30-day API data limit",
            "Callout",
        ),
        Spacer(1, 4 * mm),
        identifiers,
        Spacer(1, 8 * mm),
        p("Prepared 23 July 2026", "Small"),
        p(
            "No API keys, OAuth codes, access tokens, refresh tokens or user login "
            "credentials are included in this evidence pack.",
            "Small",
        ),
    ]


def overview_story() -> list:
    return [
        p("1. Application purpose", "SectionTitle"),
        p(
            "Wanwu Facts Publisher converts the operator's already verified source "
            "material into original Mandarin educational videos. It creates an original "
            "script, narration, subtitles, graphics, thumbnail and rendered video; "
            "performs source and safety checks; verifies the immutable authorized channel "
            "ID; and uploads only to the owner-controlled Wanwu Facts channel."
        ),
        p("Access boundary", "Subhead"),
        *bullets([
            "No public sign-up, customer dashboard or multi-tenant access.",
            "The only OAuth user is the channel owner.",
            "The client is not sold and does not operate unrelated third-party channels.",
            "It does not automate views, likes, comments, subscriptions or recommendations.",
        ]),
        p("Owner controls", "Subhead"),
        *bullets([
            "The owner authorizes OAuth and confirms the immutable channel ID.",
            "The owner selects scheduled public, private or unlisted visibility.",
            "Title, description, tags, visibility, schedule, source evidence and safety audit are recorded before upload.",
            "Production requires separate API-audit and automation switches; missing approval fails closed.",
        ]),
        p("Normal volume", "Subhead"),
        p(
            "Two uploads per week: one landscape video and one vertical Short from the "
            "same approved topic. This is approximately 104 videos.insert calls per year. "
            "The default quota is sufficient."
        ),
    ]


def api_story() -> list:
    rows = [
        ["Method", "Purpose", "Stored result", "Maximum retention"],
        ["channels.list", "Verify authenticated channel ID.", "Channel match result.", "30 days"],
        ["videos.insert", "Upload owner-approved video and metadata.", "Video ID, schedule, result.", "30 days"],
        ["thumbnails.set", "Attach original thumbnail.", "Success or failure.", "30 days"],
        ["videos.list", "Confirm processing succeeds.", "Temporary processing status.", "30 days"],
    ]
    return [
        p("2. API use and OAuth scope rationale", "SectionTitle"),
        p("Requested OAuth scopes", "Subhead"),
        *bullets([
            "<b>youtube.upload</b> - required to upload original owner-approved videos.",
            "<b>youtube.readonly</b> - required to verify authenticated channel identity and processing status.",
            "No YouTube Analytics, Reporting, full-account management, Google Drive, Gmail or profile scopes are requested.",
        ]),
        Spacer(1, 4 * mm),
        info_table(rows, [27 * mm, 59 * mm, 47 * mm, 32 * mm]),
        Spacer(1, 7 * mm),
        p("Video metadata and visibility", "Subhead"),
        p(
            "The client always supplies title and description. The account owner can "
            "choose scheduled public, private or unlisted. Scheduled publication is "
            "implemented by uploading privately with a future publishAt value, as required "
            "by the YouTube Data API. The client does not change the visibility of existing videos."
        ),
    ]


def architecture_story() -> list:
    boxes = [
        ["1", "Owner consent", "OAuth grants upload and channel-read access."],
        ["2", "Local production", "Original script, audio, graphics and video."],
        ["3", "Safety audit", "Sources, claims, media and metadata checked."],
        ["4", "Identity lock", "Authorized channel ID must exactly match."],
        ["5", "Upload and verify", "Upload, processing check, record, then prune."],
    ]
    table = Table(
        [[p(n, "Small"), p(title, "Small"), p(body, "Small")] for n, title, body in boxes],
        colWidths=[10 * mm, 42 * mm, 112 * mm],
        hAlign="LEFT",
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLUE),
        ("TEXTCOLOR", (0, 0), (0, -1), WHITE),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.6, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    return [
        p("3. Architecture and data flow", "SectionTitle"),
        table,
        Spacer(1, 8 * mm),
        p("Execution environment", "Subhead"),
        *bullets([
            "GitHub Actions runs the private application from a private source repository.",
            "OAuth client ID, client secret, refresh token and expected channel ID are stored as repository secrets.",
            "Rendered media and evidence are produced in the runner; temporary audit artifacts expire after no more than 14 days.",
            "The public documentation repository contains no credentials and no private production source code.",
        ]),
        p("Fail-closed controls", "Subhead"),
        *bullets([
            "OAuth token refresh must succeed.",
            "The authenticated channel ID must equal UCr240l6wo4xEH45LKd1TreA.",
            "The API compliance approval flag must be present.",
            "The separate automation flag must be present for scheduled runs.",
            "Safety, source and media checks must pass before upload.",
        ]),
    ]


def privacy_story() -> list:
    return [
        p("4. Privacy and authorized data", "SectionTitle"),
        p(
            "The client uses YouTube API Services only for channel verification, upload, "
            "processing confirmation, retry safety and publication records. It does not "
            "sell API data, profile viewers, serve advertising or disclose authorized data "
            "to unrelated third parties."
        ),
        p("Data accessed", "Subhead"),
        *bullets([
            "Channel ID and basic channel metadata.",
            "Owner-created title, description, tags, thumbnail, video file and schedule.",
            "Upload-session information, video ID and temporary processing status.",
            "OAuth refresh token retained only while the authorization remains active.",
        ]),
        p("Retention and deletion", "Subhead"),
        *bullets([
            "Completed YouTube API response data is automatically deleted no later than 30 days after completion.",
            "Build and audit artifacts expire after no more than 14 days.",
            "Verified deletion requests are completed as soon as practical and within seven calendar days.",
            "Revocation is available through Google Account security settings.",
            "Deleting client-held data does not delete content stored by YouTube.",
        ]),
        p("Security", "Subhead"),
        *bullets([
            "Least-privilege OAuth scopes.",
            "GitHub Actions Secrets; no secrets in source control or logs.",
            "Immutable channel-ID verification.",
            "Short artifact retention and automatic API-data pruning.",
            "Separate compliance and automation switches.",
        ]),
    ]


def evidence_story() -> list:
    return [
        p("5. Evidence and review checklist", "SectionTitle"),
        p("Public documentation", "Subhead"),
        *bullets([
            "Homepage: https://izeowz-coder.github.io/wanwufacts-api-compliance/",
            "Privacy Policy: https://izeowz-coder.github.io/wanwufacts-api-compliance/privacy.html",
            "Terms of Use: https://izeowz-coder.github.io/wanwufacts-api-compliance/terms.html",
            "Deletion and revocation: https://izeowz-coder.github.io/wanwufacts-api-compliance/data-deletion.html",
        ]),
        p("Actual screenshots to attach separately", "Subhead"),
        *bullets([
            "Google OAuth consent page showing the API client name and both requested YouTube scopes.",
            "Google Account third-party access page showing the revocation path.",
            "GitHub Actions manual-run page showing scheduled public, private and unlisted choices.",
            "Dry-run manifest showing title, description, visibility and schedule without uploading.",
        ]),
        p("Operator attestation boundary", "Subhead"),
        p(
            "The applicant must enter their legal name, contact email and required "
            "attestations directly in the official form. Credentials and tokens must never "
            "be included in screenshots, documents or support correspondence."
        ),
        p("Policy references", "Subhead"),
        *bullets([
            "YouTube Terms of Service: https://www.youtube.com/t/terms",
            "Google Privacy Policy: https://policies.google.com/privacy",
            "Google authorization revocation: https://security.google.com/settings/security/permissions",
            "YouTube API Developer Policies: https://developers.google.com/youtube/terms/developer-policies",
        ]),
    ]


def terms_story() -> list:
    return [
        p("Terms of Use", "SectionTitle"),
        p(
            "Wanwu Facts Publisher is a private internal client intended only for the "
            "authenticated owner of the configured channel. Use is also subject to the "
            "YouTube Terms of Service and YouTube API Services policies."
        ),
        p("Authorized use", "Subhead"),
        *bullets([
            "Operate only the owner-controlled Wanwu Facts channel.",
            "Upload only material for which the owner has the necessary rights.",
            "Use the owner-selected visibility and do not alter existing video visibility.",
            "Disclose program-generated narration and graphics where appropriate.",
        ]),
        p("Prohibited use", "Subhead"),
        *bullets([
            "No automated views, likes, comments, subscriptions or engagement.",
            "No scraping, viewer profiling or derived YouTube metrics.",
            "No spam, deceptive content or circumvention of quota and audit controls.",
            "No sale, sublicensing or operation of unrelated third-party channels.",
        ]),
        p("Termination", "Subhead"),
        p(
            "The owner may disable automation or revoke Google access at any time. The "
            "operator may suspend the client for security, compliance, reliability or "
            "platform-policy changes."
        ),
    ]


def build(filename: str, story: list) -> None:
    doc = SimpleDocTemplate(
        str(OUTPUT / filename),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=19 * mm,
        bottomMargin=22 * mm,
        title="Wanwu Facts Publisher API Compliance Evidence",
        author="Wanwu Facts Publisher",
        subject="YouTube Data API Services compliance audit evidence",
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


build(
    "audit-evidence-complete.pdf",
    cover_story()
    + [PageBreak()]
    + overview_story()
    + [PageBreak()]
    + api_story()
    + [PageBreak()]
    + architecture_story()
    + [PageBreak()]
    + privacy_story()
    + [PageBreak()]
    + evidence_story(),
)
build("01-homepage-and-overview.pdf", cover_story() + [PageBreak()] + overview_story())
build("02-privacy-policy.pdf", privacy_story())
build("03-terms-of-use.pdf", terms_story())
build("04-oauth-and-upload-flow.pdf", api_story())
build("05-architecture.pdf", architecture_story())

print(f"Generated audit PDFs in {OUTPUT}")
