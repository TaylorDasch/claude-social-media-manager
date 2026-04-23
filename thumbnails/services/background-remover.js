const fs = require('fs');
const path = require('path');
const { execFileSync, execSync } = require('child_process');
const sharp = require('sharp');

// Use the rembg Python library directly (not the CLI) — the CLI pulls in
// broken optional deps like watchdog/filetype on some installs.
const REMBG_SCRIPT = `
import sys
try:
    from rembg import remove
    from PIL import Image
except ImportError as e:
    sys.stderr.write("rembg library not installed: " + str(e) + "\\n")
    sys.exit(2)

inp = sys.argv[1]
outp = sys.argv[2]
with open(inp, "rb") as f:
    data = f.read()
out = remove(data)
with open(outp, "wb") as f:
    f.write(out)
`;

function haveRembgLib() {
  try {
    execSync('python3 -c "from rembg import remove"', { stdio: 'ignore' });
    return true;
  } catch {
    return false;
  }
}

let rembgAvailable = null;

async function removeBackground(inputPath, outputPath) {
  if (rembgAvailable === null) rembgAvailable = haveRembgLib();

  if (rembgAvailable) {
    try {
      execFileSync('python3', ['-c', REMBG_SCRIPT, inputPath, outputPath], { stdio: ['ignore', 'ignore', 'pipe'] });
      return outputPath;
    } catch (e) {
      console.warn(`[bg-remover] rembg library call failed, falling back to sharp alpha: ${e.message}`);
      rembgAvailable = false;
    }
  } else {
    console.warn('[bg-remover] rembg library not available — falling back to naive sharp alpha');
    console.warn('[bg-remover] install with: python3 -m pip install rembg onnxruntime --break-system-packages');
  }

  await sharp(inputPath)
    .ensureAlpha()
    .png()
    .toFile(outputPath);
  return outputPath;
}

async function cropUpperBody(inputPath, outputPath) {
  const img = sharp(inputPath);
  const meta = await img.metadata();
  const top = 0;
  const height = Math.round(meta.height * 0.75);
  await img.extract({ left: 0, top, width: meta.width, height }).toFile(outputPath);
  return outputPath;
}

async function makeFlipped(inputPath, outputPath) {
  await sharp(inputPath).flop().toFile(outputPath);
  return outputPath;
}

async function processExpressionPhoto(rawPath, outDir) {
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  const base = path.basename(rawPath, path.extname(rawPath));
  const transparentPath = path.join(outDir, `${base}.png`);
  const flippedPath = path.join(outDir, `${base}-flipped.png`);
  const tmpRemoved = path.join(outDir, `${base}.__tmp_removed.png`);

  await removeBackground(rawPath, tmpRemoved);
  await cropUpperBody(tmpRemoved, transparentPath);
  await makeFlipped(transparentPath, flippedPath);

  try { fs.unlinkSync(tmpRemoved); } catch {}

  return { transparentPath, flippedPath };
}

module.exports = {
  removeBackground,
  cropUpperBody,
  makeFlipped,
  processExpressionPhoto,
};
