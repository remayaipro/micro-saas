#!/usr/bin/env python3
"""JSON Formatter/Validator - CLI Tool for pretty-print, validate, minify JSON"""

import argparse
import json
import sys
import os

def format_json(input_data, output_data=None, indent=2, validate_only=False):
    """Format, validate, or minify JSON"""
    
    try:
        # Parse input (file or stdin)
        if input_data == '-':
            content = sys.stdin.read()
            data = json.loads(content) if content.strip() else {}
        elif os.path.isfile(input_data):
            with open(input_data, 'r') as f:
                data = json.load(f)
        else:
            # Try parsing as direct JSON string
            data = json.loads(input_data)
        
        # Validate only
        if validate_only:
            print("✓ Valid JSON")
            return 0
        
        # Pretty print (default)
        output = json.dumps(data, indent=indent, ensure_ascii=False)
        
        # Write to file or stdout
        if output_data:
            with open(output_data, 'w') as f:
                f.write(output)
            print(f"Formatted JSON saved to: {output_data}")
        else:
            print(output)
        
        # Print stats
        original_len = len(json.dumps(data))
        minified_len = len(json.dumps(data, separators=(',', ':')))
        print(f"\nStats: {original_len:,} chars -> minified: {minified_len:,} chars", file=sys.stderr)
        
        return 0
        
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def minify_json(input_data, output_data=None):
    """Minify JSON (remove whitespace)"""
    
    try:
        # Parse input
        if input_data == '-':
            content = sys.stdin.read()
            data = json.loads(content) if content.strip() else {}
        elif os.path.isfile(input_data):
            with open(input_data, 'r') as f:
                data = json.load(f)
        else:
            data = json.loads(input_data)
        
        # Minify
        output = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
        
        # Write output
        if output_data:
            with open(output_data, 'w') as f:
                f.write(output)
            print(f"Minified JSON saved to: {output_data}")
        else:
            print(output)
        
        return 0
        
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description='JSON Formatter/Validator')
    parser.add_argument('input', help='Input JSON file, string, or "-" for stdin')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-i', '--indent', type=int, default=2, help='Indent spaces (default: 2)')
    parser.add_argument('-m', '--minify', action='store_true', help='Minify JSON (remove whitespace)')
    parser.add_argument('-v', '--validate', action='store_true', help='Validate only, no output')
    
    args = parser.parse_args()
    
    if args.minify:
        return minify_json(args.input, args.output)
    else:
        return format_json(args.input, args.output, args.indent, args.validate)

if __name__ == '__main__':
    exit(main())