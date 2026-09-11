Qarro FIRST PLAYABLE

Current development line: v3.4 Kanto encounter diversity + Russian localization foundation.

Runtime policy:
- Gen I-V only.
- No ordinary-wild starters or Legendary/Mythical species before postgame.
- Kanto keeps a strong local Gen I identity while Gen II-V species are distributed biome-by-biome across FireRed land encounters.
- New visible ground items start after Viridian City and use standard FireRed pickup behavior.
- Pokemon, move and ability names remain English; Russian localization is applied to UI/system/dialogue layers incrementally.
- Ash Bond / Ash Cap remain outside FIRST PLAYABLE.

Zone-completion workflow:
- Work one coherent gameplay area/block at a time.
- In the same pass, complete both required content/mechanics fixes and all remaining user-facing Russian localization for that area.
- Pokemon, Move and Ability names remain English; all other intended user-facing text is Russian.
- Localization changes must use exact fail-closed source anchors and must not touch Ash Bond / Ash Cap.
- Do not advance to the next gameplay area until the current area passes the full FireRed build (`make firered`) and regression/integrity checks.
- When earlier untranslated gaps are discovered, close them from the beginning of progression forward before extending localization farther ahead.
