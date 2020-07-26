# Custom Data-Driven IOT Farming Experience

Small farming project that relies on feedback from sensors to control parameters for optimal plant growth.

## Authors
AJ Kingsley, Kevin Kraydich, and Michael Rakowiecki

## Overview

TODO

## Hardware

The hardware used for this project includes:

1x  [Raspberry Pi 4](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TD42S27/)<br>
2x  [CO<sub>2</sub>, Humidity, Temperature, and Barometric Pressure Sensors](https://www.amazon.com/gp/product/B076955G5S/)<br>
1x  [IR Camera](https://www.amazon.com/gp/product/B07VSPSNL8)<br>
1x  [4-Channel Relay Module](https://www.amazon.com/gp/product/B0057OC5O8/)<br>

## Purpose

TODO

## Usage

### Email and Text Notifications

In order for this feature to work properly, you will need to add a config file (`config.json`) to `src/alerts/text` which stores API credentials as well as users' names and phone numbers. Here is an example of what this file might look like:

    {
        "twilio" {
            "account_SID": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "auth_token": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "sending_number": "+15558675309"
        },
        "email": {
            "username": "youremail@provider.com",
            "password": "hunter2",
            "smtp": "smtp.gmail.com",
            "port": "587"
        },
        "users": [
            {
                "name": "John Smith",
                "number": "+15558675309",
                "email": "john.smith@provider.com"
            }
        ]
    }

Note: phone numbers must be in [E.164](https://www.twilio.com/docs/glossary/what-e164) format, per Twilio's API.
