from scripts.pawn import Pawn, PawnConfig, PawnState

class PlayerPawn(Pawn):
    def __init__(self, data_provider, uid):
        init_x, init_y = data_provider.getPlayerInitialPos()
        config = PawnConfig(
            speed=2,
            damage=50,
            max_health=100,
            footprint_width=20,
            footprint_height=10,
            attack_distance=60,
            animations={
                PawnState.IDLE: "data/paladin_idle.json",
                PawnState.WALK: "data/paladin_walk.json",
                PawnState.ATTACK: "data/paladin_attack.json",
                PawnState.DIE: "data/paladin_die.json",
                PawnState.DMG: "data/paladin_damaged.json"
            }
        )
        super().__init__(data_provider, init_x, init_y, uid, config)

        # Movement flags controlled by PlayerController
        self.want_up = False
        self.want_down = False
        self.want_left = False
        self.want_right = False

    def Update(self):
        if (self.state == PawnState.DMG or self.state == PawnState.DIE):
            return

        if self.want_attack:
            if (self.state == PawnState.IDLE or self.state == PawnState.WALK):
                self.setState(PawnState.ATTACK)
                self.want_attack = False
    
        if (self.state == PawnState.IDLE or self.state == PawnState.WALK):
            dx = 0
            dy = 0
            if self.want_up: dy -= self.speed
            if self.want_down: dy += self.speed
            if self.want_right: dx += self.speed
            if self.want_left: dx -= self.speed

            new_x = self.pos_x + dx
            new_y = self.pos_y + dy

            if self.tryMove(new_x, new_y):
                self.data_provider.onPlayerMove(dx, dy)

            if abs(dx) > 0 or abs(dy) > 0:
                self.setState(PawnState.WALK)
            else:
                self.setState(PawnState.IDLE)

            if dx < 0:
                self.checkFlip(dx)
            elif dx > 0:
                self.checkFlip(dx)

    def onDeathComplete(self):
        """Player stays visible when dead but doesn't move"""
        self.view.running = False
        self.view.setLastFrame()  # Keep player visible in death pose