# CI-only Logen (dual checkout)

Use this layout when **Logen is not** vendored or submodule’d inside your app repo. The workflow checks out your **app** repo, then checks out **this (Logen) repo** into `_logen/`, runs `logen2.py`, and commits only localization files.

## Copy into your app repository

1. Copy [`regenerate-localizations.yml`](regenerate-localizations.yml) to **`.github/workflows/regenerate-localizations.yml`** in the **app** repo.
2. Edit the file:
   - **`repository:`** — your public Logen slug (e.g. `GoodRequest/Logen`).
   - **`ref:`** — branch, tag, or SHA (pin a tag for reproducibility).
   - **`python3` line** — path is **`_logen/Logen/logen2.py`** if the Logen repo root contains a `Logen/` directory with the script (matches this repository’s layout).
   - **`--project`**, **`--sheet`**, **`--last_column`**, **`--first_row`**, and **`git add`** paths — match your Xcode project.
   - Main strings and `InfoPlist` are generated in the same workflow job by two Logen invocations.
   - Optional flavour-specific overrides are passed through the `overlay_sheet` workflow input and map to Logen `--overlay_sheet`.
3. Append the contents of [`APP_REPO_DOTGITIGNORE`](APP_REPO_DOTGITIGNORE) to the app repo’s **`.gitignore`** so `_logen/` is never staged.
4. On the **app** repo: **Settings → Secrets and variables → Actions** → create **`LOGEN_SA_JSON`** (full service account JSON). Optionally add variable **`LOGEN_SHEET_ID`** for `--id`.

## Workflow inputs

- **`overlay_sheet`** — optional tab name for flavour-specific overrides. Leave empty to generate from the base sheet only.

## Private Logen

If Logen is private, add `token:` to the Logen checkout step (PAT with `contents: read` on the Logen repo), stored as an app-repo secret.
