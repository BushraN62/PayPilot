import csv
import io
import os
import zipfile
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# College Scorecard API and bulk field-of-study data sources.
API_KEY = os.getenv("COLLEGE_SCORECARD_API_KEY")
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"
PROGRAMS_SOURCE_URL = (
    "https://data.ed.gov/dataset/9dc70e6b-8426-4d71-b9d5-70ce6094a3f4/"
    "resource/ff68afc4-6d23-459d-9f60-4006e4f85583/download/"
    "most-recent-cohorts-field-of-study_04172025.zip"
)

# Local cache avoids repeated API and bulk-data requests during searches.
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
COLLEGES_FILE = DATA_DIR / "colleges.csv"
PROGRAMS_FILE = DATA_DIR / "programs.csv"
PER_PAGE = 100

# User-facing filter values mapped to College Scorecard codes.
ownership_map = {
    "Public": 1,
    "Private Nonprofit": 2,
    "Private For-Profit": 3,
}

degree_map = {
    "Certificate": 1,
    "Associate": 2,
    "Bachelor": 3,
    "Graduate": 4,
}

# CIP prefixes used to group Scorecard programs into broader major categories.
MAJOR_CIP_PREFIXES = {
    "Computer Science": ("11",),
    "Engineering": ("14",),
    "Business": ("52",),
    "Nursing": ("5138",),
    "Healthcare": ("51",),
    "Education": ("13",),
    "Biology": ("2601",),
    "Mathematics": ("27",),
    "Psychology": ("4201",),
    "Economics": ("4506",),
    "Communications": ("09",),
    "Science": ("26", "40"),
    "Arts": ("50",),
}

# API fields retained in the local college cache.
COLLEGE_FIELDS = [
    "id",
    "school.name",
    "school.state",
    "school.ownership",
    "school.degrees_awarded.predominant",
    "latest.cost.tuition.in_state",
    "latest.earnings.10_yrs_after_entry.median",
    "latest.aid.median_debt.completers.overall",
    "latest.completion.rate",
    "latest.admissions.admission_rate.overall",
]

COLLEGE_COLUMNS = [
    "id",
    "name",
    "state",
    "ownership",
    "degree",
    "tuition",
    "earnings",
    "debt",
    "graduation_rate",
    "acceptance_rate",
]

PROGRAM_COLUMNS = ["school_id", "cip_code", "program_name"]

# Cache major-to-school matches so repeated searches avoid rescanning programs.csv.
PROGRAM_CACHE = {}


def _fetch_all(fields):
    """Fetch all pages for the requested College Scorecard fields."""
    if not API_KEY:
        raise RuntimeError(
            "COLLEGE_SCORECARD_API_KEY is required to build the local data cache."
        )

    records = []
    page = 0

    while True:
        response = requests.get(
            BASE_URL,
            params={
                "api_key": API_KEY,
                "fields": ",".join(fields),
                "per_page": PER_PAGE,
                "page": page,
            },
            timeout=30,
        )
        response.raise_for_status()

        payload = response.json()
        results = payload.get("results", [])

        if not results:
            break

        records.extend(results)

        # Stop when metadata or page size indicates the final page.
        metadata = payload.get("metadata", {})
        total = metadata.get("total")

        if total is not None and len(records) >= total:
            break

        if len(results) < PER_PAGE:
            break

        page += 1

    return records


def _write_csv(path, fieldnames, rows):
    """Write records to a UTF-8 CSV file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _read_csv(path):
    """Read a CSV file into a list of dictionaries."""
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def _download_programs():
    """Download and normalize Scorecard field-of-study program data."""
    response = requests.get(PROGRAMS_SOURCE_URL, timeout=120)
    response.raise_for_status()

    # The bulk download contains the field-of-study CSV inside a ZIP archive.
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        csv_name = next(
            name for name in archive.namelist()
            if name.lower().endswith(".csv")
        )

        with archive.open(csv_name) as raw_file:
            reader = csv.DictReader(
                io.TextIOWrapper(raw_file, encoding="utf-8-sig")
            )

            return [
                {
                    "school_id": row.get("UNITID", ""),
                    "cip_code": row.get("CIPCODE", ""),
                    "program_name": row.get("CIPDESC", ""),
                }
                for row in reader
                if row.get("UNITID") and row.get("CIPCODE")
            ]


def _build_cache():
    """Build the local college and program datasets."""
    college_records = _fetch_all(COLLEGE_FIELDS)

    # Flatten Scorecard field names into the simpler structure used by the app.
    colleges = [
        {
            "id": record.get("id"),
            "name": record.get("school.name"),
            "state": record.get("school.state"),
            "ownership": record.get("school.ownership"),
            "degree": record.get("school.degrees_awarded.predominant"),
            "tuition": record.get("latest.cost.tuition.in_state"),
            "earnings": record.get(
                "latest.earnings.10_yrs_after_entry.median"
            ),
            "debt": record.get(
                "latest.aid.median_debt.completers.overall"
            ),
            "graduation_rate": record.get("latest.completion.rate"),
            "acceptance_rate": record.get(
                "latest.admissions.admission_rate.overall"
            ),
        }
        for record in college_records
    ]

    _write_csv(COLLEGES_FILE, COLLEGE_COLUMNS, colleges)
    _write_csv(PROGRAMS_FILE, PROGRAM_COLUMNS, _download_programs())


def _number(value):
    """Convert cached CSV values to numeric types when possible."""
    try:
        number = float(value) if value not in (None, "") else None
        return (
            int(number)
            if number is not None and number.is_integer()
            else number
        )
    except (TypeError, ValueError):
        return None


def _matching_school_ids(major):
    """Return school IDs offering programs that match a major's CIP prefixes."""
    prefixes = MAJOR_CIP_PREFIXES.get(major)

    if not prefixes:
        return None

    if major in PROGRAM_CACHE:
        return PROGRAM_CACHE[major]

    matching = set()

    with PROGRAMS_FILE.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Normalize CIP codes before comparing them with configured prefixes.
            cip = row["cip_code"].replace(".", "")

            if any(cip.startswith(prefix) for prefix in prefixes):
                matching.add(row["school_id"])

    PROGRAM_CACHE[major] = matching
    return matching


def search_colleges(
    state=None,
    school_type=None,
    major=None,
    degree_level=None,
    min_earnings=None,
    max_debt=None,
    max_tuition=None,
):
    """Search the local College Scorecard cache using optional filters."""
    # Build the cache lazily on the first search.
    if not COLLEGES_FILE.exists() or not PROGRAMS_FILE.exists():
        _build_cache()

    matching_ids = _matching_school_ids(major) if major else None
    selected_ownership = (
        ownership_map.get(school_type) if school_type else None
    )
    selected_degree = (
        degree_map.get(degree_level) if degree_level else None
    )

    colleges = []

    for row in _read_csv(COLLEGES_FILE):
        if state and row["state"] != state:
            continue

        if (
            selected_ownership
            and _number(row["ownership"]) != selected_ownership
        ):
            continue

        if (
            selected_degree
            and _number(row["degree"]) != selected_degree
        ):
            continue

        if min_earnings and (
            _number(row["earnings"]) is None
            or _number(row["earnings"]) < min_earnings
        ):
            continue

        if max_debt and (
            _number(row["debt"]) is None
            or _number(row["debt"]) > max_debt
        ):
            continue

        if max_tuition and (
            _number(row["tuition"]) is None
            or _number(row["tuition"]) > max_tuition
        ):
            continue

        if matching_ids is not None and row["id"] not in matching_ids:
            continue

        colleges.append({
            "id": row["id"],
            "name": row["name"],
            "state": row["state"],
            "tuition": _number(row["tuition"]),
            "earnings": _number(row["earnings"]),
            "debt": _number(row["debt"]),
            "graduation_rate": _number(row["graduation_rate"]),
            "acceptance_rate": _number(row["acceptance_rate"]),
        })

    return colleges


def get_colleges_by_ids(school_ids):
    """Return cached colleges matching the provided Scorecard IDs."""
    if not school_ids:
        return []

    if not COLLEGES_FILE.exists() or not PROGRAMS_FILE.exists():
        _build_cache()

    selected_ids = {str(school_id) for school_id in school_ids}
    colleges = []

    for row in _read_csv(COLLEGES_FILE):
        if row["id"] not in selected_ids:
            continue

        colleges.append({
            "id": row["id"],
            "name": row["name"],
            "state": row["state"],
            "tuition": _number(row["tuition"]),
            "earnings": _number(row["earnings"]),
            "debt": _number(row["debt"]),
            "graduation_rate": _number(row["graduation_rate"]),
            "acceptance_rate": _number(row["acceptance_rate"]),
        })

    college_by_id = {
        str(college["id"]): college
        for college in colleges
    }

    # Return results in the same order the IDs were submitted.
    return [
        college_by_id[school_id]
        for school_id in map(str, school_ids)
        if school_id in college_by_id
    ]

