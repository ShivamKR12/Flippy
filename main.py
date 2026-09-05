import random, sys, pygame, time, copy, os
from pygame.locals import *


class Flippy:
    # Game constants
    FPS = 10
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    SPACESIZE = 50
    BOARDWIDTH = 8
    BOARDHEIGHT = 8
    WHITE_TILE = 'WHITE_TILE'
    BLACK_TILE = 'BLACK_TILE'
    EMPTY_SPACE = 'EMPTY_SPACE'
    HINT_TILE = 'HINT_TILE'
    ANIMATIONSPEED = 25
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 155, 0)
    BRIGHTBLUE = (0, 50, 255)
    BROWN = (174, 94, 0)

    TEXTBGCOLOR1 = BRIGHTBLUE
    TEXTBGCOLOR2 = GREEN
    GRIDLINECOLOR = BLACK
    TEXTCOLOR = WHITE
    HINTCOLOR = BROWN

    def __init__(self):
        pygame.init()
        self.main_clock = pygame.time.Clock()
        self.display_surf = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
        pygame.display.set_caption('flippy')

        logo = pygame.image.load(self.resource_path('flippylogo.png'))
        pygame.display.set_icon(logo)

        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.big_font = pygame.font.Font('freesansbold.ttf', 32)

        board_image = pygame.image.load(self.resource_path('flippyboard.png'))
        board_image = pygame.transform.smoothscale(board_image, (self.BOARDWIDTH * self.SPACESIZE, self.BOARDHEIGHT * self.SPACESIZE))
        self.board_image_rect = board_image.get_rect()
        self.board_image_rect.topleft = (self.XMARGIN, self.YMARGIN)

        self.bg_image = pygame.image.load(self.resource_path('flippybackground.png'))
        self.bg_image = pygame.transform.smoothscale(self.bg_image, (self.WINDOWWIDTH, self.WINDOWHEIGHT))
        self.bg_image.blit(board_image, self.board_image_rect)

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def start(self):
        while True:
            if not self.run_game():
                break
        self.terminate()

    def get_space_clicked(self, mousex, mousey):
        x = (mousex - self.XMARGIN) // self.SPACESIZE
        y = (mousey - self.YMARGIN) // self.SPACESIZE
        if self.is_on_board(x, y):
            return (x, y)
        return None

    def draw_info(self, board_to_draw, player_tile, computer_tile, turn):
        scores = self.get_score_of_board(board_to_draw)
        player_score = scores[player_tile]
        computer_score = scores[computer_tile]

        player_text = f'Player: {player_score}'
        computer_text = f'Computer: {computer_score}'
        turn_text = f'Turn: {turn.capitalize()}'

        player_surf = self.font.render(player_text, True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        player_rect = player_surf.get_rect()
        player_rect.topleft = (self.WINDOWWIDTH - 120, 70)

        computer_surf = self.font.render(computer_text, True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        computer_rect = computer_surf.get_rect()
        computer_rect.topleft = (self.WINDOWWIDTH - 120, 90)

        turn_surf = self.font.render(turn_text, True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        turn_rect = turn_surf.get_rect()
        turn_rect.topleft = (self.WINDOWWIDTH - 120, 110)

        self.display_surf.blit(player_surf, player_rect)
        self.display_surf.blit(computer_surf, computer_rect)
        self.display_surf.blit(turn_surf, turn_rect)

    def get_computer_move(self, main_board, computer_tile):
        valid_moves = self.get_valid_moves(main_board, computer_tile)
        if valid_moves:
            return random.choice(valid_moves)
        return None

    def run_game(self):
        main_board = self.get_new_board()
        self.reset_board(main_board)
        show_hints = False
        turn = random.choice(['computer', 'player'])
        consecutive_passes = 0

        self.draw_board(main_board)
        player_tile, computer_tile = self.enter_player_tile()

        new_game_surf = self.font.render('New Game', True, self.TEXTCOLOR, self.TEXTBGCOLOR2)
        new_game_rect = new_game_surf.get_rect()
        new_game_rect.topright = (self.WINDOWWIDTH - 8, 10)

        hints_surf = self.font.render('Hints', True, self.TEXTCOLOR, self.TEXTBGCOLOR2)
        hints_rect = hints_surf.get_rect()
        hints_rect.topright = (self.WINDOWWIDTH - 8, 40)

        while True:
            if turn == 'player':
                valid_moves = self.get_valid_moves(main_board, player_tile)
                if valid_moves:
                    consecutive_passes = 0
                    movexy = None
                    while movexy is None:
                        if show_hints:
                            board_to_draw = self.get_board_with_valid_moves(main_board, player_tile)
                        else:
                            board_to_draw = main_board

                        self.check_for_quit()

                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                mousex, mousey = event.pos
                                if new_game_rect.collidepoint((mousex, mousey)):
                                    return True
                                elif hints_rect.collidepoint((mousex, mousey)):
                                    show_hints = not show_hints
                                
                                movexy = self.get_space_clicked(mousex, mousey)
                                if movexy is not None and not self.is_valid_move(main_board, player_tile, movexy[0], movexy[1]):
                                    movexy = None

                        self.draw_board(board_to_draw)
                        self.draw_info(board_to_draw, player_tile, computer_tile, turn)
                        self.display_surf.blit(new_game_surf, new_game_rect)
                        self.display_surf.blit(hints_surf, hints_rect)
                        self.main_clock.tick(self.FPS)
                        pygame.display.update()

                    self.make_move(main_board, player_tile, movexy[0], movexy[1], True, main_board)
                    turn = 'computer'
                else:
                    consecutive_passes += 1
                    turn = 'computer'
            else:
                valid_moves = self.get_valid_moves(main_board, computer_tile)
                if valid_moves:
                    consecutive_passes = 0
                    self.draw_board(main_board)
                    self.draw_info(main_board, player_tile, computer_tile, turn)
                    self.display_surf.blit(new_game_surf, new_game_rect)
                    self.display_surf.blit(hints_surf, hints_rect)
                    pygame.display.update()
                    time.sleep(random.randint(5, 15) * 0.1)
                    x, y = self.get_computer_move(main_board, computer_tile)
                    self.make_move(main_board, computer_tile, x, y, True, main_board)
                    turn = 'player'
                else:
                    consecutive_passes += 1
                    turn = 'player'

            if consecutive_passes >= 2:
                break

        self.draw_board(main_board)
        self.draw_info(main_board, player_tile, computer_tile, turn)
        scores = self.get_score_of_board(main_board)

        if scores[player_tile] > scores[computer_tile]:
            text = 'You beat the computer by %s points! Congratulations!' % (scores[player_tile] - scores[computer_tile])
        elif scores[player_tile] < scores[computer_tile]:
            text = 'You lost. The computer beat you by %s points.' % (scores[computer_tile] - scores[player_tile])
        else:
            text = 'The game was a tie!'

        text_surf = self.font.render(text, True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2))
        self.display_surf.blit(text_surf, text_rect)

        text2_surf = self.big_font.render('Play again?', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        text2_rect = text2_surf.get_rect()
        text2_rect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2) + 50)

        yes_surf = self.big_font.render('Yes', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        yes_rect = yes_surf.get_rect()
        yes_rect.center = (int(self.WINDOWWIDTH / 2) - 60, int(self.WINDOWHEIGHT / 2) + 90)

        no_surf = self.big_font.render('No', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        no_rect = no_surf.get_rect()
        no_rect.center = (int(self.WINDOWWIDTH / 2) + 60, int(self.WINDOWHEIGHT / 2) + 90)

        while True:
            self.check_for_quit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if yes_rect.collidepoint((mousex, mousey)):
                        return True
                    elif no_rect.collidepoint((mousex, mousey)):
                        return False

            self.display_surf.blit(text_surf, text_rect)
            self.display_surf.blit(text2_surf, text2_rect)
            self.display_surf.blit(yes_surf, yes_rect)
            self.display_surf.blit(no_surf, no_rect)
            pygame.display.update()
            self.main_clock.tick(self.FPS)

    def translate_board_to_pixel_coord(self, x, y):
        return self.XMARGIN + x * self.SPACESIZE + int(self.SPACESIZE / 2), self.YMARGIN + y * self.SPACESIZE + int(self.SPACESIZE / 2)

    def animate_tile_change(self, tiles_to_flip, tile_color, additional_tile, main_board):
        if tile_color == self.WHITE_TILE:
            additional_tile_color = self.WHITE
        else:
            additional_tile_color = self.BLACK

        additional_tile_x, additional_tile_y = self.translate_board_to_pixel_coord(additional_tile[0], additional_tile[1])
        pygame.draw.circle(self.display_surf, additional_tile_color, (additional_tile_x, additional_tile_y), int(self.SPACESIZE / 2) - 4)
        pygame.display.update()
        self.main_clock.tick(self.ANIMATIONSPEED)

        for rgb_values in range(0, 255, int(self.ANIMATIONSPEED * 2.55)):
            if tile_color == self.WHITE_TILE:
                color = tuple([rgb_values] * 3)
            elif tile_color == self.BLACK_TILE:
                color = tuple([255 - rgb_values] * 3)

            for x, y in tiles_to_flip:
                centerx, centery = self.translate_board_to_pixel_coord(x, y)
                pygame.draw.circle(self.display_surf, color, (centerx, centery), int(self.SPACESIZE / 2) - 4)

            pygame.draw.circle(self.display_surf, additional_tile_color, (additional_tile_x, additional_tile_y), int(self.SPACESIZE / 2) - 4)
            self.draw_board(main_board)
            pygame.display.update()
            self.main_clock.tick(self.ANIMATIONSPEED)
            self.check_for_quit()

    def draw_board(self, board):
        self.display_surf.blit(self.bg_image, self.bg_image.get_rect())

        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                centerx, centery = self.translate_board_to_pixel_coord(x, y)
                if board[x][y] == self.WHITE_TILE or board[x][y] == self.BLACK_TILE:
                    tile_color = self.WHITE if board[x][y] == self.WHITE_TILE else self.BLACK
                    pygame.draw.circle(self.display_surf, tile_color, (centerx, centery), int(self.SPACESIZE / 2) - 4)
                if board[x][y] == self.HINT_TILE:
                    pygame.draw.rect(self.display_surf, self.HINTCOLOR, (centerx - 4, centery - 4, 8, 8))

        for x in range(self.BOARDWIDTH + 1):
            startx = (x * self.SPACESIZE) + self.XMARGIN
            starty = self.YMARGIN
            endx = (x * self.SPACESIZE) + self.XMARGIN
            endy = self.YMARGIN + (self.BOARDHEIGHT * self.SPACESIZE)
            pygame.draw.line(self.display_surf, self.GRIDLINECOLOR, (startx, starty), (endx, endy))

        for y in range(self.BOARDHEIGHT + 1):
            startx = self.XMARGIN
            starty = (y * self.SPACESIZE) + self.YMARGIN
            endx = self.XMARGIN + (self.BOARDWIDTH * self.SPACESIZE)
            endy = (y * self.SPACESIZE) + self.YMARGIN
            pygame.draw.line(self.display_surf, self.GRIDLINECOLOR, (startx, starty), (endx, endy))

    def get_new_board(self):
        board = []
        for _ in range(self.BOARDWIDTH):
            board.append([self.EMPTY_SPACE] * self.BOARDHEIGHT)
        return board

    def reset_board(self, board):
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                board[x][y] = self.EMPTY_SPACE
        
        board[3][3] = self.WHITE_TILE
        board[3][4] = self.BLACK_TILE
        board[4][3] = self.BLACK_TILE
        board[4][4] = self.WHITE_TILE

    def get_score_of_board(self, board):
        xscore = 0
        oscore = 0
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                if board[x][y] == self.WHITE_TILE:
                    xscore += 1
                if board[x][y] == self.BLACK_TILE:
                    oscore += 1
        return {self.WHITE_TILE: xscore, self.BLACK_TILE: oscore}

    def enter_player_tile(self):
        text_surf = self.font.render('Do you want to be white or black?', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(self.WINDOWWIDTH / 2), int(self.WINDOWHEIGHT / 2))

        x_surf = self.big_font.render('White', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        x_rect = x_surf.get_rect()
        x_rect.center = (int(self.WINDOWWIDTH / 2) - 60, int(self.WINDOWHEIGHT / 2) + 40)

        o_surf = self.big_font.render('Black', True, self.TEXTCOLOR, self.TEXTBGCOLOR1)
        o_rect = o_surf.get_rect()
        o_rect.center = (int(self.WINDOWWIDTH / 2) + 60, int(self.WINDOWHEIGHT / 2) + 40)

        while True:
            self.check_for_quit()
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    if x_rect.collidepoint((mousex, mousey)):
                        return [self.WHITE_TILE, self.BLACK_TILE]
                    elif o_rect.collidepoint((mousex, mousey)):
                        return [self.BLACK_TILE, self.WHITE_TILE]

            self.display_surf.blit(text_surf, text_rect)
            self.display_surf.blit(x_surf, x_rect)
            self.display_surf.blit(o_surf, o_rect)
            pygame.display.update()
            self.main_clock.tick(self.FPS)

    def make_move(self, board, tile, xstart, ystart, real_move=False, main_board=None):
        tiles_to_flip = self.is_valid_move(board, tile, xstart, ystart)
        if not tiles_to_flip:
            return False

        board[xstart][ystart] = tile
        if real_move:
            self.animate_tile_change(tiles_to_flip, tile, (xstart, ystart), main_board if main_board is not None else board)
            for x, y in tiles_to_flip:
                board[x][y] = tile
        return True

    def is_valid_move(self, board, tile, xstart, ystart):
        if board[xstart][ystart] != self.EMPTY_SPACE or not self.is_on_board(xstart, ystart):
            return False

        board[xstart][ystart] = tile
        other_tile = self.get_opponent_tile(tile)
        tiles_to_flip = []

        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection

            if self.is_on_board(x, y) and board[x][y] == other_tile:
                x += xdirection
                y += ydirection
                if not self.is_on_board(x, y):
                    continue

                while board[x][y] == other_tile:
                    x += xdirection
                    y += ydirection
                    if not self.is_on_board(x, y):
                        break

                if not self.is_on_board(x, y):
                    continue

                if board[x][y] == tile:
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tiles_to_flip.append([x, y])

        board[xstart][ystart] = self.EMPTY_SPACE
        if len(tiles_to_flip) == 0:
            return False
        return tiles_to_flip

    def is_on_board(self, x, y):
        return x >= 0 and x < self.BOARDWIDTH and y >= 0 and y < self.BOARDHEIGHT

    def get_board_with_valid_moves(self, board, tile):
        dupe_board = copy.deepcopy(board)
        for x, y in self.get_valid_moves(dupe_board, tile):
            dupe_board[x][y] = self.HINT_TILE
        return dupe_board

    def get_valid_moves(self, board, tile):
        valid_moves = []
        for x in range(self.BOARDWIDTH):
            for y in range(self.BOARDHEIGHT):
                if self.is_valid_move(board, tile, x, y):
                    valid_moves.append((x, y))
        return valid_moves

    def get_opponent_tile(self, tile):
        if tile == self.WHITE_TILE:
            return self.BLACK_TILE
        return self.WHITE_TILE

    def check_for_quit(self):
        for event in pygame.event.get(QUIT):
            self.terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.terminate()
            else:
                pygame.event.post(event)

    def terminate(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Flippy()
    game.start()
