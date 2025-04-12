def format_gold_into_k_notation(gold: int) -> str:
    """
    Format a gold amount into a k notation string.
    """
    if gold < 1000:
        return f"{gold}gp"
    return f"{gold / 1000:.1f}k gp"


def format_gold_into_pp_gp_sp_cp_notation(gold: int) -> str:
    """
    Format a gold amount into a pp, gp, sp, cp notation string.
    """
    total_cp = int(gold * 100)
    pp = total_cp // 1000
    gp = (total_cp % 1000) // 100
    sp = (total_cp % 100) // 10
    cp = total_cp % 10

    parts = []
    if pp > 0:
        parts.append(f"{pp}pp")
    if gp > 0:
        parts.append(f"{gp}gp")
    if sp > 0:
        parts.append(f"{sp}sp")
    if cp > 0:
        parts.append(f"{cp}cp")

    return " ".join(parts)


def format_bab_into_multiattack(bab: int) -> str:
    """
    Format a Base Attack Bonus into a multiattack notation string.
    """
    bonuses = []
    while bab >= 1:
        bonuses.append(f"+{bab}")
        bab -= 5
    return "/".join(bonuses)
