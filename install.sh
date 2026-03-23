#!/usr/bin/env bash

sudo mv main.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable main.service
sudo systemctl start main.service
sudo systemctl status main.service
