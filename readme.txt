NXS Upgrade Prompt (v1.0.0)
===========================

What it is
----------
A lightweight WordPress shortcode that renders a membership upgrade banner based on a JSON rules file (the same structure as `membership_upgrade_rules.json`).

How to install
--------------
1) Upload the `nxs-upgrade-prompt` folder as a plugin, or install the ZIP via Plugins → Add New → Upload Plugin.
2) Activate the plugin.
3) Create a page and add the shortcode:

[nxs_upgrade_prompt
  rules_url="{YOUR_RULES_JSON_URL}"
  member_id="demo_member_123"
  current_tier="Explorer"
  credits_used_pct="0.83"
  peak_bookings_14d="2"
  waitlist_events_30d="1"
  household_members="4"
  has_annual="false"
  recent_renewals_count="3"
  upgrade_url="https://portal.nationalsportsdome.com/upgrade?familyplus"
  keep_url="https://portal.nationalsportsdome.com/keep-current"
  compare_url="https://nationalsportsdome.com/memberships"
]

Notes
-----
- The shortcode attributes map directly to the internal fields required by the rules engine.
- You can populate these dynamically using your member portal or WP hooks (e.g., logged-in user meta, query params).
- The JS fetches `rules_url` at runtime; host your JSON at a public URL or within WordPress (Media Library).

Security
--------
- Do not expose sensitive PII in the page HTML. Prefer opaque IDs (e.g., a hashed member ID) and resolve the real identity server-side during the upgrade flow.

Changelog
---------
- 2025-10-02 – Initial release.

