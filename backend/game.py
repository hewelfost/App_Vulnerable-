import random

class PongGame:
    def __init__(self, width=400, height=300, paddle_height=60, paddle_width=10, ball_size=10):
        self.width = width
        self.height = height
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width
        self.ball_size = ball_size
        self.reset()

    def reset(self):
        self.paddle1_y = self.height / 2 - self.paddle_height / 2
        self.paddle2_y = self.height / 2 - self.paddle_height / 2
        self.score1 = 0
        self.score2 = 0
        self._reset_ball()

    def _reset_ball(self):
        self.ball_x = self.width / 2
        self.ball_y = self.height / 2
        self.ball_vx = random.choice([-4, 4])
        self.ball_vy = random.choice([-3, 3])

    def move_paddle(self, player, direction, step=15):
        delta = -step if direction == "up" else step
        if player == 1:
            self.paddle1_y = min(max(self.paddle1_y + delta, 0), self.height - self.paddle_height)
        else:
            self.paddle2_y = min(max(self.paddle2_y + delta, 0), self.height - self.paddle_height)

    def update(self):
        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        if self.ball_y <= 0 or self.ball_y >= self.height:
            self.ball_vy *= -1

        if self.ball_x <= self.paddle_width:
            if self.paddle1_y <= self.ball_y <= self.paddle1_y + self.paddle_height:
                self.ball_vx *= -1
            else:
                self.score2 += 1
                self._reset_ball()

        if self.ball_x >= self.width - self.paddle_width:
            if self.paddle2_y <= self.ball_y <= self.paddle2_y + self.paddle_height:
                self.ball_vx *= -1
            else:
                self.score1 += 1
                self._reset_ball()

        return self.state()

    def state(self):
        return {
            "width": self.width, "height": self.height,
            "paddle_height": self.paddle_height, "paddle_width": self.paddle_width,
            "ball_size": self.ball_size,
            "paddle1_y": self.paddle1_y, "paddle2_y": self.paddle2_y,
            "ball_x": self.ball_x, "ball_y": self.ball_y,
            "score1": self.score1, "score2": self.score2,
        }