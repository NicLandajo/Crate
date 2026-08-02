# Organizing Your Libraries Before You Ingest

## One Hour Now, Hundreds Later

Crate will happily browse any folder you point it at. It will generate thumbnails, collapse sequences, and let you search whatever chaos lives on your server. But Crate can only be as clear as the directories underneath it, and the single highest-leverage thing a Curator can do, before installing Crate and exposing a single library to the pipeline, is to spend one focused session organizing those directories by what the assets actually *are*.

This chapter is a recommendation, not a requirement. Crate imposes no folder rules. But every studio that skips this step ends up doing it later, with ten times more files and twenty artists mid-shot.

## The Principle: Typify, Don't Just Store

An asset library is not a backup, it is a menu. Artists don't browse a library to admire your files; they arrive with a need in their head ("I need smoke drifting left, camera-side") and they will find it, or not, in about fifteen seconds before they give up and re-render something that already existed.

The difference between finding and not finding is almost never the asset. It is the folder.

Front Smoke is not the same asset as Side Smoke Rising, Debris Falling is not Exploding Debris. A crackling fireplace loop is not a gas jet. If those distinctions matter to the artist choosing the element, and they always do, they should exist as folders, not as knowledge trapped in one Curator's memory.

## The One-Level Rule

You do not need a taxonomy PhD. Aim for **at least one level of meaningful sub-organization inside each category, and rarely more than two.**

**A flat dump is too little:**

```
Smoke/
    smk_001.exr … smk_412.exr        ← 400 sequences, one folder, zero meaning
```

**This is too much:**

```
Smoke/Exterior/Day/Backlit/Thick/Slow/Left_To_Right/   ← nobody will ever click seven levels deep
```

**This is right:**

```
Smoke/
    Front Smoke/
    Side Smoke Rising/
    Smoke Plumes Distant/
    Wisps and Tendrils/
```

One glance at the tree answers the artist's first question, *what kind?* , and the thumbnails answer the second. Over-nesting hides assets just as effectively as under-nesting; deep trees also mean deeper cache paths and more clicking for everyone, every day, forever.

## Split by the Characteristics That Drive the Choice

Which characteristic earns a folder? The one an artist would actually use to *reject* an asset. Typical examples per element family:

- **Smoke / Fog:** direction and behavior - Front, Side Rising, Rolling, Ambient Haze.
- **Debris:** motion type - Falling, Exploding Outward, Trickling, Ground Impact.
- **Fire:** scale and behavior - Torch, Wall of Flame, Licks, Embers Only.
- **Textures:** surface family - Concrete, Metal Painted, Metal Bare, Fabric.
- **3D objects:** what it is, then variant - Electronics/Motherboard/, Props/Guns/.

Resolution, frame rate, and codec generally do **not** earn folders, Crate's cards and metadata already surface those. Folders are for meaning; metadata is for specs.

## Why This Pays Off Specifically in Crate

Crate rewards a well-typed tree several times over:

1. **The tree is the interface.** Crate's browser shows your directory structure directly. A meaningful tree means artists navigate by intent instead of scrolling a thousand cards.
2. **Search gets sharper.** Crate's filter matches names, and folder discipline naturally produces disciplined file names. "side smoke" finds something only if those words exist somewhere.
3. **Caches stay manageable.** Each library keeps an isolated thumbnail cache. Reorganizing folders *after* ingest means regenerated thumbnails and re-learned locations; organizing first means you generate once.
4. **Curation stays delegable.** Folder colors, Discover branches, and Cart sharing all reference paths. Stable, self-describing paths mean another Curator can maintain the library without a guided tour.
5. **Hidden housekeeping stays hidden.** Anything prefixed with `.` or `_` is invisible to artists (see *crate_hide_prefixes.txt*), so keep your WIP and staging folders prefixed and your public tree purely meaningful.

## A Curator's Pre-Ingest Checklist

Before pointing a new library at Crate:

1. List the 5–15 categories the library really contains.
2. Inside each, split once by the characteristic artists choose by.
3. Name folders in plain, searchable words — "Side Smoke Rising", not "smk_sd_r_v2".
4. Prefix anything artists shouldn't see with `_` or `.`.
5. Only then add the library in **Settings → Libraries** and let Crate build its cache.

The first time an artist finds *Side Smoke Rising* in eight seconds instead of asking in the channel, re-rendering, or settling for *Front Smoke* flipped and hoping - this chapter has paid for itself. It will keep paying every day the library exists.
