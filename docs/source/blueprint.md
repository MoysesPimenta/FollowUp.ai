# WhatsApp CRM – Comprehensive Development Blueprint **v1.5 (20 Jul 2025)**

> **Changelog v1.5** — Added Section 11 _“Implementation Prompt – Execute the Backlog.”_  
> Earlier versions v1.1‑v1.4 introduced non‑functional hardening, risk register, cost model, and TDD prompts.

---

## 1  Executive Summary

Modern SMBs across LATAM rely on WhatsApp as their primary sales & support channel, yet they lack purpose‑built CRM tooling.  
**WhatsApp CRM** is a _multi‑tenant, AI‑powered_ platform that:

- Prevents lost leads with automated follow‑ups & SLA timers.
- Surfaces buying signals and churn risks via conversational AI.
- Consolidates contact, deal, and conversation data into one GDPR/LGPD‑compliant workspace.
- Ships as a SaaS (cloud) and on‑prem appliance for regulated industries.

**North‑Star Metric:** _Monthly Revenue per Active Account (MRPA)_ – target US \$45 within 12 months of GA.

---

## 2  Problem Statement & Value Proposition

| Pain (Today)                                            | Impact                                | Solution (WhatsApp CRM)                                    |
| ------------------------------------------------------- | ------------------------------------- | ---------------------------------------------------------- |
| Operators forget to reply or follow up.                 | Lost deals & churn.                   | SLA timers + smart nudges + queue view.                    |
| No single customer view; messages live on staff phones. | No analytics, compliance risk.        | Centralised inbox, contact & deal entities, audit log.     |
| Manual, error‑prone broadcast & drip campaigns.         | Low repeat business, spam violations. | Template lifecycle manager, opt‑in tracking, A/B engine.   |
| Hard to respect WhatsApp Business & LGPD rules.         | Account bans & fines.                 | Built‑in policy matrix, consent ledger, data‑subject APIs. |

---

## 3  Goals & KPIs

| Priority | Goal                                          | KPI                           | Target (6 mo) |
| -------- | --------------------------------------------- | ----------------------------- | ------------- |
| P0       | 100 % of inbound messages answered within SLA | Median first‑response time    | < 2 min       |
| P0       | Never miss scheduled follow‑up                | Follow‑up success rate        | > 98 %        |
| P1       | Increase conversion                           | Lead‑to‑order rate            | +15 pp        |
| P2       | Reduce operator workload                      | Messages sent per closed deal | –25 %         |

---

## 4  Personas & Key User Stories

### 4.1 Personas

- **Sales Rep “Ana”** – handles 120 leads/day, needs quick templates & reminders.
- **Store Manager “Bruno”** – watches team SLA dashboard, reassigns chats.
- **Compliance Officer “Clara”** – audits data requests, ensures LGPD export/delete.
- **Customer‑Success “Diego”** – runs post‑purchase follow‑ups & NPS surveys.

### 4.2 Top Stories (extract)

1. _As Ana_, when a new WhatsApp message arrives, I see it in a shared inbox with contact context so I can reply in one click.  
   **Acceptance:** message displayed < 1 s, “Reply” opens composer with canned templates.
2. _As Bruno_, I receive a Slack alert if SLA 5 min breached.
3. _As Clara_, I export all data for a phone number within 1 min in JSON/CSV.
4. _As Diego_, I schedule a drip campaign only to customers that bought ≥ R\$200 and have no open tickets.

(Full backlog in `/docs/backlog.md`.)

---

## 5  Functional Requirements

### 5.1 Messaging Core

- **Webhook receiver** for WhatsApp Business Cloud API.
- **Conversation routing** (round‑robin, skills, “mine” queue).
- **Threaded notes** & internal mentions `@`.

### 5.2 Automation & AI

- **Follow‑up Engine** – GPT‑4o‑mini with fine‑tuned function calls.
- **Sentiment & intent detection** to prioritise angry or purchase‑ready customers.
- **Translation** (Portuguese ↔ Spanish/English) on demand.

### 5.3 Campaigns

- **Template Manager** – create → submit for Meta approval → monitor status.
- **Broadcast** with opt‑in ledger; respect 24‑hour session rule.
- **A/B testing** with Bayesian bandits.

### 5.4 CRM Entities

- Contacts, Deals, Products, Pipelines, Tags (many‑to‑many).
- Bulk import/export (CSV, XLSX, vCard).
- Merge duplicate contacts (fuzzy phone/email).

### 5.5 Analytics

- Funnel & cohort dashboards (Next.js + Recharts).
- Export to Google Sheets & BigQuery.

---

## 6  Non‑Functional Requirements

| Aspect             | Requirement                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| **Performance**    | p95 API ≤ 200 ms; 2 k msgs/sec sustained.                                               |
| **Scalability**    | Horizontally scalable on Kubernetes; multi‑region active‑active.                        |
| **Availability**   | 99.95 % SLO; RPO < 5 min, RTO < 15 min.                                                 |
| **Security**       | ISO 27001 controls; OWASP Top‑10 safe; end‑to‑end HTTPS 1.3.                            |
| **Compliance**     | LGPD, GDPR, WhatsApp Commerce & Business Policy matrix attached in `/docs/policies.md`. |
| **Observability**  | OpenTelemetry traces → Grafana Cloud; alerting on ≥ 2 × error budget.                   |
| **Cost**           | COGS ceiling US$ 0.008 per processed message (see `/docs/cost‑model.xlsx`).             |
| **Sustainability** | GreenOps: weekly carbon report, idle dev cluster auto‑sleep.                            |

---

## 7  Architecture Overview

┌───────────────┐ HTTPS/Webhook ┌───────────────┐
│ WhatsApp Meta │ ─────────────────────────────> │ Ingress (NGINX│
│ Cloud API │ │ + Cert‑Mgr) │
└───────────────┘ └──────┬────────┘
│gRPC/REST
┌─────────────▼──────────────┐
│ API Gateway (GraphQL‑Helm)│
└──────┬───────────┬─────────┘
Kafka (NATS) │ │
┌───────────────┐ ┌───────▼────┐ ┌───▼────────┐
│ Message Srv │ <-- events ------------│ CRM Srv │ │ AI Engine │
└───────────────┘ │ (NestJS) │ │ (Python) │
▲ └┬──────────┘ └──┬─────────┘
│ │Write Model │OpenAI
│ Redis CQRS cache │ │
┌─────┴─────┐ ▼ ▼
│ React │ <‑‑ WebSockets/GraphQL Sub ┌──────┐ ┌────────────┐
│ Next.js │ │ Postgres │ │ VectorDB │
└───────────┘ └──────────┘ └────────────┘

- **Tech Stack**
  - Backend – TypeScript (NestJS + Prisma).
  - Frontend – Next 14 App Router, React, Tailwind, TanStack Query.
  - Infra – Kubernetes (Pulumi + Helm), PostgreSQL 16, NATS JetStream, Redis 7.
  - AI – OpenAI (gpt‑4o‑mini) via function‑calling, embeddings via `text‑embedding‑3‑small`, stored in pgvector.
  - Mobile – PWA, with push via Web Push & Firebase optional.

---

## 8  Roadmap & Milestones

| Sprint (2 w) | Theme                  | Key Deliverables                                         |
| ------------ | ---------------------- | -------------------------------------------------------- |
| 0            | **Bootstrap**          | Repo scaffold, Codex setup script, CI, health‑check.     |
| 1            | **Messaging MVP**      | Webhook ingest, send API, contact read/write.            |
| 2            | **Inbox UI α**         | Live chat, SLA timer, operator mentions.                 |
| 3            | **Follow‑up Engine α** | Rule designer, cron scheduler, basic GPT reply.          |
| 4            | **Campaigns β**        | Template mgr, broadcast, opt‑in ledger.                  |
| 5            | **Analytics β**        | Funnel chart, export CSV.                                |
| 6            | **Security & LGPD**    | Consent table, export/delete APIs, role matrix.          |
| 7            | **Mobile PWA**         | Installable app, notifications.                          |
| 8            | **Hardening**          | Load test 2 k msg/s, chaos drill, multi‑region failover. |
| 9            | **Billing & Plans**    | Stripe usage‑based, webhooks, invoices.                  |
| 10           | **Public GA**          | Production readiness review, docs, marketing site.       |

---

## 9  Kick‑off Prompt for the Coding AI (Phase 0)

_(See full text in Section 9 of this document.)_

---

## 10  Full‑Build Prompt – Continuous Implementation (500 + Tasks)

_(See full text in Section 10.)_

---

## 11  Implementation Prompt – Execute the Backlog

_(See full text in Section 11.)_

---

## 12  Risk Register (snapshot)

| #   | Risk                     | Likelihood | Impact | Mitigation                                                                     |
| --- | ------------------------ | ---------- | ------ | ------------------------------------------------------------------------------ |
| 1   | WhatsApp API quota spike | Medium     | High   | Adaptive rate‑limit + proactive quota increase request.                        |
| 2   | PII leakage via AI       | Low        | High   | On‑device redaction, zero‑retention policy, encryption at rest & in vector DB. |
| 3   | Vendor lock (OpenAI)     | Medium     | Medium | Abstraction layer; fallback to open‑source Llama 3‑Instruct on GPU node.       |
| 4   | Multi‑region DB lag      | Medium     | Medium | pg logical replication, stickiness on writes, RPO 5 min.                       |

---

## 13  BCDR Playbook (excerpt)

- **Backups:** physical base‑backup + WAL every 5 min → object storage (S3 São Paulo & São José dos Campos).
- **Failover Test:** quarterly chaos game day simulating region outage; target RTO 15 min.
- **Run‑book:** `/runbooks/db‑failover.md`.

---

## 14  Policy Matrix (WhatsApp + LGPD)

| Policy Area            | Rule                                        | Enforced In                               |
| ---------------------- | ------------------------------------------- | ----------------------------------------- |
| 24 h session messaging | No marketing msg outside session.           | API layer rejects, UI disables send.      |
| Template opt‑in        | Must store explicit consent with timestamp. | DB `consents` table, enforced by trigger. |
| Data subject rights    | Export/delete within 30 d.                  | `/v1/compliance/...` endpoints.           |

Full text in `/docs/policies.md`.

---

## 15  Cost Model (high level)

| Component           | Driver                        | Monthly Budget (100k conv./mo) |
| ------------------- | ----------------------------- | ------------------------------ |
| Compute (K8s)       | API pods, AI worker           | \$ 350                         |
| OpenAI tokens       | GPT4o‑mini 0.0005 / 1k tokens | \$ 260                         |
| WhatsApp Meta       | 0.034 /msg                    | \$ 3 400                       |
| Postgres (Aiven HA) | I/O & storage                 | \$ 180                         |
| **Total COGS**      |                               | **\$ 4 190 (~ \$0.041/msg)**   |

Goal: stay ≤ \$0.05/msg at 100 k conv.

---

## 16  Contribution Guide

- **Branching:** `main` → `dev` → feature branches.
- **Commits:** Conventional Commits, signed (`‑S`).
- **PR template:** checklist (tests, docs, changelog).
- **Code of Conduct:** adapted Contributor Covenant v2.

---

## 17  Appendices

- **A:** ADR‑0001 Tech Stack Decision
- **B:** ERD (Prisma schema)
- **C:** API OpenAPI 3.1 spec
- **D:** Terraform/Pulumi stack diagram
- **E:** Glossary (SLA, HSM, Session).

---

_End of Blueprint v1.5_
