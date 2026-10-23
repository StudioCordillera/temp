"""
A TI-BASIC interpreter for the subset MATHKIT uses, written to test the
real program source on a PC.

It loads programs from built .8xp files (or source text), splits them into
the calculator's tokens with the tivars token sheet, and runs them with:

  * 14-significant-digit decimal floats (TI keeps 14 digits internally)
  * TI operator precedence, implied multiplication, optional closing ) and "
  * Ans updated only by expression statements and stores
  * 1-based lists, custom lists (ʟNAME), strings Str0-Str9
  * real and a+bi modes (√ of a negative is ERR:NONREAL ANS in Real mode)
  * TI errors: DIVIDE BY 0, DOMAIN, NONREAL ANS, INVALID DIM, DATA TYPE,
    UNDEFINED, SYNTAX, OVERFLOW, DIM MISMATCH, ARGUMENT, LABEL
  * a 26 x 10 home screen with Disp / Output( / ClrHome / Input / Menu(
  * getKey, Pause and Input driven by a scripted key sequence
  * graph-screen commands logged but not drawn
  * a block stack, so a Goto or Menu( out of an open block is reported
    as a leak (the calculator leaks memory there)

When the script runs out while the program waits for a key, the run stops
and the screen is captured. That is how a test reads the answer screen.

Not modelled (and not used by MATHKIT): matrices, ►Frac, Asm(, IS>(,
DS<(, graph drawing itself, statistics, the y= editor, archive access,
memory limits other than a crude string/list size check.
"""

from __future__ import annotations

import decimal
import math
import os
import re
from decimal import Decimal as D

CTX = decimal.Context(prec=14, rounding=decimal.ROUND_HALF_EVEN, Emax=999, Emin=-999)
HI = decimal.Context(prec=30)
ROWS, COLS = 10, 26


class TIError(Exception):
    def __init__(self, kind, where=""):
        super().__init__(f"ERR:{kind} {where}")
        self.kind = kind


class Halt(Exception):
    """The key script ran out while the program waited for input."""


class StopProgram(Exception):
    pass


class ReturnProgram(Exception):
    pass


# ---------------------------------------------------------------- numbers
def R(x):
    """Round to 14 significant digits; check overflow."""
    if isinstance(x, int):
        x = D(x)
    x = CTX.plus(x)
    if x.is_nan():
        raise TIError("DOMAIN")
    if x != 0 and abs(x) >= D("1E100"):
        raise TIError("OVERFLOW")
    if x != 0 and abs(x) < D("1E-99"):
        return D(0)
    return x


class C:
    """Complex value (only produced in a+bi mode)."""
    __slots__ = ("re", "im")

    def __init__(self, re, im):
        self.re, self.im = R(re), R(im)


def simplify(v):
    if isinstance(v, C) and v.im == 0:
        return v.re
    return v


def is_num(v):
    return isinstance(v, (D, C))


def re_im(v):
    if isinstance(v, C):
        return v.re, v.im
    return v, D(0)


def num_add(a, b):
    if isinstance(a, D) and isinstance(b, D):
        return R(HI.add(a, b))
    ar, ai = re_im(a); br, bi = re_im(b)
    return simplify(C(HI.add(ar, br), HI.add(ai, bi)))


def num_sub(a, b):
    if isinstance(a, D) and isinstance(b, D):
        return R(HI.subtract(a, b))
    ar, ai = re_im(a); br, bi = re_im(b)
    return simplify(C(HI.subtract(ar, br), HI.subtract(ai, bi)))


def num_mul(a, b):
    if isinstance(a, D) and isinstance(b, D):
        return R(HI.multiply(a, b))
    ar, ai = re_im(a); br, bi = re_im(b)
    return simplify(C(ar * br - ai * bi, ar * bi + ai * br))


def num_div(a, b):
    if isinstance(a, D) and isinstance(b, D):
        if b == 0:
            raise TIError("DIVIDE BY 0")
        return R(HI.divide(a, b))
    ar, ai = re_im(a); br, bi = re_im(b)
    den = HI.add(HI.multiply(br, br), HI.multiply(bi, bi))
    if den == 0:
        raise TIError("DIVIDE BY 0")
    return simplify(C(HI.divide(ar * br + ai * bi, den), HI.divide(ai * br - ar * bi, den)))


def num_neg(a):
    if isinstance(a, D):
        return R(-a)
    return simplify(C(-a.re, -a.im))


def to_real(v, err="DATA TYPE"):
    if isinstance(v, D):
        return v
    raise TIError(err)


def is_int(x):
    return x == x.to_integral_value()


def csqrt(v, interp):
    if isinstance(v, D):
        if v >= 0:
            return R(HI.sqrt(v)) if v > 0 else D(0)
        if not interp.complex_mode:
            raise TIError("NONREAL ANS")
        return simplify(C(D(0), HI.sqrt(-v)))
    z = complex(float(v.re), float(v.im)) ** 0.5
    return simplify(C(D(repr(z.real)), D(repr(z.imag))))


def num_pow(a, b, interp):
    if isinstance(b, D) and is_int(b) and abs(b) <= 1000:
        n = int(b)
        if n == 0:
            if (isinstance(a, D) and a == 0):
                raise TIError("DOMAIN")
            return D(1)
        if isinstance(a, D) and a == 0 and n < 0:
            raise TIError("DIVIDE BY 0")
        r = D(1)
        base = a
        for _ in range(abs(n)):
            r = num_mul(r, base) if not isinstance(r, D) or not isinstance(base, D) else R(HI.multiply(r, base))
        if n < 0:
            r = num_div(D(1), r)
        return r
    if isinstance(a, D) and isinstance(b, D):
        if a < 0:
            if not interp.complex_mode:
                raise TIError("NONREAL ANS")
            z = complex(float(a), 0) ** float(b)
            return simplify(C(D(repr(z.real)), D(repr(z.imag))))
        if a == 0:
            if b > 0:
                return D(0)
            raise TIError("DOMAIN")
        return R(HI.power(a, b))
    z = complex(*map(float, re_im(a))) ** complex(*map(float, re_im(b)))
    return simplify(C(D(repr(z.real)), D(repr(z.imag))))


def fmt_num(v, mode="Float"):
    """The home screen / toString( form of a number (Float, Real or a+bi)."""
    if isinstance(v, C):
        re_s = "" if v.re == 0 else fmt_num(v.re)
        if v.im == 0:
            return re_s or "0"
        mag = abs(v.im)
        ims = ("" if mag == 1 else fmt_num(mag)) + "𝑖"
        if not re_s:
            return ("⁻" if v.im < 0 else "") + ims
        return re_s + ("-" if v.im < 0 else "+") + ims
    x = v
    if x == 0:
        return "0"
    neg = x < 0
    a = abs(x)
    a10 = decimal.Context(prec=10).plus(a)
    if a10 >= D("1E10") or a10 < D("1E-3"):
        s = f"{a10:E}"
        mant, exp = s.split("E")
        if "." in mant:
            mant = mant.rstrip("0").rstrip(".")
        s = mant + "ᴇ" + str(int(exp)).replace("-", "⁻")
    else:
        s = format(a10, "f")
        if "." in s:
            s = s.rstrip("0").rstrip(".")
        if s.startswith("0."):
            s = s[1:]
    return ("⁻" if neg else "") + s


# ----------------------------------------------------------------- tokens
_TOKEN_CACHE = {}


# Programs tokenized with maximal munch: their string literals must hold
# the calculator's function tokens (√(, ln(, ⁻¹ ...) to match what a user
# types. Every other program uses tivars' default "smart" mode.
MAX_MUNCH = {"ZEXPR", "ZLA", "ZLTOK"}


def tokenize(text, mode="smart"):
    """Split program text into calculator tokens with the tivars token sheet."""
    from tivars.tokenizer import encode, decode
    if (text, mode) in _TOKEN_CACHE:
        return _TOKEN_CACHE[(text, mode)]
    data, _ = encode(text.replace("⌊", "ʟ"), mode=mode)
    toks, _ = decode(data)
    out = [t.langs["en"].display for t in toks]
    _TOKEN_CACHE[(text, mode)] = out
    return out


def tokens_from_8xp(path):
    from tivars.types import TIProgram
    from tivars.tokenizer import decode
    p = TIProgram()
    with open(path, "rb") as fh:
        p.load_from_file(fh)
    toks, _ = decode(p.data)
    return [t.langs["en"].display for t in toks]


LETTERS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZθ")
DIGITS = set("0123456789")
STRVARS = {f"Str{i}" for i in range(10)}
LISTS = {"L₁", "L₂", "L₃", "L₄", "L₅", "L₆"}
YVARS = {f"Y{c}" for c in "₀₁₂₃₄₅₆₇₈₉"}
WINDOW = {"Xmin", "Xmax", "Ymin", "Ymax", "Xscl", "Yscl", "Xres", "ΔX", "ΔY", "TblStart", "ΔTbl"}
CMP = {"=", "≠", "<", ">", "≤", "≥"}
FUNCS = {"abs(", "round(", "iPart(", "fPart(", "int(", "gcd(", "lcm(", "max(", "min(", "√(",
         "sub(", "length(", "inString(", "toString(", "expr(", "dim(", "sum(", "prod(", "seq(",
         "cumSum(", "augment(", "not(", "remainder(", "real(", "imag(", "conj(", "angle(",
         "sin(", "cos(", "tan(", "ln(", "log(", "𝑒^(", "₁₀^(", "³√(", "mean(", "eval(", "ΔList("}
POSTFIX = {"²", "³", "⁻¹", "!"}
# key script characters -> tokens typed on an Input line
KEYTOK = {"~": "⁻", "√": "√(", "i": "𝑖", "π": "π", "`": "⁻¹", "≤": "≤", "≥": "≥", "≠": "≠"}
GETKEY = {"\n": 105, "#": 45, "<": 25, ">": 34, "[": 24, "]": 26,
          "0": 102, "1": 92, "2": 93, "3": 94, "4": 82, "5": 83, "6": 84, "7": 72, "8": 73, "9": 74,
          "+": 95, "-": 85, "*": 65, "/": 55, "(": 62, ")": 63, ",": 52, "~": 104, ".": 103,
          "X": 32, "^": 14, "²": 61}


def disp_width(tok_list):
    return sum(len(t) for t in tok_list)


# --------------------------------------------------------------- the parser
class Node:
    __slots__ = ("kind", "a", "b", "c")

    def __init__(self, kind, a=None, b=None, c=None):
        self.kind, self.a, self.b, self.c = kind, a, b, c


class Parser:
    """Recursive-descent parser over a token list (one statement)."""

    def __init__(self, toks, pos=0):
        self.t = toks
        self.i = pos

    def peek(self, k=0):
        j = self.i + k
        return self.t[j] if j < len(self.t) else None

    def take(self):
        tok = self.t[self.i]
        self.i += 1
        return tok

    def at_end(self):
        return self.i >= len(self.t) or self.peek() in ("→",)

    def close(self):
        """Accept ')' or an implied close at the end of the statement / before →."""
        p = self.peek()
        if p == ")":
            self.i += 1
        elif p is None or p == "→":
            pass
        else:
            raise TIError("SYNTAX", f"expected ) got {p!r}")

    # precedence levels
    def expr(self):
        return self.or_()

    def or_(self):
        n = self.and_()
        while self.peek() in (" or ", " xor "):
            op = self.take()
            n = Node("bin", op.strip(), n, self.and_())
        return n

    def and_(self):
        n = self.rel()
        while self.peek() == " and ":
            self.take()
            n = Node("bin", "and", n, self.rel())
        return n

    def rel(self):
        n = self.add()
        while self.peek() in CMP:
            op = self.take()
            n = Node("bin", op, n, self.add())
        return n

    def add(self):
        n = self.mul()
        while self.peek() in ("+", "-"):
            op = self.take()
            n = Node("bin", op, n, self.mul())
        return n

    def starts_value(self, p):
        if p is None:
            return False
        return (p in DIGITS or p in (".", "ᴇ", "(", "{", "\"", "π", "𝑒", "𝑖", "Ans", "getKey", "ʟ", "⁻")
                or p in LETTERS or p in STRVARS or p in LISTS or p in YVARS or p in FUNCS or p in WINDOW)

    def mul(self):
        n = self.neg()
        while True:
            p = self.peek()
            if p in ("*", "/"):
                self.take()
                n = Node("bin", p, n, self.neg())
            elif self.starts_value(p):
                n = Node("bin", "*", n, self.neg())
            else:
                return n

    def neg(self):
        if self.peek() == "⁻":
            self.take()
            return Node("neg", self.neg())
        return self.pow()

    def pow(self):
        n = self.postfix()
        while self.peek() == "^":
            self.take()
            if self.peek() == "⁻":
                self.take()
                e = Node("neg", self.postfix_neg())
            else:
                e = self.postfix()
            n = Node("pow", n, e)
        return n

    def postfix_neg(self):
        if self.peek() == "⁻":
            self.take()
            return Node("neg", self.postfix_neg())
        return self.postfix()

    def postfix(self):
        n = self.primary()
        while self.peek() in POSTFIX:
            n = Node("post", self.take(), n)
        return n

    def number(self):
        s = ""
        while self.peek() is not None and (self.peek() in DIGITS or self.peek() == "."):
            s += self.take()
        if s.count(".") > 1 or s == ".":
            raise TIError("SYNTAX", "number")
        m = D(s) if s else D(1)
        if self.peek() == "ᴇ":
            self.take()
            sg = 1
            if self.peek() == "⁻":
                self.take()
                sg = -1
            ds = ""
            while self.peek() is not None and self.peek() in DIGITS:
                ds += self.take()
            if not ds:
                raise TIError("SYNTAX", "exponent")
            m = m.scaleb(sg * int(ds))
        return Node("num", R(m))

    def listname(self):
        """After ʟ: up to 5 letters/digits (first is a letter)."""
        name = ""
        while len(name) < 5 and self.peek() is not None and (self.peek() in LETTERS or self.peek() in DIGITS):
            if not name and self.peek() in DIGITS:
                break
            name += self.take()
        if not name:
            raise TIError("SYNTAX", "list name")
        return "ʟ" + name

    def args(self):
        out = []
        if self.peek() == ")":
            self.take()
            return out
        while True:
            out.append(self.expr())
            if self.peek() == ",":
                self.take()
                continue
            self.close()
            return out

    def primary(self):
        p = self.peek()
        if p is None:
            raise TIError("SYNTAX", "unexpected end")
        if p in DIGITS or p in (".", "ᴇ"):
            return self.number()
        if p in LETTERS:
            self.take()
            return Node("var", p)
        if p in ("π", "𝑒", "𝑖", "Ans", "getKey"):
            self.take()
            return Node("const", p)
        if p in STRVARS or p in WINDOW:
            self.take()
            return Node("var", p)
        if p in LISTS or p == "ʟ":
            self.take()
            name = self.listname() if p == "ʟ" else p
            if self.peek() == "(":
                self.take()
                idx = self.expr()
                self.close()
                return Node("lidx", name, idx)
            return Node("list", name)
        if p in YVARS:
            self.take()
            if self.peek() == "(":
                self.take()
                a = self.expr()
                self.close()
                return Node("ycall", p, a)
            return Node("yvar", p)
        if p == "(":
            self.take()
            n = self.expr()
            self.close()
            return n
        if p == "{":
            self.take()
            items = []
            if self.peek() == "}":
                raise TIError("SYNTAX", "empty list")
            while True:
                items.append(self.expr())
                if self.peek() == ",":
                    self.take()
                    continue
                if self.peek() == "}":
                    self.take()
                elif self.peek() not in (None, "→"):
                    raise TIError("SYNTAX", "list literal")
                break
            return Node("listlit", items)
        if p == "\"":
            self.take()
            s = []
            while self.peek() is not None and self.peek() not in ("\"", "→"):
                if self.peek() in (":", "\n"):
                    raise TIError("SYNTAX", "colon in string")
                s.append(self.take())
            if self.peek() == "\"":
                self.take()
            return Node("str", tuple(s))
        if p in FUNCS:
            self.take()
            if p == "seq(":
                # seq(expr,var,start,end[,step])
                e = self.expr(); self.expect(",")
                v = self.take()
                if v not in LETTERS:
                    raise TIError("SYNTAX", "seq var")
                self.expect(",")
                rest = self.args()
                return Node("seq", e, v, rest)
            return Node("call", p, self.args())
        raise TIError("SYNTAX", f"unexpected {p!r}")

    def expect(self, tok):
        if self.peek() != tok:
            raise TIError("SYNTAX", f"expected {tok!r}")
        self.take()


# ----------------------------------------------------------------- program
class Program:
    def __init__(self, name, toks):
        self.name = name
        self.toks = toks
        # split statements at ':' and newline, but not inside strings
        stmts, cur, in_str = [], [], False
        for t in toks:
            if t == "\"":
                in_str = not in_str
                cur.append(t)
                continue
            if in_str and t == "→":
                in_str = False
            if not in_str and t in (":", "\n"):
                stmts.append(cur)
                cur = []
                continue
            if in_str and t == "\n":
                in_str = False
                stmts.append(cur)
                cur = []
                continue
            cur.append(t)
        stmts.append(cur)
        self.stmts = stmts
        self.labels = {}
        for i, s in enumerate(stmts):
            if s and s[0] == "Lbl ":
                name = "".join(s[1:])
                if not (1 <= len(s) - 1 <= 2):
                    raise TIError("SYNTAX", f"label {name!r} in {self.name}")
                self.labels.setdefault(name, i)
        self.ast = {}

    def opener(self, i):
        s = self.stmts[i]
        return bool(s) and (s[0] in ("Then", "For(", "While ", "Repeat "))

    def find_end(self, i, stop_at_else=False, interp=None):
        """Scan forward from statement i (an opener) to its End (or Else)."""
        depth = 0
        j = i + 1
        if interp is not None:
            interp.cost["skip"] += 1
        while j < len(self.stmts):
            s = self.stmts[j]
            if s:
                h = s[0]
                if h in ("Then", "For(", "While ", "Repeat "):
                    depth += 1
                elif h == "End":
                    if depth == 0:
                        return j
                    depth -= 1
                elif h == "Else" and depth == 0 and stop_at_else:
                    return j
            j += 1
        raise TIError("SYNTAX", f"no End in {self.name}")


class Frame:
    def __init__(self, prog):
        self.prog = prog
        self.pc = 0
        self.blocks = []  # (kind, stmt index, data)


# -------------------------------------------------------------- interpreter
class Interp:
    def __init__(self, loader, keys="", max_steps=3_000_000):
        self.loader = loader          # name -> Program
        self.script = list(keys)
        self.vars = {v: D(0) for v in LETTERS}
        self.strs = {}
        self.lists = {}
        self.yvars = {}
        self.window = {"Xmin": D(-10), "Xmax": D(10), "Ymin": D(-10), "Ymax": D(10), "Xscl": D(1), "Yscl": D(1)}
        self.ans = D(0)
        self.complex_mode = False
        self.mode = "Float"
        self.screen = [[" "] * COLS for _ in range(ROWS)]
        self.row = 0
        self.graph_log = []
        self.events = []
        self.leaks = []
        self.warnings = []
        self.steps = 0
        self.max_steps = max_steps
        # cost counters for the speed estimate
        self.cost = {"stmt": 0, "tok": 0, "call": 0, "listel": 0, "strch": 0, "draw": 0, "skip": 0}
        self.cost_marks = []
        self.inputs_done = 0
        self.last_input_cost = None
        self.answer_costs = []
        self.waiting_reason = None
        self.on_wait = None

    # ---------------------------------------------------------- screen
    def scroll(self):
        self.screen.pop(0)
        self.screen.append([" "] * COLS)
        self.row -= 1

    def newline_check(self):
        while self.row >= ROWS:
            self.scroll()

    def put_chars(self, r, c, chars, wrap=True):
        for ch in chars:
            if c >= COLS:
                if not wrap:
                    return
                r += 1
                c = 0
            if r >= ROWS:
                return
            self.screen[r][c] = ch
            c += 1

    def chars(self, toks):
        out = []
        for t in toks:
            out.extend(list(t))
        return out

    def disp_line(self, chars, right=False):
        self.newline_check()
        if len(chars) > COLS:
            self.warnings.append("DISP TOO WIDE: " + "".join(chars))
            chars = chars[:COLS - 1] + ["…"]
        start = COLS - len(chars) if right else 0
        self.screen[self.row] = [" "] * COLS
        self.put_chars(self.row, start, chars, wrap=False)
        self.row += 1

    def screen_text(self):
        return "\n".join("".join(r).rstrip() for r in self.screen)

    # ---------------------------------------------------------- keys
    def next_key(self, reason):
        if not self.script:
            self.waiting_reason = reason
            if self.on_wait:
                self.on_wait(self, reason)
            raise Halt(reason)
        return self.script.pop(0)

    # ---------------------------------------------------------- values
    def get_list(self, name):
        if name not in self.lists:
            raise TIError("UNDEFINED", name)
        return self.lists[name]

    def eval(self, node):
        k = node.kind
        if k == "num":
            return node.a
        if k == "var":
            n = node.a
            if n in LETTERS:
                return self.vars[n]
            if n in STRVARS:
                if n not in self.strs:
                    raise TIError("UNDEFINED", n)
                return self.strs[n]
            if n in WINDOW:
                return self.window.get(n, D(0))
        if k == "const":
            n = node.a
            if n == "Ans":
                return self.ans
            if n == "π":
                return R(D("3.14159265358979323846"))
            if n == "𝑒":
                return R(D("2.71828182845904523536"))
            if n == "𝑖":
                return C(D(0), D(1))
            if n == "getKey":
                return D(self.getkey())
        if k == "str":
            return node.a
        if k == "list":
            return list(self.get_list(node.a))
        if k == "lidx":
            lst = self.get_list(node.a)
            i = to_real(self.eval(node.b))
            if not is_int(i) or i < 1 or i > len(lst):
                raise TIError("INVALID DIM", f"{node.a}({i})")
            self.cost["listel"] += 1
            return lst[int(i) - 1]
        if k == "listlit":
            vals = [self.eval(x) for x in node.a]
            for v in vals:
                if not is_num(v):
                    raise TIError("DATA TYPE", "list item")
            self.cost["listel"] += len(vals)
            return vals
        if k == "neg":
            return self.unop(num_neg, self.eval(node.a))
        if k == "post":
            v = self.eval(node.b)
            op = node.a
            if op == "²":
                return self.unop(lambda x: num_mul(x, x), v)
            if op == "³":
                return self.unop(lambda x: num_mul(num_mul(x, x), x), v)
            if op == "⁻¹":
                return self.unop(lambda x: num_div(D(1), x), v)
            if op == "!":
                def fact(x):
                    x = to_real(x)
                    if not is_int(x) or x < 0 or x > 69:
                        raise TIError("DOMAIN")
                    return R(math.factorial(int(x)))
                return self.unop(fact, v)
        if k == "pow":
            return self.binop(lambda a, b: num_pow(a, b, self), self.eval(node.a), self.eval(node.b))
        if k == "bin":
            return self.binary(node.a, node.b, node.c)
        if k == "call":
            return self.call(node.a, node.b)
        if k == "seq":
            return self.seq(node)
        if k == "ycall":
            return self.ycall(node.a, self.eval(node.b))
        if k == "yvar":
            return self.ycall(node.a, self.vars["X"])
        raise TIError("SYNTAX", f"node {k}")

    def unop(self, f, v):
        if isinstance(v, list):
            self.cost["listel"] += len(v)
            return [f(x) for x in v]
        if isinstance(v, tuple):
            raise TIError("DATA TYPE")
        return f(v)

    def binop(self, f, a, b):
        if isinstance(a, tuple) or isinstance(b, tuple):
            raise TIError("DATA TYPE")
        if isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                raise TIError("DIM MISMATCH")
            self.cost["listel"] += len(a)
            return [f(x, y) for x, y in zip(a, b)]
        if isinstance(a, list):
            self.cost["listel"] += len(a)
            return [f(x, b) for x in a]
        if isinstance(b, list):
            self.cost["listel"] += len(b)
            return [f(a, y) for y in b]
        return f(a, b)

    def binary(self, op, na, nb):
        a = self.eval(na)
        b = self.eval(nb)
        if op == "+":
            if isinstance(a, tuple) and isinstance(b, tuple):
                self.cost["strch"] += len(a) + len(b)
                return a + b
            return self.binop(num_add, a, b)
        if op == "-":
            return self.binop(num_sub, a, b)
        if op == "*":
            return self.binop(num_mul, a, b)
        if op == "/":
            return self.binop(num_div, a, b)
        if op in CMP:
            if isinstance(a, tuple) and isinstance(b, tuple):
                if op == "=":
                    return D(int(a == b))
                if op == "≠":
                    return D(int(a != b))
                raise TIError("DATA TYPE")

            def cmp(x, y):
                if op in ("=", "≠"):
                    eq = re_im(x) == re_im(y)
                    return D(int(eq if op == "=" else not eq))
                x, y = to_real(x), to_real(y)
                return D(int({"<": x < y, ">": x > y, "≤": x <= y, "≥": x >= y}[op]))
            return self.binop(cmp, a, b)
        if op in ("and", "or", "xor"):
            def lg(x, y):
                x, y = to_real(x) != 0, to_real(y) != 0
                return D(int(x and y if op == "and" else (x or y) if op == "or" else x != y))
            return self.binop(lg, a, b)
        raise TIError("SYNTAX", op)

    def as_int(self, v, lo=None):
        v = to_real(v)
        if not is_int(v):
            raise TIError("DOMAIN", "not an integer")
        if lo is not None and v < lo:
            raise TIError("DOMAIN", "too small")
        return int(v)

    def call(self, f, argn):
        # functions that must not evaluate all arguments first
        args = [self.eval(a) for a in argn]
        n = len(args)

        def need(lo, hi=None):
            if n < lo or n > (hi if hi is not None else lo):
                raise TIError("ARGUMENT", f)

        if f == "abs(":
            need(1)
            return self.unop(lambda x: R(abs(x)) if isinstance(x, D) else R(HI.sqrt(x.re * x.re + x.im * x.im)), args[0])
        if f == "√(":
            need(1)
            return self.unop(lambda x: csqrt(x, self), args[0])
        if f == "round(":
            need(1, 2)
            nd = 9 if n == 1 else self.as_int(args[1], 0)
            if nd > 9:
                raise TIError("DOMAIN", "round digits")
            return self.unop(lambda x: R(to_real(x).quantize(D(1).scaleb(-nd), rounding=decimal.ROUND_HALF_UP)) if to_real(x).adjusted() < 90 else x, args[0])
        if f == "iPart(":
            need(1)
            return self.unop(lambda x: R(to_real(x).to_integral_value(rounding=decimal.ROUND_DOWN)), args[0])
        if f == "fPart(":
            need(1)
            return self.unop(lambda x: R(to_real(x) - to_real(x).to_integral_value(rounding=decimal.ROUND_DOWN)), args[0])
        if f == "int(":
            need(1)
            return self.unop(lambda x: R(to_real(x).to_integral_value(rounding=decimal.ROUND_FLOOR)), args[0])
        if f in ("gcd(", "lcm("):
            need(2)

            def g(a, b):
                a, b = to_real(a), to_real(b)
                if not is_int(a) or not is_int(b) or a < 0 or b < 0:
                    raise TIError("DOMAIN", f)
                if a >= D("1E12") or b >= D("1E12"):
                    raise TIError("DOMAIN", f + " too big")
                a, b = int(a), int(b)
                if f == "gcd(":
                    return D(math.gcd(a, b))
                return D(0 if a == 0 or b == 0 else a * b // math.gcd(a, b))
            return self.binop(g, args[0], args[1])
        if f == "remainder(":
            need(2)

            def rm(a, b):
                a, b = to_real(a), to_real(b)
                if not is_int(a) or not is_int(b) or a < 0 or b < 0:
                    raise TIError("DOMAIN", f)
                if b == 0:
                    raise TIError("DIVIDE BY 0")
                return D(int(a) % int(b))
            return self.binop(rm, args[0], args[1])
        if f in ("max(", "min("):
            pick = max if f == "max(" else min
            if n == 1:
                lst = args[0]
                if not isinstance(lst, list):
                    raise TIError("DATA TYPE", f)
                if not lst:
                    raise TIError("INVALID DIM", f + " of an empty list")
                self.cost["listel"] += len(lst)
                return pick(to_real(x) for x in lst)
            need(2)
            return self.binop(lambda a, b: pick(to_real(a), to_real(b)), args[0], args[1])
        if f == "not(":
            need(1)
            return self.unop(lambda x: D(int(to_real(x) == 0)), args[0])
        if f in ("real(", "imag(", "conj(", "angle("):
            need(1)

            def ri(x):
                r_, i_ = re_im(x)
                if f == "real(":
                    return r_
                if f == "imag(":
                    return i_
                if f == "conj(":
                    return simplify(C(r_, -i_))
                return R(D(repr(math.atan2(float(i_), float(r_)))))
            return self.unop(ri, args[0])
        if f in ("sin(", "cos(", "tan(", "ln(", "log(", "𝑒^(", "₁₀^(", "³√("):
            need(1)

            def tr(x):
                x = float(to_real(x))
                try:
                    if f == "sin(":
                        y = math.sin(x)
                    elif f == "cos(":
                        y = math.cos(x)
                    elif f == "tan(":
                        y = math.tan(x)
                    elif f in ("ln(", "log("):
                        if x == 0:
                            raise TIError("DOMAIN")
                        if x < 0:
                            raise TIError("NONREAL ANS")
                        y = math.log(x) if f == "ln(" else math.log10(x)
                    elif f == "𝑒^(":
                        y = math.exp(x)
                    elif f == "₁₀^(":
                        y = 10 ** x
                    else:
                        y = math.copysign(abs(x) ** (1 / 3), x)
                except OverflowError:
                    raise TIError("OVERFLOW")
                return R(D(repr(y)))
            return self.unop(tr, args[0])
        if f == "dim(":
            need(1)
            v = args[0]
            if not isinstance(v, list):
                raise TIError("DATA TYPE", "dim(")
            return D(len(v))
        if f == "sum(":
            need(1, 3)
            lst = args[0]
            if not isinstance(lst, list):
                raise TIError("DATA TYPE", "sum(")
            a = self.as_int(args[1], 1) if n > 1 else 1
            b = self.as_int(args[2], 1) if n > 2 else len(lst)
            if a > len(lst) + 1 or b > len(lst):
                raise TIError("INVALID DIM", "sum(")
            r = D(0)
            for x in lst[a - 1:b]:
                r = num_add(r, x)
            self.cost["listel"] += len(lst)
            return r
        if f == "prod(":
            need(1)
            r = D(1)
            for x in args[0]:
                r = num_mul(r, x)
            self.cost["listel"] += len(args[0])
            return r
        if f == "mean(":
            need(1)
            return num_div(self.call("sum(", [Node("num", None)]) if False else sum_list(args[0]), D(len(args[0])))
        if f == "cumSum(":
            need(1)
            r, out = D(0), []
            for x in args[0]:
                r = num_add(r, x)
                out.append(r)
            self.cost["listel"] += len(out)
            return out
        if f == "ΔList(":
            need(1)
            lst = args[0]
            if len(lst) < 2:
                raise TIError("INVALID DIM")
            self.cost["listel"] += len(lst)
            return [num_sub(lst[i + 1], lst[i]) for i in range(len(lst) - 1)]
        if f == "augment(":
            need(2)
            a, b = args
            if isinstance(a, list) and isinstance(b, list):
                if len(a) + len(b) > 999:
                    raise TIError("INVALID DIM")
                self.cost["listel"] += len(a) + len(b)
                return a + b
            raise TIError("DATA TYPE", "augment(")
        if f == "length(":
            need(1)
            if not isinstance(args[0], tuple):
                raise TIError("DATA TYPE", "length(")
            return D(len(args[0]))
        if f == "sub(":
            need(3)
            s = args[0]
            if not isinstance(s, tuple):
                raise TIError("DATA TYPE", "sub(")
            a, ln = self.as_int(args[1]), self.as_int(args[2])
            if a < 1 or ln < 1 or a + ln - 1 > len(s):
                raise TIError("DOMAIN", f"sub({len(s)},{a},{ln})")
            self.cost["strch"] += ln
            return s[a - 1:a - 1 + ln]
        if f == "inString(":
            need(2, 3)
            s, t = args[0], args[1]
            if not isinstance(s, tuple) or not isinstance(t, tuple):
                raise TIError("DATA TYPE", "inString(")
            st = self.as_int(args[2]) if n == 3 else 1
            if st < 1:
                raise TIError("DOMAIN", "inString(")
            self.cost["strch"] += len(s)
            L = len(t)
            for j in range(st - 1, len(s) - L + 1):
                if s[j:j + L] == t:
                    return D(j + 1)
            return D(0)
        if f == "toString(":
            need(1)
            v = args[0]
            if isinstance(v, tuple):
                return v
            if isinstance(v, list):
                raise TIError("DATA TYPE", "toString( list")
            return tuple(self.str_tokens(fmt_num(v)))
        if f == "eval(":
            need(1)
            return args[0]
        if f == "expr(":
            need(1)
            s = args[0]
            if not isinstance(s, tuple):
                raise TIError("DATA TYPE", "expr(")
            if not s:
                raise TIError("SYNTAX", "expr( empty")
            return self.eval_tokens(list(s))
        raise TIError("SYNTAX", f"func {f}")

    def str_tokens(self, s):
        """Turn a number's display string into tokens (digits, ., ⁻, ᴇ, 𝑖, +, -)."""
        return list(s)

    def eval_tokens(self, toks):
        key = tuple(toks)
        ast = self._expr_cache.get(key) if hasattr(self, "_expr_cache") else None
        if ast is None:
            if not hasattr(self, "_expr_cache"):
                self._expr_cache = {}
            ps = Parser(list(toks))
            ast = ps.expr()
            if ps.i != len(toks):
                raise TIError("SYNTAX", "expr(: " + "".join(toks))
            self._expr_cache[key] = ast
        self.cost["tok"] += len(toks)
        return self.eval(ast)

    def seq(self, node):
        e, v, rest = node.a, node.b, node.c
        if len(rest) not in (2, 3):
            raise TIError("ARGUMENT", "seq(")
        a = to_real(self.eval(rest[0]))
        b = to_real(self.eval(rest[1]))
        st = to_real(self.eval(rest[2])) if len(rest) == 3 else D(1)
        if st == 0:
            raise TIError("DOMAIN", "seq step")
        saved = self.vars[v]
        out = []
        x = a
        while (st > 0 and x <= b) or (st < 0 and x >= b):
            self.vars[v] = x
            out.append(self.eval(e))
            x = num_add(x, st)
            if len(out) > 999:
                raise TIError("INVALID DIM", "seq too long")
        self.vars[v] = saved
        self.cost["listel"] += 2 * len(out)
        return out

    def ycall(self, y, x):
        if y not in self.yvars or not self.yvars[y]:
            raise TIError("UNDEFINED", y)
        saved = self.vars["X"]
        if isinstance(x, list):
            res = []
            for xi in x:
                self.vars["X"] = xi
                res.append(self.eval_tokens(list(self.yvars[y])))
        else:
            self.vars["X"] = x
            res = self.eval_tokens(list(self.yvars[y]))
        self.vars["X"] = saved
        return res

    def mark_input(self):
        self.last_input_cost = dict(self.cost)

    def getkey(self):
        if self.last_input_cost is not None:
            self.answer_costs.append({k: self.cost[k] - self.last_input_cost[k] for k in self.cost})
            self.last_input_cost = None
        if not self.script:
            self.waiting_reason = "getKey"
            if self.on_wait:
                self.on_wait(self, "getKey")
            raise Halt("getKey")
        ch = self.script.pop(0)
        if ch not in GETKEY:
            raise RuntimeError(f"no getKey code for {ch!r}")
        return GETKEY[ch]

    # ---------------------------------------------------------- stores
    def store(self, val, toks):
        """Store val into the target written in toks (after →)."""
        if not toks:
            raise TIError("SYNTAX", "store target")
        t0 = toks[0]
        if len(toks) == 1 and t0 in LETTERS:
            if not is_num(val):
                raise TIError("DATA TYPE", f"→{t0}")
            self.vars[t0] = val
            return
        if len(toks) == 1 and t0 in STRVARS:
            if not isinstance(val, tuple):
                raise TIError("DATA TYPE", f"→{t0}")
            self.strs[t0] = val
            return
        if len(toks) == 1 and t0 in WINDOW:
            self.window[t0] = to_real(val)
            return
        if len(toks) == 1 and t0 in YVARS:
            if not isinstance(val, tuple):
                raise TIError("DATA TYPE", f"→{t0}")
            self.yvars[t0] = val
            return
        if t0 in LISTS or t0 == "ʟ":
            ps = Parser(toks)
            ps.take()
            name = ps.listname() if t0 == "ʟ" else t0
            if ps.peek() is None:
                if isinstance(val, list):
                    self.lists[name] = list(val)
                elif is_num(val):
                    raise TIError("DATA TYPE", f"→{name}")
                else:
                    raise TIError("DATA TYPE", f"→{name}")
                self.cost["listel"] += len(val)
                return
            if ps.peek() == "(":
                ps.take()
                i = to_real(self.eval(ps.expr()))
                ps.close()
                if not is_num(val):
                    raise TIError("DATA TYPE")
                lst = self.lists.get(name)
                if lst is None:
                    raise TIError("UNDEFINED", name)
                if not is_int(i) or i < 1 or i > len(lst) + 1:
                    raise TIError("INVALID DIM", f"{name}({i})")
                if i == len(lst) + 1:
                    if len(lst) >= 999:
                        raise TIError("INVALID DIM")
                    lst.append(val)
                else:
                    lst[int(i) - 1] = val
                return
        if t0 == "dim(":
            ps = Parser(toks)
            ps.take()
            lt = ps.take()
            name = ps.listname() if lt == "ʟ" else lt
            ps.close()
            n = self.as_int(val)
            if n < 1 or n > 999:
                raise TIError("INVALID DIM", "dim")
            lst = self.lists.setdefault(name, [])
            if len(lst) > n:
                del lst[n:]
            else:
                lst.extend([D(0)] * (n - len(lst)))
            return
        raise TIError("SYNTAX", "store to " + "".join(toks))

    # ---------------------------------------------------------- statements
    def run(self, name):
        self.frames = []
        try:
            self.call_prog(name)
        except StopProgram:
            pass

    def call_prog(self, name):
        prog = self.loader(name)
        if len(self.frames) > 40:
            raise TIError("MEMORY", "call depth")
        fr = Frame(prog)
        self.frames.append(fr)
        self.cost["call"] += 1
        try:
            while fr.pc < len(prog.stmts):
                self.exec_stmt(fr)
        except ReturnProgram:
            pass
        finally:
            self.frames.pop()

    def split_store(self, s):
        """Index of the top-level → in statement s, outside strings."""
        in_str = False
        for j, t in enumerate(s):
            if t == "\"":
                in_str = not in_str
            elif t == "→":
                if in_str:
                    in_str = False
                return j
        return -1

    def parse_expr_at(self, prog, idx, toks, start=0):
        key = (idx, start)
        if key in prog.ast:
            return prog.ast[key]
        ps = Parser(toks, start)
        node = ps.expr()
        end = ps.i
        prog.ast[key] = (node, end)
        return node, end

    def exec_stmt(self, fr):
        prog = fr.prog
        i = fr.pc
        s = prog.stmts[i]
        fr.pc += 1
        self.steps += 1
        if self.steps > self.max_steps:
            raise TIError("TIMEOUT", "step limit")
        self.cost["stmt"] += 1
        self.cost["tok"] += len(s)
        if not s:
            return
        h = s[0]
        if h == "If ":
            node, end = self.parse_expr_at(prog, i, s, 1)
            c = to_real(self.eval(node))
            nxt = prog.stmts[fr.pc] if fr.pc < len(prog.stmts) else None
            if nxt and nxt[0] == "Then":
                if c != 0:
                    fr.blocks.append(("if", fr.pc))
                    fr.pc += 1
                else:
                    j = prog.find_end(fr.pc, stop_at_else=True)
                    self.cost["skip"] += sum(len(x) + 1 for x in prog.stmts[fr.pc:j])
                    if prog.stmts[j][0] == "Else":
                        fr.blocks.append(("if", j))
                    fr.pc = j + 1
            elif c == 0:
                if fr.pc < len(prog.stmts):
                    self.cost["skip"] += len(prog.stmts[fr.pc]) + 1
                fr.pc += 1
            return
        if h == "Then":
            raise TIError("SYNTAX", "Then without If")
        if h == "Else":
            # reached the end of a true branch: skip to End
            j = self.end_of_else(prog, i)
            self.cost["skip"] += sum(len(x) + 1 for x in prog.stmts[i:j])
            if not fr.blocks or fr.blocks[-1][0] != "if":
                raise TIError("SYNTAX", "Else")
            fr.blocks.pop()
            fr.pc = j + 1
            return
        if h == "End":
            if not fr.blocks:
                raise TIError("SYNTAX", f"End without block in {prog.name}")
            kind, at, *rest = fr.blocks[-1]
            if kind == "if":
                fr.blocks.pop()
                return
            if kind == "for":
                var, endv, step = rest
                v = num_add(self.vars[var], step)
                self.vars[var] = v
                if (step > 0 and v <= endv) or (step < 0 and v >= endv):
                    fr.pc = at + 1
                else:
                    fr.blocks.pop()
                return
            if kind == "while":
                fr.blocks.pop()
                fr.pc = at
                return
            if kind == "repeat":
                st = prog.stmts[at]
                node, _ = self.parse_expr_at(prog, at, st, 1)
                c = to_real(self.eval(node))
                if c != 0:
                    fr.blocks.pop()
                else:
                    fr.pc = at + 1
                return
        if h == "For(":
            var = s[1]
            if var not in LETTERS or s[2] != ",":
                raise TIError("SYNTAX", "For(")
            ps = Parser(s, 3)
            a = to_real(self.eval(ps.expr()))
            ps.expect(",")
            b = to_real(self.eval(ps.expr()))
            st = D(1)
            if ps.peek() == ",":
                ps.take()
                st = to_real(self.eval(ps.expr()))
            ps.close()
            if st == 0:
                raise TIError("DOMAIN", "For step 0")
            self.vars[var] = a
            if (st > 0 and a > b) or (st < 0 and a < b):
                j = prog.find_end(i)
                self.cost["skip"] += sum(len(x) + 1 for x in prog.stmts[i:j])
                fr.pc = j + 1
            else:
                fr.blocks.append(("for", i, var, b, st))
            return
        if h == "While ":
            node, _ = self.parse_expr_at(prog, i, s, 1)
            if to_real(self.eval(node)) != 0:
                fr.blocks.append(("while", i))
            else:
                j = prog.find_end(i)
                self.cost["skip"] += sum(len(x) + 1 for x in prog.stmts[i:j])
                fr.pc = j + 1
            return
        if h == "Repeat ":
            fr.blocks.append(("repeat", i))
            return
        if h == "Lbl ":
            return
        if h == "Goto ":
            self.goto(fr, "".join(s[1:]))
            return
        if h == "Return":
            raise ReturnProgram()
        if h == "Stop":
            raise StopProgram()
        if h == "prgm":
            self.call_prog("".join(s[1:]))
            return
        if h in self.COMMANDS:
            self.COMMANDS[h](self, fr, i, s)
            return
        # expression statement, optional store
        j = self.split_store(s)
        if j >= 0:
            node, end = self.parse_expr_at(prog, i, s[:j], 0)
            if end != j:
                raise TIError("SYNTAX", "".join(s))
            v = self.eval(node)
            self.store(v, s[j + 1:])
            if is_num(v) or isinstance(v, (list, tuple)):
                self.ans = v
            return
        node, end = self.parse_expr_at(prog, i, s, 0)
        if end != len(s):
            raise TIError("SYNTAX", "".join(s))
        self.ans = self.eval(node)

    def end_of_else(self, prog, i):
        depth = 0
        j = i + 1
        while j < len(prog.stmts):
            st = prog.stmts[j]
            if st:
                if st[0] in ("Then", "For(", "While ", "Repeat "):
                    depth += 1
                elif st[0] == "End":
                    if depth == 0:
                        return j
                    depth -= 1
            j += 1
        raise TIError("SYNTAX", "Else without End")

    def goto(self, fr, label):
        prog = fr.prog
        if label not in prog.labels:
            raise TIError("LABEL", label)
        if fr.blocks:
            self.leaks.append(f"{prog.name}: Goto {label} with {len(fr.blocks)} open block(s)")
        # the calculator finds a label by scanning from the top of the program
        self.cost["skip"] += sum(len(x) + 1 for x in prog.stmts[:prog.labels[label]])
        fr.pc = prog.labels[label] + 1

    # ---------------------------------------------------------- commands
    def args_of(self, prog, i, s, start):
        key = ("args", i, start)
        if key not in prog.ast:
            ps = Parser(s, start)
            out = []
            if ps.peek() is not None:
                while True:
                    out.append(ps.expr())
                    if ps.peek() == ",":
                        ps.take()
                        continue
                    break
            if ps.peek() == ")":
                ps.take()
            if ps.peek() is not None:
                raise TIError("SYNTAX", "".join(s))
            prog.ast[key] = out
        return prog.ast[key]

    def c_clrhome(self, fr, i, s):
        self.screen = [[" "] * COLS for _ in range(ROWS)]
        self.row = 0

    def c_disp(self, fr, i, s):
        for node in self.args_of(fr.prog, i, s, 1):
            v = self.eval(node)
            if isinstance(v, tuple):
                self.disp_line(self.chars(v))
            elif isinstance(v, list):
                self.disp_line(list("{" + " ".join(fmt_num(x) for x in v) + "}"), right=True)
            else:
                self.disp_line(list(fmt_num(v)), right=True)

    def c_output(self, fr, i, s):
        a = self.args_of(fr.prog, i, s, 1)
        if len(a) != 3:
            raise TIError("ARGUMENT", "Output(")
        r = self.as_int(self.eval(a[0]))
        c = self.as_int(self.eval(a[1]))
        if not (1 <= r <= ROWS and 1 <= c <= COLS):
            raise TIError("DOMAIN", "Output( position")
        v = self.eval(a[2])
        ch = self.chars(v) if isinstance(v, tuple) else list(fmt_num(v))
        self.put_chars(r - 1, c - 1, ch, wrap=True)

    def c_input(self, fr, i, s):
        # Input "PROMPT",var   or   Input var
        prompt = ["?"]
        j = 1
        if len(s) > 1 and s[1] == "\"":
            k = 2
            pt = []
            while k < len(s) and s[k] != "\"":
                pt.append(s[k]); k += 1
            prompt = self.chars(pt)
            j = k + 2  # skip closing quote and comma
            if s[k + 1] != ",":
                raise TIError("SYNTAX", "Input")
        target = s[j:]
        self.newline_check()
        typed = []
        r0 = self.row

        def show():
            nonlocal r0
            ch = prompt + self.chars(typed)
            need = max(1, (len(ch) + 1 + COLS - 1) // COLS)
            while r0 + need > ROWS:
                self.scroll(); r0 -= 1
            for r in range(r0, min(ROWS, r0 + need)):
                self.screen[r] = [" "] * COLS
            self.put_chars(r0, 0, ch)
            return need
        while True:
            show()
            k = self.next_key("Input")
            if k == "\n":
                break
            if k == "#":
                typed = []
                continue
            typed.append(KEYTOK.get(k, k))
        need = show()
        self.row = r0 + max(1, (len(prompt) + disp_width(typed) + COLS - 1) // COLS)
        self.inputs_done += 1
        self.mark_input()
        self.cost_marks.append(("input", dict(self.cost)))
        self.events.append(("input", "".join(prompt), "".join(typed)))
        if len(target) == 1 and target[0] in STRVARS:
            self.strs[target[0]] = tuple(typed)
            return
        v = self.eval_tokens(typed)
        self.store(v, target)

    def c_menu(self, fr, i, s):
        a = self.args_of(fr.prog, i, s, 1)
        title = self.eval(a[0])
        items = []
        for k in range(1, len(a), 2):
            txt = self.eval(a[k])
            lab_node = a[k + 1]
            # label is the raw tokens; recover from the AST
            items.append((txt, self.label_of(lab_node)))
        if len(items) > 7 or not items:
            raise TIError("ARGUMENT", "Menu(")
        saved = [row[:] for row in self.screen]
        sel = 0
        while True:
            self.screen = [[" "] * COLS for _ in range(ROWS)]
            self.put_chars(0, 0, self.chars(title)[:COLS], wrap=False)
            for n_, (txt, _) in enumerate(items):
                self.put_chars(n_ + 1, 0, list(f"{n_ + 1}:") + self.chars(txt)[:COLS - 2], wrap=False)
            k = self.next_key("Menu")
            if k == "<":
                sel = (sel - 1) % len(items)
            elif k == ">":
                sel = (sel + 1) % len(items)
            elif k == "\n":
                break
            elif k in "1234567" and int(k) <= len(items):
                sel = int(k) - 1
                break
        self.screen = saved
        self.mark_input()
        self.events.append(("menu", "".join(self.chars(title)), sel + 1))
        self.goto(fr, items[sel][1])

    def label_of(self, node):
        if node.kind == "var":
            return node.a
        if node.kind == "num":
            v = node.a
            return str(int(v)) if is_int(v) else str(v)
        if node.kind == "bin" and node.a == "*":
            return self.label_of(node.b) + self.label_of(node.c)
        raise TIError("SYNTAX", "menu label")

    def c_pause(self, fr, i, s):
        if len(s) > 1:
            self.c_disp(fr, i, s)
        while True:
            k = self.next_key("Pause")
            if k == "\n":
                return

    def c_delvar(self, fr, i, s):
        t = s[1:]
        if len(t) == 1 and t[0] in LETTERS:
            self.vars[t[0]] = D(0)
        elif len(t) == 1 and t[0] in STRVARS:
            self.strs.pop(t[0], None)
        elif t and t[0] == "ʟ":
            self.lists.pop("ʟ" + "".join(t[1:]), None)
        elif len(t) == 1 and t[0] in LISTS:
            self.lists.pop(t[0], None)
        else:
            raise TIError("SYNTAX", "DelVar")

    def c_clrlist(self, fr, i, s):
        names = []
        cur = []
        for t in s[1:] + [","]:
            if t == ",":
                if cur:
                    names.append("".join(cur))
                cur = []
            else:
                cur.append(t)
        for nm in names:
            if nm not in LISTS and not nm.startswith("ʟ"):
                raise TIError("SYNTAX", "ClrList")
            if nm not in self.lists and nm not in LISTS:
                # TI's behaviour on a missing custom list is not documented,
                # so the harness treats it as an error (programs must create
                # the list first, as ZLNEW does with SetUpEditor)
                raise TIError("UNDEFINED", "ClrList " + nm)
            self.lists[nm] = []

    def c_setup(self, fr, i, s):
        names = "".join(s[1:])
        for nm in [x for x in names.split(",") if x]:
            self.lists.setdefault("ʟ" + nm, [])

    def c_mode(self, fr, i, s):
        h = s[0]
        if h == "Real":
            self.complex_mode = False
        elif h == "a+b𝑖":
            self.complex_mode = True
        elif h in ("Float", "Fix "):
            self.mode = h

    def c_graph(self, fr, i, s):
        self.cost["draw"] += 1
        text = "".join(s)
        if len(s) > 1 and s[0] in ("Vertical ", "Horizontal ", "Pt-On(", "Text(", "Line("):
            try:
                vals = [self.eval(a) for a in self.args_of(fr.prog, i, s, 1)]
                text = s[0] + ",".join("".join(v) if isinstance(v, tuple) else fmt_num(v) for v in vals)
            except TIError:
                pass
        self.graph_log.append(text)

    def c_sorta(self, fr, i, s):
        a = self.args_of(fr.prog, i, s, 1)
        names = []
        for n_ in a:
            if n_.kind != "list":
                raise TIError("ARGUMENT", "SortA(")
            names.append(n_.a)
        key = self.get_list(names[0])
        order = sorted(range(len(key)), key=lambda j: to_real(key[j]))
        for nm in names:
            l_ = self.get_list(nm)
            if len(l_) != len(key):
                raise TIError("DIM MISMATCH")
            self.lists[nm] = [l_[j] for j in order]
        self.cost["listel"] += len(key) * 4

    def c_strequ(self, fr, i, s):
        a = self.args_of(fr.prog, i, s, 1)
        v = self.eval(a[0])
        if not isinstance(v, tuple) or a[1].kind != "yvar":
            raise TIError("DATA TYPE", "String►Equ(")
        self.yvars[a[1].a] = v

    def c_equstr(self, fr, i, s):
        a = self.args_of(fr.prog, i, s, 1)
        if a[0].kind != "yvar" or a[1].kind != "var":
            raise TIError("DATA TYPE", "Equ►String(")
        y = a[0].a
        if not self.yvars.get(y):
            raise TIError("UNDEFINED", "Equ►String( of empty " + y)
        self.strs[a[1].a] = self.yvars[y]

    def c_drawf(self, fr, i, s):
        self.cost["draw"] += 40
        node, _ = self.parse_expr_at(fr.prog, i, s, 1)
        text = "".join(s)
        if node.kind == "call" and node.a == "expr(":
            v = self.eval(node.b[0])
            if isinstance(v, tuple):
                text = "DrawF " + "".join(v)
        self.graph_log.append(text)
        # sample the expression the way the grapher would, ignoring errors
        saved = self.vars["X"]
        for xx in (D(-3), D("0.5"), D(2)):
            self.vars["X"] = xx
            try:
                self.eval(node)
            except TIError:
                pass
        self.vars["X"] = saved

    COMMANDS = {}


def sum_list(lst):
    r = D(0)
    for x in lst:
        r = num_add(r, x)
    return r


Interp.COMMANDS = {
    "ClrHome": Interp.c_clrhome,
    "Disp ": Interp.c_disp,
    "Output(": Interp.c_output,
    "Input ": Interp.c_input,
    "Menu(": Interp.c_menu,
    "Pause ": Interp.c_pause,
    "DelVar ": Interp.c_delvar,
    "SetUpEditor ": Interp.c_setup,
    "SetUpEditor": lambda self, fr, i, s: None,
    "Real": Interp.c_mode,
    "a+b𝑖": Interp.c_mode,
    "Float": Interp.c_mode,
    "Fix ": Interp.c_mode,
    "SortA(": Interp.c_sorta,
    "ClrList ": Interp.c_clrlist,
    "String►Equ(": Interp.c_strequ,
    "Equ►String(": Interp.c_equstr,
    "DrawF ": Interp.c_drawf,
}
for _g in ("ClrDraw", "DispGraph", "Text(", "Pt-On(", "Line(", "Vertical ", "Horizontal ", "AxesOn ",
           "AxesOff", "GridOff", "PlotsOff ", "FnOff ", "FnOn ", "Pt-Off(", "Circle(", "LabelOff", "CoordOff"):
    Interp.COMMANDS[_g] = Interp.c_graph


# ------------------------------------------------------------------ loading
class Library:
    """Loads programs by name from build/*.8xp (preferred) or src/*.txt."""

    def __init__(self, root, prefer="build"):
        self.root = root
        self.prefer = prefer
        self.cache = {}

    def __call__(self, name):
        if name in self.cache:
            return self.cache[name]
        b = os.path.join(self.root, "build", name + ".8xp")
        s = os.path.join(self.root, "src", name + ".txt")
        if self.prefer == "build" and os.path.exists(b):
            toks = tokens_from_8xp(b)
        elif os.path.exists(s):
            with open(s, encoding="utf-8") as fh:
                toks = tokenize(fh.read().rstrip("\n"), "max" if name in MAX_MUNCH else "smart")
        else:
            raise TIError("UNDEFINED", "prgm" + name)
        p = Program(name, toks)
        self.cache[name] = p
        return p


# Estimated CE timings (ms). These are assumptions, not measurements: see
# REPORT.md. A statement costs a base amount plus a per-token parse cost;
# list elements, string characters and subprogram calls add their own.
COST_MS = {"stmt": 0.9, "tok": 0.12, "call": 4.0, "listel": 0.06, "strch": 0.004, "draw": 2.0, "skip": 0.02}


def ram_bytes(interp, loader=None, running=()):
    """Rough RAM the kit's own variables take: 9 bytes per real list element,
    1-2 bytes per string token, plus a VAT entry per variable, plus the
    programs that are running (an archived program is copied to RAM to run)."""
    total = 0
    for name, lst in interp.lists.items():
        if name.startswith("ʟMK"):
            total += 2 + 9 * len(lst) * (2 if any(isinstance(x, C) for x in lst) else 1) + 12
    for name, st in interp.strs.items():
        total += 2 + sum(2 if len(t) > 1 or ord(t[0]) > 127 else 1 for t in st) + 9
    if loader is not None:
        for name in running:
            p = loader(name)
            total += sum(2 if len(t) > 1 or (t and ord(t[0]) > 127) else 1 for t in p.toks) + 20
    return total


def cost_ms(c):
    return sum(COST_MS[k] * c.get(k, 0) for k in COST_MS)
