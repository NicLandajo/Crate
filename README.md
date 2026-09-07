# CRATE 2 for Nuke | Feature Tour Video
[![Crate 2.0 — Intro Tour](https://img.youtube.com/vi/DI1a0VykNU8/maxresdefault.jpg)](https://youtu.be/DI1a0VykNU8)

# About Crate

Crate is an asset browser and processing suite that runs inside Nuke. It browses your studio's libraries like a folder tree, previews geometry and Gaussian splats in 3D before import, and drops assets straight into the Node Graph.

It generates thumbnails automatically as you browse, including from geometry and Gaussian splats. Thumbnails are cached once and shared, so the first artist to open a folder pays the cost and everyone else reads the result.

Built for teams. Curators configure libraries, users and engines; Visitors browse and import. Access, write privileges and interface options are set per role, so an artist sees a simple browser while a pipeline lead sees the controls.

Libraries and their caches are separate, so you can keep thumbnails and animated previews on SSD or NVMe while the raw elements live on high-capacity storage server.

Compatible with Nuke 15, 16 and 17, on PySide2 and PySide6. Development and testing focused on Nuke 17.

Apache 2.0 · [Third-party licenses](THIRD_PARTY_LICENSES.md)

# Building your Crate | 3 Steps Quick Install

<h3 style="font-size: 1.5em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  1) Please read "crate_manual_library_organization.md" recommendation first
</h3>

<h3 style="font-size: 1.5em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  2) Download Crate Engines and recommended plugins/tools from
</h3>

link 1 Crate Image Engines https://drive.google.com/file/d/1aTyaviI9aqxl9kP2Epu1HIMULeY7qVvX/view?usp=sharing

link 2 Crate Plugins (optional) https://drive.google.com/file/d/1RfncmBcdVcyZL6NlJDoe_Amw_WABeFSu/view?usp=sharing

link 3 splat-transform Engine https://drive.google.com/file/d/1pJtFgzg9Z8gBl74MensZ0lLqzJWt7hRN/view?usp=sharing

Your Crate Engines folder should look like this:

<pre>
    Crate Image Engines/
    ├── _plugins/
    ├── f3d/
    ├── ffmpeg/
    ├── imagemagick/
    ├── mediainfo/
    ├── OpenImageIO/
    └── splat-transform/ 
    </pre>

<p>For Windows, the path <code>C:\Users\Public\Crate Image Engines</code> is highly recommended.</p>

<blockquote>
<strong>Important Security Note:</strong> If you choose to install this in a different directory, please ensure your operating system permissions, antivirus, or security software do not block Nuke from accessing this folder. Restrictive environments may prevent the tools and plugins from executing correctly.
</blockquote>

<blockquote>
<strong>Platform support.</strong> Crate is developed and tested on Windows 10 22H2 and works on Windows 11. The engine bundle contains Windows <code>.exe</code> binaries, including the Node.js runtime used by splat-transform.
<br><br>
macOS and Linux are not supported yet. The path is short, though: every engine path is configurable in <code>crate_engines.txt</code>, so pointing Crate at native builds of FFmpeg, OpenImageIO, F3D, ImageMagick, MediaInfo and splat-transform is the first step. Node.js is already present on most Linux and macOS machines, so the splat conversion panel is likely the easiest piece to get running. The remaining work is a small number of Windows-only calls in <code>crate_flight_recorder.py</code>. Contributions welcome.
</blockquote>

<blockquote>
<strong>OS Permissions:</strong> To run the application properly with read + write + execute permissions as a normal user, place the files in the shared folder for your operating system, talk to your admin or find the way for your OS admin to give these permissions so Crate can operate normally from Nuke.
</blockquote>


<h3 style="font-size: 1.5em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  3) Download Crate release and connect to pipeline
</h3>


3.1. Download Crate release. Place the crate_2.#.# folder on a network location every Nuke workstation can read, e.g. \\YourServer\pipeline\nuke\crate_2.#.#

3.2. Register it in Nuke. Add this line to your studio's init.py:

     nuke.pluginAddPath("\\\\YourServer\\pipeline\\nuke\\crate_2.#.#")

3.3. Launch Nuke and claim your install. On first launch, Crate detects that no Curators exist yet and shows a "Welcome to Crate" dialog. If you are the asset manager or pipeline lead, press Claim as Curator, this registers your username with full         access.

3.4. Prepare Crate while it's locked. Claiming automatically locks Crate for all users, so you can set it up safely before it's used. Open Crate from Nuke's menu and configure everything from Settings: start with connecting Crate Engines by pointing       the paths to the location where you placed them.

3.5. Set up at least one library. You must do this first so that the subsequent use of Crate proceeds smoothly as it comes to life.
     Cache tip: Give each library its own dedicated cache folder named after the library (e.g. Crate Caches/Libraries/Smoke)

3.6. Although Crate is intuitive, we recommend reading the user manual at this point; click on Settings/User Manual. It should be noted that this manual is primarily aimed at Curators, Pipe TDs, IT staff, and the like, rather than the casual user (such as a compositing artist who quickly opens Crate to grab an element and leave, The Visitor). We will cover the use of Crate for Visitors in future video tutorials, but the interface is very simple, and all users will be able to use it immediately without needing any introduction.

3.7. Continue to setup Crate modules and all the settings.

3.8. Try out Crate's locked mode for a few days to ensure everything works as expected.

3.9. Unlock and go live. When configuration is done, release the lock from Settings. Crate is now live for the whole pipeline: Curators manage content, everyone else browses as Visitors.
    Crate will now handle everything automatically, adding users to its database as they use it for the first time. Over the coming days and weeks, Crate's charts and analytics will provide
    feedback on how everything is performing and whether any adjustments are needed.

# Update Crate to the latest version

Always read the "version.txt" file for update/install instructions. Remember to backup your current version first (entire Crate folder and config files at all its locations) for easy rollback.
Only then, once you have ensured that you can fully restore your previous version, should you proceed to update and connect the new version.

Check for updates using the Update button in Crate's Settings.

## Licenses

Crate is under Apache License.

F3D, which Crate depends on, is licensed under the BSD 3-Clause License.

ImageMagick, which Crate depends on, is licensed under the ImageMagick License (the "License").

FFmpeg, which Crate depends on, is distributed here as the `full_build` from
gyan.dev, licensed under the **GNU General Public License v3**. This build
includes GPL components (libx264, libx265, frei0r).
Corresponding source: https://github.com/FFmpeg/FFmpeg/commit/33b215d155
GPL v3 applies to the FFmpeg binary only. Crate is Apache 2.0 and invokes
FFmpeg as a separate process, which does not create a combined work. You may
point Crate at any FFmpeg build you prefer via `crate_engines.txt`.

MediaInfo, which Crate depends on, is under the BSD 2-Clause License

OpenImageIO, which Crate depends on, is under the Apache-2.0 License
(project: https://github.com/AcademySoftwareFoundation/OpenImageIO).
The Windows binaries in the Crate Image Engines bundle are a community
build (https://github.com/pitvfx/OpenImageIO), since ASWF does not
publish official Windows binaries. The build bundles third-party
components (Qt 6 under LGPL-3.0, Python under PSF, and others) under
their own licenses, see the licensing note included alongside the
engines bundle.

Playcanvas SplatTransform - 3D Gaussian Splat Converter, which Crate depends on, is under MIT License.

Splat , WebGL 3D Gaussian Splat Viewer, which Crate depends on, is under MIT License.

3dgsconverter, a Python command-line utility for converting Splats, which Crate depends on, is under MIT License.

## Crate engines

Crate calls six external engines. A prebuilt bundle is provided so you don't have to compile or configure anything.

These are third-party binaries, redistributed under their own licenses. FFmpeg in this bundle is GPL v3 — source: https://github.com/FFmpeg/FFmpeg/commit/33b215d155 The other engines are permissively licensed (Apache 2.0, BSD).

GPL v3 applies to the FFmpeg binary only. Crate is Apache 2.0 and runs each engine as a separate process. You can also point Crate at your own engine builds via crate_engines.txt.

Crate uses F3D, OpenImageIO, FFmpeg, ImageMagick, MediaInfo, and PlayCanvas SplatTransform as background engines for automatic thumbnail generation, animated previews, metadata extraction, color-managed image processing, 3D geo/splat preview monitoring and Gaussian Splat family format conversion, all on the fly as you browse.

https://github.com/ImageMagick

https://github.com/f3d-app

https://github.com/AcademySoftwareFoundation

https://github.com/pitvfx/OpenImageIO

https://github.com/MediaArea/MediaInfo

https://github.com/FFmpeg

https://github.com/playcanvas/splat-transform

https://nodejs.org/   (Crate JavaScript runtime used by the "splat-transform" engine)

## Credits & Acknowledgments

### Splat

WebGL implementation of a real-time renderer for 3D Gaussian Splatting by antimatter15

[https://github.com/antimatter15/splat](https://github.com/antimatter15/splat)

Used as ply to splat converter

### 3dgsconverter

A versatile, high-performance tool for converting between various 3D Gaussian Splatting formats by Francesco Fugazzi

[https://github.com/francescofugazzi/3dgsconverter](https://github.com/francescofugazzi/3dgsconverter)

Used as splats family types to .ksplat

### Crate Camera Database

Lives on [https://github.com/CrateTools/CrateCamDB](https://github.com/CrateTools/CrateCamDB) and Curators can update from it right from Crate's interface.

Crate's Camera module ships with a reference database of digital cinema, broadcast, drone, mobile, and film camera sensor specifications. This data is derived in part from **[VFXCamDB](https://vfxcamdb.com)** and **[Matchmove machine](https://camdb.matchmovemachine.com/)** 

Crate Camera module would not exist in its current form without those projects. If you find this data useful, please consider [supporting VFXCamDB](https://vfxcamdb.com/donate/) and [supporting Matchmove machine](https://camdb.matchmovemachine.com/donate) directly.

Any inaccuracies in Crate's database are ours, not VFXCamDB's or Matchmove Machine's; corrections are welcome via the issue tracker.

---

#
