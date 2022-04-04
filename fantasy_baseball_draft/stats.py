"""Handle stats."""

def pitcher_fwar(pitcher, spg, league):
    fwar = (
        pitcher.k / spg['so'] 
        + pitcher.w / spg['w']
        + pitcher.s / spg['s']
        + ((league['era'] - pitcher.era)/9 * pitcher.inn / spg['xer']).fillna(0)
        + ((league['whip'] - pitcher.whip) * pitcher.inn / spg['xwhip']).fillna(0)
    )
    return fwar

def hitter_fwar(hitter, spg, league):
    ba = hitter.h /hitter.ab
    fwar = (
        hitter.r / spg['r']
        + hitter.hr / spg['hr']
        + hitter.rbi / spg['rbi']
        + hitter.sb / spg['sb']
        + ((ba - league['ba']) * hitter.ab / spg['xh']).fillna(0)
    )
    return fwar