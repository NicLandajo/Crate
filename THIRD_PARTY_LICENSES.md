# Third-Party Licenses and Attribution

Crate is released under the **Apache License 2.0**.

Crate does not include or link against any of the software below. It invokes
each engine as a **separate process**, passing arguments on the command line and
reading the result. The licenses of those engines apply to those engines only —
not to Crate, and not to anything you make with Crate.

For convenience, prebuilt engine binaries are offered as a separate download so
that Crate works without users having to compile or configure anything. That
makes this project a **redistributor** of the software listed here. The terms and
source links below are provided to meet those obligations.

---

## FFmpeg — GPL v3

**This is the only component under a copyleft license. Please read this section.**

| | |
|---|---|
| Project | FFmpeg — https://ffmpeg.org |
| Build | `full_build` from https://www.gyan.dev/ffmpeg/builds/ |
| Version | `2026-02-15-git-33b215d155-full_build-www.gyan.dev` |
| License | **GNU General Public License v3** |
| **Corresponding source** | **https://github.com/FFmpeg/FFmpeg/commit/33b215d155** |

This build is GPL v3 because it is compiled with GPL-licensed libraries,
including `libx264`, `libx265` and `frei0r`.

The complete GPL v3 text and the build's own `README.txt` are included in the
FFmpeg folder of the engine download. **Do not remove them** — they must stay
with the binary if you pass it on.

**What this means in practice**

- GPL v3 covers the FFmpeg binary. It does **not** extend to Crate, because
  Crate runs FFmpeg as a separate process rather than linking to it.
- You are free to obtain FFmpeg yourself from any source and point Crate at it.
  The bundled download is a convenience, not a requirement. Engine paths are
  configurable in `crate_engines.txt`.
- If you redistribute the FFmpeg binary, the same obligations pass to you:
  include the license text and keep the source link visible alongside it.

**Studio and legal note.** Some facilities have policies covering GPL v3
specifically. If that applies to you, install FFmpeg through your own approved
channel and set `FFMPEG_PATH` in `crate_engines.txt`. Crate does not care where
the binary comes from.

---

## OpenImageIO — Apache License 2.0

| | |
|---|---|
| Project | https://github.com/AcademySoftwareFoundation/OpenImageIO |
| Used for | Decoding and resizing EXR, DPX, Cineon, HDR, TIFF and other film formats for thumbnails |
| License | Apache License 2.0 |

Permissive. Redistribution requires the license text and NOTICE file, which are
included in the OpenImageIO folder of the engine download.

---

## F3D — BSD 3-Clause

| | |
|---|---|
| Project | https://github.com/f3d-app/f3d |
| Used for | Offscreen rendering of geometry and Gaussian splats for card thumbnails, and the Inspect 3D viewer |
| License | BSD 3-Clause |

Permissive. The license text is included in the F3D folder of the engine
download.

---

## ImageMagick — ImageMagick License

| | |
|---|---|
| Project | https://imagemagick.org |
| Used for | Stills conversion and inspection, layered and less common image formats |
| License | ImageMagick License (derived from Apache 2.0) |

Permissive. The license text is included in the ImageMagick folder of the engine
download.

---

## MediaInfo — BSD 2-Clause

| | |
|---|---|
| Project | https://mediaarea.net/en/MediaInfo |
| Used for | Reading technical metadata: codec, bit depth, colour primaries, timecode, duration |
| License | BSD 2-Clause |

Permissive, read-only, never modifies source files. The license text is included
in the MediaInfo folder of the engine download.

---

## splat_transform

| | |
|---|---|
| Project | https://github.com/playcanvas/splat-transform |
| Used for | Gaussian splat format conversion behind the SPLAT-C panel |
| License | See the project repository |

The license text is included with the binary in the engine download.

---

## Camera data

Crate's camera database would not exist without two projects that chose to
publish work they could have kept.

**VFX Camera Database**
https://vfxcamdb.com

**Matchmove Machine**
https://matchmovemachine.com

Sensor dimensions, crop modes and camera specifications are derived from these
sources and used with permission. They are **reference data, not software**, and
are not covered by Crate's Apache 2.0 license. If you fork Crate or reuse the
camera database, please contact the original sources directly rather than
assuming permission carries over.

---

## Runtime

Crate runs inside **Foundry Nuke** and uses the Qt bindings Nuke provides
(PySide6, or PySide2 on older versions). Crate does not redistribute Qt or
PySide.

---

## Getting the engines yourself

Nothing here has to come from the Crate download. Every engine path is
configurable in `crate_engines.txt`, and Crate will use whatever binaries you
point it at — your studio's approved builds, a package manager, or your own
compilations. The bundled download exists so that people who are not comfortable
assembling five command-line tools can still use Crate.

---

## Corrections

If you maintain one of these projects and anything here is wrong, misattributed,
or you would prefer to be credited differently, please open an issue and it will
be corrected.
