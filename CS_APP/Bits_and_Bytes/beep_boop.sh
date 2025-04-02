echo "Hello daan!"

while true; do
    read input
    if [[ "$input" =~ ^[0-9]+ ]]; then
        for i in $(seq $input); do
            echo "daan";
        done
    fi
done
