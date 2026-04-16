

from dash.testing.application_runners import import_app
import pytest


# ── Fixture: start the Dash app once for all three tests ────────────────
@pytest.fixture(scope="module")
def dash_duo_app(dash_duo):
    """Import and start the Dash app."""
    app = import_app("task_3.app")
    dash_duo.start_server(app)
    yield dash_duo


# ── Test 1: Header is present ──────────────────────────────────────────
def test_header_present(dash_duo):
    app = import_app("task_3.app")
    dash_duo.start_server(app)

    # Wait for the H1 element to render
    dash_duo.wait_for_element("#title", timeout=10)
    header = dash_duo.find_element("#title")

    assert header is not None, "Header element (#title) was not found"
    assert header.text != "", "Header text should not be empty"
    assert "Pink Morsel" in header.text, (
        f"Expected 'Pink Morsel' in header, got: '{header.text}'"
    )


# ── Test 2: Visualisation is present ───────────────────────────────────
def test_visualisation_present(dash_duo):
    app = import_app("task_3.app")
    dash_duo.start_server(app)

    # Wait for the Graph component to render
    dash_duo.wait_for_element("#sales-graph", timeout=10)
    graph = dash_duo.find_element("#sales-graph")

    assert graph is not None, "Graph element (#sales-graph) was not found"
    # Plotly renders an SVG with class "main-svg" inside the graph div
    dash_duo.wait_for_element("#sales-graph .main-svg", timeout=10)
    svg = dash_duo.find_element("#sales-graph .main-svg")
    assert svg is not None, "Graph SVG was not rendered"


# ── Test 3: Region picker is present ───────────────────────────────────
def test_region_picker_present(dash_duo):
    app = import_app("task_3.app")
    dash_duo.start_server(app)

    # Wait for the RadioItems component to render
    dash_duo.wait_for_element("#region-filter", timeout=10)
    picker = dash_duo.find_element("#region-filter")

    assert picker is not None, "Region picker (#region-filter) was not found"

    # Verify all five options exist
    labels = picker.find_elements("css selector", "label")
    label_texts = [label.text.strip().lower() for label in labels]

    expected = {"all", "north", "east", "south", "west"}
    assert expected.issubset(set(label_texts)), (
        f"Expected region options {expected}, but found: {label_texts}"
    )
