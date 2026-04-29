#!/bin/bash

# code for usernames
IFS=$'\n' read -r -d "" -a users < <(cut -d $'\t' -f1 users.tsv|sort -u) 
#echo "${users[@]}"

#number of users registered
u=${#users[@]}

#-storing games 
games=(ConnectFour Othello Tic-Tac-Toe)
g=${#games[@]}


#creating ASSOCIATIVE ARRAYS
declare -A  w       # w[i,j] -> number of wins of ith user in jth game
declare -A  l       # l[i,j] -> number of loses of ith user in jth game
declare -A  wl      # wl[i,j] -> win by lose ratio of ith player in jth game

for((i=0;i<u;i++));do
    for((j=0;j<g;j++));do
        w["$i,$j"]=0  
        l["$i,$j"]=0  
    done
done

#creating some useful variable for index marking
wi=0     #winner index
li=0     #loser index
gi=0     #game index

while read -r line ;do
    LINE=$(echo "${line}"|tr -d '\r')
    if [[ -n "${LINE}" ]]; then
        IFS=',' read -r -a arr <<< "$LINE"  #stores line of history.csv as an array
        for((i=0;i<u;i++));do
            if [[ "${arr[0]}" = "${users[$i]}" ]]; then
                wi=${i}
            fi
            if [[ "${users[$i]}" = "${arr[1]}" ]]; then
                li=${i} 
            fi   
        done
        
        for((j=0;j<g;j++));do
            if [[ "${games[$j]}" = "${arr[3]}" ]]; then
                gi=${j}
            fi
        done
    
        ((w[$wi,$gi]++))    #increasing count of respective users game wins of that line
        ((l[$li,$gi]++))    #increasing count of respective users game loses of that line
    fi

done < history.csv

for((i=0;i<u;i++));do
    for((j=0;j<g;j++));do
        if [[ ${l[$i,$j]} -eq 0 ]];then
            wl["$i,$j"]="infinity"
            continue
        fi
        wl["$i,$j"]=$(echo "scale=3;${w[$i,$j]}/${l[$i,$j]}" | bc )
        
    done
done

#storing files per each game
touch connect4.csv othello.csv tictactoe.csv
touch 1.csv 2.csv 3.csv
>connect4.csv
>othello.csv
>tictactoe.csv


for((i=0;i<u;i++));do
    echo "${users[$i]},${w[$i,0]},${l[$i,0]},${wl[$i,0]}">>connect4.csv
done

for((i=0;i<u;i++));do
    echo "${users[$i]},${w[$i,1]},${l[$i,1]},${wl[$i,1]}">>othello.csv
done

for((i=0;i<u;i++));do
    echo "${users[$i]},${w[$i,2]},${l[$i,2]},${wl[$i,2]}">>tictactoe.csv
done
#k stores maxlength of username
k=0
for((i=0;i<u;i++));do
    if [[ ${#users[$i]} -gt ${k} ]]; then
        k=${#users[$i]}
    fi
done

# if k is less than "Username" length it will be problem
if [[ 8 -gt ${k} ]];then
    k=8 
fi

#1.csv,2.csv,3.csv stores the sorted files of respective games connet4.csv,othello.csv,tictactoe.csv
#--sorting by wins--------
if [[ "$1" = "wins" ]];then
    sort  -t ',' -k2,2rn -k3,3n connect4.csv > 1.csv
    sort  -t ',' -k2,2rn -k3,3n othello.csv > 2.csv
    sort  -t ',' -k2,2rn -k3,3n tictactoe.csv > 3.csv
fi

#--sorting by loses ------- 
if [[ "$1" = "losses" ]];then
    sort  -t ',' -k3,3rn -k2,2n connect4.csv > 1.csv
    sort  -t ',' -k3,3rn -k2,2n othello.csv > 2.csv
    sort  -t ',' -k3,3rn -k2,2n tictactoe.csv > 3.csv
fi

#--sorting by winbyloss ratio---
if [[ "$1" = "ratio" ]];then
#emptying the files
    >1.csv
    >2.csv
    >3.csv
#now sorting using awk
#add 1 in 5th column if w/l=infinity else add 0
awk '
    BEGIN{
        FS=","
        OFS=","
    }
    {
        if("$4" == "infinity"){
             print $0,1 >> "1.csv" 
        }
        else{
            print $0,0 >> "1.csv"
        }
    }
' connect4.csv 

sort -t "," -k5,5r -k4,4rn -k2,2rn 1.csv > "connect4.csv"
cut -d ","  -f1-4 connect4.csv >"1.csv"

awk '
    BEGIN{
        FS=","
        OFS=","
    }
    {
        if("$4" == "infinity"){
             print $0,1 >> "2.csv"
        }
        else{
            print $0,0 >> "2.csv"
        }
    }
' othello.csv

sort -t "," -k5,5r -k4,4rn -k2,2rn 2.csv > "othello.csv"
cut -d ","  -f1-4 othello.csv > "2.csv"

awk '
    BEGIN{
        FS=","
        OFS=","
    }
    {
        if("$4" == "infinity"){
             print $0,1 >> "3.csv"
        }
        else{
            print $0,0 >> "3.csv"
        }
    }
' tictactoe.csv

sort -t "," -k5,5r -k4,4rn -k2,2rn 3.csv > "tictactoe.csv"
cut -d ","  -f1-4 tictactoe.csv >"3.csv"
fi

#printing the table
sep1=$(printf '%0.0s-' $(seq 1 $((k+2))))
sep2=$(printf '%0.0s-' $(seq 1 15))
label=$(printf "| %-${k}s | %-13s | %-13s | %-13s |" "Username" "No_of_wins" "No_of_losses" "Winbylosses" )


echo "****************************LEADERBOARD*****************************"
echo "1.connect4"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
echo "${label}"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
while read -r line ;do
IFS="," read -r -a arr <<< "${line}"
printf "| %-${k}s | %-13s | %-13s | %-13s |\n" "${arr[0]}" "${arr[1]}" "${arr[2]}" "${arr[3]}"
done < 1.csv
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"

echo "                            "

echo "2.othello"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
echo "${label}"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
while read -r line ;do
IFS="," read -r -a arr <<< "${line}"
printf "| %-${k}s | %-13s | %-13s | %-13s |\n" "${arr[0]}" "${arr[1]}" "${arr[2]}" "${arr[3]}"
done < 2.csv
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"

echo "            "

echo "3.tictactoe"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
echo "${label}"
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
while read -r line ;do
IFS="," read -r -a arr <<< "${line}"
printf "| %-${k}s | %-13s | %-13s | %-13s |\n" "${arr[0]}" "${arr[1]}" "${arr[2]}" "${arr[3]}"
done < 3.csv
echo "+${sep1}+${sep2}+${sep2}+${sep2}+"
echo "*********************************END*********************************"



#for plotting bargraph
>count_of_games.csv
>a.csv #created for temperory storage of information
for((i=0;i<u;i++));do
    let tw=0 #totalwins
    let tl=0 #totallo
    for((j=0;j<g;j++));do
        tw=$((tw + w[$i,$j]))
        tl=$((tl + l[$i,$j]))
    done
    
    echo "${users[$i]},${tw},${w[$i,0]},${w[$i,1]},${w[$i,2]},${tl},${l[$i,0]},${l[$i,1]},${l[$i,2]}" >> count_of_games.csv 
done


sort -t "," -k2rn count_of_games.csv > a.csv
cat a.csv > count_of_games.csv
rm connect4.csv othello.csv tictactoe.csv 1.csv 2.csv 3.csv a.csv

