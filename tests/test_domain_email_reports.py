"""Tests of the email report view model."""
import datetime

from dnstwister.domain.email_report import EmailReport


def test_noisy_flags_separates_domains_in_report():
    """Tests domains with the noisy flag set are ."""
    new = (
        ('www.example1.com', '127.0.0.1'),
        ('www.example7.com', '127.0.0.9'),
    )
    updated = (
        ('www.example2.com', '127.0.0.1', '127.0.0.2'),
        ('www.example9.com', '127.0.0.3', '127.0.0.4'),
    )
    deleted = (
        'www.example3.com',
        'www.example15.com',
    )
    noisy = (
        ('www.example7.com', 'www.example2.com', 'www.example3.com')
    )

    delta_report = {
        'new': new,
        'updated': updated,
        'deleted': deleted,
    }

    report = EmailReport(delta_report, noisy, include_noisy_domains=True)

    assert report.new == (('www.example1.com', '127.0.0.1'),)
    assert report.updated == (('www.example9.com', '127.0.0.3', '127.0.0.4'),)
    assert report.deleted == ('www.example15.com',)
    assert report.noisy == (
        'www.example7.com', 'www.example2.com', 'www.example3.com'
    )



def test_noisy_noisy_domains_can_be_hidden():
    """Tests domains with the noisy flag set are ."""
    new = (
        ('www.example1.com', '127.0.0.1'),
        ('www.example7.com', '127.0.0.9'),
    )
    updated = (
        ('www.example2.com', '127.0.0.1', '127.0.0.2'),
        ('www.example9.com', '127.0.0.3', '127.0.0.4'),
    )
    deleted = (
        'www.example3.com',
        'www.example15.com',
    )
    noisy = (
        ('www.example7.com', 'www.example2.com', 'www.example3.com')
    )

    delta_report = {
        'new': new,
        'updated': updated,
        'deleted': deleted,
    }

    report = EmailReport(delta_report, noisy, include_noisy_domains=False)

    assert report.new == (('www.example1.com', '127.0.0.1'),)
    assert report.updated == (('www.example9.com', '127.0.0.3', '127.0.0.4'),)
    assert report.deleted == ('www.example15.com',)
    assert len(report.noisy) == 0
