# Domain, hosting and growth recommendations — October 6, 2026

## Domain

First choice: **utahseasonalguide.com**. It matches the site's name, describes the year-round scope and is easy to spell. A direct Verisign .com registry RDAP check on October 6 returned HTTP 404 (no registered domain found). The comparison lookup for utahcelebrates.com returned a registered domain. This is a registration-status check, not a reservation; registrar checkout must confirm current availability and the final price. No domain was purchased.

Registry endpoints: https://rdap.verisign.com/com/v1/domain/utahseasonalguide.com and https://rdap.verisign.com/com/v1/domain/utahcelebrates.com .

## Registration and hosting

| Option | Published standard .com cost | Practical choice |
|---|---:|---|
| Porkbun | $11.08/year registration and renewal | Recommended for straightforward registration, free WHOIS privacy and flexible DNS. Keep Netlify hosting. |
| Cloudflare Registrar | $10.46/year registration and renewal | Slightly cheaper; requires using Cloudflare's nameservers. Hosting can still remain on Netlify. |
| Netlify Free credit plan | $0/month; 300 credits/month | Keep the existing GitHub/Netlify workflow while traffic is modest. Watch usage rather than buying a hosting package immediately. |

Prices checked October 6, 2026; non-premium domains. Netlify's current credit plans have free, unlimited Forms submissions, but legacy plans differ. The site's actual plan remains unverified behind account sign-in. Forms detection must be enabled regardless of plan. Domain ownership contact details must be accurate; use supported WHOIS privacy rather than publishing a personal name on the website.

A dedicated Gmail can receive private form notifications. Later, a domain-based contact address can be used: Porkbun offers free forwarding; a full mailbox is separately advertised at $3/month, billed annually. Forwarding is receiving mail, not a complete send-and-reply mailbox.

Sources: https://porkbun.com/products/domains ; https://pricing.registrar.cloudflare.com/ ; https://developers.cloudflare.com/registrar/get-started/register-domain/ ; https://www.netlify.com/pricing/ ; https://www.netlify.com/changelog/2026-04-14-pricing-updates-april-2026/ .

## Apps

Use the installable web app first. It gives the guide a home-screen icon and its own window, with saved events, filters, calendars and cached browsing from the same codebase. Native installation, calendar import and private-preview authentication still need physical-device checks.

A dedicated iOS/Android app is technically viable, especially once there is demand for account-based saved lists, saved-event change alerts, a useful map and stronger offline trip planning. A cross-platform implementation can reuse much of the web work, but publishing, native testing, account verification and updates add ongoing work. A bare website wrapper is a weaker App Store proposition: Apple's minimum-functionality rules ask for utility beyond repackaging a website.

Published account fees: Apple Developer Program $99/year; Google Play Console $25 once. These are account fees, not development/maintenance estimates. Organization identity and store disclosure requirements need review if keeping personal identity off public listings is a priority.

Sources: https://developer.apple.com/support/compare-memberships/ ; https://support.google.com/googleplay/android-developer/answer/6112435 ; https://developer.apple.com/app-store/review/guidelines/ .

## Recommended additions, in order

1. Easy listing corrections and accommodation feedback. Already introduced; verify real form receipt before launch.
2. Visitor photo submissions with permission, credit, useful captions and review before publication. Event/date context makes photos useful; strip private location metadata from uploads.
3. Structured visitor tips: parking, crowds, terrain, sensory conditions and what age groups enjoyed it. Date the feedback and distinguish visitor reports from organizer-confirmed access details.
4. Shareable outing lists and a map that helps combine nearby events. Saved lists currently remain local and exportable; shared/cloud lists would require additional functionality.
5. Opt-in alerts when a saved event changes date, sells out or is cancelled. Do not imply reminders are active in the current build.
6. Customer reviews after a moderation and correction process is in place. Begin with practical tips rather than a star score dominated by a few early reviewers.

Keep ordinary inclusion free and paid placements visibly labeled. Sponsorship pricing research and the $35/week or $99/month pilot recommendation are in sponsorship-rates-2026-10-06.md. No advertiser is currently displayed.
