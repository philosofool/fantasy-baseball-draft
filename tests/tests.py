# some tests

from fantasy_baseball_draft.spg import matches_eligible, position_value

def test_matches_eligible():
    """Test of matches_eligible."""
    eligible = ['C', 'C, CF', '1B, C', '1B, C, SS', 'CF', 'SS']
    result = matches_eligible(eligible, 'C')
    assert np.array_equal(result, [True, True, True, True, False, False])

def test_postion_value():
    """Test of postiion_values."""
    fwar = np.arange(11, 0, -1) + 2
    eligible = np.array(('c' + ' 1b'*6 + ' c'*4).split())
    result = position_value(fwar, eligible, 'c', 4)
    assert result == 3
    result = position_value(fwar, eligible, 'c', 1)
    assert result == 13
    np.testing.assert_raises(ValueError, position_value, fwar, eligible, 'c', 10)

    fwar = pd.Series(fwar)  # series may not play with internals of position_value.
    result = position_value(fwar, eligible, 'c', 4)
    assert result == 3

if __name__ == '__main__':
    test_matches_eligible()
    test_postion_value()