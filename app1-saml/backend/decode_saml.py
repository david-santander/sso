#!/usr/bin/env python3
import base64
import zlib
import xml.dom.minidom
from urllib.parse import unquote

def decode_saml_request(encoded_string):
    """Decode a SAML request that is base64 encoded and compressed"""
    
    # First, decode from base64
    try:
        decoded = base64.b64decode(encoded_string)
        print("✓ Base64 decoded successfully")
        print(f"  Decoded length: {len(decoded)} bytes")
    except Exception as e:
        print(f"✗ Base64 decode failed: {e}")
        return None
    
    # Try different decompression methods
    decompression_methods = [
        ("zlib with -15 wbits (raw deflate)", lambda d: zlib.decompress(d, -15)),
        ("zlib default", lambda d: zlib.decompress(d)),
        ("zlib with 16 wbits (gzip)", lambda d: zlib.decompress(d, 16)),
        ("zlib with -8 wbits", lambda d: zlib.decompress(d, -8)),
        ("zlib with 32 wbits (auto-detect)", lambda d: zlib.decompress(d, 32)),
    ]
    
    decompressed = None
    successful_method = None
    
    for method_name, decompress_func in decompression_methods:
        try:
            decompressed = decompress_func(decoded)
            print(f"\n✓ Decompression successful with: {method_name}")
            print(f"  Decompressed length: {len(decompressed)} bytes")
            successful_method = method_name
            break
        except Exception as e:
            print(f"✗ {method_name} failed: {type(e).__name__}")
    
    if decompressed is None:
        print("\n✗ All decompression methods failed")
        return None
    
    # Try to decode as UTF-8
    try:
        xml_string = decompressed.decode('utf-8')
        print("✓ UTF-8 decode successful")
    except Exception as e:
        print(f"✗ UTF-8 decode failed: {e}")
        return None
    
    # Pretty print XML
    try:
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml = dom.toprettyxml(indent="  ")
        
        # Remove empty lines
        lines = pretty_xml.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        pretty_xml = '\n'.join(non_empty_lines)
        
        return pretty_xml, successful_method
    except Exception as e:
        print(f"✗ XML parsing failed: {e}")
        print("\nRaw decompressed content:")
        print(xml_string)
        return xml_string, successful_method


def main():
    encoded_saml = """fVNNj9owFLzvr4hyZ+2QEIgFkSj0A4lCBOkeeqkc51GsOnZqO13672tnoctKLLlYGs/Me/P8MjW0ES2Zd/Yod/C7A2MfguDUCGlIfzULOy2JooYbImkDhlhG9vOvazJ8xKTVyiqmRPhGdF9DjQFtuZJetFrOwu3m43r7ebX5McFZCng0ytIkPWQRHqcpJFFC4yrOsojBsKrGdZKMvfAJtHEes9BZ9kbGdLCSxlJpHYiHowEeDYZpicckjgmOv3vW0uXjktpeebS2JQgJxag4KmPJBE8w0kBFY5AxatAqhi4JkQ/mLYoz8IHLmsuf97NWLyRDvpRlMSi2+9JbzC8TWChpugb0HvQfzuDbbn2jqxhj3FdHDhEVZb/C3JkEwdSDpA+u85uyKbqmvIpasnGtrpaFEpz97XH/fVK6ofb9RNFj1CO8Hhx6KumkaYHxA4c6/G8zF0I9L9wcLcxCqzsIA/Sm+HnRoO7Xzg3BwskGC9W0VHPjnwZOlNlzzNeo1/SFcHu0g0N+d9UYYZ7n4MIdz0rX/vmAudqlpq55pe15SDfNX7pGd9rOHy7X1/9Q/g8="""
    
    print("SAML Request Decoder")
    print("=" * 60)
    print(f"\nInput length: {len(encoded_saml)} characters")
    print("\nDecoding process:")
    print("-" * 40)
    
    result = decode_saml_request(encoded_saml.strip())
    
    if result:
        pretty_xml, method = result
        print("\n" + "=" * 60)
        print(f"Successfully decoded using: {method}")
        print("=" * 60)
        print("\nDecoded SAML Request (XML):")
        print("-" * 60)
        print(pretty_xml)
    else:
        print("\n✗ Failed to decode SAML request")


if __name__ == "__main__":
    main()