from time import sleep

from bistiming import SimpleTimer

print("[Example 1]")
with SimpleTimer():
    sleep(1)

print("\n[Example 2] timer with description")
with SimpleTimer("Waiting"):
    sleep(1)

print("\n[Example 3] timer without starting message")
with SimpleTimer("Waiting", verbose_start=False):
    sleep(1)

print("\n[Example 4] timer without ending message")
with SimpleTimer("Waiting", verbose_end=False):
    sleep(1)
