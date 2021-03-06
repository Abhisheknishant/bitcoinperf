
import io

from . import logparse


fake_log = """


2019-12-13T20:13:52Z [init] Bitcoin Core version v0.19.99.0-ddecb671f (release build)
2019-12-13T20:14:01Z [shutoff] Recorded 0 unconfirmed txs from mempool in 0s
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block and undo data to disk started
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block and undo data to disk completed (7.83ms)
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block index to disk started
2019-12-13T20:14:01Z [shutoff] WriteBatch memory usage: db=index, before=0.0MiB, after=22.6MiB
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block index to disk completed (355.24ms)
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write coins cache to disk (1201 coins, 276kB) started
2019-12-13T20:14:01Z [shutoff] Writing final batch of 0.08 MiB
2019-12-13T20:14:01Z [shutoff] WriteBatch memory usage: db=chainstate, before=0.0MiB, after=0.1MiB
2019-12-13T20:14:01Z [shutoff] Committed 1201 changed transaction outputs (out of 1201) to coin database...
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write coins cache to disk (1201 coins, 276kB) completed (0.00s)
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block and undo data to disk started
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block and undo data to disk completed (0.15ms)
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block index to disk started
2019-12-13T20:14:01Z [] leveldb: Level-0 table #5: started
2019-12-13T20:14:01Z [shutoff] WriteBatch memory usage: db=index, before=22.6MiB, after=22.6MiB
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write block index to disk completed (3.54ms)
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write coins cache to disk (0 coins, 11kB) started
2019-12-13T20:14:01Z [shutoff] Writing final batch of 0.00 MiB
2019-12-13T20:14:01Z [shutoff] WriteBatch memory usage: db=chainstate, before=0.1MiB, after=0.1MiB
2019-12-13T20:14:01Z [shutoff] Committed 0 changed transaction outputs (out of 0) to coin database...
2019-12-13T20:14:01Z [shutoff] FlushStateToDisk: write coins cache to disk (0 coins, 11kB) completed (0.00s)
2019-12-13T20:1
"""

def test_logparse():
    filehandle = io.StringIO(fake_log)
    assert logparse.get_flush_times(filehandle) == [
        logparse.FlushEvent(9, 0.00, 1201, 276),
        logparse.FlushEvent(9, 0.00, 0, 11)]
