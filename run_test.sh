DarkGray='\033[1;30m'
Yellow='\033[1;33m'
NC='\033[0m' # No Color
for i in $(seq $1 $2)
do
    for j in $(seq $3 $4)
    do
        echo ===============================
        echo "${DarkGray}"public_test_data/0"$i"_"$j".lsp"${NC}"
        cat ../public_test_data/0"$i"_"$j".lsp
        echo "${Yellow}"
        python3 yacc.py ../public_test_data/0"$i"_"$j".lsp
        echo "${NC}"
    done
done

if [ $# -eq 5 ]
then
    for i in $(seq 1 $5)
    do
        for j in $(seq 1 2)
        do
            echo ===============================
            echo "${DarkGray}"public_test_data/b"$i"_"$j".lsp"${NC}"
            cat ../public_test_data/b"$i"_"$j".lsp
            echo "${Yellow}"
            python3 yacc.py ../public_test_data/b"$i"_"$j".lsp
            echo "${NC}"
        done
    done
fi