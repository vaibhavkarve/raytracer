list:
    @just --list


typecheck:
    uv run mypy -m raytracer
    uv run pyright

run:
    uv run -m raytracer.main | display
