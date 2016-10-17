from time import sleep

from bistiming import IterTimer


def main():
    n_iter = 100

    print("[Example 1]")
    with IterTimer("Waiting iteration", n_iter) as timer:
        for i in range(n_iter):
            timer.update(i)
            sleep(0.01)

    print("\n[Example 2] update period 10")
    with IterTimer("Waiting iteration", n_iter, 10) as timer:
        for i in range(n_iter):
            timer.update(i)
            sleep(0.01)

    print("\n[Example 3] hide the message using verbose 0")
    with IterTimer("Waiting iteration", n_iter, verbose=0) as timer:
        for i in range(n_iter):
            timer.update(i)
            sleep(0.01)


if __name__ == '__main__':
    main()
