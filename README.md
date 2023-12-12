<a href="https://www.goodrequest.com/">
    <img src="https://global-uploads.webflow.com/5dca73a3dff894e401b4d7c0/5ed9fa51800a236c9261b703_GR_new%20logos-02.svg" alt="" class="gr-logo" align="right">
</a>

# LOGEN (**Lo**calization **Gen**erator)

![Version](https://img.shields.io/badge/latest_version-2.0.3-blueviolet)
[![Python Version](https://img.shields.io/badge/python-3.9-blue)](https://www.python.org/downloads/release/python-390/)
![Swift Version](https://img.shields.io/badge/swift-5+-yellow)
![SPM](https://img.shields.io/badge/SwiftPM-supported-green)
![Hotel](https://img.shields.io/badge/Hotel%3F-Trivago-orange)

Logen is a Python script that helps with generating localized strings for Swift projects from Google Docs spreadsheets.

# How to set up:

---
## Python
First of all you need to install `python 3.9` on your machine:
1. Recommended way of installing python on macOS is via *Homebrew Package Manager*. You can grab Homebrew from the official website:
```
https://brew.sh
```
2. Use Homebrew to download the latest Python 3 version using the following command:
```shell
brew install python
```
3. Check if Python is available and installed correctly. You should see a path to the Python binary in your system.
```shell
which python3
```
4. Check if you have `pip` python package manager installed. The path should lead to the same directory as the command above.
```shell
which pip3
```

---
## Xcode integration
1. Add Logen to your [Swift Build Tools' `Package.swift`](./res/BuildToolsTutorial.md) via SwiftPM.
```
.package(url: "git@bitbucket.org:GoodRequest/logen_ios.git", .upToNextMajor(from: "2.0.0"))
```
Hit *Cmd+S* and you should see Xcode starting to fetch the package for you. Wait until all package dependencies are resolved.

2. Open project settings and create a new build target
 - Click `+` in the bottom left corner
 - Open tab "Other"
 - Select "Aggregate"
 - Give it a name (eg. "Logen 2")
 - and "Finish"


3. Select the target you just created and switch to "Build Phases" tab.
 - Click `+` in the top left corner
 - Select "New Run Script Phase"
 - (not required) Rename the build phase to something more descriptive


4. Copy and paste this script (also remove two wild `#`, those are there only to prevent Bitbucket from obliterating the formatting of this readme):
```shell
SCRIPT_PATH="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/logen2.py"
CREDS="${BUILD_DIR%/Build/*}/SourcePackages/checkouts/Logen/credentials.json"
TOKEN="${PROJECT_DIR}/logen2_token.json"
#
GOOGLE_SHEETS_ID="SHEET ID HERE"
SHEET="SHEET NAME HERE"
FIRST_ROW="1"
LAST_COLUMN="E"
#
if test -f "${SCRIPT_PATH}"; then
    python3 "${SCRIPT_PATH}" --id "${GOOGLE_SHEETS_ID}" --sheet "${SHEET}" --first_row "${FIRST_ROW}" --last_column "${LAST_COLUMN}" --project "${PROJECT_NAME}" --credentials "${CREDS}" --token "${TOKEN}"
else
    echo "warning: Script not found, add it from https://bitbucket.org/GoodRequest/logen_ios/ 😭😩🤦‍♂️"
fi
```

| Parameters | Required | Description |
|---|---|---|
| `--id` | yes | Spreadsheet identifier. You can find it inside a link from your  browser, when you open google spreadsheets (for example, if your link is `https://docs.google.com/spreadsheets/d/ASDFGHJKL/edit#gid=0`, the identifier is `ASDFGHJKL`). |
| `--project` | yes | Project name. Recommended value is `"${PROJECT_NAME}"` (Xcode build variable). |
| `--sheet` | yes | Name of the sheet in spreadsheet. You can find it in the bottom left. |
| `--first_row` | no | First row of the spreadsheet. This is an optional argument (with a  default value of 1) in case you need to skip the first couple of rows. |
| `--last_column` | yes | Last column in the sheet that contains data. For example if your spreadsheet has 7 columns, the last one is marked G.<br><br>P.S. if you need explaining what sheets and ranges are, you should probably take an Excel course |
| `--credentials` | no | Credentials authorizing the app to use google's API. Recommended value is the location of credentials.json in build directory. `"${BUILD_DIR%/Build/*}/SourcePackages/checkouts/logen_ios/credentials.json"` Default value points to credentials.json file in the same directory where the script is invoked from. |
| `--token` | no | Credentials authorizing the user to use google's API. Recommended value is `"${PROJECT_DIR}/logen2_token.json"`, or anywhere else in the user's computer. This token should **not** be pushed to git. |
| `--localization_path` | no | Path **inside** the project directory, where the final localization files should be exported into. Does **not** start nor end with a slash. Does **not** specify the localization language. Default value: `Resources/Localization`. |


5. Generate your token file:
 - Run the target!
 - Your web browser should open. Log in with your google account ending in `@goodrequest.com`. It's best to have your password already saved in the browser/keychain, since the timeout is rather short.
 - Give Logen 2 access to spreadsheets API
 - In case the browser gets stuck on loading, hit *Cmd+R* to refresh the website (but it shouldn't really happen)
 - You should get redirected to a success screen


6. Add the token file to `.gitignore`

7. Enjoy your localizations!

![Slovak parrot](https://cultofthepartyparrot.com/flags/hd/slovakiaparrot.gif)
![USA parrot](https://cultofthepartyparrot.com/flags/hd/unitedstatesofamericaparrot.gif)
![Deutscher papagei](https://cultofthepartyparrot.com/flags/hd/germanyparrot.gif)
![Spain parrot](https://cultofthepartyparrot.com/flags/hd/spainparrot.gif)

---
## Spreadsheet setup
There isn't much to set up in the spreadsheets. They should follow this general formatting:

| Description | 1234 iOS ASDF        | Android      | SK        | EN            |
|-------------|----------------------|--------------|-----------|---------------|
| Any         | Title of this column | This should  | Preklad 1 | Translation 1 |
| description | should contain       | burn in hell | Preklad 2 | Translation 2 |
| you         | the word "iOS"       |              | Preklad 3 | Translation 3 |
| want        | somewhere            |              | Preklad 4 | ...           |

It's important to note that the language column should be exactly 2 letters long and reflect the same language code that's used in the project.
