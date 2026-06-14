# Product Improvements

## Current Product Weaknesses

1. The session input is minimal and may not capture meeting type, persona, region, or deal stage.
2. The workflow does not yet let users approve or remove sources before report generation.
3. The report can explain unknowns, but it does not turn them into assigned research tasks.
4. Follow-up chat is session-bound and does not build account memory across multiple meetings.
5. There is no collaboration model for sales teams, managers, or enablement reviewers.
6. Cost controls are not visible to workspace owners.

## Top 3 Improvements

1. Add meeting context fields such as persona, deal stage, region, and planned agenda.
2. Add source review with pin, remove, and request-more controls.
3. Add account memory across sessions so repeated research compounds over time.

## Buyer, User, and Payment Rationale

Sales leaders, revenue operations teams, and founders buy the product because they want better meeting preparation without manual research overhead. Account executives, sales development representatives, customer success managers, and partnerships teams use it before calls. Teams pay when the briefing improves discovery quality, reduces prep time, and creates more consistent account strategy.

## Success Metrics

- Time from session creation to usable report.
- Percentage of reports opened before meetings.
- Follow-up questions per completed report.
- Source coverage per report section.
- User-rated usefulness after a meeting.
- Meetings influenced and opportunities advanced.

## 4-Week Roadmap

- Week 1: Add meeting context fields, report quality rubric, and stronger source coverage.
- Week 2: Add source review and manual source controls.
- Week 3: Add account memory and comparison against prior sessions.
- Week 4: Add team sharing, manager review, and usage analytics.

## Cost, Scaling, and Reliability Risks

The biggest cost risk is repeated model calls during gap research. The biggest scaling risk is long-running workflow execution inside the API process. The biggest reliability risk is source fetch failure or stale public information. Bound attempts, cache source fetches, move execution to workers, and surface unknowns instead of over-claiming.

## Feature to Remove

Remove unrestricted follow-up chat before a report is complete. It invites answers without enough context and weakens trust.

## Feature to Add

Add source review before final report generation. It gives users control over the evidence base and improves confidence in outreach recommendations.

## First 90-Day Roadmap

- Days 1-30: Ship reliable session creation, workflow progress, structured reports, source review, and report feedback.
- Days 31-60: Add account memory, team sharing, and CRM export.
- Days 61-90: Add manager analytics, cost controls, and workflow customization by sales motion.

## First Owner-Level Change

The first change would be adding richer meeting context at session creation. Better context improves every downstream node and makes the final briefing more specific to the upcoming conversation.

