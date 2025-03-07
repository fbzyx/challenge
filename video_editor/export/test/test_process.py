import unittest
from unittest.mock import patch, MagicMock
from export.export import video_exporter_func
from models.dc_video import DCVideoExportParams
from export.process import export_process


class TestExportProcess(unittest.TestCase):
    """
    Test export_process function
    """

    @patch("multiprocessing.Process")
    def test_export_process_with_valid_output_path(self, mock_process):
        """
        Test that export_process starts a process when output_path is defined.
        """
        # create a mock export parameters object
        export_params = MagicMock(spec=DCVideoExportParams)
        export_params.output_path = "output/video.mp4"

        # mock the process instance
        mock_process_instance = MagicMock()
        mock_process.return_value = mock_process_instance

        # call the function
        result = export_process(export_params)

        # assertions
        mock_process.assert_called_once_with(
            target=video_exporter_func, args=(export_params,)
        )
        # ensure process starts
        mock_process_instance.start.assert_called_once()
        # ensure process is returned
        self.assertEqual(result, mock_process_instance)

    def test_export_process_with_no_output_path(self):
        """
        Test that export_process returns None when output_path is None.
        """
        export_params = MagicMock(spec=DCVideoExportParams)
        # No output path
        export_params.output_path = None
        result = export_process(export_params)

        # function should return None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
