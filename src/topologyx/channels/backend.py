import json
import os
from importlib.util import find_spec
from pathlib import Path

FALLBACK_KERAS_BACKEND = "jax"
KERAS_DEFAULT_BACKEND = "tensorflow"
KERAS_BACKEND_MODULES = {"jax", "numpy", "openvino", "tensorflow", "torch"}


def locate_keras_config() -> Path:
    if "KERAS_HOME" in os.environ:
        keras_home = os.environ["KERAS_HOME"]
    else:
        home_directory = os.path.expanduser("~")
        writable_base = home_directory if os.access(home_directory, os.W_OK) else "/tmp"
        keras_home = os.path.join(writable_base, ".keras")
    return Path(os.path.expanduser(keras_home)) / "keras.json"


def read_configured_backend() -> str:
    try:
        config = json.loads(locate_keras_config().read_text())
    except (OSError, ValueError):
        return KERAS_DEFAULT_BACKEND
    if not isinstance(config, dict):
        return KERAS_DEFAULT_BACKEND
    backend = config.get("backend", KERAS_DEFAULT_BACKEND)
    return backend if isinstance(backend, str) else KERAS_DEFAULT_BACKEND


def select_keras_backend() -> None:
    if "KERAS_BACKEND" in os.environ:
        return
    backend = read_configured_backend()
    if backend in KERAS_BACKEND_MODULES and find_spec(backend) is None:
        os.environ["KERAS_BACKEND"] = FALLBACK_KERAS_BACKEND
