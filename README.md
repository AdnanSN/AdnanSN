<!--
  adnan.log: the profile README of @AdnanSN.
  Printed sheets in assets/ are built by .github/readme/build_static.py (see .github/readme/HOW-IT-WORKS.md).
  The stats sheet and the snake are reprinted every night by .github/workflows/profile-graphs.yml
  and published to the `output` branch.
-->

<p align="center">
  <img src="assets/header.svg" width="100%" alt="A sheet of green-bar printer paper, adnan.log. Hi, I'm Adnan: AI engineer and full-stack developer, building LLM systems that show their work. MSc Computer Science and Software Engineering at Constructor University Bremen, from Chennai. Log: 2025, two papers and the start of freelancing; Feb 2026, shipped LLM pipelines on AWS as a Forward Deployed AI Engineer; May 2026, graduated B.Tech in AI and Data Science with a CGPA of 8.36; Sep 2026, moved from Chennai to Bremen for the MSc; Oct 2026, won the SereneDB challenge at the schubKI National AI Hackathon; now open to Werkstudent roles.">
</p>

<p align="center">
  <a href="https://linkedin.com/in/adnansn"><img src="https://img.shields.io/badge/LinkedIn-adnansn-2a78d6?style=flat-square" alt="LinkedIn: adnansn"></a>
  <a href="mailto:adnannalawalas@gmail.com"><img src="https://img.shields.io/badge/Email-adnannalawalas%40gmail.com-1E232B?style=flat-square" alt="Email: adnannalawalas@gmail.com"></a>
  <img src="https://img.shields.io/badge/Based_in-Bremen%2C_Germany-56605A?style=flat-square" alt="Based in Bremen, Germany">
  <img src="https://img.shields.io/badge/Open_to-Werkstudent_roles-1baf7a?style=flat-square" alt="Open to Werkstudent roles">
  <img src="https://komarev.com/ghpvc/?username=AdnanSN&style=flat-square&color=56605A&label=profile+views" alt="Profile views">
</p>

### 🏆 Fresh off the printer

In October 2026, [@Arnie1x](https://github.com/Arnie1x) and I won the **SereneDB challenge** ("Making Sense of Logs") at the **schubKI National AI Hackathon 2026**. Our project, **[Exhibit](https://github.com/Arnie1x/exhibit)**, is an MCP server that answers questions about logs for engineers, team leads and managers. We built it on one rule: SQL computes, the LLM explains. Every number in an answer comes with the query that produced it, so anyone can re-run it. My lane was the data and the SQL: views, role-scoped access, and checking every figure against ground truth.

<a href="https://github.com/Arnie1x/exhibit"><img src="assets/exhibit.svg" width="100%" alt="Exhibit by the numbers: 15 of 15 eval questions match golden SQL; phrase and facet search over 5.28 million rows in 13 ms; full rebuild from raw logs in about 20 seconds; built in 48 hours by a team of two among 200+ participants. Charts: log lines parsed and indexed, and incidents found at different episode gaps. 99.64% of the 152,734 'data TLB error interrupt' lines came from a single node."></a>

<details>
<summary>The numbers behind the charts</summary>

| What we measured | Value |
| --- | --- |
| BGL log lines parsed | 4,747,963 |
| OpenStack log lines parsed | 207,812 |
| OTel rows indexed (a 10-second slice of a 1-billion-row file) | 5,275,597, indexed in 60 s |
| Phrase + facet search over that slice | 13 ms |
| Incidents in 152,734 "data TLB error interrupt" lines, at a 1 / 5 / 60-minute gap | 132 / 117 / 57 |
| Share of those lines from a single node | 99.64% |
| Eval questions matching golden SQL | 15 of 15 |
| Full rebuild from raw logs | about 20 s |

</details>

### 🛠️ Things I've shipped

<table>
<tr>
<td width="50%" valign="top">

**🔎 [Exhibit](https://github.com/Arnie1x/exhibit)**<br>
Role-aware log intelligence over SereneDB, built in 48 hours with [@Arnie1x](https://github.com/Arnie1x). Engineers get incidents instead of raw lines, and a lint step rejects any answer that claims more than the logs can show.<br>
<sub>`SQL` `SereneDB` `MCP` `Docker`</sub>

</td>
<td width="50%" valign="top">

**🎬 Training-content pipeline** at SARAEdx Foundry<br>
Turns expert screen recordings into structured training documents: faster-whisper transcripts, LLM-written scripts validated as JSON with Pydantic, a self-check against the source, and a human approval gate. Shipped on AWS (EC2, ECS) with Docker and CI/CD.<br>
<sub>`Python` `Pydantic` `OpenAI API` `AWS` `Docker` (client work, private)</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🧾 [Quotation SaaS](https://quotation-pearl.vercel.app)**<br>
For Indian supplier SMBs: an LLM reads a customer's messy RFQ and turns it into structured line items and a draft quote.<br>
<sub>`Next.js` `Supabase` `PostgreSQL` `Google OAuth` `LLMs`</sub>

</td>
<td width="50%" valign="top">

**☕ [Morrick's Keep Coffee](https://morrickskeepcoffee.com)**<br>
Online store for a coffee roaster, from scope and pricing through payments to the custom domain.<br>
<sub>`Next.js` `TypeScript` `Supabase` `Cashfree` `Vercel`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

**🏛️ Archivio**<br>
Project management for a growing architecture firm, built around handing out and tracking tasks across the office.<br>
<sub>`Supabase` `Vercel` (client work, private)</sub>

</td>
<td width="50%" valign="top">

**📄 Research and hackathons**<br>
Papers on *Hybrid Edge-Based Traffic Signal Control Using Reinforcement Learning* and a *Conversational AI-Driven Image Recognition Chatbot with Webcam Integration* (NCAIBIA 2025). My final-year project was an AI + IoT traffic-management system, and an AI study planner I built placed top 5 of 60 teams at SRM Hackforge '25.<br>
<sub>`Computer vision` `Reinforcement learning` `IoT`</sub>

</td>
</tr>
</table>

<details>
<summary>From the archive</summary>

- [Object detection with YOLOv8](https://github.com/AdnanSN/Object-detection-using-YOLOv8): YOLOv8 + OpenCV
- [Email spam classifier](https://github.com/AdnanSN/Email-spam-classifier-website): scikit-learn model behind a Flask site
- [Student management system](https://github.com/AdnanSN/Student-management-system): Python
- [Code-N-Surge Error404](https://github.com/AdnanSN/Code-N-Surge-Error404): hackathon website

</details>

### 🧭 How I got here

<img src="assets/journey.svg" width="100%" alt="My history as a git graph, newest first: open to Werkstudent roles (now); won the SereneDB challenge at schubKI (Oct 2026); moved to Bremen and started the MSc at Constructor University (Sep 2026); freelance chapter merged (Sep 2026); built Archivio; graduated B.Tech AI and Data Science with CGPA 8.36 (May 2026); shipped the AI quotation SaaS; joined SARAEdx Foundry as Forward Deployed AI Engineer (Feb 2026); launched the Morrick's Keep Coffee store; passed IELTS (band 8.0) and Oracle OCI AI Foundations (2025); published RL traffic-signal control; started freelancing (2025); top 5 of 60 at SRM Hackforge '25; presented a vision chatbot paper at NCAIBIA 2025; full-stack intern at Scrapify Ecotech (Dec 2024); data analyst intern at National Trading Co. (May 2024); Youth Red Cross department coordinator (Oct 2023); started B.Tech at Velammal Engineering College (Aug 2022).">

### 🧰 What I build with

<table>
<tr><td><sub>Languages</sub></td><td><img src="https://skillicons.dev/icons?i=py,ts,js,java,cpp,c,r" height="40" alt="Python, TypeScript, JavaScript, Java, C++, C, R"></td></tr>
<tr><td><sub>AI and data</sub></td><td><img src="https://skillicons.dev/icons?i=pytorch,tensorflow,sklearn,opencv,postgres,supabase,mysql,mongodb" height="40" alt="PyTorch, TensorFlow, scikit-learn, OpenCV, PostgreSQL, Supabase, MySQL, MongoDB"></td></tr>
<tr><td><sub>Web</sub></td><td><img src="https://skillicons.dev/icons?i=react,nextjs,nodejs,tailwind,flask,spring" height="40" alt="React, Next.js, Node.js, Tailwind CSS, Flask, Spring Boot"></td></tr>
<tr><td><sub>Cloud and tools</sub></td><td><img src="https://skillicons.dev/icons?i=aws,docker,vercel,linux,bash,git,github,raspberrypi" height="40" alt="AWS, Docker, Vercel, Linux, Bash, Git, GitHub, Raspberry Pi"></td></tr>
</table>

<sub>Also in the toolbox: LLM APIs, MCP servers, Pydantic, faster-whisper, SereneDB, Oracle Cloud and Claude Code.</sub>

### 📈 Reprinted every night

<img src="https://raw.githubusercontent.com/AdnanSN/AdnanSN/output/stats.svg" width="100%" alt="My GitHub activity over the last 12 months and my languages by code size, reprinted every night by a GitHub Action.">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/AdnanSN/AdnanSN/output/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/AdnanSN/AdnanSN/output/snake.svg" width="100%" alt="A snake eating my contribution graph">
</picture>

### 🎒 Off the keyboard

- 🌍 Swapped Marina Beach for the Weser: Chennai to Bremen is about 7,600 km.
- 🗣️ I speak English, Hindi, Tamil, Urdu and Gujarati, read Arabic, and I'm learning German.
- 🏸 I play in the badminton club at Constructor, I'm learning tennis, and I've played padel and pickleball.
- 🎶 I love going to music festivals.

### 📬 Say hi

Hiring a Werkstudent in Bremen or remotely in Germany? I can work up to 20 hours a week during the semester and full-time in the breaks. [LinkedIn](https://linkedin.com/in/adnansn) or [email](mailto:adnannalawalas@gmail.com) both reach me, and [Instagram](https://instagram.com/_.addstagram._) is for everything else.

<img src="assets/footer.svg" width="100%" alt="The end of the printout: exit, logout, process completed. Thanks for reading, say hi!">
