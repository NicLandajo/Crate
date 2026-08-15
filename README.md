<img width="1009" height="201" alt="cratelogo" src="https://github.com/user-attachments/assets/37514f9a-b08d-40eb-8cd1-fba917e85e9d" />

# CRATE 2 - Not released yet

<h3 style="font-size: 30em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  Building your Crate - 3 Steps Quick Install
</h3>

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
    └── OpenImageIO/
    └── splat-transform/ 
    </pre>

<p>For Windows, the path <code>C:\Users\Public\Crate Image Engines</code> is highly recommended.</p>

<blockquote>
<strong>Important Security Note:</strong> If you choose to install this in a different directory, please ensure your operating system permissions, antivirus, or security software do not block Nuke from accessing this folder. Restrictive environments may prevent the tools and plugins from executing correctly.
</blockquote>

<blockquote>
<strong>Important Security Note:</strong> Platform Support: Crate has been primarily developed and tested on Windows 10 22H2. It should work on Windows 11, macOS, and Linux, but we cannot guarantee fully smooth functionality on these platforms yet. Some tweaking may be required, especially regarding file permissions and executable flags on macOS and Linux.
</blockquote>

<blockquote>
<strong>OS Permissions:</strong> To run the application properly with read + write + execute permissions as a normal user, place the files in the shared folder for your operating system, talk to your admin or find the way for your OS admin to give this permissions so Crate can operate normally from Nuke.
</blockquote>


<h3 style="font-size: 1.5em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  3) Download Crate release and connect to pipeline
</h3>


3.1. Download Crate release. Place the crate_2.0.0 folder on a network location every Nuke workstation can read, e.g. \\YourServer\pipeline\nuke\crate_2.0.0.

3.2. Register it in Nuke. Add this line to your studio's init.py:

     nuke.pluginAddPath("\\\\YourServer\\pipeline\\nuke\\crate_2.0.0")

3.3. Launch Nuke and claim your install. On first launch, Crate detects that no Curators exist yet and shows a "Welcome to Crate" dialog. If you are the asset manager or pipeline lead, press Claim as Curator, this registers your username with full         access.

3.4. Prepare Crate while it's locked. Claiming automatically locks Crate for all users, so you can set it up safely before it´s used. Open Crate from Nuke's menu and configure everything from Settings: start with connecting Crate Engines by pointing       the paths to the location where you placed them.

3.5. Set up at least one library. You must do this first so that the subsequent use of Crate proceeds smoothly as it comes to life.
     Cache tip: Give each library its own dedicated cache folder named after the library (e.g. Crate Caches/Libraries/Smoke)

3.6. Although Crate is intuitive, we recommend reading the user manual at this point; click on Settings/User Manual. It should be noted that this manual is primarily aimed at Curators, Pipe TDs, IT staff, and the like, rather than the casual user (such as a compositing artist who quickly opens Crate to grab an element and leave, The Visitor). We will cover the use of Crate for Visitors in future video tutorials, but the interface is very simple, and all users will be able to use it immediately without needing any introduction.

3.7. Continue to setup Crate modules and all the settings.

3.8. Try out Crate's locked mode for a few days to ensure everything works as expected.

3.9. Unlock and go live. When configuration is done, release the lock from Settings. Crate is now live for the whole pipeline: Curators manage content, everyone else browses as Visitors.
    Crate will now handle everything automatically, adding users to its database as they use it for the first time. Over the coming days and weeks, Crate’s charts and analytics will provide
    feedback on how everything is performing and whether any adjustments are needed.

# ABOUT CRATE

It´s the first 3D browser for Nuke that generates thumbnails from gaussian splats and geometry automatically for you without intervention.

We´re are working to build a first long term solid foundation and allow users to update their Crate versions easily in the future.

Crate 2 is a major update both for it´s interface, functions, engines and code. It works very different compared to V1, a clean install is needed.

It´s compatible with PySide2 to PySide6 across Nuke 15 16 17, however, the full potential and features of Crate 2 and all its exhaustive testing has been done in Nuke 17 vith a focus on the future.

New studio professional tools, Curators vs Visitors access, user read and write privileges, user interface privileges according to role. 

Library objects vs storage tiers it allows to have the thumbnails and animated previews on a separate cache. You might choose to locate the cache over ssd/nvme disk and the raw elements on an array or high capacity disks.

## Licenses

Crate is under Apache License.

F3D, which Crate depends on, is licensed under the BSD 3-Clause License.

ImageMagik, which Crate depends on, is licensed under the ImageMagick License (the "License").

FFmpeg, which Crate depends on, is LGPL-2.1+ at its core; the build included in the Crate Image Engines bundle is a gyan.dev full build, licensed GPL v3 (see the README and license inside the bundle).

MediaInfo, which Crate depends on, is under the BSD 2-Clause License

OpenImageIO, which Crate depends on, is under the Apache-2.0 License
(project: https://github.com/AcademySoftwareFoundation/OpenImageIO).
The Windows binaries in the Crate Image Engines bundle are a community
build (https://github.com/pitvfx/OpenImageIO), since ASWF does not
publish official Windows binaries. The build bundles third-party
components (Qt 6 under LGPL-3.0, Python under PSF, and others) under
their own licenses — see the licensing note included alongside the
engines bundle.

Playcanvas SplatTransform - 3D Gaussian Splat Converter, which Crate depends on, is under MIT License.

Splat , WebGL 3D Gaussian Splat Viewer, which Crate depends on, is under MIT License.

3dgsconverter, a Python command-line utility for converting Splats, which Crate depends on, is under MIT License.

## Crate engines

Crate uses F3D, OpenImageIO, FFmpeg, ImageMagick, MediaInfo, and PlayCanvas SplatTransform as background engines for automatic thumbnail generation, animated previews, metadata extraction, color-managed image processing, 3D geo/splat preview monitoring and Gaussian Splat family format conversion — all on the fly as you browse.

The engines will continue to allow Crate to grow into new and more professional features, many of them already on new Crate 2

https://github.com/ImageMagick

https://github.com/f3d-app

https://github.com/AcademySoftwareFoundation

https://github.com/pitvfx/OpenImageIO

https://github.com/MediaArea/MediaInfo

https://github.com/FFmpeg

https://github.com/playcanvas/splat-transform

https://nodejs.org/   (Crate JavaScript runtime used by the "splat-transform" engine)

## Credits & Acknowledgments

<h3 style="font-size: 30em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  Splat
</h3>

WebGL implementation of a real-time renderer for 3D Gaussian Splatting by antimatter15

[https://github.com/antimatter15/splat](https://github.com/antimatter15/splat)

Used as ply to splat converter

<h3 style="font-size: 30em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  3dgsconverter
</h3>

A versatile, high-performance tool for converting between various 3D Gaussian Splatting formats by Francesco Fugazzi

[https://github.com/francescofugazzi/3dgsconverter](https://github.com/francescofugazzi/3dgsconverter)

Used as splats family types to .ksplat

<h3 style="font-size: 30em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  Crate Camera Database
</h3>

Lives on [https://github.com/CrateTools/CrateCamDB](https://github.com/CrateTools/CrateCamDB) and Curators can update from it right from Crate´s interface.

Crate's Camera module ships with a reference database of digital cinema, broadcast, drone, mobile, and film camera sensor specifications. This data is derived in part from **[VFXCamDB](https://vfxcamdb.com)** maintained by **Tony D'Agostino** and **[Matchmove machine](https://camdb.matchmovemachine.com/)** maintained by **Matchmove machine**.

We are genuinely grateful and the Camera module would not exist in its current form without Tony D'Agostino and Matchmove machine work. If you find this data useful, please consider [supporting VFXCamDB](https://vfxcamdb.com/donate/) and [supporting Matchmove machine](https://camdb.matchmovemachine.com/donate) directly.

Any inaccuracies in Crate's database are ours, not Vfx Camera Database and Matchmove machine; corrections are welcome via the issue tracker, and significant ones will be reported back to the mentioned parent databases.

<h3 style="font-size: 30em; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 8px; margin-bottom: 15px;">
  Recommended sites to download Gaussians splat for tests
</h3>

https://superspl.at/

## Known Issue — Occasional Nuke crashes during asset import

Crate v2.0.0 may experience occasional Nuke crashes when importing assets into the node graph. The crash is an access violation inside Nuke's own node engine (DDImage.dll) that affects approximately 4% of import operations across both Nuke 16 and 17. It is not caused by Crate — the same files open without issue through Nuke's own File → Read menu. Any user who imports assets (double-click, right-click → Import, or drag into DAG) can encounter it, though in practice Curators see it more often because library building and curation involve far more imports per session than typical browsing. If you experience a crash, simply relaunch Nuke and continue working; no project data is lost. Save your Nuke scripts frequently during heavy import sessions. This issue has been reported to Foundry with crash dumps from both Nuke 16 and 17 and is tracked under their internal bug ID 616942. A future Nuke point release is expected to resolve it.

Solutions are welcome on the ticket section

#

Questions - Learning - Deployment: Nic Landajo - nicolas.landajo@gmail.com
