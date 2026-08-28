import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from savings_made_simple import get_summary

class TestGetSummary():
    '''class to test the 'get_summary' method'''
    def test_no_weeks_logged_yet(self):
        "Make sure amt when no weeks are logged is unchanged"
        start, finish, spending = 1000, 200, []
        summary = get_summary(start=start, finish=finish, weekly_spending_list=spending)

        expected_remaining_allowed = (start - finish) - sum(spending)
        expected_weeks_remaining = 13 - len(spending)
        expected_adjusted_avg = expected_remaining_allowed / expected_weeks_remaining

        assert summary["adjusted_avg"] == expected_adjusted_avg
        assert summary["total_spent"] == 0
        assert summary["money_left"] == 1000
        assert summary["on_track"] is True

    def test_off_track_when_overspending(self):
        "Make sure get summary flags off track when user is over-spending"
        summary = get_summary(start=1000, finish=200, weekly_spending_list=[300])
        assert summary["on_track"] is False

    def test_adjusted_avg_none(self):
        "Make sure adjusted avg is None when spend > start - finish"
        summary = get_summary(start=1000, finish=200, weekly_spending_list=[801])
        assert summary["adjusted_avg"] is None

    def test_adjusted_avg_float(self):
        "Make sure adjusted avg is a float when spend < start - finish"
        summary = get_summary(start=1000, finish=200, weekly_spending_list=[30, 50, 10, 70, 6, 11])
        assert isinstance(summary['adjusted_avg'], float)
        assert summary['adjusted_avg'] > 0

class TestCalculateWeek():
    '''class to test the 'calculate_week' method'''
    def
