from watchman import Watchman
import sys
import json

if not(len(sys.argv) == 3 or len(sys.argv) == 4):
    print('Command-line arguments must follow this format:')
    print('$ python watchman-test.py [rootPath] [subscriptionName] [clockspec value]')
else:
    print(sys.argv[1])
    rootPath = sys.argv[1]

    print(sys.argv[2])
    subscriptionName = sys.argv[2]

    clockSpec = None
    if len(sys.argv) == 4:
        print(sys.argv[3])
        clockSpec = sys.argv[3]

    print('\n====Checking Watchman interface====\n')
    watch = Watchman()
    # print('Subscribing...')
    # subResult = watch.subscribe(rootPath, subscriptionName)
    # print(subResult)

    # print('Unsubscribing...')
    # unsubResult = watch.unsubscribe(rootPath, subscriptionName)
    # print(unsubResult)

    print('Checking clock:')
    clock = watch.clock(rootPath)
    print(clock)

    if not (clockSpec is None):
        print('\nGetting changed files:')
        # The third argument is optional
        result = watch.since(rootPath, clockSpec, ['**/*.txt'])
        print(json.dumps(result, indent = 4))
