tmux new -d -s led

tmux send-keys -t led.0 "cd ~/Documents/LED/" ENTER
tmux send-keys -t led.0 "sudo python ./led.py" ENTER
