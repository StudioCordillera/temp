"""Shared test plumbing: run a MATHKIT program from build/*.8xp with a key
script and return what the calculator would show."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tibasic  # noqa: E402
from tibasic import D  # noqa: E402

LIB = tibasic.Library(ROOT, prefer="build")

# what a fresh calculator holds before MATHKIT runs: a user equation in Y₀
# and Y₁, a user X, and the user's own window (RU-6 checks these survive)
USER_Y = ("X", "²", "+", "1")


class Run:
    def __init__(self, it, halted, error):
        self.it = it
        self.halted = halted
        self.error = error
        self.screen = it.screen_text()
        self.flat = " ".join(l.strip() for l in self.screen.split("\n") if l.strip())
        # cost from the last Input to the first wait after it
        self.answer_ms = None

    def has(self, s):
        return s in self.screen or s in self.flat


def new_interp(keys, work=1):
    it = tibasic.Interp(LIB, keys=keys)
    it.yvars["Y₀"] = USER_Y
    it.yvars["Y₁"] = USER_Y
    it.vars["X"] = D(7)
    if not work:
        it.lists["ʟMKS"] = [D(0), D(0), D(0)]
    return it


def run(prog, keys, work=1, snippet=None, setup=None):
    it = new_interp(keys, work)
    if setup:
        setup(it)
    marks = {}

    def on_wait(interp, reason):
        if "first_wait" not in marks:
            marks["first_wait"] = dict(interp.cost)
    it.on_wait = on_wait
    halted, error = False, None
    if snippet is not None:
        LIB.cache["ZTEST"] = tibasic.Program("ZTEST", tibasic.tokenize(snippet))
        prog = "ZTEST"
    try:
        it.run(prog)
    except tibasic.Halt:
        halted = True
    except tibasic.TIError as e:
        error = str(e)
    r = Run(it, halted, error)
    return r


def answer_cost(it):
    """Estimated ms from the last ENTER on an input to the next key wait."""
    return None
