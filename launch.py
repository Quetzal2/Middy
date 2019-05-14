st1="""\033[1;33;40m
\033[1;31;40m  _______ __     __     __
\033[1;33;40m |   |   |__|.--|  |.--|  |.--.--.
\033[1;32;40m |       |  ||  _  ||  _  ||  |  |
\033[1;36;40m |__|_|__|__||_____||_____||___  |
\033[1;37;40m      -- DISCORD BOT --  \033[1;35;40m  |_____|

\033[1;37;40m Revision -\033[1;31;40m 1
\033[1;37;40m Version  - \033[1;31;40m1.2.2
\033[1;37;40m https://github.com/raithsphere/Middy
\033[1;37;40m At times I question you RaithSphere...
"""

import os
import sys
import time
import logging
import tempfile
import traceback
import subprocess
from bot import Middy


# Setup initial loggers

tmpfile = tempfile.TemporaryFile('w+', encoding='utf8')
log = logging.getLogger('launcher')
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(logging.Formatter(
    fmt="[%(levelname)s] %(name)s: %(message)s"
))

sh.setLevel(logging.INFO)
log.addHandler(sh)

tfh = logging.StreamHandler(stream=tmpfile)
tfh.setFormatter(logging.Formatter(
    fmt="[%(relativeCreated).9f] %(asctime)s - %(levelname)s - %(name)s: %(message)s"
))
tfh.setLevel(logging.DEBUG)
log.addHandler(tfh)


def finalize_logging():
    if os.path.isfile("logs/middy.log"):
        log.info("Moving old middy log")
        try:
            if os.path.isfile("logs/middy.log.last"):
                os.unlink("logs/middy.log.last")
            os.rename("logs/middy.log", "logs/middy.log.last")
        except:
            pass

    with open("logs/middy.log", 'w', encoding='utf8') as f:
        tmpfile.seek(0)
        f.write(tmpfile.read())
        tmpfile.close()

        f.write('\n')
        f.write(" CHECKS PASSED ".center(80, '#'))
        f.write('\n\n')

    global tfh
    log.removeHandler(tfh)
    del tfh

    fh = logging.FileHandler("logs/middy.log", mode='a')
    fh.setFormatter(logging.Formatter(
        fmt="[%(relativeCreated).9f] %(name)s-%(levelname)s: %(message)s"
    ))
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)

    sh.setLevel(logging.INFO)

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='logs/middy.log', encoding='utf-8', mode='a')
    handler.setFormatter(logging.Formatter(
    fmt="[%(relativeCreated).9f] %(asctime)s - %(levelname)s - %(name)s: %(message)s"
))
    logger.addHandler(handler)


print(st1)
finalize_logging()
bot = Middy()
bot.run()
