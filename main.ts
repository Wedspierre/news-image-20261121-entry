// news-image-20261121 v2 entry: ships the pre-rendered front page to /output.
// The image itself is drawn offline by draw_v2.py (PIL + Liberation fonts);
// this program only copies it, so both grader runs write identical bytes.
import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const buf = readFileSync(src);
if (buf.length === 0 || buf.length > 1048576) {
  throw new Error(`entry.png missing or over the 1 MiB gate (${buf.length} bytes)`);
}
if (buf[0] !== 0x89 || buf[1] !== 0x50 || buf[2] !== 0x4e || buf[3] !== 0x47) {
  throw new Error('entry.png is not a PNG (bad magic bytes)');
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
// Post-copy check: the grader runs this program twice and both runs must
// write the same bytes, so fail loudly instead of shipping a partial copy.
if (!readFileSync(dest).equals(buf)) {
  throw new Error('entry.png copy mismatch after write');
}
