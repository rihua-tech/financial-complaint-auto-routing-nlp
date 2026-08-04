"""Offline tests for CFPB ingestion, validation, and local-first behavior."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

import pandas as pd
import requests

from src import download_data


class DownloadDataTests(unittest.TestCase):
    def setUp(self):
        # Fail immediately if production code attempts an unmocked HTTP request.
        self.network_guard = patch(
            "requests.sessions.Session.request",
            side_effect=AssertionError("A real network request was attempted."),
        )
        self.network_guard.start()
        self.addCleanup(self.network_guard.stop)

    @staticmethod
    def response(status_code=200, payload=None, headers=None, json_error=None):
        response = Mock(spec=requests.Response)
        response.status_code = status_code
        response.headers = headers or {}

        if json_error is None:
            response.json.return_value = payload
        else:
            response.json.side_effect = json_error

        if 200 <= status_code < 400:
            response.raise_for_status.return_value = None
        else:
            response.raise_for_status.side_effect = requests.exceptions.HTTPError(
                f"HTTP {status_code}",
                response=response,
            )

        return response

    @staticmethod
    def record(
        complaint_id="1",
        date_received="2024-01-01",
        narrative="Synthetic complaint text.",
        product="Credit card",
    ):
        return {
            "complaint_what_happened": narrative,
            "product": product,
            "date_received": date_received,
            "complaint_id": complaint_id,
            "company": "Synthetic company",
        }

    @classmethod
    def valid_frame(cls):
        return pd.DataFrame(
            [
                cls.record(complaint_id="1", date_received="2024-01-01"),
                cls.record(
                    complaint_id="2",
                    date_received="2024-12-31",
                    product="Mortgage",
                ),
            ]
        )

    def test_successful_api_response_uses_expected_request_and_no_retry(self):
        payload = {
            "hits": {
                "hits": [
                    {"_source": self.record(), "sort": ["2024-01-01", "1"]},
                ]
            }
        }
        session = Mock()
        session.get.return_value = self.response(payload=payload)

        with patch("src.download_data.time.sleep") as sleep:
            result = download_data.fetch_cfpb_page(
                date_start="2024-01-01",
                date_end="2024-01-01",
                search_after="previous_token",
                page_size=25,
                session=session,
                timeout=7,
            )

        self.assertEqual(result, payload)
        self.assertEqual(download_data.extract_records(result), [self.record()])
        session.get.assert_called_once()
        sleep.assert_not_called()
        _, kwargs = session.get.call_args
        self.assertEqual(kwargs["params"]["date_received_min"], "2024-01-01")
        self.assertEqual(kwargs["params"]["date_received_max"], "2024-01-01")
        self.assertEqual(kwargs["params"]["search_after"], "previous_token")
        self.assertEqual(kwargs["params"]["size"], 25)
        self.assertEqual(kwargs["headers"], download_data.REQUEST_HEADERS)
        self.assertEqual(kwargs["timeout"], 7)

    def test_successful_page_is_parsed_and_filtered_into_expected_rows(self):
        records = [
            self.record(complaint_id="1"),
            self.record(complaint_id="2", product="Mortgage"),
        ]
        payload = {
            "hits": {
                "hits": [
                    {"_source": record, "sort": ["2024-01-01", index]}
                    for index, record in enumerate(records)
                ]
            }
        }
        session = Mock()
        session.get.return_value = self.response(payload=payload)

        page = download_data._fetch_next_valid_page(
            date_start="2024-01-01",
            date_end="2024-01-01",
            date_end_exclusive="2024-01-02",
            search_after=None,
            page_size=10,
            session=session,
        )

        self.assertEqual(page["raw_record_count"], 2)
        self.assertEqual(len(page["valid_df"]), 2)
        self.assertTrue(set(download_data.REQUIRED_COLUMNS).issubset(page["valid_df"].columns))
        self.assertEqual(page["next_search_after"], "2024-01-01_1")
        self.assertFalse(page["exhausted"])
        session.get.assert_called_once()

    def test_429_uses_retry_after_then_succeeds(self):
        session = Mock()
        session.get.side_effect = [
            self.response(status_code=429, headers={"Retry-After": "2.5"}),
            self.response(payload={"hits": {"hits": []}}),
        ]

        with patch("src.download_data.time.sleep") as sleep:
            result = download_data.fetch_cfpb_page(
                "2024-01-01",
                "2024-01-01",
                session=session,
                max_retries=2,
            )

        self.assertEqual(result, {"hits": {"hits": []}})
        self.assertEqual(session.get.call_count, 2)
        sleep.assert_called_once_with(2.5)

    def test_503_uses_exponential_backoff_then_succeeds(self):
        session = Mock()
        session.get.side_effect = [
            self.response(status_code=503),
            self.response(payload={"hits": {"hits": []}}),
        ]

        with patch("src.download_data.time.sleep") as sleep:
            result = download_data.fetch_cfpb_page(
                "2024-01-01",
                "2024-01-01",
                session=session,
                max_retries=2,
                backoff_seconds=0.25,
            )

        self.assertEqual(result, {"hits": {"hits": []}})
        self.assertEqual(session.get.call_count, 2)
        sleep.assert_called_once_with(0.25)

    def test_5xx_retry_exhaustion_raises_clear_http_error(self):
        session = Mock()
        session.get.side_effect = [self.response(status_code=500) for _ in range(3)]

        with patch("src.download_data.time.sleep") as sleep:
            with self.assertRaisesRegex(requests.exceptions.HTTPError, "HTTP 500"):
                download_data.fetch_cfpb_page(
                    "2024-01-01",
                    "2024-01-01",
                    session=session,
                    max_retries=2,
                    backoff_seconds=0.5,
                )

        self.assertEqual(session.get.call_count, 3)
        self.assertEqual([call.args[0] for call in sleep.call_args_list], [0.5, 1.0])

    def test_403_fails_immediately_with_actionable_guidance(self):
        session = Mock()
        session.get.return_value = self.response(status_code=403)

        with patch("src.download_data.time.sleep") as sleep:
            with self.assertRaisesRegex(requests.exceptions.HTTPError, "403 Forbidden") as error:
                download_data.fetch_cfpb_page(
                    "2024-01-01",
                    "2024-01-01",
                    session=session,
                )

        self.assertIn("existing local ignored CSV files", str(error.exception))
        session.get.assert_called_once()
        sleep.assert_not_called()

    def test_invalid_json_is_propagated_without_retry(self):
        session = Mock()
        session.get.return_value = self.response(json_error=ValueError("invalid JSON"))

        with patch("src.download_data.time.sleep") as sleep:
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                download_data.fetch_cfpb_page(
                    "2024-01-01",
                    "2024-01-01",
                    session=session,
                )

        session.get.assert_called_once()
        sleep.assert_not_called()

    def test_missing_hits_container_extracts_no_records(self):
        self.assertEqual(download_data.extract_hits({"unexpected": {}}), [])
        self.assertEqual(download_data.extract_records({"unexpected": {}}), [])

    def test_empty_download_fails_before_writing_output(self):
        with TemporaryDirectory() as temp_dir:
            expected_path = download_data.raw_csv_path(temp_dir, 2024)
            with (
                patch(
                    "src.download_data.download_daily_stratified_sample",
                    return_value=(pd.DataFrame(), [], []),
                ),
                patch("src.download_data.save_raw_csv") as save,
            ):
                with self.assertRaisesRegex(ValueError, "No valid CFPB records"):
                    download_data.download_save_validate_year(
                        year=2024,
                        project_root=temp_dir,
                        total_rows=2,
                        verbose=False,
                    )

            save.assert_not_called()
            self.assertFalse(expected_path.exists())

    def test_filter_valid_records_requires_all_columns(self):
        incomplete = [{"product": "Credit card", "complaint_id": "1"}]

        with self.assertRaisesRegex(ValueError, "Missing required CFPB columns"):
            download_data.filter_valid_records(
                incomplete,
                date_start="2024-01-01",
                date_end_exclusive="2025-01-01",
            )

    def test_filter_valid_records_removes_unusable_out_of_window_and_duplicates(self):
        records = [
            self.record(complaint_id="1"),
            self.record(complaint_id="1", narrative="Duplicate ID"),
            self.record(complaint_id="2", narrative="  "),
            self.record(complaint_id="3", product=""),
            self.record(complaint_id="", product="Mortgage"),
            self.record(complaint_id="4", date_received="2023-12-31"),
            self.record(complaint_id="5", date_received="not-a-date"),
        ]

        result = download_data.filter_valid_records_for_year(records, year=2024)

        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["complaint_id"], "1")
        self.assertTrue(set(download_data.REQUIRED_COLUMNS).issubset(result.columns))

    def test_validate_dataset_reports_valid_required_structure(self):
        validation = download_data.validate_dataset(self.valid_frame(), year=2024)

        self.assertEqual(validation["row_count"], 2)
        self.assertEqual(validation["column_count"], 5)
        self.assertEqual(validation["date_min"], "2024-01-01")
        self.assertEqual(validation["date_max"], "2024-12-31")
        self.assertEqual(validation["missing_empty_narratives"], 0)
        self.assertEqual(validation["missing_empty_products"], 0)
        self.assertEqual(validation["duplicate_complaint_ids"], 0)
        self.assertEqual(validation["rows_outside_year"], 0)
        self.assertTrue(validation["all_records_within_year"])

    def test_validate_dataset_detects_blanks_duplicates_and_wrong_year(self):
        frame = pd.DataFrame(
            [
                self.record(complaint_id="1"),
                self.record(complaint_id="1", narrative=" ", product=""),
                self.record(complaint_id="3", date_received="2025-01-01"),
            ]
        )

        validation = download_data.validate_dataset(frame, year=2024)

        self.assertEqual(validation["missing_empty_narratives"], 1)
        self.assertEqual(validation["missing_empty_products"], 1)
        self.assertEqual(validation["duplicate_complaint_ids"], 1)
        self.assertEqual(validation["rows_outside_year"], 1)
        self.assertFalse(validation["all_records_within_year"])

    def test_validate_dataset_rejects_missing_required_column(self):
        frame = self.valid_frame().drop(columns=["product"])

        with self.assertRaisesRegex(ValueError, "product"):
            download_data.validate_dataset(frame, year=2024)

    def test_load_existing_empty_csv_fails_without_network(self):
        with TemporaryDirectory() as temp_dir:
            path = download_data.raw_csv_path(temp_dir, 2024)
            path.parent.mkdir(parents=True)
            path.touch()

            with self.assertRaises(pd.errors.EmptyDataError):
                download_data.load_validate_existing_year(
                    year=2024,
                    project_root=temp_dir,
                    verbose=False,
                )

    def test_local_first_loads_existing_csv_without_download(self):
        with TemporaryDirectory() as temp_dir:
            path = download_data.raw_csv_path(temp_dir, 2024)
            download_data.save_raw_csv(self.valid_frame(), path)

            with patch("src.download_data.download_save_validate_year") as download:
                result = download_data.load_or_download_validate_year(
                    year=2024,
                    project_root=temp_dir,
                    verbose=False,
                )

            download.assert_not_called()
            self.assertEqual(result["source"], "existing_csv")
            self.assertTrue(result["loaded_existing"])
            self.assertEqual(len(result["dataframe"]), 2)
            self.assertEqual(result["output_path"], path)

    def test_missing_local_file_delegates_to_download_path(self):
        sentinel = {"source": "mocked_download", "loaded_existing": False}
        session = Mock()

        with TemporaryDirectory() as temp_dir:
            with patch(
                "src.download_data.download_save_validate_year",
                return_value=sentinel,
            ) as download:
                result = download_data.load_or_download_validate_year(
                    year=2024,
                    project_root=temp_dir,
                    total_rows=2,
                    page_size=5,
                    max_pages_per_day=1,
                    sleep_seconds=0,
                    session=session,
                    verbose=False,
                )

        self.assertIs(result, sentinel)
        download.assert_called_once_with(
            year=2024,
            project_root=temp_dir,
            total_rows=2,
            page_size=5,
            max_pages_per_day=1,
            sleep_seconds=0,
            session=session,
            verbose=False,
        )

    def test_save_raw_csv_creates_only_requested_parent_and_file(self):
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_path = root / "approved" / "nested" / "sample.csv"

            saved = download_data.save_raw_csv(self.valid_frame(), output_path)

            self.assertEqual(saved, output_path)
            self.assertTrue(output_path.is_file())
            self.assertEqual(list(root.rglob("*.csv")), [output_path])
            loaded = pd.read_csv(output_path)
            self.assertEqual(len(loaded), 2)

    def test_download_save_validate_writes_expected_temporary_raw_path(self):
        frame = self.valid_frame()
        monthly_log = [{"month": "2024-01", "rows_collected": 2}]
        daily_log = [{"date": "2024-01-01", "initial_selected_rows": 2}]

        with TemporaryDirectory() as temp_dir:
            expected_path = download_data.raw_csv_path(temp_dir, 2024)
            with patch(
                "src.download_data.download_daily_stratified_sample",
                return_value=(frame, monthly_log, daily_log),
            ) as download:
                result = download_data.download_save_validate_year(
                    year=2024,
                    project_root=temp_dir,
                    total_rows=2,
                    verbose=False,
                )

            download.assert_called_once()
            self.assertEqual(result["source"], "api_download")
            self.assertFalse(result["loaded_existing"])
            self.assertEqual(result["output_path"], expected_path)
            self.assertTrue(expected_path.is_file())
            self.assertEqual(list(Path(temp_dir).rglob("*.csv")), [expected_path])


if __name__ == "__main__":
    unittest.main()
