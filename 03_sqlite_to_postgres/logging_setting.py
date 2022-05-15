import logging

base_logger = logging.getLogger(__name__)
base_logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s:%(filename)s:%(message)s:')

file_handler = logging.FileHandler('sqlite_psql_migrate.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

base_logger.addHandler(stream_handler)
base_logger.addHandler(file_handler)
