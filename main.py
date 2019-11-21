import time
import pandas as pd


with open("data.csv", "r") as f:
    headers = f.readline().replace("\n", "").split(",")
    vs = [l.replace("\n", "").split(",") for l in f.readlines()]

m = len(vs[0]) - 1
vs = [(v[m], tuple(v[:m])) for v in vs]

v_start = ("First dance", ("", "", "", "BS", "JI"))
v_end = ("End", ("", "", "", "", ""))


def cost(v1, v2):
    """The cost of going from v1 to v2

    This is the number of people which need to be found to come up and play a
    song

    """
    assert v2 != v_start
    assert v1 != v_end

    _, s1 = v1
    _, s2 = v2
    s1 = set(s1) - {""}
    s2 = set(s2) - {""}

    # Charge loads if Heidi and Joe are playing after the first dance, or in
    # the last song
    if v1 == v_start and ("JW" in s2 or "HN" in s2):
        return 100
    if v2 == v_end and ("JW" in s1 or "HN" in s1):
        return 100

    return len(s2 - s1)


def key(s, v):
    ns = sorted(n for n, _ in s)
    return ("|".join(ns), v[0])


g_memo = {}
p_memo = {}


def g(s, v):
    """Min cost of a path
    - Starting at v_start
    - Visiting everything in s exactly once
    - Ending at v"""

    if len(s) == 0:
        return cost(v_start, v)

    k = key(s, v)
    if k not in g_memo:
        min_c = None
        for elem in s:
            # Condition on elem being penultimate
            s_small = s.copy()
            s_small.remove(elem)
            c = g(s_small, elem) + cost(elem, v)
            if min_c is None or c < min_c:
                min_c = c
                min_elem = elem
        g_memo[k] = min_c
        p_memo[k] = min_elem

    return g_memo[k]


def p(s, v):
    """In the optimal path according to g, return the penultimate elem"""
    if len(s) == 0:
        return v_start

    return p_memo[key(s, v)]


###############
print("Begin")
start_time = time.time()
vs = set(vs)
final_cost = g(vs, v_end)
end_time = time.time()
alg_time = end_time - start_time
print("End")
print(f"Seconds: {alg_time:.2f}")
print()
###############


def add_row(v1, v2, rows):
    row = {}
    for k, val in zip(headers, v2[1] + (v2[0],)):
        row[k] = val

    row["Cost"] = cost(v1, v2) if v1 is not None else 0

    songs = row["Songs"].split(" & ")

    for i, song in enumerate(songs):
        song_row = row.copy()
        song_row["Songs"] = song
        if i < len(songs) - 1:
            song_row["Cost"] = 0
        rows.append(song_row.copy())


v_last = v_end
v_penultimate = p(vs, v_last)


all_rows = []
while len(vs) > 0:
    add_row(v_penultimate, v_last, all_rows)

    v_last = v_penultimate
    vs.remove(v_penultimate)
    v_penultimate = p(vs, v_last)

add_row(v_penultimate, v_last, all_rows)
add_row(None, v_penultimate, all_rows)

all_rows.reverse()
df = pd.DataFrame(all_rows)
headers.reverse()
df = df[headers + ["Cost"]]

print(df)
print()
print("Total:", final_cost)

# OUTPUT:

# Begin
# End
# Seconds: 7.17

#                              Songs Vocals Keys Bass Guitar Drums  Cost
# 0                      First dance     JI   BS                       0
# 1       Let's Stay Together (F)(*)     JI   BS   DJ     GW    TL     3
# 2                   Forget You (C)     JI   BS   DJ     GW    TL     0
# 3              Crazy in Love (Dm)*     JI   JO   DJ     GW    TL     1
# 4   Girls Just Wanna Have Fun (E)*     JI   DA   DJ     GW    TL     1
# 5           Backstreets Back (Bbm)     JI   DA   DJ     GW    TL     0
# 6             Master Blaster (Cm)*     HN   DA   DJ     GW    TL     1
# 7              Lady Marmalade (Gm)     JI   JW   DJ     GW    TL     2
# 8             Isn't She Lovely (E)     JI   JW   DJ     GW    TL     0
# 9                  Easy Lover (Fm)     JI   JW   DJ     GW    AI     1
# 10                American Boy (E)     JI   JO   GF     DJ    JW     2
# 11                  Señorita (Gb)*     JI   DA   GF     GW    JW     2
# 12      Somebody Else's Guy (Abm)*     HN   JW   GF     GW    AI     2
# 13               Runaway Baby (Eb)     HN   JO   DH     GW    JW     2
# 14              Superstition (Em)*     JI   BS   DH     JS    JW     3
# 15                   Valerie (Eb)*     JI   BS   DH     JS    AI     1
# 16                    Respect (C)*     JI   BS   DH     JS    AI     0
# 17     Play That Funky Music (Em)*     JI   BS   DH     JS    AI     0
# 18        I Got You (I Feel Good)*     JI   BS   DH     JS    AI     0
# 19              Ain't Nobody (Ebm)     JI   BS   DH     JS    AI     0
# 20                   Treasure (Ab)     JI   JO   DH     JS    AI     1
# 21       Locked Out Of Heaven (Dm)     JI   JO   DH     JS    AI     0
# 22                Uptown Funk (D)*     JI   DA   DH     JS    AI     1
# 23                 Good Times (Em)     JI   DA   DH     JS    TL     1
# 24                             End                                   0

# Total: 24
