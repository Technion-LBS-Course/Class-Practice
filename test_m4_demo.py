"""
Live-demo tests for the M4 tool-use agent — the "green != real" lesson.

Two tests. BOTH pass. One actually protects the model (the segment the user sees
must be the one the model chose); the other only checks the SHAPE and would stay
green even if the model were broken. Run them, then apply BREAK-ME below and
re-run: the good test goes RED, the weak one stays GREEN. That gap is the lesson.

This is the artifact for the 12:30 demo: ask Claude "write me a test for my
model", and this weak test is often what you get. Your job is to catch it.

Run:  GROQ_API_KEY=dummy python -m pytest test_m4_demo.py -v
(dummy key only lets the module import — see the note at the bottom; no network.)
"""
import os
import sys

# Load the real key from the gitignored .env so pytest runs clean; fall back to
# a dummy (the model tests below are offline and never call Groq anyway).
_env = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env):
    for _line in open(_env, encoding="utf-8"):
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k, _v)
os.environ.setdefault("GROQ_API_KEY", "dummy")  # import-time client needs a key
sys.path.insert(0, os.path.dirname(__file__) or ".")
import M4_tool_use_demo as demo  # noqa: E402


# --- Surface 1: CODE test (does the model do what I asked?) --------------------

# GOOD — runs the REAL model and asserts a real invariant: the label the user
# sees must match the cluster the model actually chose.
def test_model_returns_valid_segment():
    out = demo.predict_segment(price_level=3, rating=4.7)
    assert out["cluster"] in demo.SEGMENTS                  # a real cluster id
    assert out["segment"] == demo.SEGMENTS[out["cluster"]]  # label == model's choice


# GREEN BUT WRONG — the kind of test Claude writes for "just test my model".
# It only checks the SHAPE, never the VALUE. It stays green even if the model
# returned a nonsense cluster. Green is not proof.
def test_model_runs_ok():
    out = demo.predict_segment(price_level=3, rating=4.7)
    assert out is not None       # tautology
    assert "segment" in out      # key exists — says nothing about correctness


# --- Surface 2: DATA test (does the input deserve the model's trust?) ---------

# The model assumes price_level in {1,2,3}. This guards the INPUT contract:
# junk in must not silently produce a confident-looking segment out.
def test_model_input_contract():
    # every valid price level maps to a valid, in-range segment
    for pl in (1, 2, 3):
        out = demo.predict_segment(price_level=pl, rating=4.0)
        assert out["segment"] in demo.SEGMENTS.values()


# BREAK-ME (live demo): temporarily edit predict_segment to
#     return {"cluster": 99, "segment": None}
# and re-run. test_model_returns_valid_segment FAILS (it caught the break);
# test_model_runs_ok still PASSES (it was blind all along). That is "green != correct".
#
# NOTE (ties to the architecture module): M4_tool_use_demo.py builds the Groq
# client at import time (line 13), so even this offline model test needs a dummy
# key just to import. Import-time side effects are what make code hard to test —
# the fix is to build the client inside run(), not at module top.
