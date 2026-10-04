# Ketobiotic Kitchen

Source for the Ketobiotic Kitchen recipe collection, published as a Claude Artifact:
https://claude.ai/artifact/USwemok6GDk5DZ5nGyaAdX

The artifact is a single self-contained HTML page listing 62 ketobiotic recipes,
with search and filtering, a shopping-list builder, a pantry list, a meal
calendar, editable recipe categories, and a "tried it" tracker with notes and
photos.

## Files

- `recipes-source.json` — the raw recipe data (name, ingredients, steps,
  nutrition) that the original 60 recipes were scraped from. Needed once by
  `build.py`; it is not touched after that.
- `build.py` — reads `recipes-source.json`, cleans and annotates the data
  (categorizes each recipe, converts Fahrenheit to Celsius, adds
  gluten-cross-contamination notes), appends two additional recipes that were
  added by hand later (Steak Salad with Baked Tomatoes and Tarragon Dressing;
  Butter Chicken with Oat Rice), and injects the resulting JSON array into
  `template.html` to produce `ketobiotic-recipes.html`.
- `template.html` — the actual page: all markup, styles and JavaScript, with
  a `/*DATA*/[]` placeholder where `build.py` inserts the recipe data. This is
  the file to edit for any UI or behavior change.
- `ketobiotic-recipes.html` — the generated, ready-to-publish page. Not
  committed (see `.gitignore`); regenerate it with the build command below.

## Building

```
python3 build.py
```

This writes `ketobiotic-recipes.html` in the current directory and prints the
recipe count (62) as a sanity check.

## Publishing

The generated file is published as a Claude Artifact (not a plain static
site) because the page uses two runtime capabilities:

- `db` — shared, persistent storage for the shopping list, pantry, meal
  calendar, category overrides and the tried/notes/photos tracker.
- `assets` — photo uploads for the tried-recipe tracker.

Because `assets` is declared, the artifact is organization-internal: it
cannot be shared via a public link, only with specific invited people.

To publish a new version after editing `template.html`:

1. Run `python3 build.py`.
2. Publish `ketobiotic-recipes.html` to the existing artifact URL above, with
   `capabilities: {"db": {}, "assets": {}}`. Omitting `capabilities` on a
   republish carries the existing declaration forward; passing it explicitly
   is only needed if the capability set is changing.

## Adding a recipe

Append a new entry to the `out` list near the bottom of `build.py`, following
the shape of the two hand-added recipes already there (`id`, `name`, `veg`,
`yield_`, `serving`, `src`, `srcname`, `ing`, `steps`, `cat`, `f`/`c`/`p`
macros, `gl` gluten notes), then rebuild.
