import { SanitizationOptions } from "@/types/tts";

const DEFAULT_OPTIONS: SanitizationOptions = {
  stripMarkdown: true,
  convertUrlsToNames: true,
  normalizeAcronyms: true,
  removeEmojis: true,
};

const BRAND_OVERRIDES: Record<string, string> = {
  "fb.me": "facebook",
  "youtu.be": "youtube",
  "t.co": "twitter",
  "github.com": "github",
  "linkedin.com": "linked in",
  "google.com": "google",
};

export class TextNormalizer {
  private static extractBrandName(rawUrl: string): string {
    try {
      const formattedUrl = rawUrl.startsWith("http") ? rawUrl : `https://${rawUrl}`;
      const parsed = new URL(formattedUrl);
      const host = parsed.hostname.toLowerCase();

      for (const [key, brand] of Object.entries(BRAND_OVERRIDES)) {
        if (host.includes(key)) return brand;
      }

      const cleanHost = host.replace(/^www\./i, "");
      const segments = cleanHost.split(".");
      return segments[0] || "link";
    } catch {
      return "link";
    }
  }

  
  public static isHindiText(text: string): boolean {
    const hindiRegex = /[\u0900-\u097F]/;
    return hindiRegex.test(text);
  }

  public static normalize(text: string, options: Partial<SanitizationOptions> = {}): string {
    const opts = { ...DEFAULT_OPTIONS, ...options };
    if (!text || typeof text !== "string") return "";

    let processed = text;

    // 1markdown fileteration 
    processed = processed.replace(/```[\s\S]*?```/g, " Code block. ");

    // url domain names
    if (opts.convertUrlsToNames) {
      const urlPattern = /(https?:\/\/[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:com|org|net|io|co|in|ai|dev|app)[^\s]*)/gi;
      processed = processed.replace(urlPattern, (match) => {
        const brand = this.extractBrandName(match);
        return ` ${brand} `;
      });
    }

    //  Emojis removal
    if (opts.removeEmojis) {
      processed = processed.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1F1E0}-\u{1F1FF}]/gu, "");
    }

    processed = processed.replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1");

    
    processed = processed.replace(/[^a-zA-Z0-9\u0900-\u097F.,!?\s'-]/g, " ");

    return processed
      .replace(/\s+/g, " ")
      .replace(/([.,!?])\s*\1+/g, "$1")
      .trim();
  }
}