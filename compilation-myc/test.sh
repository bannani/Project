./compil.sh test/test_operations_int.myc
echo -n -e "\e[1;37m test operations int ........"
./test/test_operations_int
if [ $? != 85 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_operations_float.myc
echo -n -e "\e[1;37m test operations float ......"
./test/test_operations_float
if [ $? != 4 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_if.myc
echo -n -e "\e[1;37m test if ...................."
./test/test_if
if [ $? != 20 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_if_else.myc
echo -n -e "\e[1;37m test if else ..............."
./test/test_if_else
if [ $? != 5 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_while.myc
echo -n -e "\e[1;37m test while ................."
./test/test_while
if [ $? != 15 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_while_++.myc
echo -n -e "\e[1;37m test while ++ .............."
./test/test_while_++
if [ $? != 11 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_while_if_else.myc
echo -n -e "\e[1;37m test while if else ........."
./test/test_while_if_else
if [ $? != 39 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_while_else_float.myc
echo -n -e "\e[1;37m test while if else float ..."
./test/test_while_else_float
if [ $? != 4 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_fonctions.myc
echo -n -e "\e[1;37m test fonction simple ......."
./test/test_fonctions
if [ $? != 12 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_fonction_float.myc
echo -n -e "\e[1;37m test fonction float ........"
./test/test_fonction_float
if [ $? != 18 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_fonction_num.myc
echo -n -e "\e[1;37m test fonction num .........."
./test/test_fonction_num
if [ $? != 2 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi

./compil.sh test/test_fonction_recursive.myc
echo -n -e "\e[1;37m test fonction recursive ...."
./test/test_fonction_recursive
if [ $? != 3 ]; then
    echo -e "\e[0;31m FAILED" 
else
    echo -e "\e[0;32m PASSED" 
fi