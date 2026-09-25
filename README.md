<div align="center">

<img src="assets/header.svg" width="100%" alt="Gabriel Coelho — Cybersecurity Analyst, Blue Team, MCP Developer"/>

<a href="https://github.com/bunnyiesart">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=20&duration=2800&pause=900&color=00E5FF&center=true&vCenter=true&width=760&lines=Hunting+threats+before+they+hunt+you+%F0%9F%9B%A1%EF%B8%8F;Building+MCP+servers+that+give+AI+analysts+real+SOC+tools;DFIR+%E2%80%A2+Threat+Intel+%E2%80%A2+Detection+Engineering;FreeBSD+%26+kernel+hardening+enthusiast+%F0%9F%98%88" alt="typing"/>
</a>

<br/>

<a href="https://bunnyiesart.github.io/portifolio/"><img src="https://img.shields.io/badge/portfolio-enter_the_battle-7c5cff?style=for-the-badge&logo=undertale&logoColor=white&labelColor=0d1117" alt="Portfolio"/></a> <a href="https://bunnyiesart.github.io/Fursec/"><img src="https://img.shields.io/badge/Fursec-free_cyber_path-ff3d8b?style=for-the-badge&logo=bookstack&logoColor=white&labelColor=0d1117" alt="Fursec"/></a> <a href="https://github.com/bunnyiesart?tab=followers"><img src="https://img.shields.io/github/followers/bunnyiesart?style=for-the-badge&logo=github&color=00e5ff&labelColor=0d1117" alt="Followers"/></a>

</div>

<br/>

## `$ whoami`

```yaml
name:      Gabriel Silva Coelho
role:      Cybersecurity Analyst @ BSDTrust
base:      Brasil 🇧🇷
blue_team: [SOC, DFIR, threat intel, detection engineering]
red_side:  [blackbox pentest, web security]
building:  MCP servers that plug AI into real SOC tooling
into:      [FreeBSD, kernel hardening, self-hosting]
speaks:    [pt-BR, en]
motto:     "Transformando vulnerabilidades em código"
```

<details>
<summary><b>🇧🇷 Versão em português</b></summary>
<br/>

Sou analista de cibersegurança com foco em **Blue Team**: SOC, resposta a incidentes (DFIR), threat intel e engenharia de detecção. Também atuo com **pentest blackbox e web**.
Hoje construo **servidores MCP** que dão a assistentes de IA acesso seguro e auditado às ferramentas do SOC: SIEM, DFIR-IRIS e mais de 20 fontes de inteligência.
Mantenho o **[Fursec](https://bunnyiesart.github.io/Fursec/)**, uma trilha gratuita de cibersegurança com ~200 cursos em PT-BR e EN.

</details>

## 🛰️ The SOC toolkit

> Everything below is built to plug an AI analyst into the real SOC: **read-only by default, audited, and hardened on the server side**.

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {'fontFamily':'JetBrains Mono, monospace', 'lineColor':'#7c5cff'}}}%%
flowchart LR
    A(["🧑‍💻 Analyst + Claude"]):::human --> G{{"🛰️ Gatte<br/>MCP gateway · audit · quarantine"}}:::gate
    G --> S["🔪 swiss<br/>20+ threat intel sources"]:::intel
    G --> I["🧬 mcp-iris<br/>DFIR-IRIS cases"]:::ir
    G --> O["🔎 mcp-opensearch<br/>SIEM search"]:::siem
    G --> B["🛡️ bluearmory<br/>graylog-mcp + skills"]:::armory
    I --> T["⚙️ auto-treat<br/>automated triage"]:::skill
    I --> R["📄 iris-report<br/>shift report PDFs"]:::skill

    classDef human  fill:#0d1117,stroke:#39d353,color:#e6edf7
    classDef gate   fill:#0b1b24,stroke:#00e5ff,stroke-width:2px,color:#e6edf7
    classDef intel  fill:#1f0d18,stroke:#ff3d8b,color:#e6edf7
    classDef ir     fill:#150f2b,stroke:#7c5cff,color:#e6edf7
    classDef siem   fill:#221906,stroke:#ffb020,color:#e6edf7
    classDef armory fill:#0b1f10,stroke:#39d353,color:#e6edf7
    classDef skill  fill:#11161f,stroke:#6b7a90,color:#c9d4e5
```

## 🔥 Featured projects

<div align="center">

<a href="https://github.com/bunnyiesart/Gatte"><img src="assets/cards/gatte.svg" width="49%" alt="Gatte"/></a> <a href="https://github.com/bunnyiesart/swiss"><img src="assets/cards/swiss.svg" width="49%" alt="swiss"/></a>
<a href="https://github.com/bunnyiesart/mcp-iris"><img src="assets/cards/mcp-iris.svg" width="49%" alt="mcp-iris"/></a> <a href="https://github.com/bunnyiesart/mcp-opensearch"><img src="assets/cards/mcp-opensearch.svg" width="49%" alt="mcp-opensearch"/></a>
<a href="https://github.com/bunnyiesart/bluearmory"><img src="assets/cards/bluearmory.svg" width="49%" alt="bluearmory"/></a> <a href="https://bunnyiesart.github.io/Fursec/"><img src="assets/cards/fursec.svg" width="49%" alt="Fursec"/></a>

</div>

## 🧰 Arsenal

<div align="center">

**Code & infra**

<img src="https://skillicons.dev/icons?i=python,go,js,ts,react,vite,nodejs,bash,docker,linux,git,githubactions&perline=12" alt="Tech stack"/>

**Security stack**

<img src="https://img.shields.io/badge/FreeBSD-AB2B28?style=for-the-badge&logo=freebsd&logoColor=white"/> <img src="https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white"/> <img src="https://img.shields.io/badge/Burp_Suite-FF6633?style=for-the-badge&logo=burpsuite&logoColor=white"/> <img src="https://img.shields.io/badge/Wireshark-1679A7?style=for-the-badge&logo=wireshark&logoColor=white"/> <img src="https://img.shields.io/badge/Wazuh-3595F8?style=for-the-badge&logo=wazuh&logoColor=white"/> <img src="https://img.shields.io/badge/Graylog-FF3633?style=for-the-badge&logo=graylog&logoColor=white"/> <img src="https://img.shields.io/badge/OpenSearch-005EB8?style=for-the-badge&logo=opensearch&logoColor=white"/> <img src="https://img.shields.io/badge/DFIR--IRIS-7c5cff?style=for-the-badge&logo=databricks&logoColor=white"/> <img src="https://img.shields.io/badge/MISP-1a1a2e?style=for-the-badge&logo=hackthebox&logoColor=white"/> <img src="https://img.shields.io/badge/VirusTotal-394EFF?style=for-the-badge&logo=virustotal&logoColor=white"/> <img src="https://img.shields.io/badge/MITRE_ATT%26CK-C8102E?style=for-the-badge&logo=target&logoColor=white"/> <img src="https://img.shields.io/badge/MCP-000000?style=for-the-badge&logo=anthropic&logoColor=white"/>

</div>

## 📡 Telemetry

<div align="center">

<img src="https://streak-stats.demolab.com?user=bunnyiesart&theme=tokyonight&hide_border=true&background=0D1117&ring=7C5CFF&fire=FF3D8B&currStreakLabel=00E5FF&sideLabels=C9D4E5&dates=6B7A90&currStreakNum=E6EDF7&sideNums=E6EDF7" width="70%" alt="Contribution streak"/>

<br/><br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/bunnyiesart/bunnyiesart/output/snake-dark.svg"/>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/bunnyiesart/bunnyiesart/output/snake.svg"/>
  <img src="https://raw.githubusercontent.com/bunnyiesart/bunnyiesart/output/snake-dark.svg" alt="Contribution snake eating my commits"/>
</picture>

</div>

<div align="center">
<img src="assets/footer.svg" width="100%" alt="monitoring... all systems nominal"/>
</div>
