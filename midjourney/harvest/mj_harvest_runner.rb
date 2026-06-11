#!/usr/bin/env ruby
# frozen_string_literal: true

require "base64"
require "fileutils"
require "json"
require "open3"
require "shellwords"
require "time"

ROOT = "/Users/taylordasch_1/claude-social-media-manager/midjourney/harvest"
MANIFEST_PATH = File.join(ROOT, "run-manifest.json")
LOG_PATH = File.join(ROOT, "harvest-run-log.json")
SREF = "1571182691"
BATCH_SIZE = 3

def sh_capture(*args)
  out, err, status = Open3.capture3(*args)
  raise "command failed: #{args.join(" ")}\n#{err}" unless status.success?

  out
end

def find_midjourney_window
  script = <<~OSA
    tell application "Google Chrome"
      repeat with w in windows
        repeat with t in tabs of w
          set u to URL of t
          if u contains "midjourney.com" then
            return (id of w as string)
          end if
        end repeat
      end repeat
    end tell
  OSA
  sh_capture("osascript", "-e", script).strip
end

$window_id = ENV.fetch("MJ_WINDOW_ID", find_midjourney_window)

def chrome_js(js)
  File.write("/tmp/mj_harvest_exec.js", js)
  2.times do |attempt|
    script = <<~OSA
      set jsCode to do shell script "cat /tmp/mj_harvest_exec.js"
      tell application "Google Chrome" to tell tab 1 of window id #{$window_id} to execute javascript jsCode
    OSA
    begin
      return sh_capture("osascript", "-e", script).strip
    rescue StandardError
      raise if attempt == 1

      $window_id = find_midjourney_window
      sleep 1
    end
  end
end

def visible_job_ids
  js = <<~JS
    JSON.stringify(Array.from(new Set(
      Array.from(document.querySelectorAll('a[href*="/jobs/"]'))
        .map(a => a.href.match(/jobs\\/([^?]+)/)?.[1])
        .filter(Boolean)
    )).slice(0, 20))
  JS
  JSON.parse(chrome_js(js))
end

def visible_upscale_cards
  js = <<~JS
    (function(){
      const seen = new Set();
      const cards = [];
      for (const a of Array.from(document.querySelectorAll('a[href*="/jobs/"]'))) {
        const id = a.href.match(/jobs\\/([^?]+)/)?.[1];
        if (!id || seen.has(id)) continue;
        seen.add(id);
        let e = a;
        for (let i = 0; i < 6 && e; i++, e = e.parentElement) {
          const text = e.innerText || '';
          if (text.includes('Upscale (S)')) {
            cards.push({id, text});
            break;
          }
        }
      }
      return JSON.stringify(cards);
    })()
  JS
  JSON.parse(chrome_js(js))
end

def prompt_fragment(item)
  item.fetch("prompt").split(" --").first.downcase.gsub(/\s+/, " ")[0, 70]
end

def find_upscale_job_for(item)
  fragment = prompt_fragment(item)
  visible_upscale_cards.find do |card|
    card.fetch("text").downcase.gsub(/\s+/, " ").include?(fragment)
  end&.fetch("id")
end

def submit_prompt(prompt)
  js = <<~JS
    (function(){
      const p = #{prompt.to_json};
      const t = document.querySelector('textarea[placeholder="What will you imagine?"]');
      if (!t) return 'ERR missing textarea';
      const setter = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value').set;
      setter.call(t, p);
      t.dispatchEvent(new Event('input', {bubbles:true}));
      const btn = Array.from(t.parentElement.parentElement.querySelectorAll('button'))
        .find(b => b.querySelector('g#PaperAirplane'));
      if (!btn) return 'ERR missing send button';
      btn.click();
      return 'OK';
    })()
  JS
  result = chrome_js(js)
  raise "submit failed: #{result}" unless result == "OK"
end

def navigate_to(url)
  chrome_js("window.location.href = #{url.to_json}; 'OK'")
end

def wait_for_upscale_controls(timeout: 60)
  start = Time.now
  loop do
    text = chrome_js("document.body.innerText")
    return true if text.include?("Creation Actions") && text.include?("Upscale")

    raise "timed out waiting for upscale controls" if Time.now - start > timeout

    sleep 3
  end
end

def click_upscale_subtle
  js = <<~JS
    (function(){
      const button = Array.from(document.querySelectorAll('button')).find(b =>
        b.innerText.trim() === 'Subtle' &&
        (b.parentElement?.parentElement?.innerText || '').startsWith('Upscale')
      );
      if (!button) return 'NO_UPSCALE_BUTTON';
      button.click();
      return 'OK';
    })()
  JS
  result = chrome_js(js)
  raise "upscale click failed: #{result}" unless result == "OK"
end

def cdn_head(url)
  js = <<~JS
    (function(){
      const x = new XMLHttpRequest();
      x.open('HEAD', #{url.to_json}, false);
      try {
        x.send();
        return JSON.stringify({status:x.status, type:x.getResponseHeader('content-type') || '', length:x.getResponseHeader('content-length') || ''});
      } catch (e) {
        return JSON.stringify({status:0, error:e.message});
      }
    })()
  JS
  JSON.parse(chrome_js(js))
end

def variant_url(job_id, index)
  candidates = [
    "https://cdn.midjourney.com/#{job_id}/0_#{index}.png",
    "https://cdn.midjourney.com/#{job_id}/0_#{index}.webp",
    "https://cdn.midjourney.com/#{job_id}/0_#{index}_2048_N.webp",
    "https://cdn.midjourney.com/#{job_id}/0_#{index}_1024_N.webp",
    "https://cdn.midjourney.com/#{job_id}/0_#{index}_640_N.webp?method=shortest"
  ]
  candidates.find do |url|
    head = cdn_head(url)
    head["status"] == 200 && head["type"].to_s.start_with?("image/")
  end
end

def wait_for_ready(job_id, timeout: 900)
  start = Time.now
  loop do
    urls = (0..3).map { |i| variant_url(job_id, i) }
    return true if urls.all?

    raise "timed out waiting for #{job_id}: #{urls.inspect}" if Time.now - start > timeout

    sleep 15
  end
end

def wait_for_variant(job_id, index, timeout: 900)
  start = Time.now
  loop do
    return true if variant_url(job_id, index)

    raise "timed out waiting for #{job_id} variant #{index + 1}" if Time.now - start > timeout

    sleep 15
  end
end

def download_asset(url)
  js = <<~JS
    (function(){
      const x = new XMLHttpRequest();
      x.open('GET', #{url.to_json}, false);
      x.overrideMimeType('text/plain; charset=x-user-defined');
      x.send();
      if (x.status !== 200) return 'ERR ' + x.status;
      const s = x.responseText;
      let b = '';
      const chunk = 0x8000;
      for (let i = 0; i < s.length; i += chunk) {
        let part = '';
        for (let j = i; j < Math.min(i + chunk, s.length); j++) {
          part += String.fromCharCode(s.charCodeAt(j) & 255);
        }
        b += part;
      }
      return btoa(b);
    })()
  JS
  encoded = chrome_js(js)
  raise "download failed for #{url}: #{encoded[0, 120]}" if encoded.start_with?("ERR")

  Base64.decode64(encoded)
end

def convert_webp_to_png(input, output)
  script = <<~PY
    from PIL import Image
    import sys
    im = Image.open(sys.argv[1])
    im.save(sys.argv[2], "PNG")
  PY
  out, err, status = Open3.capture3("python3", "-c", script, input, output)
  raise "webp conversion failed: #{err}#{out}" unless status.success?
end

def download_png(job_id, index, path)
  url = variant_url(job_id, index)
  raise "no downloadable asset for #{job_id} variant #{index + 1}" unless url

  FileUtils.mkdir_p(File.dirname(path))
  bytes = download_asset(url)
  if url.split("?").first.end_with?(".png")
    File.binwrite(path, bytes)
  else
    tmp = "/tmp/mj_variant_#{job_id}_#{index}.webp"
    File.binwrite(tmp, bytes)
    convert_webp_to_png(tmp, path)
  end
end

def load_log
  JSON.parse(File.read(LOG_PATH))
rescue Errno::ENOENT
  {"brand_sref" => SREF, "submitted" => [], "completed" => [], "downloads" => [], "failed" => [], "prompt_count" => 48}
end

def save_log(log)
  File.write(LOG_PATH, JSON.pretty_generate(log))
end

def prompt_done?(item)
  (1..4).all? do |variant|
    expected = File.join(ROOT, item.fetch("folder"), "#{item.fetch("id")}-#{item.fetch("slug")}-v#{variant}.png")
    File.file?(expected) || !Dir.glob(File.join(ROOT, item.fetch("folder"), "#{item.fetch("id")}-*-v#{variant}.png")).empty?
  end
end

def download_prompt_variants(item, job_id, log)
  wait_for_ready(job_id)
  (0..3).each do |index|
    path = File.join(ROOT, item.fetch("folder"), "#{item.fetch("id")}-#{item.fetch("slug")}-v#{index + 1}.png")
    next if File.file?(path) && File.size(path).positive?

    download_png(job_id, index, path)
    log.fetch("downloads") << {"id" => item.fetch("id"), "variant" => index + 1, "path" => path, "job_id" => job_id, "at" => Time.now.iso8601}
    save_log(log)
    puts "downloaded #{path}"
  end
  log.fetch("completed") << {"id" => item.fetch("id"), "job_id" => job_id, "at" => Time.now.iso8601}
  save_log(log)
end

def wait_for_new_jobs(before, count, timeout: 300)
  start = Time.now
  loop do
    ids = visible_job_ids.reject { |id| before.include?(id) }
    return ids.first(count) if ids.length >= count

    raise "timed out waiting for #{count} new jobs; saw #{ids.inspect}" if Time.now - start > timeout

    sleep 5
  end
end

def run_manual_download(id, job_id)
  manifest = JSON.parse(File.read(MANIFEST_PATH)).fetch("prompts")
  item = manifest.find { |p| p.fetch("id") == id }
  raise "unknown prompt #{id}" unless item

  log = load_log
  download_prompt_variants(item, job_id, log)
end

def run_manual_upscale(id, job_id)
  manifest = JSON.parse(File.read(MANIFEST_PATH)).fetch("prompts")
  item = manifest.find { |p| p.fetch("id") == id }
  raise "unknown prompt #{id}" unless item

  log = load_log
  path = File.join(ROOT, item.fetch("folder"), "#{item.fetch("id")}-#{item.fetch("slug")}-UPSCALE.png")
  wait_for_variant(job_id, 0)
  download_png(job_id, 0, path)
  log["upscales"] ||= []
  log.fetch("upscales") << {"id" => id, "job_id" => job_id, "source_variant" => 1, "path" => path, "at" => Time.now.iso8601}
  save_log(log)
  puts "downloaded #{path}"
end

def run_download_job(job_id, folder, basename)
  log = load_log
  (0..3).each do |index|
    path = File.join(ROOT, folder, "#{basename}-v#{index + 1}.png")
    wait_for_variant(job_id, index)
    download_png(job_id, index, path)
    log.fetch("downloads") << {"id" => basename, "variant" => index + 1, "path" => path, "job_id" => job_id, "at" => Time.now.iso8601}
    save_log(log)
    puts "downloaded #{path}"
  end
end

def hero_job_map
  completed = load_log.fetch("completed").each_with_object({}) { |entry, h| h[entry.fetch("id")] = entry.fetch("job_id") }
  completed.merge(
    "A1" => "0c02deae-09ce-437f-b7df-68f7f86ab8e9",
    "A2" => "904e995c-a2ee-4a5a-a9cb-fb65888b5700",
    "A3" => "2de1ab87-c3c8-44dc-bc0a-1769eeb38a60",
    "A4" => "559b2968-dce5-43a4-8ade-9f9371af9618",
    "A6" => "6c356088-1478-44a0-b40c-a5409d39dbd4",
    "A7" => "ecec2146-a662-455d-8261-2910bea75189",
    "A8" => "5a13e73a-241c-434a-a6cb-89ca150b11ea"
  )
end

def upscale_done?(item)
  !Dir.glob(File.join(ROOT, item.fetch("folder"), "#{item.fetch("id")}-*-UPSCALE.png")).empty?
end

def run_hero_upscales
  manifest = JSON.parse(File.read(MANIFEST_PATH)).fetch("prompts")
  heroes = manifest.select { |item| %w[A B E K].include?(item.fetch("section")) && item.fetch("hero") }
  jobs = hero_job_map
  log = load_log

  heroes.each do |item|
    next if upscale_done?(item)

    id = item.fetch("id")
    original_job_id = jobs[id]
    unless original_job_id
      log["upscale_failed"] ||= []
      log.fetch("upscale_failed") << {"id" => id, "error" => "missing source job id", "at" => Time.now.iso8601}
      save_log(log)
      warn "missing source job id for #{id}"
      next
    end

    begin
      navigate_to("https://www.midjourney.com/jobs/#{original_job_id}?index=0")
      wait_for_upscale_controls
      upscale_job_id = find_upscale_job_for(item)
      unless upscale_job_id
        click_upscale_subtle
        start = Time.now
        loop do
          upscale_job_id = find_upscale_job_for(item)
          break if upscale_job_id

          raise "timed out waiting for matching upscale card" if Time.now - start > 480

          sleep 5
        end
      end
      puts "upscale mapped #{id} -> #{upscale_job_id}"
      run_manual_upscale(id, upscale_job_id)
    rescue StandardError => e
      log["upscale_failed"] ||= []
      log.fetch("upscale_failed") << {"id" => id, "source_job_id" => original_job_id, "error" => e.message, "at" => Time.now.iso8601}
      save_log(log)
      warn "failed upscale #{id}: #{e.message}"
    end
  end
end

def run_batch(ids = nil)
  manifest = JSON.parse(File.read(MANIFEST_PATH)).fetch("prompts")
  manifest = manifest.select { |item| ids.include?(item.fetch("id")) } if ids
  log = load_log
  skipped_ids = log.fetch("failed").select { |f| f["stage"] == "skip" }.map { |f| f["id"] }
  todo = manifest.reject { |item| prompt_done?(item) || skipped_ids.include?(item.fetch("id")) }

  todo.each_slice(BATCH_SIZE) do |batch|
    before = visible_job_ids
    batch.each do |item|
      prompt = item.fetch("prompt").gsub("YOURCODE", SREF)
      submit_prompt(prompt)
      log.fetch("submitted") << {"id" => item.fetch("id"), "at" => Time.now.iso8601, "prompt" => prompt}
      save_log(log)
      puts "submitted #{item.fetch("id")}"
      sleep 3
    rescue StandardError => e
      log.fetch("failed") << {"id" => item.fetch("id"), "stage" => "submit", "error" => e.message, "at" => Time.now.iso8601}
      save_log(log)
      warn "failed submit #{item.fetch("id")}: #{e.message}"
    end

    submitted = batch.reject { |item| log.fetch("failed").any? { |f| f["id"] == item.fetch("id") && f["stage"] == "submit" } }
    next if submitted.empty?

    new_ids = wait_for_new_jobs(before, submitted.length)
    job_by_id = submitted.reverse.zip(new_ids).to_h
    submitted.each do |item|
      job_id = job_by_id.fetch(item)
      puts "mapped #{item.fetch("id")} -> #{job_id}"
      download_prompt_variants(item, job_id, log)
    rescue StandardError => e
      log.fetch("failed") << {"id" => item.fetch("id"), "stage" => "download", "job_id" => job_id, "error" => e.message, "at" => Time.now.iso8601}
      save_log(log)
      warn "failed download #{item.fetch("id")}: #{e.message}"
    end
  end
end

case ARGV[0]
when "manual"
  run_manual_download(ARGV.fetch(1), ARGV.fetch(2))
when "upscale"
  run_manual_upscale(ARGV.fetch(1), ARGV.fetch(2))
when "download-job"
  run_download_job(ARGV.fetch(1), ARGV.fetch(2), ARGV.fetch(3))
when "hero-upscales"
  run_hero_upscales
when "ids"
  run_batch(ARGV[1..])
else
  run_batch
end
