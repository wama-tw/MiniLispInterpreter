for i in $(seq $1 $2)
do
    # echo "$i"
    for j in $(seq $3 $4)
    do
        # echo "$j"
        echo ===============================
        echo public_test_data/0"$i"_"$j".lsp
        cat ../public_test_data/0"$i"_"$j".lsp
        echo 
        python3 yacc.py ../public_test_data/0"$i"_"$j".lsp
    done
done