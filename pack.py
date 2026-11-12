import zlib, base64

def main():
    with open('engine.py', 'rb') as f:
        data = f.read()
    
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    compressed = compressor.compress(data) + compressor.flush()
    blob = base64.b85encode(compressed).decode('ascii')
    
    content = f"import zlib,base64;exec(zlib.decompress(base64.b85decode('{blob}'),-15))\n"
    
    with open('main.py', 'w', encoding='ascii') as f:
        f.write(content)
        
    size = len(content.encode('ascii'))
    print(f"main.py written. Size: {size} bytes")

if __name__ == '__main__':
    main()
