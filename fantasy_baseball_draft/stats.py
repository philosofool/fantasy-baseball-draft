"""Handle stats."""

def pitcher_fwar(pitcher, spg):
    league = spg['median']
    spg = spg.spg
    fwar = (
        pitcher.k * spg['k'] 
        + pitcher.w * spg['w']
        + pitcher.s * spg['s']
        + ((league['era'] - pitcher.era)/9 * pitcher.ip * spg['era']).fillna(0)
        + ((league['whip'] - pitcher.whip) * pitcher.ip * spg['whip']).fillna(0)
    )
    return fwar

def hitter_fwar(hitter, spg):
    league = spg['median']
    spg = spg.spg
    ba = hitter.h / hitter.ab
    fwar = (
        hitter.r * spg['r']
        + hitter.hr * spg['hr']
        + hitter.rbi * spg['rbi']
        + hitter.sb * spg['sb']
        + ((ba - league['ba']) * hitter.ab * spg['ba']).fillna(0)
    )
    return fwar