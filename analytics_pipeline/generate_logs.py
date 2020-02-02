from faker import Faker
from datetime import datetime
import random
import time

LOG_LINE = """\
{remote_addr} - - [{time_local} +0000] "{request_type} {request_path} HTTP/1.1" {status} {body_bytes_sent} "{http_referer}" "{http_user_agent}"\
"""

LOG_FILES = ["a.log", "b.log"]
MAX_LOG_NUMS = 200

def generate_log_line():
    """
    function to generate a random fake log line
    """
    fake = Faker()
    remote_addr = fake.ipv4()
    time_local = datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
    
    request_type = random.choice(["GET", "POST", "PUT"])
    request_path = "/" + fake.uri_path()

    status = random.choice([200, 401, 404])
    body_bytes_sent = random.choice(range(5, 1000, 1))
    http_referer = fake.uri()
    http_user_agent = fake.user_agent()

    log_line = LOG_LINE.format(
        remote_addr=remote_addr,
        time_local=time_local,
        request_type=request_type,
        request_path=request_path,
        status=status,
        body_bytes_sent=body_bytes_sent,
        http_referer=http_referer,
        http_user_agent=http_user_agent
    )

    return log_line

def write_log_line(log_file, line):
    with open(log_file, "a") as f:
        f.write(line)
        f.write("\n")

def clear_log_file(log_file):
    with open(log_file, "w+") as f:
        f.write("")

if __name__ == "__main__":
    # loop over files
    for log_file in LOG_FILES:
        # clear the log file
        clear_log_file(log_file)
        # reset the lines
        lines_written = 0
        # loop till the maz log count
        while lines_written < MAX_LOG_NUMS:
            line = generate_log_line()
            write_log_line(log_file, line)
            lines_written += 1
            sleep_time = random.choice(range(1, 5, 1))
            time.sleep(sleep_time)
