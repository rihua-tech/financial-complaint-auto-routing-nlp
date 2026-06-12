"""CFPB complaint download helpers.

This module is the source of truth for the raw data-ingestion workflow used by
the download notebook. It preserves original CFPB API columns while filtering
to records that are usable for later NLP modeling: non-empty complaint
narratives, non-empty product labels, calendar-year dates, and unique complaint
IDs.
"""

from __future__ import annotations

import math
import time
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd
import requests


BASE_URL = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
REQUEST_HEADERS = {"User-Agent": "financial-complaint-auto-routing-nlp/1.0 (student ML project)"}
REQUIRED_COLUMNS = ["complaint_what_happened", "product", "date_received", "complaint_id"]
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


def _parse_dates(date_values: pd.Series) -> pd.Series:
    """Parse CFPB date values and normalize them to timezone-naive UTC."""
    return pd.to_datetime(date_values, errors="coerce", utc=True).dt.tz_convert(None)


def _complaint_id_keys(df: pd.DataFrame) -> pd.Series:
    """Return normalized complaint ID keys for validation and deduplication."""
    return df["complaint_id"].fillna("").astype(str).str.strip()


def month_windows(year: int) -> list[dict[str, str]]:
    """Return inclusive monthly API date windows for a calendar year."""
    windows = []

    for month in range(1, 13):
        start = pd.Timestamp(year=year, month=month, day=1)
        end = start + pd.offsets.MonthEnd(0)
        windows.append(
            {
                "month": f"{year}-{month:02d}",
                "start": start.strftime("%Y-%m-%d"),
                "end": end.strftime("%Y-%m-%d"),
            }
        )

    return windows


def daily_windows_for_month(month_window: dict[str, str]) -> list[dict[str, str]]:
    """Return inclusive daily API date windows for one month window."""
    days = pd.date_range(month_window["start"], month_window["end"], freq="D")
    return [
        {
            "month": month_window["month"],
            "date": day.strftime("%Y-%m-%d"),
            "start": day.strftime("%Y-%m-%d"),
            "end": day.strftime("%Y-%m-%d"),
            "end_exclusive": (day + pd.Timedelta(days=1)).strftime("%Y-%m-%d"),
        }
        for day in days
    ]


def build_monthly_targets(year: int = 2024, total_rows: int = 50_000) -> list[dict[str, int | str]]:
    """Build roughly equal monthly row targets with the final month adjusted."""
    if total_rows <= 0:
        raise ValueError("total_rows must be positive.")

    windows = month_windows(year)
    target_per_month = math.ceil(total_rows / len(windows))
    remaining_rows = total_rows
    targets = []

    for index, window in enumerate(windows):
        if index == len(windows) - 1:
            month_target = remaining_rows
        else:
            month_target = min(target_per_month, remaining_rows)

        targets.append({**window, "target_rows": month_target})
        remaining_rows -= month_target

    return targets


def allocate_month_target_to_days(month_target: dict[str, int | str]) -> list[dict[str, int | str]]:
    """Allocate one monthly target as evenly as possible across its days."""
    daily_windows = daily_windows_for_month(month_target)
    target_rows = int(month_target["target_rows"])
    base_target = target_rows // len(daily_windows)
    remainder = target_rows % len(daily_windows)

    daily_targets = []
    for index, daily_window in enumerate(daily_windows):
        daily_target = base_target + (1 if index < remainder else 0)
        daily_targets.append({**daily_window, "target_rows": daily_target})

    return daily_targets


def build_daily_targets(year: int = 2024, total_rows: int = 50_000) -> list[dict[str, int | str]]:
    """Build daily row targets across a monthly-balanced calendar year sample."""
    daily_targets = []

    for monthly_target in build_monthly_targets(year=year, total_rows=total_rows):
        daily_targets.extend(allocate_month_target_to_days(monthly_target))

    return daily_targets


def raw_csv_relative_path(year: int) -> Path:
    """Return the repository-relative raw CSV path for a calendar year."""
    return Path("data") / "raw" / f"cfpb_complaints_{year}_raw.csv"


def raw_csv_path(project_root: str | Path, year: int) -> Path:
    """Return the absolute raw CSV path for a calendar year."""
    return Path(project_root) / raw_csv_relative_path(year)


def extract_hits(api_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the hit objects from a CFPB API response."""
    return api_json.get("hits", {}).get("hits", [])


def extract_records(api_json: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract complaint records from a CFPB API response."""
    return [hit.get("_source", {}) for hit in extract_hits(api_json)]


def get_next_search_after(api_json: dict[str, Any]) -> str | None:
    """Build the CFPB search_after token from the final hit in a page."""
    hits = extract_hits(api_json)

    if not hits:
        return None

    sort_values = hits[-1].get("sort")

    if not sort_values:
        return None

    return "_".join(str(value) for value in sort_values)


def fetch_cfpb_page(
    date_start: str,
    date_end: str,
    search_after: str | None = None,
    page_size: int = 1_000,
    session: requests.Session | None = None,
    timeout: int = 30,
    max_retries: int = 3,
    backoff_seconds: float = 1.0,
) -> dict[str, Any]:
    """Fetch one CFPB API page for a date window."""
    params = {
        "date_received_min": date_start,
        "date_received_max": date_end,
        "has_narrative": "true",
        "sort": "created_date_desc",
        "size": page_size,
        "frm": 0,
        "no_aggs": "true",
        "no_highlight": "true",
    }

    if search_after is not None:
        params["search_after"] = search_after

    client = session or requests

    for attempt in range(max_retries + 1):
        try:
            response = client.get(BASE_URL, params=params, headers=REQUEST_HEADERS, timeout=timeout)
        except requests.exceptions.RequestException as exc:
            if attempt >= max_retries:
                raise requests.exceptions.RequestException(
                    f"CFPB API request failed for {date_start} to {date_end} after "
                    f"{attempt + 1} attempts: {exc}"
                ) from exc

            time.sleep(backoff_seconds * (2**attempt))
            continue

        if response.status_code == 403:
            raise requests.exceptions.HTTPError(
                "CFPB API request returned 403 Forbidden. The CFPB API rejected this request; "
                "retry later, reduce the page size, or use existing local ignored CSV files "
                "if they are already available.",
                response=response,
            )

        if response.status_code in TRANSIENT_STATUS_CODES and attempt < max_retries:
            retry_after = response.headers.get("Retry-After")
            if retry_after is not None:
                try:
                    sleep_for = float(retry_after)
                except ValueError:
                    sleep_for = backoff_seconds * (2**attempt)
            else:
                sleep_for = backoff_seconds * (2**attempt)

            time.sleep(sleep_for)
            continue

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise requests.exceptions.HTTPError(
                f"CFPB API request failed with HTTP {response.status_code} "
                f"for {date_start} to {date_end}.",
                response=response,
            ) from exc

        return response.json()

    raise requests.exceptions.HTTPError(
        f"CFPB API request failed after {max_retries + 1} attempts "
        f"for {date_start} to {date_end}."
    )


def deduplicate_by_complaint_id(df: pd.DataFrame) -> pd.DataFrame:
    """Deduplicate records by complaint_id while preserving original columns."""
    if df.empty:
        return df.copy()

    missing_columns = [column for column in ["complaint_id"] if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required CFPB columns: {missing_columns}")

    complaint_id_keys = _complaint_id_keys(df)
    keep_rows = complaint_id_keys.ne("") & ~complaint_id_keys.duplicated()
    return df.loc[keep_rows].copy()


def filter_valid_records(
    records: Iterable[dict[str, Any]],
    date_start: str,
    date_end_exclusive: str,
) -> pd.DataFrame:
    """Filter raw records while preserving original CFPB API columns."""
    df = pd.DataFrame(records)

    if df.empty:
        return df

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required CFPB columns: {missing_columns}")

    text_has_value = df["complaint_what_happened"].fillna("").astype(str).str.strip().ne("")
    product_has_value = df["product"].fillna("").astype(str).str.strip().ne("")
    complaint_id_has_value = _complaint_id_keys(df).ne("")

    received_dates = _parse_dates(df["date_received"])
    start = pd.Timestamp(date_start)
    end_exclusive = pd.Timestamp(date_end_exclusive)
    in_window = received_dates.notna() & received_dates.ge(start) & received_dates.lt(end_exclusive)

    filtered = df[text_has_value & product_has_value & complaint_id_has_value & in_window].copy()
    return deduplicate_by_complaint_id(filtered)


def filter_valid_records_for_year(records: Iterable[dict[str, Any]], year: int) -> pd.DataFrame:
    """Filter raw records to valid rows inside a calendar year."""
    return filter_valid_records(
        records=records,
        date_start=f"{year}-01-01",
        date_end_exclusive=f"{year + 1}-01-01",
    )


def _fetch_next_valid_page(
    date_start: str,
    date_end: str,
    date_end_exclusive: str,
    search_after: str | None,
    page_size: int,
    session: requests.Session,
) -> dict[str, Any]:
    """Fetch and filter the next API page for one date window."""
    api_json = fetch_cfpb_page(
        date_start=date_start,
        date_end=date_end,
        search_after=search_after,
        page_size=page_size,
        session=session,
    )
    raw_records = extract_records(api_json)
    next_search_after = get_next_search_after(api_json)
    exhausted = not raw_records or next_search_after is None
    valid_df = filter_valid_records(
        records=raw_records,
        date_start=date_start,
        date_end_exclusive=date_end_exclusive,
    )

    return {
        "valid_df": valid_df,
        "raw_record_count": len(raw_records),
        "next_search_after": next_search_after,
        "exhausted": exhausted,
    }


def _merge_record_frames(frames: list[pd.DataFrame]) -> pd.DataFrame:
    """Merge record frames and deduplicate complaint IDs."""
    non_empty_frames = [frame for frame in frames if not frame.empty]

    if not non_empty_frames:
        return pd.DataFrame()

    return deduplicate_by_complaint_id(pd.concat(non_empty_frames, ignore_index=True))


def collect_daily_sample(
    daily_target: dict[str, int | str],
    page_size: int = 1_000,
    max_pages_per_day: int = 10,
    sleep_seconds: float = 0.05,
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Collect enough valid records for one day, or all available records."""
    client = session or requests.Session()
    target_rows = int(daily_target["target_rows"])
    records_df = pd.DataFrame()
    search_after = None
    pages_downloaded = 0
    raw_records_downloaded = 0
    exhausted = False

    while len(records_df) < target_rows and pages_downloaded < max_pages_per_day:
        page_result = _fetch_next_valid_page(
            date_start=str(daily_target["start"]),
            date_end=str(daily_target["end"]),
            date_end_exclusive=str(daily_target["end_exclusive"]),
            search_after=search_after,
            page_size=page_size,
            session=client,
        )
        records_df = _merge_record_frames([records_df, page_result["valid_df"]])
        pages_downloaded += 1
        raw_records_downloaded += int(page_result["raw_record_count"])
        search_after = page_result["next_search_after"]
        exhausted = bool(page_result["exhausted"])

        if exhausted:
            break

        if len(records_df) < target_rows:
            time.sleep(sleep_seconds)

    return {
        **daily_target,
        "records_df": records_df,
        "search_after": search_after,
        "exhausted": exhausted,
        "pages_downloaded": pages_downloaded,
        "raw_records_downloaded": raw_records_downloaded,
        "max_pages_hit": pages_downloaded >= max_pages_per_day and not exhausted,
        "backfilled_rows": 0,
    }


def _take_unselected_rows(
    candidate_df: pd.DataFrame,
    selected_ids: set[str],
    limit: int,
) -> pd.DataFrame:
    """Take rows whose complaint IDs are not already selected."""
    if candidate_df.empty or limit <= 0:
        return pd.DataFrame(columns=candidate_df.columns)

    candidate_ids = _complaint_id_keys(candidate_df)
    available_rows = candidate_df[~candidate_ids.isin(selected_ids)].copy()
    return available_rows.head(limit).copy()


def _append_rows(selected_df: pd.DataFrame, rows_to_add: pd.DataFrame) -> pd.DataFrame:
    """Append rows to a selected sample and deduplicate complaint IDs."""
    if rows_to_add.empty:
        return selected_df

    return _merge_record_frames([selected_df, rows_to_add])


def backfill_month_from_daily_states(
    selected_df: pd.DataFrame,
    daily_states: list[dict[str, Any]],
    month_target_rows: int,
    page_size: int,
    max_pages_per_day: int,
    sleep_seconds: float,
    session: requests.Session,
) -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    """Backfill a monthly shortfall from other days in the same month."""
    selected_df = deduplicate_by_complaint_id(selected_df)

    while len(selected_df) < month_target_rows:
        progress_made = False

        for state in daily_states:
            remaining_rows = month_target_rows - len(selected_df)
            if remaining_rows <= 0:
                break

            selected_ids = set(_complaint_id_keys(selected_df))
            candidate_rows = _take_unselected_rows(state["records_df"], selected_ids, remaining_rows)

            if not candidate_rows.empty:
                selected_df = _append_rows(selected_df, candidate_rows)
                state["backfilled_rows"] += len(candidate_rows)
                progress_made = True

            remaining_rows = month_target_rows - len(selected_df)
            if remaining_rows <= 0:
                break

            can_fetch_more = not state["exhausted"] and state["pages_downloaded"] < max_pages_per_day
            if not can_fetch_more:
                continue

            page_result = _fetch_next_valid_page(
                date_start=str(state["start"]),
                date_end=str(state["end"]),
                date_end_exclusive=str(state["end_exclusive"]),
                search_after=state["search_after"],
                page_size=page_size,
                session=session,
            )
            state["records_df"] = _merge_record_frames([state["records_df"], page_result["valid_df"]])
            state["pages_downloaded"] += 1
            state["raw_records_downloaded"] += int(page_result["raw_record_count"])
            state["search_after"] = page_result["next_search_after"]
            state["exhausted"] = bool(page_result["exhausted"])
            state["max_pages_hit"] = state["pages_downloaded"] >= max_pages_per_day and not state["exhausted"]
            progress_made = True

            selected_ids = set(_complaint_id_keys(selected_df))
            candidate_rows = _take_unselected_rows(state["records_df"], selected_ids, remaining_rows)

            if not candidate_rows.empty:
                selected_df = _append_rows(selected_df, candidate_rows)
                state["backfilled_rows"] += len(candidate_rows)

            time.sleep(sleep_seconds)

        if not progress_made:
            break

    return selected_df, daily_states


def collect_monthly_daily_stratified_sample(
    monthly_target: dict[str, int | str],
    page_size: int = 1_000,
    max_pages_per_day: int = 10,
    sleep_seconds: float = 0.05,
    session: requests.Session | None = None,
    verbose: bool = True,
) -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    """Collect one monthly sample by sampling each day and backfilling locally."""
    client = session or requests.Session()
    daily_targets = allocate_month_target_to_days(monthly_target)
    daily_states = []
    selected_frames = []
    daily_log = []

    for daily_target in daily_targets:
        state = collect_daily_sample(
            daily_target=daily_target,
            page_size=page_size,
            max_pages_per_day=max_pages_per_day,
            sleep_seconds=sleep_seconds,
            session=client,
        )
        target_rows = int(state["target_rows"])
        selected_day_df = state["records_df"].head(target_rows).copy()
        selected_frames.append(selected_day_df)
        shortfall = max(0, target_rows - len(selected_day_df))
        daily_states.append(state)
        daily_log.append(
            {
                "month": state["month"],
                "date": state["date"],
                "target_rows": target_rows,
                "initial_valid_rows": len(state["records_df"]),
                "initial_selected_rows": len(selected_day_df),
                "shortfall_before_backfill": shortfall,
                "pages_downloaded": state["pages_downloaded"],
                "raw_records_downloaded": state["raw_records_downloaded"],
                "max_pages_hit": state["max_pages_hit"],
            }
        )

    selected_df = _merge_record_frames(selected_frames)
    month_target_rows = int(monthly_target["target_rows"])
    rows_before_backfill = len(selected_df)
    selected_df, daily_states = backfill_month_from_daily_states(
        selected_df=selected_df,
        daily_states=daily_states,
        month_target_rows=month_target_rows,
        page_size=page_size,
        max_pages_per_day=max_pages_per_day,
        sleep_seconds=sleep_seconds,
        session=client,
    )
    selected_df = selected_df.head(month_target_rows).copy()

    backfilled_rows_by_date = {state["date"]: state["backfilled_rows"] for state in daily_states}
    pages_by_date = {state["date"]: state["pages_downloaded"] for state in daily_states}
    raw_by_date = {state["date"]: state["raw_records_downloaded"] for state in daily_states}

    for log_row in daily_log:
        log_row["backfilled_rows"] = backfilled_rows_by_date[log_row["date"]]
        log_row["final_pages_downloaded"] = pages_by_date[log_row["date"]]
        log_row["final_raw_records_downloaded"] = raw_by_date[log_row["date"]]

    month_log = {
        "month": monthly_target["month"],
        "target_rows": month_target_rows,
        "rows_before_backfill": rows_before_backfill,
        "rows_collected": len(selected_df),
        "daily_windows": len(daily_targets),
        "daily_windows_with_shortfall": sum(row["shortfall_before_backfill"] > 0 for row in daily_log),
        "daily_shortfall_before_backfill": sum(row["shortfall_before_backfill"] for row in daily_log),
        "rows_backfilled": sum(row["backfilled_rows"] for row in daily_log),
        "month_shortfall_after_backfill": max(0, month_target_rows - len(selected_df)),
        "pages_downloaded": sum(row["final_pages_downloaded"] for row in daily_log),
        "raw_records_downloaded": sum(row["final_raw_records_downloaded"] for row in daily_log),
        "days_hitting_page_limit": sum(row["max_pages_hit"] for row in daily_log),
    }

    if verbose:
        print(
            f"{monthly_target['month']}: collected {len(selected_df):,} of "
            f"{month_target_rows:,}; daily shortfall before backfill: "
            f"{month_log['daily_shortfall_before_backfill']:,}; "
            f"month shortfall after backfill: {month_log['month_shortfall_after_backfill']:,}."
        )

    return selected_df, month_log, daily_log


def download_daily_stratified_sample(
    year: int = 2024,
    total_rows: int = 50_000,
    page_size: int = 1_000,
    max_pages_per_day: int = 10,
    sleep_seconds: float = 0.05,
    session: requests.Session | None = None,
    verbose: bool = True,
) -> tuple[pd.DataFrame, list[dict[str, Any]], list[dict[str, Any]]]:
    """Download a monthly-balanced and daily-stratified CFPB sample."""
    monthly_frames = []
    monthly_log = []
    daily_log = []
    client = session or requests.Session()

    for monthly_target in build_monthly_targets(year=year, total_rows=total_rows):
        month_df, month_log, month_daily_log = collect_monthly_daily_stratified_sample(
            monthly_target=monthly_target,
            page_size=page_size,
            max_pages_per_day=max_pages_per_day,
            sleep_seconds=sleep_seconds,
            session=client,
            verbose=verbose,
        )
        monthly_frames.append(month_df)
        monthly_log.append(month_log)
        daily_log.extend(month_daily_log)

    final_df = _merge_record_frames(monthly_frames)
    return final_df, monthly_log, daily_log


def validate_dataset(df: pd.DataFrame, year: int = 2024) -> dict[str, Any]:
    """Return validation statistics for a CFPB raw dataset."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required CFPB columns: {missing_columns}")

    received_dates = _parse_dates(df["date_received"])
    start = pd.Timestamp(year=year, month=1, day=1)
    end_exclusive = pd.Timestamp(year=year + 1, month=1, day=1)
    in_year = received_dates.notna() & received_dates.ge(start) & received_dates.lt(end_exclusive)
    rows_per_month = (
        received_dates.dt.to_period("M")
        .astype(str)
        .value_counts()
        .sort_index()
        .to_dict()
    )
    rows_per_day = (
        received_dates.dt.strftime("%Y-%m-%d")
        .value_counts()
        .sort_index()
        .to_dict()
    )
    expected_dates = pd.date_range(start, end_exclusive - pd.Timedelta(days=1), freq="D")
    missing_dates = [date.strftime("%Y-%m-%d") for date in expected_dates if date.strftime("%Y-%m-%d") not in rows_per_day]

    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "date_min": received_dates.min().date().isoformat(),
        "date_max": received_dates.max().date().isoformat(),
        "rows_per_month": rows_per_month,
        "rows_per_day": rows_per_day,
        "unique_dates_covered": len(rows_per_day),
        "expected_dates_in_year": len(expected_dates),
        "missing_dates": missing_dates,
        "product_classes": df["product"].nunique(),
        "missing_empty_narratives": int(
            df["complaint_what_happened"].fillna("").astype(str).str.strip().eq("").sum()
        ),
        "missing_empty_products": int(df["product"].fillna("").astype(str).str.strip().eq("").sum()),
        "duplicate_complaint_ids": int(_complaint_id_keys(df).duplicated().sum()),
        "rows_outside_year": int((~in_year).sum()),
        "all_records_within_year": bool(in_year.all()),
    }


def save_raw_csv(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Save the raw CFPB dataset to a local CSV path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def load_validate_existing_year(
    year: int,
    project_root: str | Path,
    verbose: bool = True,
) -> dict[str, Any]:
    """Load and validate an existing local raw CFPB CSV for one year."""
    output_path = raw_csv_path(project_root=project_root, year=year)
    output_relative_path = raw_csv_relative_path(year)

    if not output_path.exists():
        raise FileNotFoundError(f"Local raw CSV does not exist for {year}: {output_relative_path.as_posix()}")

    if verbose:
        print(f"Using existing local raw CSV for {year}: {output_relative_path.as_posix()}")

    df = pd.read_csv(output_path)
    validation = validate_dataset(df=df, year=year)

    return {
        "year": year,
        "output_path": output_path,
        "output_relative_path": output_relative_path,
        "dataframe": df,
        "monthly_log": [],
        "daily_log": [],
        "validation": validation,
        "source": "existing_csv",
        "loaded_existing": True,
    }


def download_save_validate_year(
    year: int,
    project_root: str | Path,
    total_rows: int = 50_000,
    page_size: int = 1_000,
    max_pages_per_day: int = 10,
    sleep_seconds: float = 0.05,
    session: requests.Session | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """Download, save, and validate one year of raw CFPB complaint data."""
    output_path = raw_csv_path(project_root=project_root, year=year)
    output_relative_path = raw_csv_relative_path(year)
    df, monthly_log, daily_log = download_daily_stratified_sample(
        year=year,
        total_rows=total_rows,
        page_size=page_size,
        max_pages_per_day=max_pages_per_day,
        sleep_seconds=sleep_seconds,
        session=session,
        verbose=verbose,
    )

    if df.empty:
        raise ValueError(f"No valid CFPB records were downloaded for {year}.")

    saved_path = save_raw_csv(df=df, output_path=output_path)
    validation = validate_dataset(df=pd.read_csv(saved_path), year=year)

    return {
        "year": year,
        "output_path": saved_path,
        "output_relative_path": output_relative_path,
        "dataframe": df,
        "monthly_log": monthly_log,
        "daily_log": daily_log,
        "validation": validation,
        "source": "api_download",
        "loaded_existing": False,
    }


def load_or_download_validate_year(
    year: int,
    project_root: str | Path,
    force_download: bool = False,
    total_rows: int = 50_000,
    page_size: int = 1_000,
    max_pages_per_day: int = 10,
    sleep_seconds: float = 0.05,
    session: requests.Session | None = None,
    verbose: bool = True,
) -> dict[str, Any]:
    """Load and validate an existing raw CSV, or download it if needed."""
    output_path = raw_csv_path(project_root=project_root, year=year)
    output_relative_path = raw_csv_relative_path(year)

    if output_path.exists() and not force_download:
        return load_validate_existing_year(year=year, project_root=project_root, verbose=verbose)

    if verbose:
        if force_download:
            print(f"FORCE_DOWNLOAD=True; downloading fresh raw CSV for {year}.")
        else:
            print(f"No local raw CSV found for {year}: {output_relative_path.as_posix()}")
            print(f"Downloading raw CSV for {year} from the CFPB API.")

    return download_save_validate_year(
        year=year,
        project_root=project_root,
        total_rows=total_rows,
        page_size=page_size,
        max_pages_per_day=max_pages_per_day,
        sleep_seconds=sleep_seconds,
        session=session,
        verbose=verbose,
    )
