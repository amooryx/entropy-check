import math

import rclib


def measure_file(path):
    """Return (byte_count, Shannon entropy in bits per byte) using bounded memory."""
    frequencies = [0] * 256
    size = 0
    with open(path, "rb") as source:
        while True:
            chunk = source.read(64 * 1024)
            if not chunk:
                break
            size += len(chunk)
            for byte in chunk:
                frequencies[byte] += 1

    if not size:
        return 0, 0.0

    entropy = -sum(
        (count / size) * math.log2(count / size)
        for count in frequencies
        if count
    )
    return size, entropy


def run(ctx):
    try:
        size, ent = measure_file(ctx.target)
    except OSError as e:
        ctx.err(str(e))
        return 1

    ctx.data["entropy"] = round(ent, 4)
    ctx.data["size"] = size
    if not size:
        ctx.warn("empty file; entropy is undefined for an empty sample")
        return 0

    ctx.info(f"size {size} bytes")
    ctx.info(f"Shannon entropy: {ent:.3f} / 8.0")
    if ent > 7.2:
        ctx.finding("High byte entropy — consistent with packed, encrypted, or compressed data",
                    "medium", detail=f"{ent:.2f} bits/byte; heuristic only")
    elif ent > 6.5:
        ctx.finding("Elevated byte entropy — possibly obfuscated", "low",
                    detail=f"{ent:.2f} bits/byte; heuristic only")
    else:
        ctx.good(
            f"byte entropy is not elevated ({ent:.2f}); "
            "this does not establish that data is plain"
        )
    return 0


if __name__ == "__main__":
    rclib.main("entropy-check", "File Shannon-entropy analysis (packing heuristic)", run,
               needs_target=True)
