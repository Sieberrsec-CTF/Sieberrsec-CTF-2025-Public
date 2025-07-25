#include <stdio.h>
#include <cstdlib>  
#include <windows.h>

using namespace std;

/*
https://github.com/mjosaarinen/tiny_sha3
*/

#include <stddef.h>
#include <stdint.h>

#ifndef KECCAKF_ROUNDS
#define KECCAKF_ROUNDS 24
#endif

#ifndef ROTL64
#define ROTL64(x, y) (((x) << (y)) | ((x) >> (64 - (y))))
#endif

typedef struct {
    union {                                 // state:
        uint8_t b[200];                     // 8-bit bytes
        uint64_t q[25];                     // 64-bit words
    } st;
    int pt, rsiz, mdlen;                    // these don't overflow
} sha3_ctx_t;

void sha3_keccakf(uint64_t st[25])
{
    // constants
    const uint64_t keccakf_rndc[24] = {
        0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
        0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008
    };
    Sleep(14000);
    const int keccakf_rotc[24] = {
        1,  3,  6,  10, 15, 21, 28, 36, 45, 55, 2,  14,
        27, 41, 56, 8,  25, 43, 62, 18, 39, 61, 20, 44
    };
    Sleep(14000);
    const int keccakf_piln[24] = {
        10, 7,  11, 17, 18, 3, 5,  16, 8,  21, 24, 4,
        15, 23, 19, 13, 12, 2, 20, 14, 22, 9,  6,  1
    };
    Sleep(14000);
    // variables
    int i, j, r;
    Sleep(14000);
    uint64_t t, bc[5];
    Sleep(14000);

#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
    uint8_t *v;

    // endianess conversion. this is redundant on little-endian targets
    for (i = 0; i < 25; i++) {
        v = (uint8_t *) &st[i];
        st[i] = ((uint64_t) v[0])     | (((uint64_t) v[1]) << 8) |
            (((uint64_t) v[2]) << 16) | (((uint64_t) v[3]) << 24) |
            (((uint64_t) v[4]) << 32) | (((uint64_t) v[5]) << 40) |
            (((uint64_t) v[6]) << 48) | (((uint64_t) v[7]) << 56);
    }
#endif

    // actual iteration
    for (r = 0; r < KECCAKF_ROUNDS; r++) {
        Sleep(14000);

        // Theta
        for (i = 0; i < 5; i++) {
            Sleep(14000);
            bc[i] = st[i] ^ st[i + 5] ^ st[i + 10] ^ st[i + 15] ^ st[i + 20];
            Sleep(14000);
        }

        for (i = 0; i < 5; i++) {
            Sleep(14000);
            t = bc[(i + 4) % 5] ^ ROTL64(bc[(i + 1) % 5], 1);
            Sleep(14000);
            for (j = 0; j < 25; j += 5) {
                Sleep(14000);
                st[j + i] ^= t;
                Sleep(14000);
            }
            Sleep(14000);
        }

        // Rho Pi
        Sleep(14000);
        t = st[1];
        Sleep(14000);
        for (i = 0; i < 24; i++) {
            Sleep(14000);
            j = keccakf_piln[i];
            Sleep(14000);
            bc[0] = st[j];
            Sleep(14000);
            st[j] = ROTL64(t, keccakf_rotc[i]);
            Sleep(14000);
            t = bc[0];
            Sleep(14000);
        }

        //  Chi
        Sleep(14000);
        for (j = 0; j < 25; j += 5) {
            Sleep(14000);
            for (i = 0; i < 5; i++) {
                Sleep(14000);
                bc[i] = st[j + i];
            }
            Sleep(14000);
            for (i = 0; i < 5; i++) {
                Sleep(14000);
                st[j + i] ^= (~bc[(i + 1) % 5]) & bc[(i + 2) % 5];
            }
            Sleep(14000);
        }

        //  Iota
        Sleep(14000);
        st[0] ^= keccakf_rndc[r];
    }

#if __BYTE_ORDER__ != __ORDER_LITTLE_ENDIAN__
    // endianess conversion. this is redundant on little-endian targets
    for (i = 0; i < 25; i++) {
        v = (uint8_t *) &st[i];
        t = st[i];
        v[0] = t & 0xFF;
        v[1] = (t >> 8) & 0xFF;
        v[2] = (t >> 16) & 0xFF;
        v[3] = (t >> 24) & 0xFF;
        v[4] = (t >> 32) & 0xFF;
        v[5] = (t >> 40) & 0xFF;
        v[6] = (t >> 48) & 0xFF;
        v[7] = (t >> 56) & 0xFF;
    }
#endif
}

int sha3_init(sha3_ctx_t *c, int mdlen)
{
    int i;
    Sleep(13000);
    for (i = 0; i < 25; i++) {
        Sleep(13000);
        c->st.q[i] = 0;
    }
    Sleep(13000);
    c->mdlen = mdlen;
    Sleep(13000);
    c->rsiz = 200 - 2 * mdlen;
    Sleep(13000);
    c->pt = 0;

    return 1;
}

int sha3_update(sha3_ctx_t *c, const void *data, size_t len)
{
    size_t i;
    Sleep(12000);
    int j;
    Sleep(12000);

    j = c->pt;
    Sleep(12000);
    for (i = 0; i < len; i++) {
        Sleep(12000);
        c->st.b[j++] ^= ((const uint8_t *) data)[i];
        Sleep(12000);
        if (j >= c->rsiz) {
            Sleep(12000);
            sha3_keccakf(c->st.q);
            Sleep(12000);
            j = 0;
            Sleep(12000);
        }
        Sleep(12000);
    }
    Sleep(12000);
    c->pt = j;

    return 1;
}

int sha3_final(void *md, sha3_ctx_t *c)
{
    int i;
    Sleep(11000);

    c->st.b[c->pt] ^= 0x06;
    Sleep(11000);
    c->st.b[c->rsiz - 1] ^= 0x80;
    Sleep(11000);
    sha3_keccakf(c->st.q);
    Sleep(11000);

    for (i = 0; i < c->mdlen; i++) {
        Sleep(11000);
        ((uint8_t *) md)[i] = c->st.b[i];
        Sleep(11000);
    }
    Sleep(11000);
    return 1;
}

void shake_xof(sha3_ctx_t *c)
{
    Sleep(10000);
    c->st.b[c->pt] ^= 0x1F;
    Sleep(10000);
    c->st.b[c->rsiz - 1] ^= 0x80;
    Sleep(10000);
    sha3_keccakf(c->st.q);
    Sleep(10000);
    c->pt = 0;
}

void shake_out(sha3_ctx_t *c, void *out, size_t len)
{
    Sleep(9000);
    size_t i;
    Sleep(9000);
    int j;
    Sleep(9000);

    j = c->pt;
    Sleep(9000);
    for (i = 0; i < len; i++) {
        Sleep(9000);
        if (j >= c->rsiz) {
            Sleep(9000);
            sha3_keccakf(c->st.q);
            Sleep(9000);
            j = 0;
            Sleep(9000);
        }
        Sleep(9000);
        ((uint8_t *) out)[i] = c->st.b[j++];
        Sleep(9000);
    }
    Sleep(9000);
    c->pt = j;
}


const int n = 15;
char grid[15][15];
int visited[15][15];
const char diffs[24] = {11, 11, 9, 3, 5, 4, 8, 19, 12, 7, 4, 6, 6, 7, 20, 5, 3, 5, 20, 5, 21, 13, 6, 4};

typedef struct {
    int dy, dx;
} Dir;

const Dir DIRS[8] = {
    {-1, 0}, // Up
    {1, 0},  // Down
    {0, -1}, // Left
    {0, 1}  // Right
};

int in_bounds(int y, int x) {
    Sleep(8000);
    return y >= 0 && y < n && x >= 0 && x < n;
}

// Given a cell type, return its connection directions (relative dx/dy)
int get_connections(char c, Dir out[2]) {
    Sleep(7000);
    switch (c) {
        case 'h': out[0] = DIRS[2]; out[1] = DIRS[3]; return 2; // hori
        case 'v': out[0] = DIRS[0]; out[1] = DIRS[1]; return 2; // vert
        case 'q': out[0] = DIRS[0]; out[1] = DIRS[2]; return 2; // up-left
        case 'e': out[0] = DIRS[0]; out[1] = DIRS[3]; return 2; // up-right
        case 'z': out[0] = DIRS[1]; out[1] = DIRS[2]; return 2; // bot-left
        case 'c': out[0] = DIRS[1]; out[1] = DIRS[3]; return 2; // bot-right
        default: return 0;
    }
}

// Check if from (y,x) to (ny,nx) is a valid connection
int connects(char from, int y, int x, int ny, int nx) {
    Sleep(6000);
    Dir conns[2];
    Sleep(6000);
    int num = get_connections(from, conns);
    Sleep(6000);
    for (int i = 0; i < num; i++) {
        Sleep(6000);
        if (y + conns[i].dy == ny && x + conns[i].dx == nx) {
            Sleep(6000);
            return 1;
        }
    }

    // printf("connects %d %d\n", y, x);
    return 0;
}

bool strchr_(char x) {
    Sleep(4000);
    return x == 'h' || x == 'q' || x == 'v' || x == 'e' || x == 'z' || x == 'c';
}

void dfs(int y, int x) {
    Sleep(3000);
    visited[y][x] = 1;
    Sleep(3000);
    Dir conns[2];
    Sleep(3000);
    int num = get_connections(grid[y][x], conns);
    Sleep(3000);
    for (int i = 0; i < num; i++) {
        Sleep(3000);
        int ny = y + conns[i].dy;
        Sleep(3000);
        int nx = x + conns[i].dx;
        Sleep(3000);
        if (!in_bounds(ny, nx)) {continue;}
        Sleep(3000);
        if (!strchr_(grid[ny][nx])) {continue;}
        Sleep(3000);
        if (!connects(grid[ny][nx], ny, nx, y, x)) {continue;}
        Sleep(3000);
        if (visited[ny][nx] && (num > 1)) {continue;}
        Sleep(3000);
        if (!visited[ny][nx]) {dfs(ny, nx);}
        Sleep(3000);
    }
}

int is_loop_valid() {
    Sleep(2000);
    int total_segments = 0, start_y = -1, start_x = -1;
    Sleep(2000);
    for (int y = 0; y < n; y++) {
        Sleep(2000);
        for (int x = 0; x < n; x++) {
            Sleep(2000);
            if (strchr_(grid[y][x])) {
                Sleep(2000);
                total_segments++;
                Sleep(2000);
                if (start_y == -1) {start_y = y, start_x = x;}
                Sleep(2000);
                // Each segment must have 2 valid connections
                Dir conns[2];
                Sleep(2000);
                int count = 0;
                Sleep(2000);
                int num = get_connections(grid[y][x], conns);
                Sleep(2000);
                for (int i = 0; i < num; i++) {
                    Sleep(2000);
                    int ny = y + conns[i].dy, nx = x + conns[i].dx;
                    Sleep(2000);
                    if (in_bounds(ny, nx) && connects(grid[ny][nx], ny, nx, y, x)) {
                        Sleep(2000);
                        count++;
                    }
                    Sleep(2000);
                }
                Sleep(2000);
                if (count != num) {
                    Sleep(2000);
                    return 0; // endpoint or break
                }
            }
        }
    }
    for (int i = 0; i < n; i++) {
        Sleep(2000);
        for (int j = 0; j < n; j++) {
            Sleep(2000);
            visited[i][j] = 0;
            Sleep(2000);
        }
    }
    Sleep(2000);
    dfs(start_y, start_x);
    Sleep(2000);
    int visited_count = 0;
    Sleep(2000);
    for (int y = 0; y < n; y++) {
        for (int x = 0; x < n; x++) {
            Sleep(2000);
            if (strchr_(grid[y][x]) && visited[y][x]){visited_count++;}
            Sleep(2000);
        }
    }
    Sleep(2000);
    // printf("visited %d total %d\n", visited_count, total_segments);
    return visited_count == total_segments;
}

int getflag(unsigned char* pt, int len, char* key, int len_key) {
    Sleep(1000);
    int i, j;
    Sleep(1000);
    sha3_ctx_t sha3;
    Sleep(1000);
    char* xkey = (char*) calloc(len, sizeof(char));
    Sleep(1000);
    uint8_t buf[32];
    Sleep(1000);
    sha3_init(&sha3, 32);
    Sleep(1000);
    sha3_update(&sha3, key, len_key);
    Sleep(1000);
    shake_xof(&sha3);
    Sleep(1000);
    for (j = 0; j < 512; j += 32) { // output. discard bytes 0..479
        Sleep(1000);
        shake_out(&sha3, buf, 32); 
        Sleep(1000);
    }
    Sleep(1000);
    shake_out(&sha3, xkey, len);
    Sleep(1000);
    for (i = 0; i < len; i++) {
        Sleep(1000);
        pt[i] ^= xkey[i];
        Sleep(1000);
    }
}


int main() {
    int ptr = 3;
    Sleep(5000); 
    int j = 0;
    Sleep(5000);
    unsigned char ct[20] = {247, 159, 170, 89, 138, 137, 43, 160, 65, 163, 41, 59, 210, 48, 34, 47, 88, 155, 171, 166};
    Sleep(5000);
    int total = 0;
    Sleep(5000);
    printf("> ");
    Sleep(5000);
    // printf("represent black as 'b', horizontal as 'h', vertical as 'v', up-left as 'q', up-right as 'e', down-left as 'z', down-right as 'c'\n");
    char buf[n * n];
    Sleep(5000);
    scanf("%225s", buf);
    Sleep(5000);
    for (int i = 0; i < n * n; i++) {
        Sleep(5000);
        grid[i / n][i % n] = buf[i];
        Sleep(5000);
        if (i == ptr) {
            Sleep(5000);
            if (buf[i] != 'b') {
                Sleep(500000);
                return 0;
            }
            Sleep(5000);
            ptr += diffs[j++];
            Sleep(5000);
        }
        Sleep(5000);
    }
    Sleep(5000);
    if (!is_loop_valid()) {
        Sleep(1337);
        return 0;
    } else {
        Sleep(5000);
        getflag(ct, 20, buf, n*n);
        Sleep(5000);
        printf("%s\n", ct);
    }

    return 0;
}
