in_dir=$1
out_dir=$2
out_file=$3

for i in `ls -d $in_dir*/`
do
    echo $i
    ./rename_files.sh $i
    base_dir=`basename $i`
    mkdir -p $out_dir$base_dir
    ./tv.sh $i $out_dir$base_dir/ $base_dir$out_file
done

cat `ls -d $out_dir*/*$out_file.csv` > $out_dir$out_file.csv
./mov-bar.py -i $out_dir$out_file.csv -o $out_dir$out_file