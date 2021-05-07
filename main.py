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
    def __init__(self, galaxy, row, col, sym):
        self.window = galaxy
        self.row = row
        self.col = col
        self.sym = sym

    async def blink(self):
        while True:
            self.window.addstr(self.row, self.col, ' ', curses.A_DIM)
            self.window.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.window.addstr(self.row, self.col, self.sym, curses.A_NORMAL)
            self.window.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.window.addstr(self.row, self.col, self.sym, curses.A_BOLD)
            self.window.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))

            self.window.addstr(self.row, self.col, self.sym, curses.A_NORMAL)
            self.window.refresh()
            await asyncio.sleep(choice(TIC_TIMEOUTS))


def draw(window):
    window.border()
    curses.curs_set(False)

    stars = [
        Star(window, randint(1, MAX_ROW), randint(1, MAX_COL), choice([STAR, NUOVA, SUN])).blink()
        for _ in range(STARS_AMOUNT)
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(stars))
    loop.close()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
