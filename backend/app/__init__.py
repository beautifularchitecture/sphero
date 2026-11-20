"""U1 chat-command core: chat input → agent translation → BLE robot command.

The public entry point is :mod:`backend.app.main`, which exposes the FastAPI
application. LangChain Deep Agents / OpenRouter and bleak are imported lazily by
their adapters so importing this package never needs network packages, an API
key, or a physical robot.
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
