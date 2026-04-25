const fs = require('fs');
const path = require('path');
const { GoogleGenerativeAI } = require('@google/generative-ai');

class NanoBananaService {
  constructor(apiKey, defaultModel = 'gemini-2.5-flash-image', hqModel = 'gemini-3-pro-image-preview') {
    if (!apiKey) throw new Error('NanoBananaService: missing Gemini API key');
    this.genAI = new GoogleGenerativeAI(apiKey);
    this.defaultModel = defaultModel;
    this.hqModel = hqModel;
  }

  _getModel(hq) {
    return this.genAI.getGenerativeModel({
      model: hq ? this.hqModel : this.defaultModel,
    });
  }

  async generateBackground(scenePrompt, options = {}) {
    const model = this._getModel(options.hq);

    const parts = [{ text: scenePrompt }];

    if (options.referenceImage) {
      const imageData = fs.readFileSync(options.referenceImage);
      const ext = path.extname(options.referenceImage).toLowerCase();
      const mimeType = ext === '.jpg' || ext === '.jpeg' ? 'image/jpeg' : 'image/png';
      parts.unshift({
        inlineData: {
          mimeType,
          data: imageData.toString('base64'),
        },
      });
    }

    const result = await model.generateContent({
      contents: [{ role: 'user', parts }],
      generationConfig: {
        responseModalities: ['IMAGE', 'TEXT'],
      },
    });

    const response = result.response;
    const candidate = response && response.candidates && response.candidates[0];
    if (!candidate) throw new Error('NanoBanana: no candidates returned');
    for (const part of candidate.content.parts) {
      if (part.inlineData && part.inlineData.data) {
        return Buffer.from(part.inlineData.data, 'base64');
      }
    }
    throw new Error('NanoBanana: no image data in response');
  }

  async generateWithCharacter(scenePrompt, expressionPhotoPath, options = {}) {
    const prompt = `Using the person in the reference photo, create a YouTube thumbnail scene: ${scenePrompt}.
The person should be positioned naturally in the scene with the same facial expression as the reference.
Photorealistic style, dramatic YouTube thumbnail lighting, high contrast, 16:9 aspect ratio.
The person should occupy roughly 40% of the left side of the frame.
Professional real estate agent appearance.`;

    return this.generateBackground(prompt, {
      ...options,
      referenceImage: expressionPhotoPath,
    });
  }
}

module.exports = { NanoBananaService };
