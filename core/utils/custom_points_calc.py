def compute_custom_points(del_count, add_count):
    """
    真实测量点位数量计算逻辑
    d > a → 真删双侧点位
    d ≤ a → 是否隐藏最后一个点位取决于奇偶
    """
    base = 21
    d = del_count
    a = add_count

    if d <= a:  # 删除次数不超过添加次数
        diff = a - d
        return 21 if diff % 2 == 0 else 20

    # 真正删除上方双侧点位
    removed_pairs = d - a
    final = base - removed_pairs * 2
    return max(final, 1)


def split_points_for_values(total_points: int):
    """
    按最新规则拆分 values:
    - 奇数：ceil & floor → 后者+1 → N+1
    - 偶数：N/2 & N/2 → 后者+1 → N+1
    """
    N = int(total_points)
    first = (N + 1) // 2
    second = (N // 2) + 1
    return first, second