#!/usr/bin/env python3
"""Translate sentences in the dataset to Tagalog"""

from deep_translator import GoogleTranslator
import time
import sys

def translate_dataset(input_file, output_file):
    translator = GoogleTranslator(source='en', target='tl')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    translated_lines = []
    
    for i, line in enumerate(lines):
        parts = line.strip().split('\t')
        if len(parts) == 3:
            label, tag, sentence = parts
            
            # Translate the sentence to Tagalog
            try:
                translated_sentence = translator.translate(sentence)
                
                # Reconstruct the line with the same formatting
                translated_line = f"{label}\t{tag}\t{translated_sentence}\n"
                translated_lines.append(translated_line)
                
                # Print progress every 10 lines and flush output
                if (i + 1) % 10 == 0:
                    print(f"Translated {i + 1} / {len(lines)} lines...", flush=True)
                
                # Small delay to avoid rate limiting - reduced from 0.1 to 0.05
                time.sleep(0.05)
                
            except Exception as e:
                print(f"Error translating line {i+1}: {e}", file=sys.stderr, flush=True)
                # Keep original if translation fails
                translated_lines.append(line)
        else:
            # Keep line as-is if it doesn't have the expected format
            translated_lines.append(line)
        
        # Write intermediate results every 100 lines
        if (i + 1) % 100 == 0:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.writelines(translated_lines)
            print(f"Saved checkpoint at {i + 1} lines", flush=True)
    
    # Write the final translated content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(translated_lines)
    
    print(f"Translation complete! Saved to {output_file}", flush=True)

if __name__ == "__main__":
    input_file = "/home/jayo/repos/CS601R-004-Labs/data/subj_number_1000.txt"
    output_file = "/home/jayo/repos/CS601R-004-Labs/data/tagalog_subj_number_1000.txt"
    
    translate_dataset(input_file, output_file)
