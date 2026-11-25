# .claude

Claude Code discovers skills in `.claude/skills/`. The actual skill definitions live in
[`.github/skills/`](../.github/skills) (shared with GitHub Copilot), so `.claude/skills`
is a local link to that folder — do not add real files here.

The link itself is git-ignored (Windows junctions/symlinks can't be committed reliably).
Recreate it after cloning:

- **Windows (no admin needed, junction):**
  ```powershell
  New-Item -ItemType Junction -Path .claude\skills -Target (Resolve-Path .github\skills)
  ```
- **macOS / Linux (or Windows with Developer Mode):**
  ```bash
  ln -s ../.github/skills .claude/skills
  ```

Verify with `ls .claude/skills` — you should see `mtb-tools`, `mtb-debug-workflow`, etc.
