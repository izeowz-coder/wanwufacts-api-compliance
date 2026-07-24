# YouTube API Services audit answer draft

This document contains non-secret, project-specific answers for the YouTube API Services Audit and Quota Extension Form. The applicant must enter their legal name, contact email and attestations directly in the official form.

## Request type

- **Selection:** Complete a compliance audit to request additional quota.
- **Clarification:** The primary purpose is to complete the compliance audit required to remove the private-only upload restriction for an API project created after 28 July 2020. The current default quota is sufficient for the stated use case.

## Applicant

- **Applicant type:** Individual user.
- **Organization size/type:** Independent Developer / Sole Proprietor.
- **Primary business category:** Digital media / education, or Other: original educational science and everyday-knowledge publishing.
- **Legal name and contact email:** Enter privately in the official form.
- **Content Owner ID:** Not applicable.
- **Google Ads Customer ID:** Not applicable.

## API project

- **Google Cloud project name:** My Project 31941
- **Project ID:** `vaulted-acolyte-503301-u0`
- **Project number:** `32758473057`
- **YouTube channel ID:** `UCr240l6wo4xEH45LKd1TreA`
- **Channel URL:** https://www.youtube.com/channel/UCr240l6wo4xEH45LKd1TreA

## API client

- **API client name:** Wanwu Facts Publisher
- **Does the name contain “YouTube”?** No.
- **Primary access URL:** https://izeowz-coder.github.io/wanwufacts-api-compliance/
- **Privacy Policy URL:** https://izeowz-coder.github.io/wanwufacts-api-compliance/privacy.html
- **Terms of Service URL:** https://izeowz-coder.github.io/wanwufacts-api-compliance/terms.html
- **Is the API client publicly accessible?** No. It is a private, single-owner internal GitHub Actions application. Its compliance documentation is public.
- **Use case:** Internal Company Tool. If the form requires “Other”, use: “Single-owner internal publishing automation for one owner-controlled educational channel.”
- **Does the API client require Google OAuth?** Yes.

## Plain-language product description

Wanwu Facts Publisher is a private, single-owner automation client that converts the operator's already verified educational source material into original Mandarin videos. It generates an original script, narration, subtitles, graphics, thumbnail and rendered video, performs source and safety checks, verifies the immutable authorized channel ID, and uploads only to the operator-controlled Wanwu Facts channel. The client is not offered to the public, has no third-party users, does not operate unrelated channels and does not automate engagement.

## YouTube API operations

- `channels.list(part=id,snippet, mine=true)` verifies that the authenticated user controls the configured channel.
- `videos.insert(part=snippet,status)` uploads an original video and owner-selected metadata.
- `thumbnails.set` attaches the original thumbnail.
- `videos.list(part=status,processingDetails)` confirms that processing completes.
- OAuth token refresh is used so the owner does not need to reauthorize every scheduled run.

## OAuth scopes

- `https://www.googleapis.com/auth/youtube.upload`: required to upload original owner-approved videos.
- `https://www.googleapis.com/auth/youtube.readonly`: required to verify the authenticated channel identity and confirm processing status.

No broader YouTube management, Analytics, Reporting, Google Drive, Gmail or profile scopes are requested.

## Owner control

The owner authorizes OAuth once, confirms the immutable channel ID, selects a visibility mode and separately enables the production schedule. Supported visibility modes are scheduled public, private and unlisted. Title, description, tags, visibility, schedule, source evidence and safety audit are written to a downloadable manifest before upload. Production fails closed unless both API audit approval and the separate automation switch are enabled.

## Data access, storage and deletion

The client accesses only channel identity data, upload-session information, video IDs, processing status and owner-created upload files and metadata. OAuth secrets are held only in GitHub Actions Secrets and are not committed or logged. Completed YouTube API response data is automatically deleted no later than 30 days after completion. Build and audit artifacts expire after no more than 14 days. Verified deletion requests are completed within seven calendar days. Access can be revoked at any time through Google Account security settings.

## API usage volume

- Two video uploads per week: one landscape video and one vertical Short derived from the same approved topic.
- Approximately 104 `videos.insert` calls per year in normal operation.
- One `channels.list` identity check per upload.
- One optional `thumbnails.set` call for the landscape video.
- A small number of `videos.list` processing checks immediately after each upload.
- No search, comments, likes, subscriptions, analytics or bulk channel operations.
- Current default quota is sufficient; no high-volume quota is required.

## Monetization and third parties

- No sale of API data.
- No advertising in the API client.
- No viewer profiling, audience analytics or derived YouTube metrics.
- No public accounts, customers or unrelated channel owners.
- GitHub Actions and Google/YouTube are the only infrastructure providers required for operation.

## Required evidence checklist

Ready in this repository:

- public homepage and API-client overview;
- public Privacy Policy;
- public Terms of Use;
- public data deletion and authorization revocation instructions;
- architecture and data-flow evidence PDF;
- OAuth scope rationale;
- upload control and retention documentation.

Still requires an actual screenshot from the signed-in Google account:

1. OAuth consent page showing **Wanwu Facts Publisher** and both requested YouTube scopes;
2. Google Account third-party access page showing how authorization can be revoked;

Ready as verified workflow evidence:

3. a successful GitHub Actions dry run with owner-selected private visibility and the production switches disabled; and
4. a sanitized manifest showing title, description, visibility and planned schedule without uploading a video.

The detailed workflow record and sanitized manifest should be submitted
privately as audit attachments. They are intentionally not published on the
public compliance site.

Do not submit credentials, authorization codes, tokens or repository secrets as evidence.
