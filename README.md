# Black Metal Themes for IntelliJ

Dark themes for IntelliJ-based IDEs, ported
from [Black Metal for Zed](https://codeberg.org/STBoyden/zed-black-metal-themes).

## Variants

- Black Metal
- Bathory
- Burzum
- Dark Funeral
- Gorgoroth
- Immortal
- Khold
- Marduk
- Mayhem
- Nile
- Venom

Each variant uses the IntelliJ 2026.2 Islands UI and includes matching UI, editor, console, and terminal colours.
IntelliJ's native icons are retained and recoloured to the selected palette, preserving familiar file and action symbols.

IntelliJ Platform 2026.2 or newer is required. Zed's Transparent and Blurred modes are omitted because IntelliJ does not
support equivalent window effects. These themes port each Opaque palette.

## Installation

Build the plugin:

```sh
./gradlew buildPlugin
```

Then select **Settings > Plugins > ⚙ > Install Plugin from Disk** and open the ZIP from `build/distributions`.

Choose a theme under **Settings > Appearance & Behaviour > Appearance**.

## Development

Palette data and mappings live in [`scripts/generate_themes.py`](scripts/generate_themes.py). Regenerate all checked-in
resources with:

```sh
python3 scripts/generate_themes.py
```

Run a development IDE with:

```sh
./gradlew runIde
```

## Attribution

The palettes come from the Black Metal terminal schemes distributed with [Ghostty](https://ghostty.org/) and are adapted
from the matching Zed extension. Native IntelliJ icons remain JetBrains assets and are recoloured through IntelliJ's
theme API rather than redistributed.
