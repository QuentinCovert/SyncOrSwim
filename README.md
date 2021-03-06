<img src="src/resources/syncOrSwimLogo.png" width="200px" height="200px" alt="SyncOrSwimLogo" />

# SyncOrSwim
A simple, fast, and secure file syncing application. SyncOrSwim seeks to solve a number of problems in existing file syncing applications: the lack of support for end-to-end encryption controlled locally by the user and the lack of control of where the file is placed remotely.

## ZenHub
We will be using the Chrome extension ZenHub to create and manage issue tracking for this project. All major additions and changes will be created as issues on ZenHub and placed on the issue board. Management of issues will be primarily on an individual basis, but it is highly encouraged to discuss with the team first on Slack before handling new or old issues.

In order to utilize ZenHub, we primarily work/contribute to this git repository on GitHub at [QuentinCovert/SyncOrSwim](https://github.com/QuentinCovert/SyncOrSwim).

## Installation
1. Download the contents of the main folder on this repo.
2. Install SQLAlchemy 3.4, PyQt4, and Watchman. This uses Python 3.4.1. These can be found at the following links:
  * http://www.sqlalchemy.org/download.html
  * https://sourceforge.net/projects/pyqt/
  * https://github.com/facebook/watchman/.
3. Make sure that Watchman is properly installed by running `watchman get-sockname` in the console. Without it, the program will not run correctly. It should return a json-formatted output similar to:
```
{
  "version": "4.7.0",
  "sockname": "/path/to/the/sock"
}
```
  * If you do not have root permission to install Watchman, see the [additional information for Watchman installation](additional-info-watchman-installation.md).

**Note**: Currently, this program is only supported and tested on Linux.

## Usage
1. Using Python 3.4.1, execute the Main module with the following command: path/to/src/Main.py
2. Follow the on-screen instructions to begin syncing files.

This is **not** a replacement for a version control system. This program is concerned with the most recent version of the root directory. 

## Repository Structure
- Diagrams
  - Figures showing use cases, class diagrams, or sequence diagrams.
- Docs
  - Documents of the project.
- Minutes
  - Summaries of meetings (virtual or physical), including date, length, and attendance.
- Src
  - Location of source code for the program. `src/Main.py` will pull in the functionality from various modules in the `src/lib` directory. 

## Contributing
1. Clone repo to local computer using `git clone`.
2. If adding or editing files in the `docs` directory, just make commits in the `master` branch.
3. If adding or changing a feature, create a new branch with the following naming convention: `issue#_briefdesc_branch`.
4. `git checkout` into the new branch and make the commits there, instead of the `master` branch.
5. When the code is stable and clean, make a pull request into `master` branch for code review.

## Contributors
* Levi Amen
* Cameron Johnson
* Quentin Covert
* Collin Victor
* Mark Hernandez

## License
This is an open source project under GPL.
