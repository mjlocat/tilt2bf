# tilt2bf
Publish stored [Tilt Hydrometer](https://tilthydrometer.com/) readings stored by [tilt2db](https://github.com/mjlocat/tilt2db) to [Brewer's Friend](https://www.brewersfriend.com) Stream API

## Why?

The Android app for the Tilt Hydrometer requires a device is always on and in BLE range to read the data and forward it on to a service or a logger. I already have a Raspberry Pi near my fermentation fridge and wanted to leverage that to get the data and move it along. There is the TiltPi, but I'm not a huge fan of Node Red and found it to lose the connection every so often requiring the service to be restarted. This project is to be paired with [tilt2db](https://github.com/mjlocat/tilt2db) for getting readings from the Tilt Hydrometer and storing them in the database. This project takes those readings in the database and submits them to the Brewer's Friend Stream API

## Prerequisites

* MySQL or MariaDB Database set up from [tilt2db](https://github.com/mjlocat/tilt2db)
* Python3
* [Brewer's Friend](https://www.brewersfriend.com/) account, Premium level or higher

## Installation

1. Clone the repository

    ``` sh
    git clone https://github.com/mjlocat/tilt2bf.git && cd tilt2bf
    ```

1. Install the python libraries

    ``` sh
    pip3 install -r requirements.txt
    ```

1. Copy `config.yaml.sample` to `config.yaml` and update the database credentials and `API_KEY` from the [Brewer's Friend Integrations Page](https://www.brewersfriend.com/homebrew/profile/integrations)

## Usage

Invoke using `python3 tilt2bf.py` (If `python` is version 3, you can use that)

```
usage: tilt2bf.py [-h] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Location of the configuration file
```
| Command Options | Description |
| --------------- | ----------- |
| `-c CONFIG, --config CONFIG` | Specify the location of the `config.yaml` file |

This takes the average of the last 15 minutes temperature and specific gravity readings for each color Tilt Hydrometer, sends each to Brewer's Friend, then exits. You'll probably want to set up a cronjob to run this.

``` crontab
*/15 * * * * (cd ~/tilt2bf && python3 tilt2bf.py)
```
Do not run more than every 15 minutes. The Brewer's Friend Stream API is rate limited to a 15 minute minimum.

## Linking to a Brew Session

You will have to link your readings to your brew session before they'll show up. You will have to send at least one reading from your Tilt Hydrometer before linking it to your brew session. From the Brew Session Fermentation page, click Link Device under Devices. Choose type Stream, then click the Device drop down. Choose the color Tilt you are using for this brew session and click Save. The next reading should show up on your graph.