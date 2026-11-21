// news-image-20261121 entry (Node 22, standard library only).
// The entry is the front page sitting next to this file: entry.png, a
// newspaper front page dated SATURDAY 21 NOVEMBER 2026 with four panels —
// COP31 climate talks in Antalya spilling into overtime after every mention
// of fossil fuels was stripped from the draft deal, Wall Street's meltdown
// as the S&P 500 sank 3.7% into correction and the Nasdaq wiped out the
// year's gains, Cyclone Akvan's aftermath on India's east coast with
// 300,000 evacuated, and Russian missile and drone strikes on Ukraine
// hitting Kryvyi Rih (two killed, 42 injured) and damaging Kyiv. This
// program just delivers those exact bytes to the grader's output directory —
// the judge sees the file as-is, nothing is re-encoded or resized.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync, unlinkSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const rawOutDir = process.env.MAKEFUN_OUTPUT_DIR;
// An empty or whitespace-only MAKEFUN_OUTPUT_DIR must fall back to the
// default: `??` alone would keep '' and join('', 'entry.png') would drop
// the file in the working directory instead of /output.
const outDir = rawOutDir?.trim() ? rawOutDir.trim() : '/output';
const source = new URL('./entry.png', import.meta.url);

// Fail fast on a bad source: if entry.png is missing or not a PNG, say so
// here instead of copying garbage and failing later on the delivered copy.
let sourceStat;
try {
  sourceStat = statSync(source);
} catch (err) {
  throw new Error(`entry.png missing next to main.ts: ${err.message}`);
}
if (sourceStat.size === 0) {
  throw new Error('entry.png is empty');
}
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!readFileSync(source).subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG: bad signature bytes in source');
}

// The grader's output directory may not exist yet — create it so the
// copy never fails on a missing folder.
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
// Unlink first: the grader runs the program twice and may reuse the
// output directory, and the copy it delivered on the first run carries
// the source's read-only mode — overwriting it in place would fail
// with EACCES, while unlinking and recreating it always succeeds.
try {
  unlinkSync(target);
} catch (err) {
  if (err.code !== 'ENOENT') throw err;
}
copyFileSync(source, target);

// The gate tells a PNG apart by its first bytes — confirm the delivered
// copy starts with the PNG signature before the hash check, so a
// same-length non-PNG could never pass as the entry.
const deliveredHead = readFileSync(target).subarray(0, 8);
if (!deliveredHead.equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG: bad signature bytes');
}

// The judge scores the file as-is, so confirm the delivered copy is
// byte-for-byte the source instead of silently shipping a short write:
// same size first, then the same SHA-256 digest, so a same-length
// corruption can no longer pass the check unnoticed.
const sourceBytes = statSync(source).size;
const targetBytes = statSync(target).size;
if (sourceBytes !== targetBytes) {
  throw new Error(`entry.png size mismatch: source ${sourceBytes} bytes, delivered ${targetBytes} bytes`);
}
const digest = (path) => createHash('sha256').update(readFileSync(path)).digest('hex');
const sourceHash = digest(source);
const targetHash = digest(target);
if (sourceHash !== targetHash) {
  throw new Error(`entry.png sha256 mismatch: source ${sourceHash}, delivered ${targetHash}`);
}
console.log(`delivered entry.png to ${outDir} (${targetBytes} bytes, sha256 ${targetHash})`);
