# quicknotes

1. Decompress the provided AppImage file

    ```bash
    ./dist/quicknotes.AppImage --appimage-extract
    ```

2. View the extracted contents. In `resources`, an `app.asar` file is present. `app.asar` is an archive format used by Electron applications to bundle their source code and assets.
3. Extract the `app.asar` file using the `asar` command-line tool:

    ```bash
    npx asar extract resources/app.asar app
    ```

4. A new `app/` directory is created, containing the source code of the application. We should focus on the `main.js` file, which is the main entry point of the Electron application. Analysing this Javascript code, we see that there is a `cfg` blob that isn't used in the app.

    ```js
    const cfg = {

  endpoint: '<https://updates.quicknotes.local/api/ping>',
  digest: Buffer.from([
    0x26,0x36,0x21,0x33,0x2e,0x3b,0x65,0x22,0x0a,0x2c,
    0x65,0x00,0x0a,0x3e,0x1b,0x65,0x02,0x0a,0x3d,0x65,
    0x22,0x0a,0x21,0x65,0x0a,0x27,0x30,0x23,0x74,0x28])
  };
    ```
5. There is a decrypt function that can be used to restore the original value of the `digest` blob:

    ```js
    function decrypt (buf) {
      return Buffer.from(buf.map(b => b ^ 0x55));
    }
    ```
6. Running the decrypt function on the blob gives us the flag `sctf{n0w_y0U_kN0W_h0w_t0_rev!}`
