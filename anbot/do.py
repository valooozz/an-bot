from game_types.game_types import GroupPosition, Sticks

def take_whole_group(groupToTake: GroupPosition, sticks: Sticks):
    group_index, group_length = groupToTake
    i = 0
    n = len(sticks)
    # Find the start index of the group_index-th group of True sticks
    group_start = None
    group_counter = 0
    while i < n:
        if sticks[i]:
            # Found a group
            if group_counter == group_index:
                group_start = i
                break
            # Skip this group
            while i < n and sticks[i]:
                i += 1
            group_counter += 1
        else:
            i += 1
    if group_start is None:
        raise ValueError("Group index out of range")
    # Remove the sticks in the group
    for j in range(group_start, group_start + group_length):
        sticks[j] = False