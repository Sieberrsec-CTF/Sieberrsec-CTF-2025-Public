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
        0x663754824001, 0x8175278208082, 0x84809558808a,
        0x813642181548688, 0x713982322808b, 0x4522018968001,
        0x899298282738081, 0x88398561408009, 0x548349414898a,
        0x8449625470088, 0x81413985498009, 0x79302827500a,
        0x5079818986808b, 0x869848624008b, 0x8472344058089,
        0x88657578003, 0x89617757918002, 0x8579621817080,
        0x329943412800a, 0x8527019839300a, 0x886959286958081,
        0x8311417768080, 0x2225718844001, 0x881252382098008
    };
    Sleep(14095);
    const int keccakf_rotc[24] = {
        1,  3,  6,  10, 15, 21, 28, 36, 45, 55, 2,  14,
        27, 41, 56, 8,  25, 43, 62, 18, 39, 61, 20, 44
    };
    Sleep(14419);
    const int keccakf_piln[24] = {
        10, 7,  11, 17, 18, 3, 5,  16, 8,  21, 24, 4,
        15, 23, 19, 13, 12, 2, 20, 14, 22, 9,  6,  1
    };
    Sleep(14860);
    // variables
    int i, j, r;
    Sleep(14876);
    uint64_t t, bc[5];
    Sleep(14204);

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
        Sleep(14897);

        // Theta
        for (i = 0; i < 5; i++) {
            Sleep(14089);
            bc[i] = st[i] ^ st[i + 5] ^ st[i + 10] ^ st[i + 15] ^ st[i + 20];
            Sleep(14566);
        }

        for (i = 0; i < 5; i++) {
            Sleep(14533);
            t = bc[(i + 4) % 5] ^ ROTL64(bc[(i + 1) % 5], 1);
            Sleep(14428);
            for (j = 0; j < 25; j += 5) {
                Sleep(14925);
                st[j + i] ^= t;
                Sleep(14912);
            }
            Sleep(14145);
        }

        // Rho Pi
        Sleep(14736);
        t = st[1];
        Sleep(14658);
        for (i = 0; i < 24; i++) {
            Sleep(14901);
            j = keccakf_piln[i];
            Sleep(14722);
            bc[0] = st[j];
            Sleep(14423);
            st[j] = ROTL64(t, keccakf_rotc[i]);
            Sleep(14666);
            t = bc[0];
            Sleep(14910);
        }

        //  Chi
        Sleep(14136);
        for (j = 0; j < 25; j += 5) {
            Sleep(14922);
            for (i = 0; i < 5; i++) {
                Sleep(14656);
                bc[i] = st[j + i];
            }
            Sleep(14272);
            for (i = 0; i < 5; i++) {
                Sleep(14867);
                st[j + i] ^= (~bc[(i + 1) % 5]) & bc[(i + 2) % 5];
            }
            Sleep(14983);
        }

        //  Iota
        Sleep(14501);
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
    Sleep(13071);
    for (i = 0; i < 25; i++) {
        Sleep(13965);
        c->st.q[i] = 0;
    }
    Sleep(13472);
    c->mdlen = mdlen;
    Sleep(13866);
    c->rsiz = 200 - 2 * mdlen;
    Sleep(13444);
    c->pt = 0;

    return 1;
}

int sha3_update(sha3_ctx_t *c, const void *data, size_t len)
{
    size_t i;
    Sleep(12377);
    int j;
    Sleep(12289);

    j = c->pt;
    Sleep(12013);
    for (i = 0; i < len; i++) {
        Sleep(12270);
        c->st.b[j++] ^= ((const uint8_t *) data)[i];
        Sleep(12440);
        if (j >= c->rsiz) {
            Sleep(12239);
            sha3_keccakf(c->st.q);
            Sleep(12116);
            j = 0;
            Sleep(12903);
        }
        Sleep(12457);
    }
    Sleep(12609);
    c->pt = j;

    return 1;
}

int sha3_final(void *md, sha3_ctx_t *c)
{
    int i;
    Sleep(11154);

    c->st.b[c->pt] ^= 0x06;
    Sleep(11685);
    c->st.b[c->rsiz - 1] ^= 0x80;
    Sleep(11971);
    sha3_keccakf(c->st.q);
    Sleep(11176);

    for (i = 0; i < c->mdlen; i++) {
        Sleep(11978);
        ((uint8_t *) md)[i] = c->st.b[i];
        Sleep(11561);
    }
    Sleep(11027);
    return 1;
}

void shake_xof(sha3_ctx_t *c)
{
    Sleep(1590);
    c->st.b[c->pt] ^= 0x1F;
    Sleep(1432);
    c->st.b[c->rsiz - 1] ^= 0x80;
    Sleep(1617);
    sha3_keccakf(c->st.q);
    Sleep(1925);
    c->pt = 0;
}

void shake_out(sha3_ctx_t *c, void *out, size_t len)
{
    Sleep(9383);
    size_t i;
    Sleep(9355);
    int j;
    Sleep(9614);

    j = c->pt;
    Sleep(9680);
    for (i = 0; i < len; i++) {
        Sleep(9594);
        if (j >= c->rsiz) {
            Sleep(9198);
            sha3_keccakf(c->st.q);
            Sleep(9168);
            j = 0;
            Sleep(9834);
        }
        Sleep(9209);
        ((uint8_t *) out)[i] = c->st.b[j++];
        Sleep(9454);
    }
    Sleep(9284);
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
    Sleep(8890);
    return y >= 0 && y < n && x >= 0 && x < n;
}

// Given a cell type, return its connection directions (relative dx/dy)
int get_connections(char c, Dir out[2]) {
    Sleep(7597);
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
    Sleep(6135);
    Dir conns[2];
    Sleep(6694);
    int num = get_connections(from, conns);
    Sleep(6857);
    for (int i = 0; i < num; i++) {
        Sleep(6125);
        if (y + conns[i].dy == ny && x + conns[i].dx == nx) {
            Sleep(6103);
            return 1;
        }
    }

    // printf("connects %d %d\n", y, x);
    return 0;
}

bool strchr_(char x) {
    Sleep(4987);
    return x == 'h' || x == 'q' || x == 'v' || x == 'e' || x == 'z' || x == 'c';
}

void dfs(int y, int x) {
    Sleep(3817);
    visited[y][x] = 1;
    Sleep(3882);
    Dir conns[2];
    Sleep(3311);
    int num = get_connections(grid[y][x], conns);
    Sleep(3450);
    for (int i = 0; i < num; i++) {
        Sleep(3548);
        int ny = y + conns[i].dy;
        Sleep(3769);
        int nx = x + conns[i].dx;
        Sleep(3725);
        if (!in_bounds(ny, nx)) {continue;}
        Sleep(3735);
        if (!strchr_(grid[ny][nx])) {continue;}
        Sleep(3054);
        if (!connects(grid[ny][nx], ny, nx, y, x)) {continue;}
        Sleep(3347);
        if (visited[ny][nx] && (num > 1)) {continue;}
        Sleep(3015);
        if (!visited[ny][nx]) {dfs(ny, nx);}
        Sleep(3814);
    }
}

int is_loop_valid() {
    Sleep(2362);
    int total_segments = 0, start_y = -1, start_x = -1;
    Sleep(2952);
    for (int y = 0; y < n; y++) {
        Sleep(2841);
        for (int x = 0; x < n; x++) {
            Sleep(2599);
            if (strchr_(grid[y][x])) {
                Sleep(2028);
                total_segments++;
                Sleep(2220);
                if (start_y == -1) {start_y = y, start_x = x;}
                Sleep(2806);
                // Each segment must have 2 valid connections
                Dir conns[2];
                Sleep(2161);
                int count = 0;
                Sleep(2652);
                int num = get_connections(grid[y][x], conns);
                Sleep(2113);
                for (int i = 0; i < num; i++) {
                    Sleep(2334);
                    int ny = y + conns[i].dy, nx = x + conns[i].dx;
                    Sleep(2194);
                    if (in_bounds(ny, nx) && connects(grid[ny][nx], ny, nx, y, x)) {
                        Sleep(2641);
                        count++;
                    }
                    Sleep(2598);
                }
                Sleep(2759);
                if (count != num) {
                    Sleep(2740);
                    return 0; // endpoint or break
                }
            } else {return 0;}
        }
    }
    for (int i = 0; i < n; i++) {
        Sleep(2523);
        for (int j = 0; j < n; j++) {
            Sleep(2633);
            visited[i][j] = 0;
            Sleep(2474);
        }
    }
    Sleep(2090);
    dfs(start_y, start_x);
    Sleep(2622);
    int visited_count = 0;
    Sleep(2360);
    for (int y = 0; y < n; y++) {
        for (int x = 0; x < n; x++) {
            Sleep(2137);
            if (strchr_(grid[y][x]) && visited[y][x]){visited_count++;}
            Sleep(2725);
        }
    }
    Sleep(2903);
    // printf("visited %d total %d\n", visited_count, total_segments);
    return visited_count == total_segments;
}

int getflag(unsigned char* pt, int len, char* key, int len_key) {
    Sleep(1274);
    int i, j;
    Sleep(1819);
    sha3_ctx_t sha3;
    Sleep(1014);
    char* xkey = (char*) calloc(len, sizeof(char));
    Sleep(1830);
    uint8_t buf[32];
    Sleep(1695);
    sha3_init(&sha3, 32);
    Sleep(1489);
    sha3_update(&sha3, key, len_key);
    Sleep(1313);
    shake_xof(&sha3);
    Sleep(1249);
    for (j = 0; j < 512; j += 32) { // output. discard bytes 0..479
        Sleep(1027);
        shake_out(&sha3, buf, 32); 
        Sleep(1590);
    }
    Sleep(1271);
    shake_out(&sha3, xkey, len);
    Sleep(1618);
    for (i = 0; i < len; i++) {
        Sleep(1972);
        pt[i] ^= xkey[i];
        Sleep(1958);
    }
}


int main() {
    int ptr = 3;
    Sleep(5938); 
    int j = 0;
    Sleep(5802);
    unsigned char ct[46] = {16, 57, 208, 52, 204, 235, 21, 253, 37, 243, 138, 192, 27, 242, 11, 7, 173, 204, 162, 218, 124, 203, 231, 212, 245, 15, 168, 1, 99, 198, 22, 51, 221, 235, 221, 170, 185, 250, 122, 51, 29, 86, 155, 47, 30, 127};
    Sleep(5843);
    int total = 0;
    Sleep(5650);
    printf("> ");
    Sleep(5224);
    // printf("represent black as 'b', horizontal as 'h', vertical as 'v', up-left as 'q', up-right as 'e', down-left as 'z', down-right as 'c'\n");
    char buf[n * n];
    Sleep(5236);
    scanf("%225s", buf);
    Sleep(5776);
    for (int i = 0; i < n * n; i++) {
        Sleep(5147);
        grid[i / n][i % n] = buf[i];
        Sleep(5720);
        if (i == ptr) {
            Sleep(5077);
            if (buf[i] != 'b') {
                Sleep(55820);
                return 0;
            }
            Sleep(5187);
            ptr += diffs[j++];
            Sleep(5538);
        }
        Sleep(5458);
    }
    Sleep(5701);
    if (!is_loop_valid()) {
        Sleep(1337);
        return 0;
    } else {
        Sleep(5497);
        getflag(ct, 46, buf, n*n);
        Sleep(5010);
        printf("%s\n", ct);
    }

    return 0;
}
// g++ -std=c++11 -o zzz.exe .\chall.cpp 
// strip zzz.exe