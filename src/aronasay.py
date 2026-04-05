#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aronasay - A CLI program like cowsay but with Arona from Blue Archive
Inspired by Momoisay by Mon4sm
Match Momoisay behavior, including clipping
"""

import sys
import textwrap
import argparse
import time

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from art import *
except ModuleNotFoundError:
    pass


def strip_ansi_codes(text):
    import re
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def get_visible_length(text):
    return len(strip_ansi_codes(text))


def visible_ljust(text, width):
    visible = get_visible_length(text)
    if visible >= width:
        return text
    return text + ' ' * (width - visible)


def create_speech_bubble(text, width=40):
    lines = []
    for line in text.split('\n'):
        if line:
            if get_visible_length(line) <= width:
                lines.append(line)
            else:
                clean_line = strip_ansi_codes(line)
                wrapped = textwrap.wrap(clean_line, width) if clean_line else ['']
                lines.extend(wrapped)
        else:
            lines.append('')

    if not lines:
        lines = ['']

    max_len = max(get_visible_length(line) for line in lines)

    bubble = []
    bubble.append(' ' + '-' * (max_len + 2))

    if len(lines) == 1:
        visible_len = get_visible_length(lines[0])
        padding = ' ' * (max_len - visible_len)
        bubble.append(f'< {lines[0]}{padding} >')
    else:
        for i, line in enumerate(lines):
            visible_len = get_visible_length(line)
            padding = ' ' * (max_len - visible_len)
            if i == 0:
                bubble.append(f'/ {line}{padding} \\')
            elif i == len(lines) - 1:
                bubble.append(f'\\ {line}{padding} /')
            else:
                bubble.append(f'| {line}{padding} |')

    bubble.append(' ' + '-' * (max_len + 2))
    return '\n'.join(bubble)


def combine_side_by_side(arona_art, speech_bubble, gap=2):
    arona_lines = arona_art.split('\n')
    bubble_lines = speech_bubble.split('\n')

    arona_width = max(get_visible_length(line) for line in arona_lines) if arona_lines else 0
    arona_height = len(arona_lines)
    bubble_height = len(bubble_lines)

    bubble_start = max(0, (arona_height - bubble_height) // 2)

    total_height = max(arona_height, bubble_start + bubble_height)
    result = []

    for i in range(total_height):
        if i < arona_height:
            arona_part = visible_ljust(arona_lines[i], arona_width)
        else:
            arona_part = ' ' * arona_width

        if bubble_start <= i < bubble_start + bubble_height:
            bubble_part = bubble_lines[i - bubble_start]
        else:
            bubble_part = ''

        result.append(arona_part + ' ' * gap + bubble_part)

    return '\n'.join(result)


def center_text(text):
    import shutil
    try:
        terminal_width = shutil.get_terminal_size().columns
    except:
        terminal_width = 80

    lines = text.split('\n')
    if not lines:
        return text

    max_line_width = max(get_visible_length(line) for line in lines)
    padding = max(0, (terminal_width - max_line_width) // 2)

    return '\n'.join(' ' * padding + line for line in lines)


def pad_frames_to_same_size(frames):
    """Pad frames to same width/height while aligning bottoms (feet planted)."""
    clean_frames = [frame.strip('\n') for frame in frames]

    max_lines = 0
    max_width = 0
    frame_line_lists = []

    for frame in clean_frames:
        lines = frame.split('\n')
        frame_line_lists.append(lines)
        max_lines = max(max_lines, len(lines))
        for line in lines:
            max_width = max(max_width, get_visible_length(line))

    padded_frames = []
    for lines in frame_line_lists:
        lines_needed = max_lines - len(lines)
        padded_lines = []

        # top padding => bottom aligned
        for _ in range(lines_needed):
            padded_lines.append(' ' * max_width)

        for line in lines:
            padded_lines.append(visible_ljust(line, max_width))

        padded_frames.append(padded_lines)

    return padded_frames


def parse_animate_args(values):
    version = 1
    text_words = []

    if not values:
        return version, text_words

    if values[0].isdigit():
        version = int(values[0])
        text_words = values[1:]
    else:
        text_words = values

    return version, text_words


def arona_animated(version=1, text='', width=40, delay=0.1, iterations=None):
    import shutil

    raw_frames = get_animation(version)

    # normalize art first so the bubble stays fixed
    normalized_art_frames = ['\n'.join(lines) for lines in pad_frames_to_same_size(raw_frames)]

    if text:
        bubble = create_speech_bubble(text, width)
        frames = [combine_side_by_side(frame, bubble) for frame in normalized_art_frames]
    else:
        frames = normalized_art_frames

    # normalize final output too
    padded_frames = pad_frames_to_same_size(frames)

    max_frame_height = len(padded_frames[0]) if padded_frames else 0
    max_frame_width = 0
    if padded_frames:
        for line in padded_frames[0]:
            max_frame_width = max(max_frame_width, get_visible_length(line))

    sys.stdout.write("\033[?25l")
    sys.stdout.write("\033[2J")
    sys.stdout.flush()

    try:
        if iterations is None:
            while True:
                for frame_lines in padded_frames:
                    try:
                        terminal_width = shutil.get_terminal_size().columns
                        terminal_height = shutil.get_terminal_size().lines
                    except:
                        terminal_width = 80
                        terminal_height = 24

                    left_padding = max(0, (terminal_width - max_frame_width) // 2)
                    start_row = max(1, (terminal_height - max_frame_height) // 2)

                    # clear animation region
                    for i in range(max_frame_height):
                        row = start_row + i
                        if row > terminal_height:
                            break
                        sys.stdout.write(f"\033[{row};1H")
                        sys.stdout.write("\033[K")

                    # draw current frame
                    for i, line in enumerate(frame_lines):
                        row = start_row + i
                        if row > terminal_height:
                            break
                        sys.stdout.write(f"\033[{row};{left_padding + 1}H")
                        sys.stdout.write(line)

                    sys.stdout.flush()
                    time.sleep(delay)
        else:
            for _ in range(iterations):
                for frame_lines in padded_frames:
                    try:
                        terminal_width = shutil.get_terminal_size().columns
                        terminal_height = shutil.get_terminal_size().lines
                    except:
                        terminal_width = 80
                        terminal_height = 24

                    left_padding = max(0, (terminal_width - max_frame_width) // 2)
                    start_row = max(1, (terminal_height - max_frame_height) // 2)

                    # clear animation region
                    for i in range(max_frame_height):
                        row = start_row + i
                        if row > terminal_height:
                            break
                        sys.stdout.write(f"\033[{row};1H")
                        sys.stdout.write("\033[K")

                    # draw current frame
                    for i, line in enumerate(frame_lines):
                        row = start_row + i
                        if row > terminal_height:
                            break
                        sys.stdout.write(f"\033[{row};{left_padding + 1}H")
                        sys.stdout.write(line)

                    sys.stdout.flush()
                    time.sleep(delay)

    except KeyboardInterrupt:
        pass
    finally:
        try:
            terminal_height = __import__('shutil').get_terminal_size().lines
        except:
            terminal_height = 24

        start_row = max(1, (terminal_height - max_frame_height) // 2)

        for i in range(max_frame_height):
            row = start_row + i
            if row > terminal_height:
                break
            sys.stdout.write(f"\033[{row};1H")
            sys.stdout.write("\033[K")

        sys.stdout.write(f"\033[{terminal_height};1H")
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
        print()


def list_all_versions():
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
  aronasay "Hello World"
  aronasay -v 2 "Custom message"
  aronasay -a
  aronasay -a hello world
  aronasay -a 1 hello world
  aronasay -l
        """
    )

    parser.add_argument('text', nargs='*', help='Text for Arona to say')
    parser.add_argument('-v', '--version', type=int, default=1,
                        help='Static version number (default: 1)')
    parser.add_argument('-a', '--animate', nargs='*',
                        help='Animated Arona: optionally give version first, then text')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List all available versions')
    parser.add_argument('-w', '--width', type=int, default=40,
                        help='Width of speech bubble (default: 40)')

    args = parser.parse_args()

    if args.list:
        list_all_versions()
        return

    if args.animate is not None:
        version, text_words = parse_animate_args(args.animate)

        if not sys.stdin.isatty():
            stdin_text = sys.stdin.read().strip()
        else:
            stdin_text = ''

        arg_text = ' '.join(text_words).strip()
        text = stdin_text or arg_text

        arona_animated(version=version, text=text, width=args.width, iterations=None)
        return

    if not sys.stdin.isatty():
        text = sys.stdin.read().strip()
    else:
        text = ' '.join(args.text) if args.text else ''

    if text:
        bubble = create_speech_bubble(text, args.width)
        arona = get_static(args.version).strip('\n')
        combined = combine_side_by_side(arona, bubble)
        centered = center_text(combined)
        print(centered)
    else:
        arona = get_static(args.version).strip('\n')
        centered = center_text(arona)
        print(centered)


if __name__ == '__main__':
    main()
