# MEP Subject Tracking — User Guide

This guide walks you through configuring and running the MEP Subject Tracking workflow, which ingests GPS telemetry and collar events from EarthRanger, derives movement ecology metrics via Google Earth Engine, and produces a comprehensive per-subject tracking report for collared wildlife in the Mara ecosystem.

---

## Overview

The workflow delivers, for each subject in the selected group:

- **3 maps** — speed map, ETD home range map, and seasonal home range map with MCP overlay, each overlaid with Community Conservancy, National Reserve, and National Park land-use layers
- **4 time-series plots** — Net Square Displacement (NSD), speed, collar event timeline, and MCP asymptote
- **5 dashboard metrics** — MCP area, ETD area, distance travelled, max displacement, and night/day ratio
- **3 dashboard tables** — subject info, subject stats, and land-use occupancy (protected area, agricultural, Kenya, and unprotected use)
- **4 CSV tables** — subject info, subject stats, occupancy, and seasonal windows
- A **Word doc** — cover page (with organisation logo) plus one fully populated section per subject, merged into a single report

---

## Prerequisites

Before running the workflow, ensure you have:

- Access to an **EarthRanger** instance with subject group observations and MEP collar events (`mep_collar_check`, `mep_collaring`, `mep_source_failure`) logged for the analysis period
- Access to a **Google Earth Engine** service account with a private key in JSON format

> The LandDX land-use database is downloaded automatically from a fixed source URL — no manual setup is required.

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In the workflow runner, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/mep-subject-tracking.git
```

Then click **Add Template**.

---

### Step 2 — Configure Connections

Navigate to **Data Sources** and click **Connect**. A dialog will appear prompting you to **Select Data Source Type**. This workflow requires two connections:

| Data Source Type | Purpose |
|-----------------|---------|
| **EarthRanger** | Pull subject group observations, subject metadata, and MEP collar events |
| **Google Earth Engine** | Compute NDVI-based wet/dry seasonal windows per subject home range |

Select **EarthRanger** first and complete Step 3, then repeat and select **Google Earth Engine** for Step 4.

---

### Step 3 — Add an EarthRanger Connection

After selecting **EarthRanger** in Step 2, fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **EarthRanger URL** — your instance URL (e.g. `your-site.pamdas.org`)
- **EarthRanger Username** and **EarthRanger Password**

> Credentials are not validated at setup time. Any authentication errors will appear when the workflow runs.

Click **Connect** to save.

---

### Step 4 — Add a Google Earth Engine Connection

After selecting **Google Earth Engine** in Step 2, fill in the connection form:

- **Data Source Name** — a label to identify this connection
- **Private Key** — click **Browse** to select your GEE service account private key file (JSON format)

> To generate a private key, follow the instructions in the [Setup Guide](https://developers.google.com/earth-engine/guides/service_account). The key is stored encrypted and used only to authenticate with Google Earth Engine.

Click **Connect** to save.

---

### Step 5 — Select the Workflow

After the template is added, it appears in the **Workflow Templates** list as **mep-subject-tracking**. Click it to open the workflow configuration form.

> The card may show **Initializing…** briefly while the environment is set up.

---

### Step 6 — Set Workflow Details, Analysis Time Range, and Base Maps

The configuration form opens with three sections at the top.

**Set workflow details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run |
| Workflow Description | Optional notes (e.g. subject group, site, or reporting period) |

**Define analysis time range**

| Field | Description |
|-------|-------------|
| Timezone | Select the local timezone (e.g. `Africa/Nairobi UTC+03:00`) |
| Since | Start date and time of the analysis period |
| Until | End date and time of the analysis period |

**Configure base map layers**

Choose the tile layer(s) to use as the base map background for the speed map, home range map, and seasonal home range map.

All GPS relocations, collar events, and GEE seasonal windows are fetched within the configured time range.

---

### Step 7 — Connect to EarthRanger, Connect to Earth Engine, and Set Subject Group

Scroll down to configure the next three sections.

**Connect to EarthRanger**

Select the EarthRanger data source configured in Step 3 from the **Data Source** dropdown (e.g. `Mara Elephant Project`).

**Connect to EarthEngine**

Select the Google Earth Engine data source configured in Step 4 from the **Data Source** dropdown.

**Subject Group**

Pick the subject group to analyse from the **Subject Group Name** drop-down, which lists the subject groups on the data source chosen under **Connect to EarthRanger** (default: `Elephants`). Each subject in the group will be processed individually.

> The LandDX land-use database (Community Conservancies, National Reserves, National Parks) is downloaded automatically and does not require configuration.

---

### Step 8 — Trajectory Segment Filter

Scroll down to configure the final section.

**Trajectory Segment Filter**

These thresholds control how raw GPS fixes are joined into trajectory segments. Segments that fall outside the limits are broken at that point, preventing implausible long-distance jumps from being included.

| Field | Default | Description |
|-------|---------|-------------|
| Min Length Meters | — | Minimum segment length to retain (leave blank to skip) |
| Max Length Meters | 5000 | Maximum segment length in metres |
| Min Time Secs | — | Minimum time between fixes (leave blank to skip) |
| Max Time Secs | 17340 | Maximum time between consecutive fixes in seconds (~4.8 hours) |
| Min Speed Kmhr | -0.01 | Minimum speed threshold (slightly negative to allow rounding errors) |
| Max Speed Kmhr | 9 | Maximum plausible speed in km/h |

> Map zoom/extent padding around each subject's data is fixed internally (25% expansion) and is not user-configurable.

Once all parameters are set, click **Submit**.

---

## Running the Workflow

Once submitted, the runner will:

1. Download the LandDX database and create Community Conservancy, National Reserve, and National Park map layers.
2. Fetch GPS observations from EarthRanger for the specified time range and subject group, convert them to the selected timezone, and derive relocations.
3. Fetch subject metadata from EarthRanger for every subject present in the relocations, and compute subject maturity (6-month threshold).
4. Fetch MEP collar events (`mep_collar_check`, `mep_collaring`, `mep_source_failure`).
5. Split subject metadata, relocations, and events by subject name.
6. Convert relocations to trajectories using the configured segment filter; classify speed into 6 bins.
7. Compute ETD home range and NDVI-derived seasonal windows via Google Earth Engine per subject.
8. Generate the speed map, home range map, and seasonal home range map per subject.
9. Generate NSD, speed, collar event, and MCP asymptote plots per subject.
10. Compute movement statistics and land-use occupancy per subject.
11. Download the Word report templates and organisation logo, and populate one section per subject.
12. Merge all sections with the cover page into a single Word doc (`overall_report.docx`).
13. Assemble the interactive dashboard and save all outputs to the directory specified by `ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`. Files marked with `<subject>` are produced once per subject in the group.

### Per-subject outputs

| File | Description |
|------|-------------|
| `<subject>_speedmap.html` / `.png` | Speed map — path coloured by 6-bin speed classification |
| `<subject>_homerange.html` / `.png` | ETD home range map — percentile contours 50–99.9th |
| `<subject>_seasonal_home_range.html` / `.png` | Seasonal home range map with MCP outline overlay |
| `<subject>_nsd_seasonal_plot.html` / `.png` | Net Square Displacement time-series with season bands |
| `<subject>_speed_seasonal_plot.html` / `.png` | Speed time-series with season bands |
| `<subject>_collared_subject_plot.html` / `.png` | Collar event timeline plot |
| `<subject>_mcp_asymptote_plot.html` / `.png` | MCP area growth curve |
| `<subject>_subject_info.csv` / `_subject_info_table.html` | Subject metadata (name, sex, DOB, status, region, notes, bio, distribution) |
| `<subject>_subject_stats.csv` / `_subject_stats_table.html` | Movement stats: maturity, days/years tracked, MCP, ETD, distance, max displacement, night/day ratio |
| `<subject>_subject_occupancy.csv` / `_subject_occupancy_table.html` | Land-use occupancy percentages by category |
| `<subject>_seasonal_windows.csv` | GEE-derived wet/dry season date windows |
| `<subject>_profile.png` | Subject profile photo from EarthRanger |
| `<subject>.docx` | Populated per-subject Word report section |

### Combined outputs

| File | Description |
|------|-------------|
| `relocations.parquet` | All subjects' cleaned GPS relocations |
| `subjects.parquet` | All subjects' metadata, including maturity flag |
| `events.parquet` | All fetched MEP collar events |
| `trajectories.parquet` | All subjects' classified trajectory segments |
| `subject_tracking_cover_page.docx` | Report cover page (organisation logo, subject count, report period) |
| `overall_report.docx` | Final merged Word doc (cover + all subject sections) |
