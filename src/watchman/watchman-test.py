from watchman import Watchman
import sys

if len(sys.argv) != 3:
    print('Command-line arguments must follow this format:')
    print('$ python watchman-test.py [rootPath] [subscriptionName]\n')
else:
    print(sys.argv[1])
    print(sys.argv[2])

    rootPath = sys.argv[1]
    subscriptionName = sys.argv[2]

    watch = Watchman()
    # print('Subscribing...')
    # watch.subscribe(rootPath, subscriptionName)

    # print('Unsubscribing...')
    # watch.unsubscribe(rootPath, subscriptionName)

    print('Checking clock')
    watch.clock(rootPath)

    # print('Getting changed files')
    # watch.since(rootPath)

    # print("Socket Location: " + watch.getSocketLocation())
    # print("Version: " + watch.checkVersion())
