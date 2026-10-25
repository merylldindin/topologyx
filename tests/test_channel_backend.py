import json
import os
from importlib.machinery import ModuleSpec
from pathlib import Path

import pytest

from topologyx.channels import backend


def install_backends(monkeypatch: pytest.MonkeyPatch, *installed: str) -> None:
    def fake_find_spec(name: str) -> ModuleSpec | None:
        return ModuleSpec(name, None) if name in installed else None

    monkeypatch.setattr(backend, "find_spec", fake_find_spec)


@pytest.fixture
def keras_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.setenv("KERAS_HOME", str(tmp_path))
    monkeypatch.delenv("KERAS_BACKEND", raising=False)
    return tmp_path


def write_keras_config(keras_home: Path, content: str) -> None:
    (keras_home / "keras.json").write_text(content)


def test_explicit_environment_backend_is_kept(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path
) -> None:
    monkeypatch.setenv("KERAS_BACKEND", "torch")
    install_backends(monkeypatch, "jax")

    backend.select_keras_backend()

    assert os.environ["KERAS_BACKEND"] == "torch"


def test_missing_config_without_tensorflow_falls_back_to_jax(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path
) -> None:
    install_backends(monkeypatch, "jax")

    backend.select_keras_backend()

    assert os.environ["KERAS_BACKEND"] == "jax"


def test_configured_backend_that_is_installed_is_kept(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path
) -> None:
    write_keras_config(keras_home, json.dumps({"backend": "tensorflow"}))
    install_backends(monkeypatch, "jax", "tensorflow")

    backend.select_keras_backend()

    assert "KERAS_BACKEND" not in os.environ


def test_configured_backend_that_is_missing_falls_back_to_jax(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path
) -> None:
    write_keras_config(keras_home, json.dumps({"backend": "torch"}))
    install_backends(monkeypatch, "jax")

    backend.select_keras_backend()

    assert os.environ["KERAS_BACKEND"] == "jax"


@pytest.mark.parametrize("content", ["not json", "[]", json.dumps({"backend": 3})])
def test_unreadable_config_is_treated_as_tensorflow(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path, content: str
) -> None:
    write_keras_config(keras_home, content)
    install_backends(monkeypatch, "jax")

    backend.select_keras_backend()

    assert os.environ["KERAS_BACKEND"] == "jax"


def test_unknown_configured_backend_is_left_to_keras(
    monkeypatch: pytest.MonkeyPatch, keras_home: Path
) -> None:
    write_keras_config(keras_home, json.dumps({"backend": "custom"}))
    install_backends(monkeypatch, "jax")

    backend.select_keras_backend()

    assert "KERAS_BACKEND" not in os.environ


def test_keras_home_with_tilde_is_expanded(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("KERAS_HOME", "~/keras-config")

    assert backend.locate_keras_config() == tmp_path / "keras-config" / "keras.json"


def test_writable_home_holds_the_keras_config(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("KERAS_HOME", raising=False)

    assert backend.locate_keras_config() == tmp_path / ".keras" / "keras.json"


def test_unwritable_home_falls_back_to_tmp(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.delenv("KERAS_HOME", raising=False)
    monkeypatch.setattr(backend.os, "access", lambda path, mode: False)

    assert backend.locate_keras_config() == Path("/tmp/.keras/keras.json")
