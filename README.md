# Task Tracker — a tiny app with a real CI/CD pipeline

This is a small Flask web app built to teach CI/CD. The app itself is simple;
the point is the pipeline that tests it, builds it, and publishes it
automatically every time you push code.

The whole pipeline runs on **just a GitHub account** — no paid hosting and no
extra sign-ups required.

## What's in here

```
task-tracker/
├── app.py                     # Flask web layer (routes + in-memory store)
├── logic.py                   # pure business logic — the part we unit test
├── templates/index.html       # the web page you see in the browser
├── tests/test_logic.py         # automated tests (run by the pipeline)
├── requirements.txt            # Python dependencies
├── Dockerfile                  # recipe to build the app into a container image
├── pyproject.toml              # config for the linter (ruff)
└── .github/workflows/ci.yml    # THE PIPELINE
```

## How the pipeline maps to the stages you learned

| Stage        | Where it happens                                              |
|--------------|--------------------------------------------------------------|
| 1. Commit    | You `git push` to GitHub — this triggers the workflow        |
| 2. Build     | `pip install` sets up the app; the Docker image is built     |
| 3. Test      | `ruff check` (lint) and `pytest` (tests) run automatically   |
| 4. Release   | The image is tagged (`:latest` and the commit hash)          |
| 5. Deploy    | The image is pushed to GitHub Container Registry (ghcr.io)   |
| 6. Monitor   | GitHub's Actions tab shows every run, green or red           |

The key rule: **`build-and-push` has `needs: test`**, so if the tests fail,
nothing gets built or published. That is CI/CD's core promise — broken code
never moves forward.

## Run it on your own computer first

You need Python 3.12+ installed.

```bash
# from inside the task-tracker folder
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open http://localhost:8000 in your browser. Add a few tasks, mark them done.

Run the tests the same way the pipeline will:

```bash
pip install ruff pytest
ruff check .
pytest -v
```

Try breaking a test on purpose (change an expected value in
`tests/test_logic.py`) and run `pytest` again to watch it fail. That red
failure is exactly what will stop the pipeline later.

## Put it on GitHub and watch the pipeline run

1. Create a **new repository** on GitHub (name it anything, keep it public to
   start — that keeps everything free and simple).
2. In the task-tracker folder, connect it and push:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: task tracker + CI/CD pipeline"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
   git push -u origin main
   ```

3. On GitHub, open the **Actions** tab. You'll see your pipeline running.
   Click into it to watch each step live. When it finishes, both jobs turn
   green.
4. The published container image appears under your profile's **Packages**
   (also linked from the repo's right sidebar).

That's a complete CI/CD loop: push → test → build → publish, all automatic.

## Make a change and see it flow through

- Edit something (add a test, change the page title in `templates/index.html`).
- Commit and push.
- Watch the Actions tab run the whole pipeline again on its own.

Open a pull request instead of pushing to main, and notice the tests still
run — but the build/publish job is skipped, because that job only runs on
pushes to `main`. That's a common real-world setup: test everything, but only
ship from the main branch.

## Where to go next

The pipeline currently *publishes* a runnable image but doesn't run it on a
public server. To get a live URL, add a deploy step targeting a free host such
as Render, Railway, or Fly.io. Each gives you a secret token you store under
the repo's **Settings → Secrets and variables → Actions**, then reference in
the workflow. Deployment strategies like blue-green and canary build on top of
this same foundation.