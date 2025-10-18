# Sysprobe
### How to use?
1. Navigate to the project directory:
   ```bash
   cd /path/to/Sysprobe
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install all the requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the project using:
   ```bash
   python3 -m sysprobe <command> [options]
   ```

### Task B: Filesystem watch
```py
# Command
python3 -m sysprobe watch --dir /tmp/sysprobe --secs 10

# Example - An output from my machine
2025-10-18T16:37:44Z    IN_CREATE       /tmp/sysprobe/a
2025-10-18T16:37:47Z    IN_MODIFY       /tmp/sysprobe/a
2025-10-18T16:37:55Z    IN_MOVED_FROM   /tmp/sysprobe/a
2025-10-18T16:37:55Z    IN_MOVED_TO     /tmp/sysprobe/b
2025-10-18T16:38:00Z    IN_DELETE       /tmp/sysprobe/b
```
### Task C: Tracing (debugfs)
```py
# Command
sudo python3 -m sysprobe trace --secs 2

# Example - An output from my machine
syscalls/sys_enter_write
    node-4156    [000] ...1. 75002.538109: sys_write(fd: 27, buf: 402f54d8, count: 12e)
sched/sched_switch
    <idle>-0       [007] d..2. 74862.483021: sched_switch: prev_comm=swapper/7 prev_pid=0 prev_prio=120 prev_state=R ==> next_comm=sudo next_pid=153261 next_prio=120
sched/sched_process_exec
    cat-153769  [006] ..... 75068.751103: sched_process_exec: filename=/usr/bin/cat pid=153769 old_pid=153769
net/netif_receive_skb
    node-119748  [002] ..s1. 75089.727722: netif_receive_skb: dev=lo skbaddr=00000000314dbd98 len=455
```
