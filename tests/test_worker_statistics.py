"""Tests of the statistics worker."""
import dnstwister
import patches
import workers.statistics


def set_up_mocks(monkeypatch):
    mock_db = patches.SimpleKVDatabase()
    monkeypatch.setattr('dnstwister.repository.statistics.db', mock_db)
    monkeypatch.setattr('dnstwister.repository.db', mock_db)

    data_repository = dnstwister.repository
    statistics_repository = dnstwister.repository.statistics

    return data_repository, statistics_repository


def test_new_email_sub_creates_new_statistics(capsys, monkeypatch):
    """A new email sub will create a new set of stats."""
    data_repository, statistics_repository = set_up_mocks(monkeypatch)

    # GIVEN a subscribed user with a delta report created.
    data_repository.subscribe_email('1234', 'a@b.com', 'example.com')
    data_repository.update_delta_report('example.com', {
        'new': [['exxample.com', '127.0.0.1']],
        'updated': [],
        'deleted': [],
    })

    # WHEN the email work is ran
    workers.statistics.increment_email_sub_deltas()

    # THEN statistics will be created for exxample.com.
    stats_data = statistics_repository.get_noise_stat('exxample.com')
    assert stats_data.domain == 'exxample.com'
    assert stats_data.deltas == 1
