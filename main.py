import curses
import asyncio
from random import randint, choice

TIC_TIMEOUTS = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
STAR = '+'
NUOVA = ':'
SUN = '*'
STARS_AMOUNT = 150
MAX_ROW = 25
MAX_COL = 79


class Star:
    def __init__(self, canvas, row, col, sym):
        self.canvas = canvas
        self.row = row
        self.col = col
        self.sym = sym

    async def blink(self):
        while True:
            self.canvas.addstr(self.row, self.col, ' ', curses.A_DIM)
            self.canvas.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.canvas.addstr(self.row, self.col, self.sym, curses.A_NORMAL)
            self.canvas.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.canvas.addstr(self.row, self.col, self.sym, curses.A_BOLD)
            self.canvas.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.canvas.addstr(self.row, self.col, self.sym, curses.A_NORMAL)
            self.canvas.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0.1)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0.1)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0.1)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def draw(window):
    window.border()
    curses.curs_set(False)

    stars = [
        Star(window, randint(1, MAX_ROW), randint(1, MAX_COL), choice([STAR, NUOVA, SUN])).blink()
        for _ in range(STARS_AMOUNT)
    ]

    events = stars.copy()
    events.append(fire(window, 20, 20))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(events))
    loop.close()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
