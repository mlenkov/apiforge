"""Tests for CLI module."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from apiforge.cli import doctor, install, main
from apiforge.exceptions import ApiForgeConfigError


class TestDoctor:
    @patch("apiforge.cli.list_configs")
    def test_doctor_no_configs(self, mock_list_configs, capsys):
        mock_list_configs.return_value = {}

        doctor()

        output = capsys.readouterr().out
        assert "No configs found" in output
        assert "apiforge install" in output

    @patch("apiforge.cli.list_configs")
    def test_doctor_unknown_provider(self, mock_list_configs, capsys):
        mock_list_configs.return_value = {"yandex": ["metrika"]}

        with pytest.raises(SystemExit) as exc_info:
            doctor(provider="nonexistent")

        assert exc_info.value.code == 1
        output = capsys.readouterr().out
        assert "Provider 'nonexistent' not found" in output

    @patch("apiforge.cli.get_config_path")
    @patch("apiforge.cli.load_config")
    @patch("apiforge.cli.list_configs")
    def test_doctor_valid_config(
        self, mock_list_configs, mock_load_config, mock_get_config_path, capsys, tmp_path
    ):
        mock_list_configs.return_value = {"yandex": ["metrika"]}

        config_file = tmp_path / "metrika.json"
        config_file.write_text(json.dumps({
            "base_url": "https://api-metrika.yandex.net",
            "resources": {
                "campaigns": {"path": "/campaigns", "method": "GET"},
            },
        }))
        mock_get_config_path.return_value = config_file
        mock_load_config.return_value = json.loads(config_file.read_text())

        with pytest.raises(SystemExit) as exc_info:
            doctor(provider="yandex", api_name="metrika")

        assert exc_info.value.code == 0
        output = capsys.readouterr().out
        assert "Valid JSON" in output
        assert "Base URL" in output
        assert "All checks passed" in output

    @patch("apiforge.cli.get_config_path")
    @patch("apiforge.cli.load_config")
    @patch("apiforge.cli.list_configs")
    def test_doctor_missing_config_file(
        self, mock_list_configs, mock_load_config, mock_get_config_path, capsys
    ):
        mock_list_configs.return_value = {"yandex": ["metrika"]}
        mock_get_config_path.return_value = Path("/nonexistent/path.json")

        with pytest.raises(SystemExit) as exc_info:
            doctor(provider="yandex", api_name="metrika")

        assert exc_info.value.code == 1
        output = capsys.readouterr().out
        assert "Config file not found" in output

    @patch("apiforge.cli.get_config_path")
    @patch("apiforge.cli.load_config")
    @patch("apiforge.cli.list_configs")
    def test_doctor_invalid_json_config(
        self, mock_list_configs, mock_load_config, mock_get_config_path, capsys, tmp_path
    ):
        mock_list_configs.return_value = {"yandex": ["metrika"]}
        config_file = tmp_path / "metrika.json"
        config_file.write_text("not valid json")
        mock_get_config_path.return_value = config_file
        mock_load_config.side_effect = ApiForgeConfigError("Invalid JSON")

        with pytest.raises(SystemExit) as exc_info:
            doctor(provider="yandex", api_name="metrika")

        assert exc_info.value.code == 1
        output = capsys.readouterr().out
        assert "Invalid JSON" in output

    @patch("apiforge.cli.get_config_path")
    @patch("apiforge.cli.load_config")
    @patch("apiforge.cli.list_configs")
    def test_doctor_resource_missing_path(
        self, mock_list_configs, mock_load_config, mock_get_config_path, capsys, tmp_path
    ):
        mock_list_configs.return_value = {"yandex": ["metrika"]}
        config_file = tmp_path / "metrika.json"
        config_file.write_text("{}")
        mock_get_config_path.return_value = config_file
        mock_load_config.return_value = {
            "base_url": "https://example.com",
            "resources": {
                "bad_resource": {"method": "GET"},
            },
        }

        with pytest.raises(SystemExit) as exc_info:
            doctor(provider="yandex", api_name="metrika")

        assert exc_info.value.code == 1
        output = capsys.readouterr().out
        assert "missing 'path'" in output


class TestInstall:
    @patch("apiforge.cli.Path.home")
    def test_install_creates_config_dir(self, mock_home, capsys, tmp_path):
        mock_home.return_value = tmp_path

        with patch("apiforge.cli.Path") as MockPath:
            config_dir = tmp_path / ".apiforge" / "configs"
            MockPath.home.return_value = tmp_path
            MockPath.return_value.__truediv__ = lambda self, x: tmp_path / ".apiforge" / x
            MockPath.return_value.__pow__ = lambda self, x: tmp_path / ".apiforge" / "configs"
            install()

        output = capsys.readouterr().out
        assert "Configs directory" in output
        assert "<provider>" in output

    @patch("apiforge.cli.Path.home")
    def test_install_prints_instructions(self, mock_home, capsys, tmp_path):
        mock_home.return_value = tmp_path

        with patch("apiforge.cli.Path") as MockPath:
            MockPath.home.return_value = tmp_path
            MockPath.return_value.__truediv__ = lambda self, x: tmp_path / ".apiforge" / x
            MockPath.return_value.__pow__ = lambda self, x: tmp_path / ".apiforge" / "configs"
            install()

        output = capsys.readouterr().out
        assert "To add configs" in output
        assert ".json" in output


class TestMain:
    @patch("apiforge.cli.doctor")
    def test_main_doctor_command(self, mock_doctor):
        with patch("sys.argv", ["apiforge", "doctor"]):
            main()

        mock_doctor.assert_called_once_with(provider=None, api_name=None)

    @patch("apiforge.cli.doctor")
    def test_main_doctor_with_provider(self, mock_doctor):
        with patch("sys.argv", ["apiforge", "doctor", "--provider", "yandex"]):
            main()

        mock_doctor.assert_called_once_with(provider="yandex", api_name=None)

    @patch("apiforge.cli.doctor")
    def test_main_doctor_with_api(self, mock_doctor):
        with patch("sys.argv", ["apiforge", "doctor", "--api", "metrika"]):
            main()

        mock_doctor.assert_called_once_with(provider=None, api_name="metrika")

    @patch("apiforge.cli.install")
    def test_main_install_command(self, mock_install):
        with patch("sys.argv", ["apiforge", "install"]):
            main()

        mock_install.assert_called_once()

    def test_main_no_command(self, capsys):
        with patch("sys.argv", ["apiforge"]):
            main()

        output = capsys.readouterr().out
        assert "usage:" in output.lower() or "apiforge" in output
