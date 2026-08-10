---
name: release-marketplace
description: Prepares and publishes a hidden IntelliJ plugin release through this project's GitHub Actions workflows. Use when asked to release, publish, or upload a new Black Metal Themes version to JetBrains Marketplace.
compatibility: Requires git, GitHub CLI authentication, Python 3, Java 21, and the PUBLISH_TOKEN GitHub Actions secret.
---

# Release Black Metal Themes

Publish through the existing GitHub Build and Release workflows. The first Marketplace version must already have been uploaded manually and approved.

Invoke with `/skill:release-marketplace patch`, `minor`, `major`, or an explicit `X.Y.Z` version. If omitted, ask which increment to use.

## Safety

- Keep Marketplace uploads hidden. Confirm `build.gradle.kts` contains `publishing { hidden = true }`.
- Never display, download, or otherwise expose `PUBLISH_TOKEN`.
- Do not require signing secrets. This project deliberately publishes unsigned builds.
- Never force-push, rewrite history, publish from a non-`main` branch, or reuse a Marketplace version.
- Push only to Codeberg. GitHub is a mirror and must receive the identical commit before its workflows are used.
- Before including pre-existing changes, show them and obtain confirmation. Never discard them.
- Publishing the GitHub draft triggers the Marketplace upload. Obtain explicit confirmation immediately before that action.

## 1. Preflight

From the repository root, run:

```sh
git branch --show-current
git status --short
git remote get-url origin
git fetch origin main
git rev-list --left-right --count origin/main...main
gh auth status
gh api repos/STBoyden/intellij-black-metal-themes --jq '.full_name'
gh secret list --repo STBoyden/intellij-black-metal-themes --app actions | grep '^PUBLISH_TOKEN\b'
```

Require:

- branch `main`;
- `origin` is the Codeberg repository;
- no unreviewed changes;
- local `main` is not behind `origin/main`;
- GitHub CLI authentication and mirror access work;
- the repository Actions secrets list contains `PUBLISH_TOKEN`;
- `.github/workflows/build.yml` and `.github/workflows/release.yml` exist;
- `build.gradle.kts` sets Marketplace publishing to hidden.

If the first manual Marketplace upload and approval cannot be established from context, ask the user.

## 2. Choose and set version

Read `version` from `gradle.properties`. It must use `X.Y.Z` numeric semantic versioning.

For `patch`, `minor`, or `major`, calculate the next version normally. For an explicit version, require it to be greater than the current version. Do not add a `v` prefix because the workflows use the exact Gradle version as the GitHub tag.

Ensure `CHANGELOG.md` has meaningful entries under `## [Unreleased]`, then update only the `version = ...` line in `gradle.properties`.

Move those entries into the selected version before committing:

```sh
./gradlew patchChangelog
```

Require `CHANGELOG.md` to contain `## [<X.Y.Z>]` with the intended entries and a fresh `## [Unreleased]` section. The Build workflow reads the selected version section for the draft release and Marketplace change notes. This keeps all changelog commits on Codeberg rather than creating branches on the GitHub mirror.

## 3. Generate and verify

Run:

```sh
python3 scripts/generate_themes.py
./gradlew clean check buildPlugin verifyPlugin
git diff --check
```

Inspect the resulting diff and confirm generated theme files are internally consistent. Stop on any failure.

## 4. Commit and push

Stage only the reviewed release changes. Commit using:

```text
chore(release): prepare <X.Y.Z>
```

Then push to Codeberg:

```sh
git push origin main
```

Record the pushed commit SHA:

```sh
SOURCE_SHA=$(git rev-parse HEAD)
```

## 5. Await the GitHub mirror

Do not inspect or run GitHub workflows until the Codeberg-to-GitHub mirror contains the exact pushed commit. Poll the GitHub `main` SHA for up to ten minutes:

```sh
deadline=$((SECONDS + 600))
while true; do
  MIRROR_SHA=$(gh api repos/STBoyden/intellij-black-metal-themes/commits/main --jq '.sha' 2>/dev/null || true)
  if [ "$MIRROR_SHA" = "$SOURCE_SHA" ]; then
    printf 'GitHub mirror reached %s\n' "$SOURCE_SHA"
    break
  fi
  if [ "$SECONDS" -ge "$deadline" ]; then
    printf 'Timed out waiting for GitHub mirror; expected %s, found %s\n' "$SOURCE_SHA" "$MIRROR_SHA" >&2
    exit 1
  fi
  sleep 15
done
```

Require exact SHA equality. If the API fails or the deadline expires, stop and report the mismatch. Never continue with an older GitHub commit or trigger a workflow manually to bypass the mirror.

## 6. Await the Build workflow

Find the Build run for the mirrored SHA, then watch it:

```sh
gh run list --repo STBoyden/intellij-black-metal-themes \
  --workflow Build --branch main --limit 10 \
  --json databaseId,headSha,status,conclusion,url

gh run watch --repo STBoyden/intellij-black-metal-themes <run-id> --exit-status
```

Select only the run whose `headSha` equals the recorded SHA. On failure, inspect it with:

```sh
gh run view --repo STBoyden/intellij-black-metal-themes <run-id> --log-failed
```

Do not publish a release after a failed build.

## 7. Review the draft

The successful Build workflow creates a draft release tagged with the exact version. Verify it:

```sh
gh release view --repo STBoyden/intellij-black-metal-themes <X.Y.Z> \
  --json tagName,name,isDraft,body,url
```

Require `isDraft` to be `true`. Show the tag, release notes, and URL. Ask the user to confirm publication. Clearly state that confirmation triggers the hidden JetBrains Marketplace upload.

## 8. Publish and monitor

After explicit confirmation:

```sh
gh release edit --repo STBoyden/intellij-black-metal-themes <X.Y.Z> --draft=false
```

Find the new Release workflow run and watch it:

```sh
gh run list --repo STBoyden/intellij-black-metal-themes \
  --workflow Release --limit 10 \
  --json databaseId,event,status,conclusion,url,createdAt

gh run watch --repo STBoyden/intellij-black-metal-themes <run-id> --exit-status
```

Use the run created by the release publication, not an older run. If GitHub has not listed it yet, report that state rather than selecting an unrelated run.

On failure, inspect `gh run view --repo STBoyden/intellij-black-metal-themes <run-id> --log-failed`. Do not create another version automatically.

## 9. Report

Report concisely:

- released version and commit SHA;
- successful Codeberg-to-GitHub mirror confirmation;
- GitHub release URL;
- Build and Release workflow conclusions;
- whether Marketplace upload succeeded;
- that hidden Marketplace updates remain subject to JetBrains review.
