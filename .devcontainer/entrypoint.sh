#!/usr/bin/env bash
echo 'Hey there !'

trap \
 "{ echo 'Bye-Bye !'; exit 255; }" \
 SIGINT SIGTERM

# from https://github.com/microsoft/vscode-remote-release/issues/3512#issuecomment-991473473
# and https://stackoverflow.com/questions/27694818/interrupt-sleep-in-bash-with-a-signal-trap
while sleep 600 & wait $!
do
    # Checking if VSCode is open on the other side
    if ! ps aux | egrep 'vscode.*[b]ootstrap-fork.*extensionHost.*' > /dev/null
    then
        echo "Time to go... : Bye-Bye"
        exit 0
    fi
done
