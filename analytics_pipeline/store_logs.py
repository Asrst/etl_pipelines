import time
import sys
import sqlite3
from datetime import datetime

DB_NAME = "db.sqlite"
LOG_FILES = ["a.log", "b.log"]

def create_table():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs (
      raw_log TEXT NOT NULL UNIQUE,
      remote_addr TEXT,
      time_local TEXT,
      request_type TEXT,
      request_path TEXT,
      status INTEGER,
      body_bytes_sent INTEGER,
      http_referer TEXT,
      http_user_agent TEXT,
      created DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    """)
    conn.close()

def parse_line(line):
    split_line = line.split(" ")
    if len(split_line) < 12:
        return []
    remote_addr = split_line[0]
    time_local = split_line[3] + " " + split_line[4]
    request_type = split_line[5]
    request_path = split_line[6]
    status = split_line[8]
    body_bytes_sent = split_line[9]
    http_referer = split_line[10]
    http_user_agent = " ".join(split_line[11:])
    created = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    return [
        remote_addr,
        time_local,
        request_type,
        request_path,
        status,
        body_bytes_sent,
        http_referer,
        http_user_agent,
        created
    ]

def insert_record(line, parsed):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    args = [line] + parsed
    cur.execute('INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)', args)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()
    for log_file in LOG_FILES:
        try:
            f = open(log_file, 'r')
            for line in f.readlines():
                line = line.strip()
                parsed = parse_line(line)
                print(parsed)
                if len(parsed) > 0:
                    insert_record(line, parsed)
            # 
            # while True:
                # where_marker = f.tell()
                # line = f.readline()

                # if not line:
                    # time.sleep(1)
                    # f.seek(where_marker)
                    # continue
                # else:
                    # line = line.strip()
                    # parsed = parse_line(line)
                    # if len(parsed) > 0:
                        # insert_record(line, parsed)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)
        finally:
            f.close()
            sys.exit()