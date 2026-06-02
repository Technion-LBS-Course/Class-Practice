# 🗺️ Tirgulim — Location-Based Services Course (Technion · 016833)

> Zac's tutorial materials for the **Location-Based Services** course at the Technion:
> hands-on guides for each project module (M2, M3, M4 …), with code examples. Demos will be added as the course progresses.

This repo is part of the course GitHub organization: [`Technion-LBS-Course`](https://github.com/Technion-LBS-Course).

---

## 🎯 Who it's for

For students in the course, as a reference while you build your final project. The tutorial sessions accompany the lectures and translate the theory into practical steps: what to do, why, and how — with code examples.

> This does not replace the lectures or your team's project submission. It's the "track" that guides you from one session to the next.

---

## 🧭 Project structure — module map

The project is built in layers. Each module builds on the previous one:

| Module | What you do | Main deliverable |
|---|---|---|
| **M2 — descriptive** | data cleaning, EDA, define the KPI | a Streamlit dashboard that shows what's going on in the data |
| **M3 — predictive** | train/test, baseline, train 2–3 models, compare | a model that predicts, wrapped in a basic Streamlit app (input → output) |
| **M4 — production** | polished UI, AI agent, deployment | a full app with a public URL |

> 🔑 **The rule that separates M2 from M3:** a dashboard that only *displays* data is still descriptive (that's M2). In M3 there must be a model that learns from the data and produces a prediction / classification / group.

---

## 📂 What's here

| Guide | Module | Description |
|---|---|---|
| [M3 — From Data to Model](M3_מסלול_מנתונים_למודל_סטודנטים.md) | M3 | The full 8-step track: from understanding the problem to Streamlit, with regression and classification examples |

More materials will be added throughout the course, module by module.

**Naming convention:** guide files are named by module — `M<number>_<description>.md` (e.g. `M3_מסלול_מנתונים_למודל_סטודנטים.md`).

> _The guides themselves are written in Hebrew (lesson content); this README is in English._

---

## 🚀 How to use

1. Open the guide for the module you're currently in (see the "What's here" table).
2. Follow the steps **in order** — each step builds on the previous one.
3. Each step offers a choice between a regression example (predict a number) and a classification example (predict a category). Pick the one that fits your project.
4. The code you write — commit + push to **your team's** repo in the [`Technion-LBS-Course`](https://github.com/Technion-LBS-Course) organization, **not** here.

---

## 🔗 Useful links

- **Course GitHub organization:** https://github.com/Technion-LBS-Course
- **Setup guide (work environment):** https://zacharadn.github.io/student-guides/technion-lbs-setup.html

---

## ✍️ Maintenance

This repo is maintained by Zac (tutorials / mentoring). Found a mistake or something unclear in one of the guides? Let me know and I'll update it.
