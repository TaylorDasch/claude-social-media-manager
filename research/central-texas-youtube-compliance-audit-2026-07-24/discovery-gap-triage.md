# Discovery-gap triage

This is an offline-only triage of the YouTube search harvest. It identifies credible local housing-service channels that were not already in `candidate-channels.tsv`; it does **not** assert that any selected channel has a compliance problem.

## Result

- 546 unique channels with a usable channel ID appeared in the search harvest.
- 58 were already in the candidate registry. The root full-catalog manifest adds no separate channels beyond that registry.
- Taylor Dasch's channel was excluded.
- Of the remaining 487 non-Taylor channels, 64 are credible housing-service gaps:
  - 29 recommended for a full-channel audit.
  - 35 recommended for a direct-video-only review.
  - 51 high-confidence and 13 medium-confidence candidates.
- The remaining 423 channels were classified as noise or insufficiently local/real-estate-specific and are not listed in the TSV.

## Selection rule

A channel was included only when the search-result title and/or channel identity provided a credible signal that it directly markets, sells, rents, builds, manages, finances, or gives relocation guidance about housing in Temple, Belton, Killeen, Harker Heights, Copperas Cove, Nolanville, or the immediately adjacent Fort Hood/Fort Cavazos market.

`full_channel_audit` means the search harvest showed repeated local housing activity or a clear local housing-business identity. `direct_video_only` means there is a discrete, locally relevant housing video but not enough offline evidence to justify cataloging an entire channel.

## False-positive rules

Excluded as noise unless the channel itself was directly marketing housing services:

- local news, government, schools, chambers, tourism, economic development, and general lifestyle/city-tour channels;
- media/photography/drone vendors whose videos merely depict a property;
- general contractors, remodelers, auto dealers, and other unrelated local businesses;
- national housing-commentary, clickbait, general investing, or out-of-market real-estate channels;
- personal military PCS/on-base housing vlogs not operated by a housing provider; and
- automated listing aggregators or generic `coldwellbanker##`/similar feeds without evidence of an identifiable local creator or firm.

The supporting [TSV](discovery-gap-triage.tsv) preserves the exact discovery examples and is intended as an intake queue for the main evidence review.
