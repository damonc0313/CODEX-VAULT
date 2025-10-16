"""Tests for the PDF converter tool."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace


class DummyDiGraph:
    """Minimal stub of networkx.DiGraph for import-time usage."""

    def __init__(self, *args, **kwargs):  # noqa: D401 - simple stub
        self.args = args
        self.kwargs = kwargs


if "networkx" not in sys.modules:
    sys.modules["networkx"] = SimpleNamespace(DiGraph=DummyDiGraph)

import pytest


class StubPage:
    """Stub page object mimicking pypdf page interface."""

    def __init__(self, text):
        self._text = text

    def extract_text(self):
        return self._text


class StubPdfReader:
    """Stub PdfReader returning pages with configurable text."""

    def __init__(self, _path):
        self.pages = [StubPage("Page with text"), StubPage(None)]


@pytest.fixture
def stub_pypdf(monkeypatch):
    """Inject a stubbed pypdf module for the duration of the test."""

    stub_module = SimpleNamespace(PdfReader=StubPdfReader)
    monkeypatch.setitem(sys.modules, "pypdf", stub_module)
    yield stub_module
    monkeypatch.delitem(sys.modules, "pypdf", raising=False)


@pytest.fixture
def pdf_converter_module():
    """Load the PDF converter module without importing the package."""

    module_path = (
        Path(__file__).resolve().parents[1] / "tools" / "pdf_converter.py"
    )
    spec = importlib.util.spec_from_file_location(
        "test_pdf_converter_module", module_path
    )
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_convert_pdf_to_text_skips_none_pages(stub_pypdf, tmp_path, pdf_converter_module):
    """Ensure pages returning None do not cause conversion errors."""

    convert_pdf_to_text = pdf_converter_module.convert_pdf_to_text

    dummy_pdf = tmp_path / "dummy.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4")

    result = convert_pdf_to_text(Path(dummy_pdf))

    assert "Page with text" in result
    assert "Page 2" not in result
