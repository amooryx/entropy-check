import math, rclib
def run(ctx):
    try: data = open(ctx.target, "rb").read()
    except OSError as e: ctx.err(str(e)); return 1
    if not data: ctx.warn("empty file"); return 0
    freq = [0]*256
    for b in data: freq[b]+=1
    ent = -sum((c/len(data))*math.log2(c/len(data)) for c in freq if c)
    ctx.info(f"size {len(data)} bytes")
    ctx.info(f"Shannon entropy: {ent:.3f} / 8.0")
    if ent > 7.2:
        ctx.finding("High entropy — likely packed/encrypted/compressed", "medium",
                    detail=f"{ent:.2f} bits/byte")
    elif ent > 6.5:
        ctx.finding("Elevated entropy — possibly obfuscated", "low", detail=f"{ent:.2f}")
    else:
        ctx.good(f"entropy normal for plain data ({ent:.2f})")
    ctx.data["entropy"] = round(ent,4); ctx.data["size"] = len(data)
    return 0
rclib.main("entropy-check", "File Shannon-entropy analysis (packing detection)", run, needs_target=True)
