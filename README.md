# TOEFL Typing Practice App

TOEFL Typing Practice App is a Python desktop application for practicing English input accuracy in TOEFL-style writing situations.

The project is designed around one simple idea: every practice session should feel fresh, while still training the specific weak points that matter most for TOEFL preparation.

## What This App Is For

This app focuses on two core skills:

1. Essay typing accuracy for TOEFL writing tasks.
2. Vocabulary spelling accuracy for word-level recall and input precision.

It is not just a fixed typing drill. The app is intended to generate practice content dynamically, recycle user mistakes intelligently, and support timed challenges so that practice stays useful over time.

## Core Practice Modes

### 1. Essay Typing Mode

This mode is for long-form English input practice.

Main training goals:

- Correct spelling
- Correct punctuation
- Correct capitalization
- Fewer missing or extra characters
- Better stability on long sentences and paragraph-like content

This mode is meant to resemble the typing pressure a learner faces when writing TOEFL essays.

### 2. Vocabulary Spelling Mode

This mode is for single-word or short-answer spelling practice.

Supported prompt styles:

- Chinese meaning to English word
- English definition to word
- Sentence cloze completion
- Word-root or prefix/suffix hints

This mode helps learners strengthen spelling recall before those mistakes show up in writing.

### 3. Timed Challenge Mode

This is a sub-mode inside Essay Typing Mode.

It is designed for time-limited performance practice:

- Type as much content as possible within a fixed time
- Or complete as many entries as possible within the time limit
- Keep accuracy high while increasing speed

This mode is meant to train pressure handling, not just raw typing speed.

## Content Strategy

The app is designed to focus on TOEFL-relevant content instead of random typing text.

Planned content sources include:

- Email-style situations
- Academic discussion content
- TOEFL high-frequency vocabulary
- Common TOEFL writing expressions
- Punctuation-heavy and long-sentence patterns

The long-term goal is to let the app generate varied practice content from these sources instead of relying on fixed passages.

## Design Principles

The project follows these principles:

- Practice content should vary from session to session.
- Practice generation should be constrained, not purely random.
- User mistakes should come back later in a controlled way.
- Difficulty should be layered and adjustable.
- The app should grow stage by stage instead of trying to solve everything at once.

## Current Status

This repository is still in the early implementation stage.

Completed so far:

- Project goals and scope definition
- Local implementation guide
- Stage-based development plan
- Repository changelog
- Stage 1 application skeleton
- Basic Python package structure

## Development Stages

The implementation plan is intentionally split into stages to keep the work manageable.

Current stage plan:

1. Stage 0: Project skeleton confirmation
2. Stage 1: Core framework setup
3. Stage 2: Essay typing mode
4. Stage 3: Vocabulary spelling mode
5. Stage 4: Timed challenge mode
6. Stage 5: Personalization and mistake review
7. Stage 6: Statistics and UX polish

The detailed stage rules live in the local implementation guide.

## Local Implementation Guide

The repository includes a local-only implementation guide that drives the actual build process:

- [LOCAL_IMPLEMENTATION_GUIDE.md](LOCAL_IMPLEMENTATION_GUIDE.md)

This file is intended for local development workflow and should not be treated as the public-facing project description.

## Project Structure

The current codebase uses a `src` layout:

- `pyproject.toml` for project metadata and packaging
- `src/toefl_typing_practice_app/` for the Python package
- `src/toefl_typing_practice_app/app.py` for application bootstrap
- `src/toefl_typing_practice_app/ui/` for UI components
- `project_change_log.md` for repository-level change tracking

## Requirements

Planned minimum environment:

- Python 3.11 or newer
- A desktop environment capable of running Tkinter-based applications

The UI layer currently uses Tkinter for the initial skeleton because it is lightweight and built into standard Python distributions.

## Running the App

At the moment the project is still a skeleton, but the intended launch command is:

```bash
python -m toefl_typing_practice_app
```

Or, once packaging is finalized:

```bash
toefl-typing-practice
```

## What Will Be Added Next

Planned next steps include:

- Real essay typing practice flow
- Dynamic practice content generation
- Vocabulary spelling questions
- Timed challenge flow
- Mistake tracking and review logic
- Session statistics and practice history

## Contributing During Development

This project is being developed in stages. When adding or changing functionality:

1. Check the local implementation guide first.
2. Keep changes aligned with the current stage.
3. Record key changes in `project_change_log.md`.
4. Keep code comments clear and explanatory.

## Repository Notes

This README is the public-facing introduction to the project.

The more detailed build instructions live in the local implementation guide so that development can stay consistent without overloading the public README with implementation details.

