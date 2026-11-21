// News-image entry for 20 November 2026 (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// the output directory the grader gives it, deterministically.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

// The output file name is fixed by the competition rules: entry.png.
// copyFileSync copies the bytes exactly, so the output is identical on
// every run; there is no network access, no randomness and no clock use.

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
