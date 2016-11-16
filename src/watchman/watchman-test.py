from watchman import Watchman

watch = Watchman()
print("Socket Location: " + watch.getSocketLocation())
print("Version: " + watch.checkVersion())
