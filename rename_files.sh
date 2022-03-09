in_dir=$1
for file in $in_dir*
do
    mv "$file" `echo "$file" | tr ' ' '_'`
done