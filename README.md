# Individual Subject Tracking Report

**Workflow ID:** `individual_subject_tracking_report`

## Overview

The **Individual Subject Tracking Report** is an automated ecoscope workflow that generates comprehensive per-subject tracking reports for collared wildlife. It connects to EarthRanger to retrieve telemetry observations and subject metadata, performs spatial and statistical analysis, and outputs a fully assembled Word document (mapbook) alongside an interactive dashboard — one report section per individual subject.

The workflow is designed primarily for use with elephant tracking programs and has been built with MEP (Mara Elephant Project) data structures in mind.

---

## Inputs

The following parameters are required to run this workflow:

| Parameter | Description | Default |
|---|---|---|
| **Subject Group Name** | The EarthRanger subject group to analyze (e.g. `"Elephants"`) | `Elephants` |
| **Time Range** | Analysis start and end date | — |
| **EarthRanger Connection** | EarthRanger instance credentials | — |
| **Earth Engine Project** | Google Earth Engine project name | — |
| **Base Maps** | Pydeck base map tile configuration | — |

> **Note:** Grouping is fixed to `subject_name`. Each subject in the specified group is processed individually.

---

## What the Workflow Does

### 1. Setup & Connections
- Sets workflow metadata and analysis time range.
- Establishes connections to **EarthRanger** (telemetry & events) and **Google Earth Engine** (seasonal analysis).
- Loads the **LandDx** geospatial database, filtering to Community Conservancies, National Reserves, and National Parks. This provides the land-use base layer overlaid on all maps.

### 2. Subject & Observation Data
- Retrieves subject metadata from EarthRanger for the chosen subject group (including inactive subjects).
- Normalizes and renames subject fields (sex, DOB, bio, region, photo, etc.).
- Fetches subject GPS observations for the analysis period and processes them into **relocations**.
- Computes **subject maturity** (based on 6-month duration threshold).

### 3. Events
- Retrieves collaring-related events from EarthRanger for the analysis period. The event types monitored (`mep_collar_check`, `mep_collaring`, `mep_source_failure`) are specific to the MEP programme and reflect the collar management events configured in that EarthRanger instance.

### 4. Trajectories
- Converts relocations to **trajectories** using a custom segment filter.
- Classifies trajectory segments into **speed bins** (6 equal-interval classes, km/h).

### 5. Maps Generated (per subject)

| Map | Description |
|---|---|
| **Speed Map** | Path layer coloured by speed bins (green → red), overlaid on land-use boundaries |
| **Home Range Map** | Elliptical Time Density (ETD) at multiple percentiles (50–99.9%), coloured RdYlGn |
| **Seasonal Home Range Map** | ETD calculated per season (wet/dry), overlaid with MCP boundary |

All maps are rendered as interactive HTML files and then screenshot to **PNG** for inclusion in the Word report.

### 6. Plots Generated (per subject)

| Plot | Description |
|---|---|
| **Net Square Displacement (NSD)** | Seasonal NSD over the analysis period |
| **Speed Plot** | Seasonal speed distribution |
| **Collared Events Plot** | Timeline of collar-related events |
| **MCP Asymptote Plot** | Minimum Convex Polygon area growth curve |

### 7. Statistics & Occupancy (per subject)

The following metrics are computed and displayed as single-value dashboard widgets:

**Movement Statistics**
- MCP Area (km²)
- ETD Area (km²)
- Distance Travelled (km²)
- Max Displacement (km²)
- Night/Day Ratio

**Land Use Occupancy** (% of home range — derived from the LandDx shapefile)
- National Protected Area use
- Community Protected Area use
- Agricultural land use (crop raid %)
- Kenya use
- Unprotected use

> These occupancy values are calculated by spatially intersecting each subject's ETD home range with the LandDx polygon layer. The categories and boundaries are entirely defined by the LandDx dataset and are tied directly to the report output.

### 8. Word Report (Mapbook)
- Downloads a **cover page template** and **subject section template** from Dropbox.
- Assembles one section per subject containing: profile photo, subject bio, speed map, home range map, seasonal home range map, NSD plot, speed plot, collared events plot, MCP plot, stats table, and occupancy table.
- Merges all sections with the cover page into a single `.docx` mapbook.

### 9. Dashboard
An interactive **Ecoscope dashboard** is generated containing all single-value widgets, maps, and plots — grouped by subject.

---

## Outputs

| Output | Format | Description |
|---|---|---|
| `mep_context.docx` | DOCX | Report cover page |
| `*_subject_section.docx` | DOCX | Per-subject report section |
| **Overall report** | DOCX | Final assembled report (cover + all sections) |
| `*_speedmap.html` / `.png` | HTML + PNG | Speed map per subject |
| `*_homerange.html` / `.png` | HTML + PNG | Home range map per subject |
| `*_seasonal_home_range.html` / `.png` | HTML + PNG | Seasonal home range map per subject |
| `*_nsd_seasonal_plot.html` / `.png` | HTML + PNG | NSD plot per subject |
| `*_speed_seasonal_plot.html` / `.png` | HTML + PNG | Speed plot per subject |
| `*_collared_subject_plot.html` / `.png` | HTML + PNG | Collared events plot per subject |
| `*_mcp_asymptote_plot.html` / `.png` | HTML + PNG | MCP asymptote plot per subject |
| `*_subject_info.csv` | CSV | Subject metadata |
| `*_subject_stats.csv` | CSV | Movement statistics |
| `*_subject_occupancy.csv` | CSV | Land use occupancy |
| `*_seasonal_windows.csv` | CSV | Seasonal window definitions |
| `*_profile.png` | PNG | Subject profile photo |
| Dashboard | Interactive | Ecoscope widget dashboard |

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS`.

---

## Skip Conditions

Tasks throughout the workflow are configured with `skipif` conditions. A task will be skipped if:
- **`any_is_empty_df`** — any upstream dataframe is empty (e.g., no observations for that subject).
- **`any_dependency_skipped`** — an upstream task was itself skipped.

This ensures the workflow gracefully handles subjects with no data without failing the entire run.

---

## Notes

- **LandDx database:** This workflow exclusively uses the LandDx geodatabase for land-use context. The database path is resolved from `$ECOSCOPE_WORKFLOWS_RESULTS`.
- **Seasonal analysis:** Season windows (wet/dry) are derived from Google Earth Engine NDVI data scoped to each subject's home range.
- **Collaring events:** Only events of types `mep_collar_check`, `mep_collaring`, and `mep_source_failure` are retrieved and visualized.
- **Report templates:** Cover page and section templates are fetched from Dropbox on each run. Set `overwrite_existing: false` to cache them locally and avoid re-downloading.
- **Screenshot rendering:** Map HTML files are rendered to PNG using a headless browser. Timeout is set to 40 seconds per map to allow full tile loading.
