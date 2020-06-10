# compilation via notre compilateur
cat $1 | ./myc
# on récupère le nom du fichier pour les noms des output
filename=$(basename $1 | cut -d'.' -f1)
# on recolle les morceaux
echo "#include \"$filename.h\"" > test/$filename.c
cat fun.c >> test/$filename.c
cat main.c >> test/$filename.c
#rm main.c
#rm fun.c
mv main.h test/$filename.h

# compilation avec gcc
gcc -o test/$filename test/$filename.c