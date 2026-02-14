#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aronasay - A CLI program like cowsay but with Arona from Blue Archive
Inspired by Momoisay by Mon4sm
FIXED VERSION - No scrolling, no freestyle
"""

import sys, os, textwrap, argparse, time, random

# Set UTF-8 encoding early
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Import art module (for local development only - install script embeds it)
try:
    from art import *
except ModuleNotFoundError:
    # Art module already embedded by install script
    pass

def create_speech_bubble(text, width=40):
    """Create a speech bubble for the given text."""
    lines = []
    for line in text.split('\n'):
        lines.extend(textwrap.wrap(line, width) if line else [''])

    if not lines:
        lines = ['']

    max_len = max(len(line) for line in lines)

    bubble = []
    bubble.append(' ' + '-' * (max_len + 2))

    if len(lines) == 1:
        bubble.append(f'< {lines[0].ljust(max_len)} >')
    else:
        for i, line in enumerate(lines):
            if i == 0:
                bubble.append(f'/ {line.ljust(max_len)} |')
            elif i == len(lines) - 1:
                bubble.append(f'\\ {line.ljust(max_len)} |')
            else:
                bubble.append(f'| {line.ljust(max_len)} |')

    bubble.append(' ' + '-' * (max_len + 2))
    return '\n'.join(bubble)


def combine_side_by_side(arona_art, speech_bubble, gap=2):
    """Combine Arona art and speech bubble side by side"""
    arona_lines = arona_art.split('\n')
    bubble_lines = speech_bubble.split('\n')

    # Get dimensions
    arona_width = max(len(line) for line in arona_lines) if arona_lines else 0
    arona_height = len(arona_lines)
    bubble_height = len(bubble_lines)

    # Calculate vertical position to center bubble with Arona
    # Center the bubble vertically
    bubble_start = max(0, (arona_height - bubble_height) // 2)

    # Create combined output
    result = []
    for i in range(max(arona_height, bubble_start + bubble_height)):
        # Arona part - CRITICAL: pad each line to arona_width for alignment
        if i < arona_height:
            arona_part = arona_lines[i].ljust(arona_width)
        else:
            arona_part = ' ' * arona_width

        # Bubble part
        if bubble_start <= i < bubble_start + bubble_height:
            bubble_part = bubble_lines[i - bubble_start]
        else:
            bubble_part = ''

        # Combine with gap
        result.append(arona_part + ' ' * gap + bubble_part)

    return '\n'.join(result)


def center_text(text):
    """Center text horizontally on the terminal"""
    import shutil
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80  # Default fallback
    
    lines = text.split('\n')
    if not lines:
        return text
    
    # Find the longest line
    max_line_width = max(len(line) for line in lines)
    
    # Calculate left padding to center
    padding = max(0, (terminal_width - max_line_width) // 2)
    
    # Add padding to each line
    centered_lines = [' ' * padding + line for line in lines]
    
    return '\n'.join(centered_lines)


def render_frame_line_by_line(frame_lines, start_row=0):
    """Render frame line by line with explicit cursor positioning to prevent scrolling"""
    for i, line in enumerate(frame_lines):
        # Move cursor to specific row and column 0
        sys.stdout.write(f"\033[{start_row + i};0H")
        # Write the line (clearing any leftover characters with spaces)
        sys.stdout.write(line)
    sys.stdout.flush()


def pad_frames_to_same_size(frames):
    """Pad all frames to same height and width, aligning from the BOTTOM"""
    # Strip trailing newlines
    clean_frames = [frame.rstrip('\n') for frame in frames]

    # Find max dimensions
    max_lines = 0
    max_width = 0

    frame_line_lists = []
    for frame in clean_frames:
        lines = frame.split('\n')
        frame_line_lists.append(lines)
        max_lines = max(max_lines, len(lines))
        for line in lines:
            max_width = max(max_width, len(line))

    # Pad all frames - IMPORTANT: Add padding at the TOP to align bottoms
    padded_frames = []
    for lines in frame_line_lists:
        # Calculate how many empty lines to add at the top
        lines_needed = max_lines - len(lines)
        
        padded_lines = []
        
        # Add empty lines at the TOP (this aligns the bottom)
        for _ in range(lines_needed):
            padded_lines.append(' ' * max_width)
        
        # Add the actual frame lines, padded to max_width
        for line in lines:
            padded_lines.append(line.ljust(max_width))

        padded_frames.append(padded_lines)

    return padded_frames


def arona_animated(version=1, delay=0.1, iterations=None):
    """Display animated Arona (infinite if iterations=None)"""
    import shutil
    
    frames = get_animation(version)

    # Pad all frames to same size
    padded_frames = pad_frames_to_same_size(frames)
    
    # Find max width and height of frames
    max_frame_width = len(padded_frames[0][0]) if padded_frames and padded_frames[0] else 0
    max_frame_height = len(padded_frames[0]) if padded_frames else 0

    # Hide cursor
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

    # Clear screen ONCE
    sys.stdout.write("\033[2J")
    sys.stdout.flush()
    
    # Store last terminal size to detect changes
    last_terminal_size = (0, 0)

    try:
        if iterations is None:
            # Infinite loop
            while True:
                for frame_lines in padded_frames:
                    # Recalculate position on each frame to handle terminal resize
                    try:
                        terminal_width = shutil.get_terminal_size().columns
                        terminal_height = shutil.get_terminal_size().lines
                        current_size = (terminal_width, terminal_height)
                        
                        # If terminal was resized, clear and recalculate
                        if current_size != last_terminal_size:
                            sys.stdout.write("\033[2J")  # Clear screen on resize
                            last_terminal_size = current_size
                    except:
                        terminal_width = 80
                        terminal_height = 24
                    
                    # Center horizontally
                    left_padding = max(0, (terminal_width - max_frame_width) // 2)
                    
                    # Position from BOTTOM - anchor bottom line at fixed position
                    bottom_margin = 2
                    start_row = max(1, terminal_height - max_frame_height - bottom_margin)
                    
                    # Render each line at its absolute position
                    for i, line in enumerate(frame_lines):
                        row = start_row + i
                        sys.stdout.write(f"\033[{row};{left_padding}H")
                        sys.stdout.write(line)
                    sys.stdout.flush()
                    time.sleep(delay)
        else:
            # Fixed iterations
            for _ in range(iterations):
                for frame_lines in padded_frames:
                    # Recalculate position on each frame to handle terminal resize
                    try:
                        terminal_width = shutil.get_terminal_size().columns
                        terminal_height = shutil.get_terminal_size().lines
                        current_size = (terminal_width, terminal_height)
                        
                        # If terminal was resized, clear and recalculate
                        if current_size != last_terminal_size:
                            sys.stdout.write("\033[2J")  # Clear screen on resize
                            last_terminal_size = current_size
                    except:
                        terminal_width = 80
                        terminal_height = 24
                    
                    # Center horizontally
                    left_padding = max(0, (terminal_width - max_frame_width) // 2)
                    
                    # Position from BOTTOM - anchor bottom line at fixed position
                    bottom_margin = 2
                    start_row = max(1, terminal_height - max_frame_height - bottom_margin)
                    
                    # Render each line at its absolute position
                    for i, line in enumerate(frame_lines):
                        row = start_row + i
                        sys.stdout.write(f"\033[{row};{left_padding}H")
                        sys.stdout.write(line)
                    sys.stdout.flush()
                    time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        # Get final terminal size for cleanup
        try:
            terminal_width = shutil.get_terminal_size().columns
            terminal_height = shutil.get_terminal_size().lines
        except:
            terminal_width = 80
            terminal_height = 24
            
        bottom_margin = 2
        start_row = max(1, terminal_height - max_frame_height - bottom_margin)
        
        # Clear the animation area
        for i in range(max_frame_height):
            row = start_row + i
            sys.stdout.write(f"\033[{row};0H")
            sys.stdout.write("\033[K")  # Clear line from cursor to end
        
        # Move cursor to bottom of screen and show cursor
        sys.stdout.write(f"\033[{terminal_height};0H")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        print()


def list_all_versions():
    """List all available versions"""
    versions = list_versions()

    print("\nAvailable Arona versions:")
    print("\nStatic versions:")
    for key in versions['static']:
        print(f"  {key}")

    print("\nAnimated versions:")
    for key in versions['animated']:
        print(f"  {key}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description='Aronasay - Make Arona say anything!',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aronasay "Hello World"              # Simple usage
  aronasay -v 2 "Custom message"      # Use specific version
  aronasay -a                         # Animated Arona (infinite)
  aronasay -a 2                       # Animated version 2 (infinite)
  aronasay -l                         # List all versions
        """
    )

    parser.add_argument('text', nargs='*', help='Text for Arona to say')
    parser.add_argument('-v', '--version', type=int, default=1,
                       help='Static version number (default: 1)')
    parser.add_argument('-a', '--animate', nargs='?', const=1, type=int,
                       help='Show animated Arona (infinite loop, Ctrl+C to stop)')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List all available versions')
    parser.add_argument('-w', '--width', type=int, default=40,
                       help='Width of speech bubble (default: 40)')

    args = parser.parse_args()

    # List versions
    if args.list:
        list_all_versions()
        return

    # Animated mode (INFINITE)
    if args.animate is not None:
        arona_animated(version=args.animate, iterations=None)
        return

    # Static mode with text
    text = ' '.join(args.text) if args.text else ''

    if text:
        bubble = create_speech_bubble(text, args.width)
        arona = get_static(args.version)

        # Combine Arona and bubble side by side
        combined = combine_side_by_side(arona, bubble)
        # Center the entire output horizontally
        centered = center_text(combined)
        print(centered)
    else:
        # No text, just show static Arona
        arona = get_static(args.version)
        # Center Arona horizontally
        centered = center_text(arona)
        print(centered)


if __name__ == '__main__':
    main()
