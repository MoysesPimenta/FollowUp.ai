# WhatsApp CRM – Comprehensive Development Blueprint **v1.2 (20 Jul 2025)**

> **Changelog v1.2**  — second audit: added WhatsApp policy matrix & template lifecycle, multi‑region deployment plan, advanced cost model, mobile UX guidelines, expanded data‑protection controls, sustainable ops, A/B testing framework, and change‑management protocol.

---

## 1  Executive Summary

**Purpose.** Design, build, and operate a secure, multi‑tenant, AI‑powered CRM centred on WhatsApp Business Cloud API, empowering businesses to automate follow‑ups, measure performance, and never lose a lead.

**Brazil‑first Edge.** Native LGPD compliance, Pix & boleto support, Portuguese UI by default, São Paulo (sa‑east‑1) data residency option, currency in BRL.

**Value Proposition & KPI targets** remain identical to v1.1 (see §1.2 KPI table).

---

## 1.2 Key Enhancements Added in v1.2

| Area           | Improvement                                                                                                                                         |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compliance     | WhatsApp policy matrix (24 h rule, template types, pricing tiers) with automated linting of outbound templates & message frequency limits.          |
| Architecture   | Multi‑region active‑active blueprint (sa‑east‑1 ↔ us‑east‑2) with global Aurora PostgreSQL & Route 53 lat‑based routing.                            |
| Cost           | FinOps cost‑forecast workbook incl. WA conversation costs, AWS infra, LLM usage, and projected ARR — budgets enforced via AWS Budgets & CloudWatch. |
| Mobile         | React Native design system, offline queue, local notifications, biometric auth support (Face ID/Android BiometricPrompt).                           |
| Security       | End‑to‑end encryption of stored chats via field‑level AES‑GCM; BYOK (bring‑your‑own‑KMS key) per tenant; automated DLP scans.                       |
| Sustainability | Monthly carbon footprint report (Cloud Carbon Footprint), GreenOps weekly alerts, auto‑scale to zero for dev environments.                          |
| Data           | Multi‑tenant sharding strategy using Postgres schemas; row‑level security (RLS) example policy.                                                     |
| Testing        | A/B test service with feature flags (LaunchDarkly) + StatsEngine sequential testing.                                                                |
| Change Mgmt    | ADR (Architecture Decision Record) template & GitOps workflow w/ versioned K8s manifests.                                                           |

---

## 2  WhatsApp Policy Compliance Matrix (new)

| Type                   | Window    | Template Category                  | Allowed Content        | CRM Enforcement                      |
| ---------------------- | --------- | ---------------------------------- | ---------------------- | ------------------------------------ |
| **User‑Initiated**     | 24 h      | N/A                                | free‑form, media       | SLA timer, auto escalate at t‑20 min |
| **Business‑Initiated** | N/A       | Marketing, Utility, Authentication | pre‑approved template  | Template linter CI, opt‑in check     |
| **Opt‑Out**            | immediate | –                                  | must stop all messages | DSAR queue auto action               |

*Outbound message middleware rejects sends if policy fails; error surfaced in UI.*

---

## 3  Multi‑Region Deployment Plan (new) 

```
Regions      sa‑east‑1  <‑‑‑‑‑‑‑‑‑‑‑►  us‑east‑2
                   ▲                    ▲
VPC Peering ◄──────┘                    └─────► RDS Global DB (Aurora)
                Active‑Active ↕ Route 53 latency‑based ↕ Active‑Active
```

* Active‑active FE via AWS CloudFront + Regional Edge Caches.
* Chat svc replicas in both regions; JetStream streams have RPO < 15 sec cross cluster.
* AI svc is region‑pinned to minimise token transit; fallback to nearest.
* **Disaster mode:** traffic shifts to healthy region within 3 min (Route 53 H‑check).

---

## 4  Cost Model & Budgets (expanded)

| Component        | Unit Cost       | Base Load (M1) | 12‑M Forecast | Notes                            |
| ---------------- | --------------- | -------------- | ------------- | -------------------------------- |
| WA Conversations | BRL 0.07 ea     | 5000 day       |  BRL 1.3 M    | assumes 20 % mo growth           |
| AWS Infra        | US\$ 2.4 k mo   | 2 env          |  US\$ 66 k    | incl. prod+stg, 30 % reserve     |
| LLM Tokens       | US\$ 0.005 / 1k | 6 M / mo       |  US\$ 50 k    | 60 % Smart Reply, 40 % summaries |
| Staff            | BRL 85 k mo     | 5 FTE          |  BRL 3.6 M    | salaries, benefits               |

* Budget alarms at 80/90/100 % via AWS Budgets → Slack #finops.\*

---

## 5  Mobile UX Guidelines (new)

* **Design Tokens:** use Tailwind + Nativewind; system font; colour accessibility AAA.
* **Offline Queue:** messages stored in SQLite; sync via App Sync offline‑mutations.
* **Push Notifications:** FCM/APNs — deep‑link to conversation.
* **Biometric Auth & PIN fallback**; secure storage via Keychain/Keystore.
* **Voice‑Note Playback** with background audio.

---

## 6  Data Protection Controls (expanded)

1. Field‑level encryption using pgcrypto; ciphertext search via ‘blind index’.
2. Per‑tenant KMS CMK (Customer Managed Key) with automatic rotation (365 d).
3. Periodic DLP Scans (AWS Macie) → security slack.
4. Privacy By Design checklist integrated into PR template.

---

## 7  Sustainability & GreenOps (new)

* **Cloud Carbon Footprint** CLI in CI → monthly report in docs.
* Auto‑hibernate dev DBs after 1 h idle.
* Spot instances for batch AI summary jobs.
* KPI: grams CO₂ / 1k messages < 30.

---

## 8  A/B Testing & Feature Flags

* LaunchDarkly SDK; default off flags.
* StatsEngine sequential t‑test w/ 95 % confidence.
* Guardrails: no degradation > 10 % on P0 KPIs.

---

## 9  Change Management Protocol

* ADRs stored in `/docs/adr/*-title.md`.
* GitHub PR must reference ADR if affecting arch.
* Version tag semantic release; auto‑changelog.
* Production deploy requires 2 approvals (SRE + Security).

---

## 10  Row‑Level Security Example Policy (Postgres)

```sql
CREATE POLICY tenant_isolation ON message USING (
  tenant_id = current_setting('app.current_tenant')::uuid
);
ALTER TABLE message ENABLE ROW LEVEL SECURITY;
```

* `SET app.current_tenant` applied by connection middleware.\*

---

## 11  Threat‑Model Updates (delta)

* Added "Model Injection" threat for LLM prompts.
* Mitigation: ISO 27001 A.5.34 prompt‑filter and output post‑processing.

---

## 12  Known Gaps To Address in v1.3

1. **GDPR Art.27 EU Rep** — pending vendor selection.
2. **External audit SOC 2** — schedule Q4 2025.
3. **Android WearOS quick‑reply** — stretch goal mobile v2.
4. **Data mesh event catalog** — needs schema registry.

---

> *End of Blueprint — Version 1.2 (July 20 2025)*
