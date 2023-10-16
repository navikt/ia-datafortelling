from datetime import datetime, timedelta

from common.visualization_utils import make_goal_indicator, formater_tittel
from key_metrics.data_prepping import (
    calculate_key_metrics,
    calculate_repeated_key_metrics,
)


def plot_key_metrics(data):
    now = datetime.now()
    antall_åpnet_kort, antall_åpnet_kort_flere_dager = calculate_key_metrics(
        data, now - timedelta(days=30), now
    )
    antall_brukt_med_måneds_mellomrom = calculate_repeated_key_metrics(
        data, now - timedelta(days=365), now
    )

    make_goal_indicator(
        antall_åpnet_kort,
        300,
        formater_tittel(
            "Antall virksomheter som har interagert med siden",
            "i løpet av de siste 30 dagene",
        ),
    ).show()

    make_goal_indicator(
        antall_åpnet_kort_flere_dager,
        30,
        formater_tittel(
            "Antall virksomheter som har interagert med siden flere dager",
            "i løpet av de siste 30 dagene",
        ),
    ).show()
    make_goal_indicator(
        antall_brukt_med_måneds_mellomrom,
        100,
        formater_tittel(
            "Antall virksomheter som har gjort noe med minst 30 dager fra første til siste hendelse",
            "i løpet av de siste 365 dagene",
        ),
    ).show()
