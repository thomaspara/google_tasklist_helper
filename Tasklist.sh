while [ -z "$(fping google.com | grep alive)" ]
do
    echo "waiting for internet ..."
    sleep 3
done
echo "Internet is now online"
script_full_path=$(dirname "$(realpath "$0")")
cd $script_full_path
git checkout .
git fetch https://github.com/thomaspara/google_tasklist_helper.git
git pull
source taskenv/bin/activate
pip install -r requirements.txt
python tasklist.py