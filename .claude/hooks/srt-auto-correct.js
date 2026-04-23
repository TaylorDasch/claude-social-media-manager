#!/usr/bin/env node

// PostToolUse hook: After writing an .SRT file, prompt to run srt-corrector
// This fires after any Write tool use in the social media manager project

const input = JSON.parse(require('fs').readFileSync('/dev/stdin', 'utf8'));

// Only trigger on Write tool
if (input.tool_name !== 'Write') {
  process.stdout.write(JSON.stringify({ decision: 'approve' }));
  process.exit(0);
}

const filePath = input.tool_input?.file_path || '';

// Check if the written file is an .SRT file
if (filePath.toLowerCase().endsWith('.srt')) {
  process.stdout.write(JSON.stringify({
    decision: 'approve',
    message: `SRT file detected: ${filePath}\n\nRun /srt-corrector on this file to fix proper nouns (Baylor Scott & White, Fort Hood, neighborhoods, builders), real estate terms, and speech-to-text errors.\n\nThen run /transcript-to-blog to convert to an AEO blog post.`
  }));
} else {
  process.stdout.write(JSON.stringify({ decision: 'approve' }));
}
