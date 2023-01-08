for i in {1..8}
do
    # echo "$i"
    for j in {1..2}
    do
        # echo "$j"
        echo 
        echo ===============================
        echo public_test_data/0"$i"_"$j".lsp
        cat ../public_test_data/0"$i"_"$j".lsp
        echo 
        python3 yacc.py ../public_test_data/0"$i"_"$j".lsp
    done
done