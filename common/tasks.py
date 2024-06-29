from .services import send_cluster_test


def send_cluster_test_message(number, message):
    send_cluster_test(f'+57{number}', message)
