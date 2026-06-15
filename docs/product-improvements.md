# Product Improvements

## Current Product Weaknesses

1. Session input misses meeting type, persona, region, and deal stage.
2. Users cannot approve or remove sources before report generation.
3. Unknowns are listed but not converted into tasks.
4. Follow-up chat does not build account memory across sessions.
5. Team collaboration, review, and cost controls are missing.

## Top 3 Improvements

1. Add richer meeting context.
2. Add source review with pin, remove, and request-more controls.
3. Add account memory across sessions.

## Buyer, User, and Payment Rationale

Sales leaders, revenue operations teams, and founders buy it to reduce prep time and standardize account strategy. Account executives, sales development representatives, customer success managers, and partnerships teams use it before calls. Teams pay when briefings improve discovery quality and meeting consistency.

## Success Metrics

- Time from session creation to usable report.
- Percentage of reports opened before meetings.
- Follow-up questions per completed report.
- Source coverage per report section.
- User-rated usefulness after a meeting.
- Meetings influenced and opportunities advanced.

## 4-Week Roadmap

- Week 1: Add meeting context fields, report quality scoring, and stronger source coverage.
- Week 2: Add source review and manual source controls.
- Week 3: Add account memory and comparison against prior sessions.
- Week 4: Add team sharing, manager review, and usage analytics.

## Cost, Scaling, and Reliability Risks

Cost risk: repeated model calls during gap research. Scaling risk: long-running workflow execution inside the API process. Reliability risk: stale or unavailable sources. Mitigations: bound attempts, cache fetches, move execution to workers, and surface unknowns clearly.

## Feature to Remove

Remove unrestricted follow-up chat before a report is complete. It invites answers without enough context and weakens trust.

## Feature to Add

Add source review before final report generation. It gives users control over the evidence base and improves confidence in outreach recommendations.

## First 90-Day Roadmap

- Days 1-30: Improve workflow reliability, source review, and report feedback.
- Days 31-60: Add account memory, team sharing, and CRM export.
- Days 61-90: Add manager analytics, cost controls, and workflow customization by sales motion.

## First Owner-Level Change

Add richer meeting context first. Better context improves every downstream node and makes the briefing more specific to the upcoming conversation.
