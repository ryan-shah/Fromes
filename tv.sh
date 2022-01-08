in_dir=$1
out_dir=$2
out_file=$3

counter=1
for i in `ls $in_dir`
do 
    name=$counter
    if [ $counter -lt 10 ]
    then
        name="0$counter"
    fi
    echo "Processing File $i"
    ./mov-bar.py -i $in_dir$i -o $out_dir$name.jpg -c -t 10 -r 1
    let counter++
done

echo "combining csv"

cat `ls $out_dir*.csv` > $out_dir$out_file.csv
./mov-bar.py -i $out_dir$out_file.csv -o $out_dir$out_file

echo "done"
