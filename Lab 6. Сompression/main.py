from huffman import HuffmanCoding
import sys

if __name__ == "__main__":
    path = sys.argv[1]
    h = HuffmanCoding(path)
    print("Compressing...")
    output_path = h.compress()
    print(f"Compressed file:  {output_path}")
    print("Decompressing...")
    output_path = h.decompress(output_path)
    print(f"Decompressed file:  {output_path}")