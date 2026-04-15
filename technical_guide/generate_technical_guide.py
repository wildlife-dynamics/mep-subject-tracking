"""
Generate the MEP Subject Tracking Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mep_subject_tracking_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mep_subject_tracking_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MEP Subject Tracking — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MEP Subject Tracking", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Per-subject home range, speed, seasonal, and occupancy analysis", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>subject_tracking</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>subject_tracking</b> workflow fetches GPS relocations for a named "
      "subject group from EarthRanger, derives trajectories, and produces a "
      "comprehensive per-subject movement ecology report. Google Earth Engine "
      "is used to detect NDVI-based seasonal windows that stratify all spatial "
      "and temporal analyses."),
    sp(4),
    p("For each subject the workflow delivers:"),
    bullet("3 maps — speed map, ETD home range map, and seasonal home range "
           "map (with MCP overlay)"),
    bullet("4 time-series plots — Net Square Displacement (NSD), speed, "
           "collar event, and MCP asymptote"),
    bullet("10 single-value dashboard metrics — protected area use (national, "
           "community), agricultural land use, Kenya use, unprotected use, "
           "MCP area, ETD area, distance travelled, max displacement, and "
           "night/day ratio"),
    bullet("4 CSV tables — subject information, subject stats, occupancy, "
           "and seasonal windows"),
    bullet("A Word mapbook — cover page + one populated section per subject"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Count", "Description"],
            ["Speed maps",             "1 per subject", "Path layer coloured by 6-bin speed classification"],
            ["Home range maps",        "1 per subject", "ETD percentile polygons (50–99.9th)"],
            ["Seasonal home range maps","1 per subject","ETD 99.9th percentile split by wet/dry season + MCP outline"],
            ["NSD seasonal plots",     "1 per subject", "Net Square Displacement with season bands"],
            ["Speed seasonal plots",   "1 per subject", "Speed time series with season bands"],
            ["Collar event plots",     "1 per subject", "Collar check/collaring/source failure events on timeline"],
            ["MCP asymptote plots",    "1 per subject", "MCP area growth curve"],
            ["Subject CSV tables",     "4 per subject", "info, stats, occupancy, seasonal windows"],
            ["Dashboard SV widgets",   "10 per subject","Occupancy %, area, distance, and ratio metrics"],
            ["Word mapbook",           "1 total",       "Cover page + per-subject report sections merged"],
        ],
        [4*cm, 2.5*cm, W - 6.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-big-life","0.0.8.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mep",     "0.0.12.*",  "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connections"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch subject groups, GPS relocations, and MEP collar events"],
            ["Google Earth Engine", "set_gee_connection",
             "Compute NDVI-based seasonal windows per subject ETD extent"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    sp(6),
    h2("2.3  LandDx database"),
    p("The workflow obtains the LandDx GeoPackage via <b>get_file_path</b>, "
      "which accepts either a <b>URL download</b> or a <b>local file path</b>. "
      "The default input method is pre-filled with the standard Dropbox URL "
      "(landDx.gpkg). The output path is resolved from "
      "<b>ECOSCOPE_WORKFLOWS_RESULTS</b>. Three polygon types are retained:"),
    make_table(
        [
            ["LandDx type", "Fill color (RGB)", "Hex", "Opacity"],
            ["Community Conservancy", "[166, 182, 151]", "#a6b697", "0.15"],
            ["National Reserve",      "[136, 167, 142]", "#88a78e", "0.15"],
            ["National Park",         "[17, 86, 49]",    "#115631", "0.15"],
        ],
        [4.5*cm, 4*cm, 2.5*cm, 2*cm],
    ),
    p("A text label layer is also created from the <b>name</b> column "
      "(Arial, size 1000 m, min 40 px / max 75 px, billboard: true) to "
      "identify each polygon on the map."),
    sp(6),
    h2("2.4  Base maps"),
    p("Base map tiles are configured by the user via <b>set_base_maps_pydeck</b>. "
      "Any tile layer supported by deck.gl can be specified."),
    sp(6),
    h2("2.5  Grouper"),
    p("The workflow groups all data by <b>subject_name</b>. The rjsf-overrides "
      "block restricts the grouper UI to Subject Name only — users cannot "
      "change the grouping dimension."),
    sp(6),
    h2("2.6  Subject group"),
    p("A user-provided string parameter (<b>Subject Group Name</b>, default: "
      "<i>Elephants</i>) is passed to both the subject info fetch and the "
      "observations fetch to scope the analysis to a single EarthRanger "
      "subject group."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. SUBJECT DATA PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Subject Data Pipeline"),
    hr(),
    p("Subject metadata is fetched and cleaned separately from GPS "
      "relocations. Both pipelines share the same subject group name "
      "and EarthRanger client."),
    sp(6),
    h2("3.1  Subject metadata"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_subject_df",
             "Fetch all subjects in the group (include_inactive: true, "
             "max_ids_per_request: 50, raise_on_empty: false)"],
            ["2", "normalize_json_column",
             "Flatten the 'additional' JSON column; skip if column absent"],
            ["3", "transform_columns",
             "Drop 7 columns (url, image_url, common_name, content_type, "
             "external_id, tm_animal_id, external_name); rename ~12 columns "
             "(id→groupby_col, name→subject_name, hex→hex_color, "
             "additional__Bio→subject_bio, additional__sex→subject_sex, "
             "additional__DOB→date_of_birth, etc.)"],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    h2("3.2  Subject maturity"),
    p("<b>compute_maturity</b> is called with <b>months_duration: 6</b> "
      "against the cleaned subject metadata and relocations GeoDataFrame "
      "(time_column: fixtime). This flags subjects that have been tracked "
      "for at least 6 months, used downstream in occupancy and stats "
      "calculations."),
    sp(6),
    h2("3.3  GPS relocations"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "get_subjectgroup_observations",
             "Fetch observations for the subject group (filter: clean, "
             "time_range, raise_on_empty: false, include_details: false)"],
            ["2", "process_relocations",
             "Retain 9 columns: groupby_col, fixtime, junk_status, geometry, "
             "extra__subject__name, extra__subject__hex, extra__subject__sex, "
             "extra__created_at, extra__subject__subject_subtype. "
             "Filter 3 invalid coordinate pairs: (180,90), (0,0), (1,1)"],
            ["3", "map_columns",
             "Rename extra__ prefix columns: name→subject_name, "
             "hex→hex_color, sex→subject_sex, etc."],
        ],
        [1.2*cm, 4*cm, W - 5.2*cm],
    ),
    sp(6),
    h2("3.4  Per-subject outputs"),
    p("After subjects are split by group (<b>split_groups</b> on subject_name):"),
    bullet("<b>persist_subject_photo</b> — downloads the subject's profile "
           "photo from EarthRanger and saves as PNG (overwrite_existing: true)"),
    bullet("<b>process_subject_information</b> — formats subject metadata "
           "(maxlen: 1000) and persists as CSV"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. EVENT DATA PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Event Data Pipeline"),
    hr(),
    p("Three MEP-specific event types are fetched from EarthRanger for the "
      "analysis time range and used in the collar event plot:"),
    make_table(
        [
            ["Event type", "Description"],
            ["mep_collar_check",    "Periodic collar condition check"],
            ["mep_collaring",       "Initial or replacement collaring event"],
            ["mep_source_failure",  "Collar or GPS source failure report"],
        ],
        [5*cm, W - 5*cm],
    ),
    sp(4),
    p("10 columns are retained: id, time, event_type, event_category, "
      "reported_by, serial_number, geometry, event_details, priority, "
      "priority_label. The event_details JSON column is normalised and "
      "the following fields are renamed:"),
    make_table(
        [
            ["Raw column", "Renamed to"],
            ["event_details__pic",             "pic"],
            ["event_details__region",          "region"],
            ["event_details__source",          "source"],
            ["event_details__details",         "details"],
            ["event_details__subject",         "groupby_col"],
            ["event_details__source_id",       "source_id"],
            ["event_details__subject_id",      "subject_name"],
            ["event_details__collaring_type",  "collaring_type"],
            ["event_details__collaring_reason","collaring_reason"],
            ["event_details__collar_checked_by","collar_checked_by"],
        ],
        [7*cm, W - 7*cm],
    ),
    p("Events are then split by subject_name to align with the per-subject "
      "processing pipeline. The required column for splitting is "
      "<b>event_details__subject_id</b>."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. TRAJECTORY PROCESSING
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Trajectory Processing"),
    hr(),
    h2("5.1  Relocations to trajectories"),
    p("Relocations are converted to trajectory segments via "
      "<b>relocations_to_trajectory</b> using a user-configurable "
      "<b>custom_trajectory_segment_filter</b>. The filter allows "
      "setting maximum time gap and speed thresholds to break trajectories "
      "at implausible movement gaps."),
    sp(6),
    h2("5.2  Temporal index"),
    p("<b>add_temporal_index</b> assigns a temporal index to each "
      "trajectory segment using <b>segment_start</b> as the time column "
      "(cast_to_datetime: true, format: mixed). The index is used for "
      "time-based seasonal aggregation."),
    sp(6),
    h2("5.3  Speed classification"),
    p("Segment speeds (speed_kmhr) are classified into 6 equal-interval "
      "bins via <b>apply_classification</b> (scheme: equal_interval, k: 6). "
      "Labels show ranges to 1 decimal place with a ' km/h' suffix. "
      "A 6-colour diverging ramp is then applied:"),
    make_table(
        [
            ["Bin rank", "Hex color", "Visual meaning"],
            ["1 (slowest)", "#1a9850", "Dark green"],
            ["2",           "#91cf60", "Light green"],
            ["3",           "#d9ef8b", "Yellow-green"],
            ["4",           "#fee08b", "Yellow"],
            ["5",           "#fc8d59", "Orange"],
            ["6 (fastest)", "#d73027", "Red"],
        ],
        [2.5*cm, 3*cm, W - 5.5*cm],
    ),
    sp(4),
    p("After classification, extra__ prefix columns are renamed "
      "(extra__hex_color→hex_color, extra__subject_name→subject_name, "
      "extra__subject_sex→subject_sex, extra__subject_subtype→subject_subtype, "
      "extra__created_at→created_at) and trajectories are split by "
      "subject_name for per-subject map rendering."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. SEASONAL ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Seasonal Analysis"),
    hr(),
    p("Seasonal windows are derived per subject using Google Earth Engine "
      "NDVI data. The workflow uses the subject's ETD polygon as the region "
      "of interest (ROI) for NDVI extraction."),
    sp(6),
    h2("6.1  ETD home range"),
    p("<b>calculate_elliptical_time_density</b> computes an ETD raster for "
      "each subject from its split trajectory GeoDataFrame. Parameters:"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Percentiles",    "50, 60, 70, 80, 90, 95, 99.9"],
            ["CRS",            "ESRI:53042 (World Azimuthal Equidistant)"],
            ["Cell size",      "Auto-scale"],
            ["max_speed_factor","1.05"],
            ["expansion_factor","1.3"],
            ["nodata_value",   "NaN"],
            ["band_count",     "1"],
        ],
        [5*cm, W - 5*cm],
    ),
    p("The ETD is reprojected to EPSG:4326 for map rendering. "
      "A RdYlGn colormap is applied to the percentile column "
      "(etd_percentile_colors) and used to colour the GeoJSON polygon layer."),
    sp(6),
    h2("6.2  Seasonal window detection"),
    p("<b>determine_season_windows</b> calls Google Earth Engine to identify "
      "wet and dry season boundaries for the analysis time range, using the "
      "ETD polygon extent as the ROI. Results are persisted as CSV per subject."),
    sp(6),
    h2("6.3  Season labelling"),
    p("<b>create_seasonal_labels</b> assigns a season label (wet/dry) to each "
      "trajectory segment and relocation based on the GEE-derived windows. "
      "These labels drive the seasonal home range calculation and all "
      "seasonal overlay plots."),
    sp(6),
    h2("6.4  Seasonal home range"),
    p("<b>calculate_seasonal_home_range</b> computes a 99.9th-percentile ETD "
      "polygon grouped by season (groupby_cols: ['season'], auto-scale). "
      "A 2-color scheme is applied:"),
    make_table(
        [
            ["Season index", "Color", "Visual"],
            ["0 (first season)",  "#00bfff", "Deep sky blue"],
            ["1 (second season)", "#ff7f50", "Coral"],
        ],
        [3.5*cm, 3*cm, W - 6.5*cm],
    ),
    sp(4),
    p("A Minimum Convex Polygon (MCP) is generated from the trajectory GDF "
      "(<b>generate_mcp_gdf</b>, planar CRS ESRI:53042) and overlaid as a "
      "hot-pink outline (#ff1493, opacity 0.35, unfilled) on the seasonal "
      "home range map."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. MAPS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Maps"),
    hr(),
    p("All three map types are rendered per subject via <b>mapvalues</b>. "
      "Each map overlays the LandDx styled polygon layers and text label "
      "layer. Map view state is auto-fit to the subject's data extent using "
      "<b>custom_view_state_deck_gdf</b> (buffer: 0.375). Screenshots use "
      "<b>zoom_map_and_screenshot</b> with wait_for_timeout: 40000 ms to "
      "allow tile rendering."),
    sp(6),
    h2("7.1  Speed map"),
    p("Built from trajectory segments as a <b>create_path_layer</b>. "
      "Segments are sorted ascending by speed_bins before rendering "
      "(slowest drawn first, fastest on top)."),
    make_table(
        [
            ["Parameter", "Value"],
            ["Layer type",         "Path (line segments)"],
            ["Color column",       "speed_bins_colormap (6-bin RdYlGn)"],
            ["Line width",         "2.55 px (min 2 px / max 8 px)"],
            ["Opacity",            "0.45"],
            ["Cap / joint style",  "Rounded"],
            ["Screenshot size",    "1280 × 720 px"],
            ["Output",             "<subject>_speedmap.html / .png"],
        ],
        [4.5*cm, W - 4.5*cm],
    ),
    sp(6),
    h2("7.2  Home range map (ETD)"),
    p("ETD percentile polygons are rendered as filled GeoJSON layers. "
      "All 7 percentile contours (50–99.9) are stacked with the outermost "
      "contour at the bottom."),
    make_table(
        [
            ["Parameter", "Value"],
            ["Layer type",      "GeoJSON polygon"],
            ["Color column",    "etd_percentile_colors (RdYlGn on percentile)"],
            ["Opacity",         "0.45"],
            ["Line width",      "1.55 px"],
            ["Screenshot size", "602 × 855 px"],
            ["Output",          "<subject>_homerange.html / .png"],
        ],
        [4.5*cm, W - 4.5*cm],
    ),
    sp(6),
    h2("7.3  Seasonal home range map"),
    p("Two seasonal ETD polygons (99.9th percentile, wet vs. dry) are "
      "rendered as filled GeoJSON layers. The MCP polygon is overlaid as "
      "an unfilled hot-pink outline."),
    make_table(
        [
            ["Layer", "Color", "Opacity", "Notes"],
            ["Seasonal HR (wet)",  "#00bfff", "0.15", "Deep sky blue fill, black outline"],
            ["Seasonal HR (dry)",  "#ff7f50", "0.15", "Coral fill, black outline"],
            ["MCP outline",        "#ff1493", "0.35", "Unfilled, hot-pink stroke only"],
        ],
        [3*cm, 3*cm, 2*cm, W - 8*cm],
    ),
    p("Screenshot size: 602 × 855 px. "
      "Output: <b>&lt;subject&gt;_seasonal_home_range.html / .png</b>"),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. SEASONAL PLOTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Seasonal Plots"),
    hr(),
    p("Four time-series plots are generated per subject. Each plot overlays "
      "the GEE-derived seasonal windows as background bands. All plot "
      "screenshots are rendered at <b>2238 × 450 px</b> with "
      "wait_for_timeout: 5 ms (fast static HTML)."),
    sp(6),
    make_table(
        [
            ["Plot", "Task", "X axis", "Y axis", "Output file"],
            ["Net Square Displacement",
             "draw_season_nsd_plot",
             "Time",
             "NSD from first fix (km²)",
             "<subject>_nsd_seasonal_plot.html/.png"],
            ["Speed",
             "draw_season_speed_plot",
             "Time",
             "Speed (km/h)",
             "<subject>_speed_seasonal_plot.html/.png"],
            ["Collar Events",
             "draw_season_collared_plot",
             "Time",
             "Event type (collar check / collaring / source failure)",
             "<subject>_collared_subject_plot.html/.png"],
            ["MCP Asymptote",
             "draw_season_mcp_plot",
             "Cumulative fixes",
             "MCP area (km²)",
             "<subject>_mcp_asymptote_plot.html/.png"],
        ],
        [3.5*cm, 4*cm, 2.5*cm, 3*cm, W - 13*cm],
    ),
    sp(6),
    note("The collar event plot uses filter_col: subject_name to match events "
         "from the MEP event pipeline (mep_collar_check, mep_collaring, "
         "mep_source_failure) to the current subject's relocations."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. STATISTICS AND OCCUPANCY
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Statistics and Occupancy Analysis"),
    hr(),
    h2("9.1  Subject statistics"),
    p("<b>compute_subject_stats</b> derives movement metrics per subject "
      "by combining the ETD GDF and trajectory GDF (grouped by subject_name). "
      "Results are persisted as CSV:"),
    make_table(
        [
            ["Metric", "Unit", "Description"],
            ["MCP",               "km²", "Minimum Convex Polygon area"],
            ["ETD",               "km²", "Elliptical Time Density 99.9th percentile area"],
            ["distance_travelled","km",  "Total path length of trajectory"],
            ["max_displacement",  "km",  "Maximum distance from first fix"],
            ["night_day_ratio",   "—",   "Ratio of nocturnal to diurnal fixes"],
        ],
        [4*cm, 1.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("9.2  Regional occupancy"),
    p("<b>compute_subject_occupancy</b> intersects the subject's ETD polygon "
      "with LandDx region templates in planar CRS ESRI:53042 to compute "
      "the proportion of home range falling in each land category. "
      "LandDx polygons are first indexed via "
      "<b>build_template_region_lookup</b> and "
      "<b>compute_template_regions</b>."),
    make_table(
        [
            ["Occupancy column",  "Unit", "Description"],
            ["national_pa_use",   "%", "National protected area use (National Park + National Reserve)"],
            ["community_pa_use",  "%", "Community conservancy use"],
            ["crop_raid_percent", "%", "Agricultural land use"],
            ["kenya_use",         "%", "Overall Kenya coverage"],
            ["unprotected",       "%", "Unprotected land use"],
        ],
        [4*cm, 1.5*cm, W - 5.5*cm],
    ),
    p("All five occupancy columns are exposed as single-value dashboard "
      "widgets (decimal_places: 2) and written to CSV per subject."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. WORD MAPBOOK
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Word Mapbook"),
    hr(),
    p("The final report is a merged Word document assembled from a cover "
      "page and one section page per subject."),
    sp(6),
    h2("10.1  Cover page"),
    make_table(
        [
            ["Template", "cer_cover_page.docx (downloaded from Dropbox)"],
            ["Output", "mep_context.docx"],
            ["Fields", "Subject count (unique subjects on trajectories), "
                       "report_period (time range), prepared_by='Ecoscope'"],
        ],
        [3*cm, W - 3*cm],
        header_row=False,
    ),
    sp(6),
    h2("10.2  Per-subject section"),
    make_table(
        [
            ["Template", "mep_subject_template_two.docx (downloaded from Dropbox)"],
            ["Output", "<subject>.docx (one file per subject, validate_images: true)"],
        ],
        [3*cm, W - 3*cm],
        header_row=False,
    ),
    sp(4),
    p("Each section is populated by <b>create_mep_subject_context</b> with "
      "the following 11 assets (assembled via zip_groupbykey):"),
    make_table(
        [
            ["Argument", "Source"],
            ["profile_photo_path",         "persist_subject_photo (.png)"],
            ["subject_info_path",           "persist_subject_info (.csv)"],
            ["speedmap_path",               "convert_speedmap_png (1280×720)"],
            ["homerange_map_path",          "convert_homerange_png (602×855)"],
            ["seasonal_homerange_map_path", "convert_season_png (602×855)"],
            ["nsd_plot_path",               "convert_nsd_png (2238×450)"],
            ["speed_plot_path",             "convert_speed_png (2238×450)"],
            ["collared_event_plot_path",    "convert_events_png (2238×450)"],
            ["mcp_plot_path",               "convert_mcp_png (2238×450)"],
            ["subject_stats_table_path",    "persist_subject_stats (.csv)"],
            ["subject_occupancy_table_path","persist_subject_occupancy (.csv)"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    sp(6),
    h2("10.3  Merge"),
    p("<b>merge_mapbook_files</b> merges the cover page with all per-subject "
      "section documents into a single output file."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 11. DASHBOARD WIDGETS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("11. Dashboard Widgets"),
    hr(),
    p("The final <b>gather_dashboard</b> call assembles 17 widget groups "
      "into an interactive Ecoscope dashboard. All widgets are per-subject "
      "grouped views merged via <b>merge_widget_views</b>."),
    sp(6),
    h2("11.1  Single-value widgets (10)"),
    make_table(
        [
            ["Widget title", "Source column", "Unit"],
            ["National protected area use", "national_pa_use",   "%"],
            ["Community protected area use","community_pa_use",   "%"],
            ["Agricultural land use",       "crop_raid_percent", "%"],
            ["Kenya use",                   "kenya_use",         "%"],
            ["Unprotected use",             "unprotected",       "%"],
            ["MCP Area",                    "MCP",               "km²"],
            ["ETD",                         "ETD",               "km²"],
            ["Distance Travelled",          "distance_travelled","km²"],
            ["Max Displacement",            "max_displacement",  "km²"],
            ["Night Day Ratio",             "night_day_ratio",   "—"],
        ],
        [5*cm, 4.5*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("11.2  Map and plot widgets (7)"),
    make_table(
        [
            ["Widget title", "Source"],
            ["Speed Map",             "persist_speedmap_html"],
            ["Home Range",            "persist_homerange_html"],
            ["Seasonal Home Range",   "persist_seasonal_home_range_html"],
            ["Net Square Displacement (NSD)", "persist_nsd_html_urls"],
            ["Speed",                 "persist_speed_html_urls"],
            ["Collared Subject Plot", "persist_collared_subject_plots"],
            ["MCP Asymptote",         "persist_mcp_html_urls"],
        ],
        [5.5*cm, W - 5.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 12. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("12. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>. "
      "Files marked with <i>&lt;subject&gt;</i> are produced once per "
      "subject in the group."),
    make_table(
        [
            ["File", "Description"],
            # per-subject
            ["<subject>_speedmap.html / .png",
             "Speed map (1280×720 px screenshot)"],
            ["<subject>_homerange.html / .png",
             "ETD home range map (602×855 px screenshot)"],
            ["<subject>_seasonal_home_range.html / .png",
             "Seasonal home range + MCP overlay (602×855 px)"],
            ["<subject>_nsd_seasonal_plot.html / .png",
             "Net Square Displacement plot (2238×450 px)"],
            ["<subject>_speed_seasonal_plot.html / .png",
             "Speed seasonal plot (2238×450 px)"],
            ["<subject>_collared_subject_plot.html / .png",
             "Collar event timeline plot (2238×450 px)"],
            ["<subject>_mcp_asymptote_plot.html / .png",
             "MCP area asymptote plot (2238×450 px)"],
            ["<subject>_subject_info.csv",
             "Subject metadata (name, sex, DOB, status, region, etc.)"],
            ["<subject>_subject_stats.csv",
             "Movement stats: MCP, ETD, distance, max displacement, night/day ratio"],
            ["<subject>_subject_occupancy.csv",
             "Occupancy percentages by land category"],
            ["<subject>_seasonal_windows.csv",
             "GEE-derived wet/dry season date windows"],
            ["<subject>_profile_photo.png",
             "Subject profile photo downloaded from EarthRanger"],
            # word report
            ["mep_context.docx",
             "Cover page (subject count, report period, prepared by)"],
            ["<subject>_section.docx",
             "Per-subject populated Word section"],
            ["<merged_mapbook>.docx",
             "Final merged Word mapbook (cover + all subject sections)"],
        ],
        [7*cm, W - 7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 13. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("13. Workflow Execution Logic"),
    hr(),
    h2("13.1  Global skip conditions"),
    p("The top-level <b>task-instance-defaults</b> block applies two skip "
      "conditions to every task unless overridden:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream "
           "DataFrame dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was skipped"),
    p("A special override <b>skipif: conditions: [never]</b> is applied to "
      "widget creation tasks to ensure dashboard entries are always created "
      "even if the underlying data is empty."),
    sp(6),
    h2("13.2  mapvalues fan-out"),
    p("The workflow uses <b>mapvalues</b> extensively to run per-subject "
      "processing in parallel. The fan-out starts at <b>split_traj_by_group</b> "
      "and <b>split_subject_by_group</b>, which partition data by subject_name. "
      "Downstream tasks receive one data slice per subject and run "
      "independently. Key fan-out chains:"),
    bullet("split_traj_by_group → sort_trajs_by_speed → apply_speed_colormap "
           "→ filter_speedmap_gdf → generate_speedmap_layers → draw_speedmap"),
    bullet("split_traj_by_group → generate_etd → determine_seasonal_windows "
           "→ add_season_labels → seasonal_home_range"),
    bullet("split_subject_by_group → download_profile_pic, "
           "download_subject_info"),
    bullet("zip_traj_etd_gdf → generate_subject_stats"),
    bullet("zip_etd_subject_df → process_subject_occupancy"),
    sp(6),
    h2("13.3  zip_groupbykey"),
    p("<b>zip_groupbykey</b> is used to pair multiple per-subject sequences "
      "by their shared key (subject_name) before passing to mapvalues tasks. "
      "Examples:"),
    bullet("zip_etd_with_traj — pairs seasonal windows with trajectory slices "
           "for season labelling"),
    bullet("zip_relocs_with_seasons — pairs seasonal windows with relocation "
           "slices for NSD/speed/collared/MCP plots"),
    bullet("zip_hr_value, zip_speed_value, zip_seasonal_value — pair view "
           "states with HTML file paths for zoom_map_and_screenshot"),
    bullet("group_subject_report_context — zips 11 per-subject asset paths "
           "into tuples for Word template population"),
    sp(6),
    h2("13.4  Screenshot timing"),
    make_table(
        [
            ["wait_for_timeout", "Applied to", "Width × Height"],
            ["40000 ms", "All map screenshots "
                         "(speed map, home range, seasonal home range)",
             "Speed: 1280×720 / HR: 602×855 / Season: 602×855"],
            ["5 ms", "All chart screenshots "
                     "(NSD, speed, collared events, MCP asymptote)",
             "2238×450 (all plots)"],
        ],
        [3*cm, 5*cm, W - 8*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 14. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("14. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-workflows-core",        "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.7.*"],
            ["ecoscope-workflows-ext-big-life","0.0.8.*"],
            ["ecoscope-workflows-ext-mep",     "0.0.12.*"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda channels. "
         "The wildcard patch-version pin (.*) allows bug-fix releases to be "
         "picked up automatically while keeping minor and major versions locked."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
