list:
    @just --list


typecheck:
    uv run mypy -m raytracer
    uv run pyright

run:
    uv run -m raytracer.main | display

profile:
    LINE_PROFILE=1 uv run -m raytracer.main
    uv run -m line_profiler -rmtz profile_output.lprof


debug:
    uv run -m pdbp -m raytracer.main
