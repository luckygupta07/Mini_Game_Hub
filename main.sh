#!/bin/bash

USERS_FILE="users.tsv"

for i in 1 2 ; do
        echo "=============== Player ${i} Authentication ==============="

    while true ; do
        read -p "Enter username: " user
        eval "user${i}='$user'"
        #declare "user${i}=${user}"

        if [ "$i" -eq 2 ] && [ "${user1}" == "${user2}" ]; then
            echo "Username1 and Username2 cannot be same. Enter different username ..."
            continue
        fi
        
        line=$(grep "^$user\b" "$USERS_FILE")

        if [ "$line" != "" ]; then
            # User exists → login
            correct_hashed_password=$(echo "$line" | cut -f2 )
            while true ; do
                read -sp "Enter password for ${user}: " password
                echo
                hashed_password=$(echo -n "$password" | sha256sum | cut -d' ' -f1 )
                if [ "$hashed_password" == "$correct_hashed_password" ]; then
                    echo "Login successful for ${user}"
                    break
                else
                    echo "Incorrect password. Try Again ..."
                fi
            done
            break
        
        else 
            # User does not exist → register
            read -p "User does not exist. Do you want to register? [y/n]: " pick
            if [ "$pick" == "y" ]; then
                read -sp "Create password: " password
                echo
                read -sp "Confirm password: " confirm
                echo

                if [ "$password" != "$confirm" ]; then
                    echo "Passwords do not match! Try Again ..."
                else
                    hashed_password=$(echo -n "$password" | sha256sum | cut -d' ' -f1 )
                    echo -e "${user}\t${hashed_password}" >> "$USERS_FILE"
                    echo "User registered successfully!"
                    break
                fi
            fi
        fi      
    done
done

echo "========== Game is starting between $user1 and $user2 =========="

python3 game.py "$user1" "$user2"
