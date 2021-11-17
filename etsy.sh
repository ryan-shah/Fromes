echo "Reading from: $1"
echo "Printing to: $2"
echo "10x25"
./mov-bar.py -i $1 -w 10 -l 25 -o $2-10x25.jpg
echo "12x30"
./mov-bar.py -i $1 -w 12 -l 30 -o $2-12x30.jpg
echo "12x36"
./mov-bar.py -i $1 -w 12 -l 36 -o $2-12x36.jpg
echo "16x40"
./mov-bar.py -i $1 -w 16 -l 40 -o $2-16x40.jpg
echo "Done"
