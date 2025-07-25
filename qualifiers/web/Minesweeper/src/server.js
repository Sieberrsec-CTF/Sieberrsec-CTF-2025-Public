const express = require('express');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');
const cookieParser = require('cookie-parser');
const app = express();
const PORT = 28576;

const ROWS = 8, COLS = 8, BOMBS = 10;
const games = {}; // uuid -> game state
const userBoards = {}; // uuid -> board state

const JWT_SECRET = (Math.floor(Math.random() * 999999) + 1).toString();
console.log(JWT_SECRET);

app.use(express.json());
app.use(express.static('public'));
app.use(cookieParser());

function generateBoard(rows, cols, bombs) {
    const realBoard = Array.from({ length: rows }, () =>
        Array.from({ length: cols }, () => ({ bomb: false, count: 0 }))
    );

    const userBoard = {};

    let placed = 0;
    while (placed < bombs) {
        let r = Math.floor(Math.random() * rows);
        let c = Math.floor(Math.random() * cols);
        if (!realBoard[r][c].bomb) {
            realBoard[r][c].bomb = true;
            placed++;
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    const nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols) {
                        realBoard[nr][nc].count += 1;
                    }
                }
            }
        }
    }

    return { realBoard, userBoard };
}

function getUUID(req, res, next) {
    const token = req.cookies.token;

    if (token) {
        try {
            const payload = jwt.verify(token, JWT_SECRET);
            req.uuid = payload.uuid;

            if (!games[req.uuid]) {
                const { realBoard, userBoard } = generateBoard(ROWS, COLS, BOMBS);
                games[req.uuid] = { realBoard, status: 'playing' };
                userBoards[req.uuid] = userBoard;
            }

            return next();
        } catch (err) {
            res.clearCookie('token');
            return res.status(403).json({ error: 'Invalid token' });
        }
    }

    const uuid = uuidv4();
    const newToken = jwt.sign({ uuid }, JWT_SECRET);
    req.uuid = uuid;

    const { realBoard, userBoard } = generateBoard(ROWS, COLS, BOMBS);
    games[uuid] = { realBoard, status: 'playing' };
    userBoards[uuid] = userBoard;

    res.cookie('token', newToken, {
        httpOnly: true,
        sameSite: 'Strict',
        secure: false
    });

    next();
}

app.get('/api/board', getUUID, (req, res) => {
    const game = games[req.uuid];
    let { realBoard, status, score } = game;
    const userBoard = userBoards[req.uuid];

    const returnedBoard = Array.from({ length: ROWS }, () =>
        Array.from({ length: COLS }, () => "")
    );

    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            const cellState = userBoard[y.toString() + x.toString()]; // updated
            if (cellState === "reveal") {
                returnedBoard[y][x] = realBoard[y][x].bomb ? '💣' : realBoard[y][x].count;
            } else if (cellState === "flagged") {
                returnedBoard[y][x] = '🚩';
            }
        }
    }

    score = score || 0;
    const flag = (score > 1_000_000_000_000) ? process.env.FLAG : null;

    res.json({ board: returnedBoard, status, score, flag });
});

app.post('/api/reveal', getUUID, (req, res) => {
    const { row, col, value } = req.body;
    const uuid = req.uuid;
    const game = games[uuid];

    const { realBoard } = game;

    const key = row.toString() + col.toString();
    userBoards[uuid][key] = value;
    console.log(uuid, key)

    if (value === 'reveal') {
        const cell = realBoard[row][col];
        if (cell.bomb) {
            game.status = 'lost';
        } else {
            let revealedCount = 0;
            for (let y = 0; y < ROWS; y++) {
                for (let x = 0; x < COLS; x++) {
                    const k = y.toString() + x.toString();
                    if (userBoards[uuid][k] === 'reveal') {
                        revealedCount++;
                    }
                }
            }

            const totalSafeCells = ROWS * COLS - BOMBS;
            if (revealedCount >= totalSafeCells) {
                game.status = 'won';
                if (typeof game.score !== 'number') {
                    game.score = 0;
                }
                game.score++;
            }
        }
    }

    res.json({ success: true });
});

app.post('/api/restart', getUUID, (req, res) => {
    const uuid = req.uuid;
    const { realBoard, userBoard } = generateBoard(ROWS, COLS, BOMBS);
    games[uuid] = { realBoard, status: 'playing' };
    userBoards[uuid] = userBoard;
    res.json({ status: 'restarted' });
});

app.listen(PORT, () => {
    console.log(`Minesweeper running on http://localhost:${PORT}`);
});
