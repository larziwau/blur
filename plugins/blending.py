from vapoursynth import core
import vapoursynth as vs

def average(clip: vs.VideoNode, weights: list[float], divisor: float | None = None) -> vs.VideoNode:
    def get_offset_clip(offset: int) -> vs.VideoNode:
        if offset > 0:
            return clip[0] * offset + clip[:-offset]
        elif offset < 0:
            return clip[-offset:] + clip[-1] * (-offset)
        else:
            return clip

    diameter = len(weights)
    radius = diameter // 2

    if divisor is None:
        divisor = sum(weights)

    assert diameter % 2 == 1, "An odd number of weights is required."

    clips = [get_offset_clip(offset) for offset in range(-radius, radius + 1)]

    expr = ""
    expr_vars = [f"src{i}" for i in range(1024)]

    for var, weight in zip(expr_vars[:diameter], weights):
        expr += f"{var} {weight} * "

    expr += "+ " * (diameter - 1)
    expr += f"{divisor} /" if divisor != 1 else ""

    clip = core.akarin.Expr(clips, expr)

    return clip
