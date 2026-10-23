# Installing MATHKIT 1.0

## 1. Check your calculator

| Need | How to check |
|---|---|
| **TI-84 Plus CE** or TI-84 Plus CE Python, **OS 5.2.0 or later** | Press **2nd**, **mem** (above **+**), then **1:About**. The OS version is on that screen. |
| **About 60 KB of free Archive** (to store the kit) | **2nd mem**, **2:Mem Management/Delete…**. The top shows **ARC FREE**. |
| **At least 30 KB of free RAM** (to run it) | Same screen, **RAM FREE** |

**Why OS 5.2.0?** The programs use `toString(`, which TI added to the CE in OS 5.2.0. `tools/build.py` checks every token against the tivars token sheet and fails the build if any needs a newer OS. The kit's highest requirement is exactly 5.2.0; `String►Equ(` dates back to the TI-83.

On OS 5.2.x, archived programs cannot be run, so keep the kit in RAM (section 4).

## 2. What to send

The `build/` folder holds:

- one `.8xp` file per program: 33 in all, the 13 you run plus 20 helpers (names starting ZL, and ZEXPR)
- `MATHKIT.8xg`, a group file holding all 33 programs

Keep a copy of the whole `build/` folder on your computer. It is how you reinstall after a RAM clear or Press-to-Test.

## 3. Transfer with TI Connect CE

1. Install **TI Connect CE** from education.ti.com and connect the calculator with its USB cable. Turn the calculator on.
2. Open **Calculator Explorer**. The calculator should appear in the list.
3. Drag `MATHKIT.8xg` from `build/` onto the calculator, or select all 33 `.8xp` files and drag them together.
4. When asked where to store them, choose **Archive** (recommended, OS 5.3 and later) or **RAM** (OS 5.2.x). See section 4.
5. **If the calculator receives one group variable** instead of 33 programs, ungroup it:
   1. Press **2nd mem**, then **8:Group…**, then **UNGROUP**.
   2. Choose MATHKIT and press **enter**.
   3. Choose **Overwrite All** if asked.
   4. Delete the group afterwards to save space: **2nd mem > 2:Mem Management/Delete…**, then **Group…**.

To run the kit, press **prgm**, choose **MATHKIT** and press **enter enter**.

## 4. Archive or RAM

**Recommended: archive the whole kit** (OS 5.3 or later).

- Programs in Archive survive a RAM clear and a dead battery, and they use no RAM while idle.
- Cemetech's OS 5.3 changelog reports that archived programs and subprograms can be run directly. That is a community source and has not been tested with MATHKIT yet: HARDWARE-TEST.md item H1 checks it.
- To archive a program: **2nd mem**, **2:Mem Management/Delete…**, **7:Prgm…**. Move to a program and press **enter**; an asterisk `*` marks it archived. Press **enter** again to unarchive.

**If a helper must be in RAM.** If `prgmMATHKIT` stops with **ERR:ARCHIVED** when it calls a helper, unarchive the helpers and leave the main programs archived. The helpers total about 12 KB:

> ZEXPR, ZLA, ZLADD, ZLCHK, ZLCST, ZLDVQ, ZLEVL, ZLFLD, ZLFMT, ZLFRC, ZLIFC, ZLMUL, ZLNEW, ZLQSV, ZLRAD, ZLSHOW, ZLSYN, ZLTOK, ZLZER, ZLZNM, ZLZRL

**Speed.** If archived programs are copied to RAM each time they run, keeping the helpers in RAM may also be faster. HARDWARE-TEST.md item H2 compares the two.

**On OS 5.2.x, keep everything in RAM.** The kit needs 58,403 bytes of RAM storage, plus working space.

## 5. How much memory the kit uses

| What | Size | Source |
|---|---|---|
| All 33 programs | **58,403 bytes** (under the 60 KB budget) | `build/sizes.txt`, token bytes plus each variable's header |
| Largest single program (ZGRAPH) | 8,561 bytes | well under the 16 KB target and the 65,535-byte limit for one variable |
| Working lists and strings while a problem runs | about 3.6 KB at most | harness measurement, largest case |
| Running programs, if archived programs are copied to RAM | about 11 KB at most (MATHKIT + ZZEROS + ZLZER + ZLZRL + ZLSYN + ZLFRC + ZLA + ZLSHOW) | estimate from `build/sizes.txt` |
| **Free RAM needed while running** | **about 15 KB; keep 30 KB free** | |

The working lists are all named ⌊MK…. Each problem reuses the same set rather than making new ones. **MATHKIT > 7:SETTINGS / QUIT > 3:CLEAN UP AND QUIT** deletes them. The settings list ⌊MKS is recreated, with show-work on, the next time any program runs.

**Fragmentation.** Archive space can fragment. If a transfer fails while plenty of ARC FREE shows, let the calculator run **Garbage Collect** when it asks, then send again.

## 6. What MATHKIT changes on your calculator

- **Overwritten:**
  - the real variables A–W, Y, Z and θ
  - the strings Str0–Str9
- **Modes:** Float and Real mode are set.
- **Graph screen:**
  - graph pages clear any drawings
  - graph pages change the window and then put it back
- **Created:** the lists named ⌊MK…
- **Never touched:** Y₀–Y₉ and X. ZEXPR and ZCHECK save X and restore it.
- **If a program stops early,** through ERR:SYNTAX after a mistyped entry or the **on** key, the last values are left behind. TI-BASIC cannot trap errors. X is restored only when a program reaches its normal end.

## 7. Uninstall

1. Run MATHKIT and choose **7:SETTINGS / QUIT > 3:CLEAN UP AND QUIT** to delete the working lists, including ⌊MKS.
2. Press **2nd mem**, then **2:Mem Management/Delete…**, then **7:Prgm…**. Delete **MATHKIT** and every program starting with **Z**: press **del** on each, then **2:Yes**.
3. If you kept the group variable, delete it under **Group…** on the same screen.

## 8. Exams and Press-to-Test

- **Ask first.** Using MATHKIT on a test needs your instructor's approval. The course bans calculators that perform symbolic manipulation, and these programs simplify, factor and show steps. Until the instructor approves, use the kit for homework and study only.
- **What Press-to-Test does.** TI documents that Press-to-Test disables programs and deletes the variables in RAM and Archive, except AppVars. MATHKIT is programs and lists, so **all of it is removed** or disabled for the exam. See [TI knowledge base 34886](https://education.ti.com/en/customer-support/knowledge-base/ti-83-84-plus-family/product-usage/34886) and the [TI Press-to-Test guide](https://edresources.ti.com/-/media/files/ti-education/us/testing-tools/press_to_test_en.pdf).
- **Reinstalling after the exam:**
  1. Leave exam mode. Connect to TI Connect CE and choose **Actions > Quit Exam Mode**, or follow TI's steps for your OS.
  2. Send the kit again from your saved copy of `build/`. One drag of `MATHKIT.8xg` restores everything (section 3).
- **Answer-only mode** exists for checking homework quickly. It does not change what your instructor allows.
