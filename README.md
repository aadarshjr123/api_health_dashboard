# 📊 API Health Dashboard --- *"Because blind debugging is overrated."* 🚦

![Dashboard Preview](assets/Screenshot.png)

## 🧠 What's This?

An interactive **API health monitoring dashboard** built to keep your
FastAPI services honest.
Watch your endpoints' performance, latency, and uptime come to life in
Grafana --- all wired up through Prometheus.

------------------------------------------------------------------------

## 💡 Features You'll Actually Care About

-   ⚡ **Request Rate** -- How busy your API really is
-   ⏱ **Latency Metrics** -- Because milliseconds matter
-   🚫 **Rate-Limited Requests** -- Catch those sneaky overusers
-   🩺 **Uptime Proxy** -- Know when your API starts pretending to be
    offline

------------------------------------------------------------------------

## 🧰 Tech Stack

  -----------------------------------------------------------------------
  Layer                 Tool               Purpose
  --------------------- ------------------ ------------------------------
  🐍 **Backend**        FastAPI            Handles endpoints and metrics

  📈 **Metrics**        Prometheus         Collects and stores
                                           performance data

  🎨 **Visualization**  Grafana            Turns numbers into something your eyes enjoy

  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 🧩 System Flow

    [ Client ]
       │
       ▼
    [ FastAPI (8000) ]
       │  └─→ /metrics → Prometheus (9090)
       │
       ▼
    [ Grafana (3030) ] ← Prometheus Data → Visual Dashboard

------------------------------------------------------------------------

## 🚀 Why Build This?

Because every developer deserves a dashboard that: - Looks good
- Actually works
- And doesn't require five coffees to debug

------------------------------------------------------------------------

## 🧭 Getting Started

1.  **Spin up everything**

    ``` bash
    docker compose up --build
    ```

2.  **Visit your new monitoring HQ:**

    -   FastAPI → <http://localhost:8000>
    -   Grafana → <http://localhost:3030>

3.  **Login to Grafana (default creds):**

    -   **User:** `admin`
    -   **Password:** `admin`

4.  **Explore metrics** and admire your API's stats in real time.

------------------------------------------------------------------------

## 👨‍💻 Developer Vibes

This project is: - 80% building - 15% fixing Docker issues - 5%
pretending you totally planned that dashboard theme
