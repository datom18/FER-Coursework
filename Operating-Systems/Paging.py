import random, time

ADDRESS_SPACE = 1024
PAGE_SIZE = 64
PAGE_NUM = int(ADDRESS_SPACE / PAGE_SIZE)
FRAME_NUM = 5


def choose_frame():
    for i in range(PAGE_NUM):
        if frame[i].count(0) == len(frame[i]):
            return i
    return -1


def print_table():
    print("Translation table: ", end=" ")
    elements = []
    sorted_table = dict(sorted(translation_table.items(), key=lambda item: item[1]))
    for key, el in sorted_table.items():
        if el[1] != 0:
            elements.append(f"Page({key})=>Frame({'0x' + hex(el[0] * PAGE_SIZE)[2:].zfill(4)})")
    print(", ".join(elements))


disk = [[random.randint(0, 100) for j in range(PAGE_SIZE)] for i in range(PAGE_NUM)]
frame = [[0] * 64 for i in range(FRAME_NUM)]
frame_log = [None] * FRAME_NUM  # keeps track of which pages are currently in frames

translation_table = {}  # consists of key = logical page(=table index), and value = (frame number, validation bit)
for i in range(0, PAGE_NUM):
    translation_table.update({i: (-1, 0)})

t = 0
frame_index = 0

while 1:

    print("---------------------------------")
    print("Proces: 0")
    print(f"t: {t}")

    logical_address = random.randint(0, ADDRESS_SPACE - 1)
    ten_bits = logical_address & 0x3FF
    table_index = (ten_bits >> 6) & 0xF  # table index = logical page
    offset = ten_bits & 0x3F

    print(f"Logical address: {'0x' + hex(logical_address)[2:].zfill(4)} (Page: {table_index})")

    if translation_table.get(table_index)[1] == 0:
        print("Page miss!")

        if frame[frame_index].count(0) != len(frame[frame_index]):
            print(f"Removing page {frame_log[frame_index]} from frame {'0x' + hex(frame_index * PAGE_SIZE)[2:].zfill(4)}")
            translation_table[frame_log[frame_index]] = (-1, 0)

        for i in range(0, PAGE_SIZE):
            frame[frame_index][i] = disk[table_index][i]

        frame_log[frame_index] = table_index
        translation_table[table_index] = (frame_index, 1)

        physical_address = frame_index*PAGE_SIZE + offset
        print(f"Page {table_index} stored in frame: {'0x' + hex(frame_index * PAGE_SIZE)[2:].zfill(4)}")
        print(f"Physical address: {'0x' + hex(physical_address)[2:].zfill(4)}")

        frame_index += 1
        frame_index = frame_index % FRAME_NUM

    elif translation_table.get(table_index)[1] == 1:
        page_location = translation_table.get(table_index)[0]
        physical_address = page_location * PAGE_SIZE + offset
        print(f"Fetching data from physical address: {'0x' + hex(physical_address)[2:].zfill(4)}...")
        data = frame[page_location][offset]
        print(f"Data: {data}")

    t += 1
    print_table()
    time.sleep(1)











