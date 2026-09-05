import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import call, patch

from workflows.pipeline import Pipeline


class TestPipeline(unittest.TestCase):
    @patch("workflows.pipeline.AuditHistory")
    @patch("workflows.pipeline.SnapshotRechecker")
    @patch("workflows.pipeline.ReadMe")
    @patch("workflows.pipeline.ReportWriter")
    @patch("workflows.pipeline.AuditRunner")
    @patch("workflows.pipeline.Pipeline._urls")
    def test_audits_every_directory_url(
        self, urls_source, runner, writer, read_me, rechecker, history
    ):
        urls = ["https://one.gov.lk", "https://two.gov.lk/services"]
        urls_source.return_value = urls
        levels = [
            SimpleNamespace(level=level, status="inconclusive")
            for level in range(6)
        ]
        audits = [
            SimpleNamespace(
                levels=levels,
                to_dict=lambda: {"levels": []},
            ),
            SimpleNamespace(
                levels=levels,
                to_dict=lambda: {"levels": []},
            ),
        ]
        runner.return_value.run.side_effect = audits
        history.return_value.fresh.return_value = False
        history.return_value.host.side_effect = ["one.gov.lk", "two.gov.lk"]
        history.return_value.folder.side_effect = [
            Path("audit.output/one.gov.lk/20260901.1530"),
            Path("audit.output/two.gov.lk/20260901.1531"),
        ]
        Pipeline().run()
        self.assertEqual(
            [
                call(
                    urls[0],
                    Path("audit.output/one.gov.lk/20260901.1530"),
                ),
                call(
                    urls[1],
                    Path("audit.output/two.gov.lk/20260901.1531"),
                ),
            ],
            runner.return_value.run.call_args_list,
        )
        read_me.return_value.update.assert_called_once_with(
            Path("latest_audit_reports")
        )

    @patch("workflows.pipeline.AuditHistory")
    @patch("workflows.pipeline.SnapshotRechecker")
    @patch("workflows.pipeline.ReadMe")
    @patch("workflows.pipeline.ReportWriter")
    @patch("workflows.pipeline.AuditRunner")
    @patch("workflows.pipeline.Pipeline._urls")
    def test_skips_recent_audits(
        self, urls_source, runner, writer, read_me, rechecker, history
    ):
        url = "https://one.gov.lk"
        stored = {"normalized_url": url}
        audit = SimpleNamespace(
            normalized_url=url,
            levels=[],
            to_dict=lambda: {"levels": []},
        )
        urls_source.return_value = [url]
        history.return_value.fresh.return_value = True
        history.return_value.latest.return_value = stored
        history.return_value.host.return_value = "one.gov.lk"
        rechecker.return_value.run.return_value = audit
        Pipeline().run()
        runner.return_value.run.assert_not_called()
        rechecker.return_value.run.assert_called_once_with(stored)
        writer.return_value.write.assert_called_once_with(
            audit, Path("latest_audit_reports/one.gov.lk")
        )
        read_me.return_value.update.assert_called_once_with(
            Path("latest_audit_reports")
        )


if __name__ == "__main__":
    unittest.main()
