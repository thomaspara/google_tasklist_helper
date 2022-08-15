#!/bin/bash
script_full_path=$(dirname "$(realpath "$0")")
cd $script_full_path
source taskenv/bin/activate
python3 g_service_helper.py thomas_parashos tasks v1 task
