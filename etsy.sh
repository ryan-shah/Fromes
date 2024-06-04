echo "Reading from: $1"

if [ -z "$2" ]
    then 
        OUTFILE="${1%%.*}"
    else 
        OUTFILE="$2"
fi

echo "Printing to: $OUTFILE"

echo "10x25"
./mov-bar.py -i $1 -w 10 -l 25 -o $OUTFILE-10x25.jpg
echo "12x30"
./mov-bar.py -i $1 -w 12 -l 30 -o $OUTFILE-12x30.jpg
echo "12x36"
./mov-bar.py -i $1 -w 12 -l 36 -o $OUTFILE-12x36.jpg
echo "16x40"
./mov-bar.py -i $1 -w 16 -l 40 -o $OUTFILE-16x40.jpg
echo "Done"
