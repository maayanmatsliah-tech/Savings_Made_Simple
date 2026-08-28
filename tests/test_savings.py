import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from savings_made_simple import get_summary, calculate_week, read_csv, create_csv_if_not_exists, update_start_finish_csv, append_to_csv

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
    def test_basic_case(self):
        'test that an empty list and one weekly expense works'
        amt, lst = calculate_week(start=1000, finish=200, week_number=1, weekly_spending_list= [], weekly_expense=30)
        assert amt == 770
        assert lst == [30]

    def test_lst_not_empty(self):
            'test that weekly expense is correctly added to list'
            amt, lst = calculate_week(start=1000, finish=200, week_number=4, weekly_spending_list= [10, 5, 5], weekly_expense=30)
            assert amt == 750
            assert lst == [10, 5, 5, 30]

    def test_calculate_week_does_not_mutate_original_list(self):
        """Documents current behavior: calculate_week mutates the list you pass in,
        in addition to returning it. This is a bug we'll remove during the DB migration."""
        original_list = [10, 20]
        weekly_expense=15
        original_len = len(original_list)

        returned_list = calculate_week(
            start=1000, finish=200, week_number=3, weekly_spending_list=original_list,
            weekly_expense=weekly_expense
        )[1]

        assert original_list[-1] == weekly_expense
        assert original_len == len(original_list)
        assert original_list is returned_list

class TestData():
    """tests to ensure correct data is inputed and correct data is returned"""

    def test_read_csv_round_trip(self, tmp_path):
        'testing full csv pipeline works'
        path = str(tmp_path / "savings.csv")
        result = read_csv(path)
        assert result == (0.0, 0, [], [], None, None)

        create_csv_if_not_exists(path)
        update_start_finish_csv(1000, 200, path)
        append_to_csv(1, 50.0, 750.0, path)
        append_to_csv(2, 30.0, 720.0, path)

        total_spent, last_week, weekly_spending_list, week_numbers, start, finish = read_csv(path)

        assert start == 1000
        assert finish == 200
        assert last_week == 2
        assert total_spent == 80.00 
        assert weekly_spending_list == [50.00, 30.00] 
        assert week_numbers == [1, 2]


