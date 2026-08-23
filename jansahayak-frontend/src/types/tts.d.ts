export type TTSEngineType = "browser" | "neural-openai" | "neural-elevenlabs";

export interface SanitizationOptions {
  stripMarkdown: boolean;
  convertUrlsToNames: boolean;
  normalizeAcronyms: boolean;
  removeEmojis: boolean;
}

export interface VoiceOption {
  id: string;
  name: string;
  lang: string;
  engine: TTSEngineType;
  gender?: "male" | "female" | "neutral";
}

export type PlaybackStatus = "idle" | "loading" | "playing" | "paused" | "error";

export interface AudioEngineState {
  status: PlaybackStatus;
  progress: number; // 0 to 100
  activeWordIndex: number | null;
  errorMessage: string | null;
}