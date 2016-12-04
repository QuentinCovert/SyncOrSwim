# Additional Info. for Watchman Installation

In the case that the user does not have root permission (i.e. is not authorized to use the `sudo` command), they may compile Watchman into their `~/bin/` directory.

Note: The ./confure command requires the absolute path, and the `~` symbol will not be resolved by Linux. In this snippet, the example `~` directory is `/home/ugrad/mhernand`.

```
cd ~

git clone https://github.com/facebook/watchman.git watchman

cd ~/watchman

git checkout v4.7.0

./autogen.sh

./configure --prefix=/home/ugrad/mhernand/watchman/output --enable-statedir=/home/ugrad/mhernand/watchman/output/state --enable-conffile=/home/ugrad/mhernand/watchman/output/watchman.json

make

make install

make clean

cp ~/watchman/output/bin/watchman* ~/bin/
```

This should then be installed for your home directory. The output should be the same as mentioned in the [README.md](README.md#Installation).